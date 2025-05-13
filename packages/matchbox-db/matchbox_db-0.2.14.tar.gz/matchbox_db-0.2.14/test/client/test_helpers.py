from importlib.metadata import version
from typing import Callable
from unittest.mock import Mock, patch

import pyarrow as pa
import pytest
from httpx import Response
from numpy import ndarray
from pandas import DataFrame
from respx import MockRouter
from sqlalchemy import Engine

from matchbox import index, match, process, query
from matchbox.client._handler import create_client
from matchbox.client._settings import ClientSettings
from matchbox.client.clean import company_name, company_number
from matchbox.client.helpers import cleaner, cleaners, comparison, select
from matchbox.client.helpers.selector import Match
from matchbox.common.arrow import SCHEMA_MB_IDS, table_to_buffer
from matchbox.common.dtos import (
    BackendRetrievableType,
    BackendUploadType,
    NotFoundError,
    UploadStatus,
)
from matchbox.common.exceptions import (
    MatchboxResolutionNotFoundError,
    MatchboxServerFileError,
    MatchboxSourceNotFoundError,
)
from matchbox.common.factories.sources import (
    linked_sources_factory,
    source_factory,
    source_from_tuple,
)
from matchbox.common.graph import DEFAULT_RESOLUTION
from matchbox.common.sources import SourceAddress, SourceConfig


def test_cleaners():
    cleaner_name = cleaner(function=company_name, arguments={"column": "company_name"})
    cleaner_number = cleaner(
        function=company_number, arguments={"column": "company_number"}
    )
    cleaner_name_number = cleaners(cleaner_name, cleaner_number)

    assert cleaner_name_number is not None


def test_process():
    crn = source_factory().query
    # Duplicate column
    crn = crn.append_column("company_name_again", crn.column("company_name"))

    cleaner_name = cleaner(
        function=company_name,
        arguments={"column": "company_name"},
    )
    # I can add the same function twice
    cleaner_name_again = cleaner(
        function=company_name,
        arguments={"column": "company_name_again"},
    )
    cleaner_number = cleaner(
        function=company_number,
        arguments={"column": "crn"},
    )
    cleaner_name_number = cleaners(cleaner_name, cleaner_name_again, cleaner_number)

    df_name_cleaned = process(data=crn, pipeline=cleaner_name_number)

    assert isinstance(df_name_cleaned, DataFrame)
    assert df_name_cleaned.shape[0] == 10


def test_comparisons():
    comparison_name_id = comparison(
        sql_condition=(
            "l.company_name = r.company_name and l.data_hub_id = r.data_hub_id"
        )
    )

    assert comparison_name_id is not None


def test_create_client():
    mock_settings = ClientSettings(api_root="http://example.com", timeout=20)
    client = create_client(mock_settings)

    assert client.headers.get("X-Matchbox-Client-Version") == version("matchbox_db")
    assert client.base_url == mock_settings.api_root
    assert client.timeout.connect == mock_settings.timeout
    assert client.timeout.pool == mock_settings.timeout
    assert client.timeout.read == 60 * 30
    assert client.timeout.write == 60 * 30


def test_select_default_engine(
    env_setter: Callable[[str, str], None],
    sqlite_warehouse: Engine,
):
    """We can select without explicit engine if default is set."""
    default_engine = sqlite_warehouse.url.render_as_string(hide_password=False)
    env_setter("MB__CLIENT__DEFAULT_WAREHOUSE", default_engine)

    # Select sources
    selection = select("bar")

    # Check selector contains what we expect
    assert selection[0].fields is None
    assert selection[0].address.full_name == "bar"
    assert selection[0].engine.url == sqlite_warehouse.url


def test_select_missing_engine():
    """We must pass an engine if a default is not set"""
    with pytest.raises(ValueError, match="engine"):
        select("test.bar")


def test_select_mixed_style(matchbox_api: MockRouter, sqlite_warehouse: Engine):
    """We can select specific columns from some of the sources"""
    linked = linked_sources_factory(engine=sqlite_warehouse)

    source1 = linked.sources["crn"].source_config
    source2 = linked.sources["cdms"].source_config

    selection = select({"crn": ["company_name"]}, "cdms", engine=sqlite_warehouse)

    assert selection[0].fields == ["company_name"]
    assert selection[1].fields is None
    assert selection[0].address == source1.address
    assert selection[1].address == source2.address
    assert selection[0].engine == sqlite_warehouse
    assert selection[1].engine == sqlite_warehouse


def test_query_no_resolution_ok_various_params(
    matchbox_api: MockRouter, sqlite_warehouse: Engine
):
    """Tests that we can avoid passing resolution name, with a variety of parameters."""
    # Dummy data and source
    testkit = source_from_tuple(
        data_tuple=({"a": 1, "b": "2"}, {"a": 10, "b": "20"}),
        data_pks=["0", "1"],
        full_name="foo",
        engine=sqlite_warehouse,
    )
    source = testkit.source_config.set_engine(sqlite_warehouse)
    address = source.address
    testkit.to_warehouse(engine=sqlite_warehouse)

    # Mock API
    matchbox_api.get(f"/sources/{address.warehouse_hash_b64}/{address.full_name}").mock(
        return_value=Response(200, json=source.model_dump())
    )

    query_route = matchbox_api.get("/query").mock(
        return_value=Response(
            200,
            content=table_to_buffer(
                pa.Table.from_pylist(
                    [
                        {"source_pk": "0", "id": 1},
                        {"source_pk": "1", "id": 2},
                    ],
                    schema=SCHEMA_MB_IDS,
                )
            ).read(),
        )
    )

    selectors = select({"foo": ["a", "b"]}, engine=sqlite_warehouse)

    # Tests with no optional params
    results = query(selectors)
    assert len(results) == 2
    assert {"foo_a", "foo_b", "id"} == set(results.columns)

    assert dict(query_route.calls.last.request.url.params) == {
        "full_name": address.full_name,
        "warehouse_hash_b64": address.warehouse_hash_b64,
    }

    # Tests with optional params
    results = query(selectors, return_type="arrow", threshold=50).to_pandas()
    assert len(results) == 2
    assert {"foo_a", "foo_b", "id"} == set(results.columns)

    assert dict(query_route.calls.last.request.url.params) == {
        "full_name": address.full_name,
        "warehouse_hash_b64": address.warehouse_hash_b64,
        "threshold": "50",
    }


def test_query_multiple_sources(matchbox_api: MockRouter, sqlite_warehouse: Engine):
    """Tests that we can query multiple sources."""
    # Dummy data and source
    testkit1 = source_from_tuple(
        data_tuple=({"a": 1, "b": "2"}, {"a": 10, "b": "20"}),
        data_pks=["0", "1"],
        full_name="foo",
        engine=sqlite_warehouse,
    )
    source1 = testkit1.source_config.set_engine(sqlite_warehouse)
    address1 = source1.address
    testkit1.to_warehouse(engine=sqlite_warehouse)

    testkit2 = source_from_tuple(
        data_tuple=({"c": "val"}, {"c": "val"}),
        data_pks=["2", "3"],
        full_name="foo2",
        engine=sqlite_warehouse,
    )
    source2 = testkit2.source_config.set_engine(sqlite_warehouse)
    address2 = source2.address
    testkit2.to_warehouse(engine=sqlite_warehouse)

    # Mock API
    matchbox_api.get(
        f"/sources/{address1.warehouse_hash_b64}/{address1.full_name}"
    ).mock(return_value=Response(200, json=source1.model_dump()))

    matchbox_api.get(
        f"/sources/{address2.warehouse_hash_b64}/{address2.full_name}"
    ).mock(return_value=Response(200, json=source2.model_dump()))

    query_route = matchbox_api.get("/query").mock(
        side_effect=[
            Response(
                200,
                content=table_to_buffer(
                    pa.Table.from_pylist(
                        [
                            {"source_pk": "0", "id": 1},
                            {"source_pk": "1", "id": 2},
                        ],
                        schema=SCHEMA_MB_IDS,
                    )
                ).read(),
            ),
            Response(
                200,
                content=table_to_buffer(
                    pa.Table.from_pylist(
                        [
                            {"source_pk": "2", "id": 1},
                            {"source_pk": "3", "id": 2},
                        ],
                        schema=SCHEMA_MB_IDS,
                    )
                ).read(),
            ),
        ]
        * 2  # 2 calls to `query()` in this test, each querying server twice
    )

    sels = select("foo", {"foo2": ["c"]}, engine=sqlite_warehouse)

    # Validate results
    results = query(sels)
    assert len(results) == 4
    assert {
        # All columns automatically selected for `foo`
        "foo_pk",
        "foo_a",
        "foo_b",
        # Only one column selected for `foo2`
        "foo2_c",
        # The id always comes back
        "id",
    } == set(results.columns)

    assert dict(query_route.calls[-2].request.url.params) == {
        "full_name": address1.full_name,
        "warehouse_hash_b64": address1.warehouse_hash_b64,
        "resolution_name": DEFAULT_RESOLUTION,
    }
    assert dict(query_route.calls[-1].request.url.params) == {
        "full_name": address2.full_name,
        "warehouse_hash_b64": address2.warehouse_hash_b64,
        "resolution_name": DEFAULT_RESOLUTION,
    }

    # It also works with the selectors specified separately
    query([sels[0]], [sels[1]])


@pytest.mark.parametrize(
    "combine_type",
    ["set_agg", "explode"],
)
def test_query_combine_type(
    combine_type: str, matchbox_api: MockRouter, sqlite_warehouse: Engine
):
    """Various ways of combining multiple sources are supported."""
    # Dummy data and source
    testkit1 = source_from_tuple(
        data_tuple=({"col": 20}, {"col": 40}, {"col": 60}),
        data_pks=["0", "1", "2"],
        full_name="foo",
        engine=sqlite_warehouse,
    )
    source1 = testkit1.source_config.set_engine(sqlite_warehouse)
    address1 = source1.address
    testkit1.to_warehouse(engine=sqlite_warehouse)

    testkit2 = source_from_tuple(
        data_tuple=({"col": "val1"}, {"col": "val2"}, {"col": "val3"}),
        data_pks=["3", "4", "5"],
        full_name="bar",
        engine=sqlite_warehouse,
    )
    source2 = testkit2.source_config.set_engine(sqlite_warehouse)
    address2 = source2.address
    testkit2.to_warehouse(engine=sqlite_warehouse)

    # Mock API
    matchbox_api.get(
        f"/sources/{address1.warehouse_hash_b64}/{address1.full_name}"
    ).mock(return_value=Response(200, json=source1.model_dump()))

    matchbox_api.get(
        f"/sources/{address2.warehouse_hash_b64}/{address2.full_name}"
    ).mock(return_value=Response(200, json=source2.model_dump()))

    matchbox_api.get("/query").mock(
        side_effect=[
            Response(
                200,
                content=table_to_buffer(
                    pa.Table.from_pylist(
                        [
                            {"source_pk": "0", "id": 1},
                            {"source_pk": "1", "id": 1},
                            {"source_pk": "2", "id": 2},
                        ],
                        schema=SCHEMA_MB_IDS,
                    )
                ).read(),
            ),
            Response(
                200,
                content=table_to_buffer(
                    pa.Table.from_pylist(
                        [
                            # Creating a duplicate value for the same Matchbox ID
                            {"source_pk": "3", "id": 2},
                            {"source_pk": "3", "id": 2},
                            {"source_pk": "4", "id": 3},
                        ],
                        schema=SCHEMA_MB_IDS,
                    )
                ).read(),
            ),
        ]  # two sources to query
    )

    sels = select("foo", "bar", engine=sqlite_warehouse)

    # Validate results
    results = query(sels, combine_type=combine_type)

    if combine_type == "set_agg":
        expected_len = 3
        for _, row in results.drop(columns=["id"]).iterrows():
            for cell in row.values:
                assert isinstance(cell, ndarray)
                # No duplicates
                assert len(cell) == len(set(cell))
    else:
        expected_len = 5

    assert len(results) == expected_len
    assert {
        "foo_pk",
        "foo_col",
        "bar_pk",
        "bar_col",
        "id",
    } == set(results.columns)


def test_query_unindexed_fields(matchbox_api: MockRouter, sqlite_warehouse: Engine):
    """We cannot query unindexed fields when only_indexed=True."""
    # Dummy data and source
    testkit = source_from_tuple(
        data_tuple=({"a": 1, "b": "2"}, {"a": 10, "b": "20"}),
        data_pks=["0", "1"],
        full_name="foo",
        engine=sqlite_warehouse,
    )
    # Drop one column
    source = testkit.source_config.model_copy(
        update={"columns": (testkit.source_config.columns[0],)}
    ).set_engine(sqlite_warehouse)
    address = source.address
    testkit.to_warehouse(engine=sqlite_warehouse)

    # Mock API
    matchbox_api.get(f"/sources/{address.warehouse_hash_b64}/{address.full_name}").mock(
        return_value=Response(200, json=source.model_dump())
    )

    matchbox_api.get("/query").mock(
        return_value=Response(
            200,
            content=table_to_buffer(
                pa.Table.from_pylist(
                    [{"source_pk": "0", "id": 1}],
                    schema=SCHEMA_MB_IDS,
                )
            ).read(),
        )
    )

    selectors = select({"foo": ["a", "b"]}, engine=sqlite_warehouse)

    # Verify exception is raised
    with pytest.raises(ValueError, match="unindexed"):
        query(selectors, only_indexed=True)


def test_query_404_resolution(matchbox_api: MockRouter, sqlite_warehouse: Engine):
    # Mock API
    matchbox_api.get("/query").mock(
        return_value=Response(
            404,
            json=NotFoundError(
                details="Resolution 42 not found",
                entity=BackendRetrievableType.RESOLUTION,
            ).model_dump(),
        )
    )

    selectors = select({"foo": ["a", "b"]}, engine=sqlite_warehouse)

    # Test with no optional params
    with pytest.raises(MatchboxResolutionNotFoundError, match="42"):
        query(selectors)


def test_query_404_source_query(matchbox_api: MockRouter, sqlite_warehouse: Engine):
    """Handles source 404 error when querying."""
    # Mock API
    matchbox_api.get("/query").mock(
        return_value=Response(
            404,
            json=NotFoundError(
                details="SourceConfig 42 not found",
                entity=BackendRetrievableType.SOURCE,
            ).model_dump(),
        )
    )

    sels = select({"foo": ["a", "b"]}, engine=sqlite_warehouse)

    # Test with no optional params
    with pytest.raises(MatchboxSourceNotFoundError, match="42"):
        query(sels)


def test_query_404_source_get(matchbox_api: MockRouter, sqlite_warehouse: Engine):
    """Handles source 404 error when retrieving source."""
    # Mock API
    address = SourceAddress.compose(full_name="foo", engine=sqlite_warehouse)

    matchbox_api.get(f"/sources/{address.warehouse_hash_b64}/{address.full_name}").mock(
        return_value=Response(
            404,
            json=NotFoundError(
                details="SourceConfig 42 not found",
                entity=BackendRetrievableType.SOURCE,
            ).model_dump(),
        )
    )

    matchbox_api.get("/query").mock(
        return_value=Response(
            200,
            content=table_to_buffer(
                pa.Table.from_pylist(
                    [{"source_pk": "0", "id": 1}], schema=SCHEMA_MB_IDS
                )
            ).read(),
        )
    )

    sels = select({"foo": ["a", "b"]}, engine=sqlite_warehouse)

    with pytest.raises(MatchboxSourceNotFoundError, match="42"):
        query(sels)


def test_query_with_batches(matchbox_api: MockRouter, sqlite_warehouse: Engine):
    """Tests that query correctly handles batching options using real warehouse data."""
    # Dummy data and source
    source_testkit = source_from_tuple(
        data_tuple=({"a": 1, "b": "2"}, {"a": 10, "b": "20"}),
        data_pks=["0", "1"],
        full_name="foo",
        engine=sqlite_warehouse,
    )
    source = source_testkit.source_config.set_engine(sqlite_warehouse)
    address = source.address
    source_testkit.to_warehouse(engine=sqlite_warehouse)

    # Mock API responses
    matchbox_api.get(f"/sources/{address.warehouse_hash_b64}/{address.full_name}").mock(
        return_value=Response(200, json=source.model_dump())
    )
    matchbox_api.get("/query").mock(
        return_value=Response(
            200,
            content=table_to_buffer(
                pa.Table.from_pylist(
                    [
                        {"source_pk": "0", "id": 1},
                        {"source_pk": "1", "id": 2},
                    ],
                    schema=SCHEMA_MB_IDS,
                )
            ).read(),
        )
    )

    sels = select({"foo": ["a", "b"]}, engine=sqlite_warehouse)

    # Test with return_batches=True
    batch_iterator = query(sels, return_batches=True, batch_size=1, return_type="arrow")

    # Check first batch
    first_batch = next(batch_iterator)
    assert isinstance(first_batch, pa.Table)
    assert len(first_batch) == 1
    assert {"foo_a", "foo_b", "id"} == set(first_batch.column_names)

    # Verify we can get the remaining batch
    remaining_batches = list(batch_iterator)
    assert len(remaining_batches) == 1

    # Test with return_batches=False
    results = query(sels, return_batches=False, batch_size=1000, return_type="arrow")

    # Basic verification
    assert isinstance(results, pa.Table)
    assert len(results) == 2
    assert {"foo_a", "foo_b", "id"} == set(results.column_names)


@patch("matchbox.client.helpers.index.SourceConfig")
def test_index_success(
    MockSource: Mock, matchbox_api: MockRouter, sqlite_warehouse: Engine
):
    """Test successful indexing flow through the API."""
    # Mock SourceConfig
    source = source_factory(
        features=[{"name": "company_name", "base_generator": "company"}],
        engine=sqlite_warehouse,
    )
    mock_source_instance = source.mock
    MockSource.return_value = mock_source_instance

    # Mock the initial source metadata upload
    source_route = matchbox_api.post("/sources").mock(
        return_value=Response(
            202,
            json=UploadStatus(
                id="test-upload-id",
                status="awaiting_upload",
                entity=BackendUploadType.INDEX,
            ).model_dump(),
        )
    )

    # Mock the data upload
    upload_route = matchbox_api.post("/upload/test-upload-id").mock(
        return_value=Response(
            202,
            json=UploadStatus(
                id="test-upload-id", status="complete", entity=BackendUploadType.INDEX
            ).model_dump(),
        )
    )

    # Call the index function
    index(
        full_name=source.source_config.address.full_name,
        db_pk=source.source_config.db_pk,
        engine=sqlite_warehouse,
    )

    # Verify the API calls
    source_call = SourceConfig.model_validate_json(
        source_route.calls.last.request.content.decode("utf-8")
    )
    assert source_call == source.source_config
    assert "test-upload-id" in upload_route.calls.last.request.url.path
    assert b"Content-Disposition: form-data;" in upload_route.calls.last.request.content
    assert b"PAR1" in upload_route.calls.last.request.content


@patch("matchbox.client.helpers.index.SourceConfig")
@pytest.mark.parametrize(
    "columns",
    [
        pytest.param(["name", "age"], id="string_columns"),
        pytest.param(
            [
                {"name": "name", "type": "TEXT"},
                {"name": "age", "type": "BIGINT"},
            ],
            id="dict_columns",
        ),
        pytest.param(None, id="default_columns"),
    ],
)
def test_index_with_columns(
    MockSource: Mock,
    matchbox_api: MockRouter,
    columns: list[str] | list[dict[str, str]],
    sqlite_warehouse: Engine,
):
    """Test indexing with different column definition formats."""
    # Create source testkit and mock
    source = source_factory(
        features=[
            {"name": "name", "base_generator": "name"},
            {"name": "age", "base_generator": "random_int"},
        ],
        engine=sqlite_warehouse,
    )
    mock_source_instance = source.mock
    MockSource.return_value = mock_source_instance

    # Mock the API endpoints
    source_route = matchbox_api.post("/sources").mock(
        return_value=Response(
            202,
            json=UploadStatus(
                id="test-upload-id",
                status="awaiting_upload",
                entity=BackendUploadType.INDEX,
            ).model_dump(),
        )
    )

    upload_route = matchbox_api.post("/upload/test-upload-id").mock(
        return_value=Response(
            202,
            json=UploadStatus(
                id="test-upload-id", status="complete", entity=BackendUploadType.INDEX
            ).model_dump(),
        )
    )

    # Call index with column definition
    index(
        full_name=source.source_config.address.full_name,
        db_pk=source.source_config.db_pk,
        engine=sqlite_warehouse,
        columns=columns,
    )

    # Verify API calls and source creation
    assert source_route.called
    source_call = SourceConfig.model_validate_json(
        source_route.calls.last.request.content.decode("utf-8")
    )
    assert source_call == source.source_config
    assert "test-upload-id" in upload_route.calls.last.request.url.path
    assert b"Content-Disposition: form-data;" in upload_route.calls.last.request.content
    assert b"PAR1" in upload_route.calls.last.request.content
    mock_source_instance.set_engine.assert_called_once_with(sqlite_warehouse)
    if columns:
        mock_source_instance.default_columns.assert_not_called()
    else:
        mock_source_instance.default_columns.assert_called_once()


@patch("matchbox.client.helpers.index.SourceConfig")
def test_index_upload_failure(
    MockSource: Mock, matchbox_api: MockRouter, sqlite_warehouse: Engine
):
    """Test handling of upload failures."""
    # Mock SourceConfig
    source = source_factory(
        features=[{"name": "company_name", "base_generator": "company"}],
        engine=sqlite_warehouse,
    )
    mock_source_instance = source.mock
    MockSource.return_value = mock_source_instance

    # Mock successful source creation
    source_route = matchbox_api.post("/sources").mock(
        return_value=Response(
            202,
            json=UploadStatus(
                id="test-upload-id",
                status="awaiting_upload",
                entity=BackendUploadType.INDEX,
            ).model_dump(),
        )
    )

    # Mock failed upload
    upload_route = matchbox_api.post("/upload/test-upload-id").mock(
        return_value=Response(
            400,
            json=UploadStatus(
                id="test-upload-id",
                status="failed",
                details="Invalid schema",
                entity=BackendUploadType.INDEX,
            ).model_dump(),
        )
    )

    # Verify the error is propagated
    with pytest.raises(MatchboxServerFileError):
        index(
            full_name=source.source_config.address.full_name,
            db_pk=source.source_config.db_pk,
            engine=sqlite_warehouse,
        )

    # Verify API calls
    source_call = SourceConfig.model_validate_json(
        source_route.calls.last.request.content.decode("utf-8")
    )
    assert source_call == source.source_config
    assert "test-upload-id" in upload_route.calls.last.request.url.path
    assert b"Content-Disposition: form-data;" in upload_route.calls.last.request.content
    assert b"PAR1" in upload_route.calls.last.request.content


def test_index_with_batch_size(matchbox_api: MockRouter, sqlite_warehouse: Engine):
    """Test that batch_size is passed correctly to hash_data when indexing."""
    # Dummy data and source
    source_testkit = source_from_tuple(
        data_tuple=({"company_name": "Company A"}, {"company_name": "Company B"}),
        data_pks=["1", "2"],
        full_name="test_companies",
        engine=sqlite_warehouse,
    )
    source = source_testkit.source_config.set_engine(sqlite_warehouse)
    source_testkit.to_warehouse(engine=sqlite_warehouse)

    # Mock the API endpoints
    source_route = matchbox_api.post("/sources").mock(
        return_value=Response(
            202,
            json=UploadStatus(
                id="test-upload-id",
                status="awaiting_upload",
                entity=BackendUploadType.INDEX,
            ).model_dump(),
        )
    )

    upload_route = matchbox_api.post("/upload/test-upload-id").mock(
        return_value=Response(
            202,
            json=UploadStatus(
                id="test-upload-id", status="complete", entity=BackendUploadType.INDEX
            ).model_dump(),
        )
    )

    # Spy on the hash_data method to verify batch_size
    with patch.object(
        SourceConfig, "hash_data", wraps=source.hash_data
    ) as spy_hash_data:
        # Call index with batch_size
        index(
            full_name=source.address.full_name,
            db_pk=source.db_pk,
            engine=sqlite_warehouse,
            batch_size=1,
        )

        # Verify batch_size was passed to hash_data
        spy_hash_data.assert_called_once()
        assert spy_hash_data.call_args.kwargs["batch_size"] == 1

        # Verify endpoints were called only once, despite multiple batches
        assert source_route.call_count == 1
        assert upload_route.call_count == 1


def test_match_ok(matchbox_api: MockRouter, sqlite_warehouse: Engine):
    """The client can perform the right call for matching."""
    # Set up mocks
    mock_match1 = Match(
        cluster=1,
        source=SourceAddress(full_name="test.source_config", warehouse_hash=b"bar"),
        source_id={"a"},
        target=SourceAddress(full_name="test.target", warehouse_hash=b"bar"),
        target_id={"b"},
    )
    mock_match2 = Match(
        cluster=1,
        source=SourceAddress(full_name="test.source_config", warehouse_hash=b"bar"),
        source_id={"a"},
        target=SourceAddress(full_name="test.target2", warehouse_hash=b"bar"),
        target_id={"b"},
    )
    # The standard JSON serialiser does not handle Pydantic objects
    serialised_matches = (
        f"[{mock_match1.model_dump_json()}, {mock_match2.model_dump_json()}]"
    )

    match_route = matchbox_api.get("/match").mock(
        return_value=Response(200, content=serialised_matches)
    )

    # Use match function
    source = select({"test.source_config": ["a", "b"]}, engine=sqlite_warehouse)
    target1 = select({"test.target1": ["a", "b"]}, engine=sqlite_warehouse)
    target2 = select({"test.target2": ["a", "b"]}, engine=sqlite_warehouse)

    res = match(
        target1,
        target2,
        source=source,
        source_pk="pk1",
        resolution_name="foo",
    )

    # Verify results
    assert len(res) == 2
    assert isinstance(res[0], Match)
    param_set = sorted(match_route.calls.last.request.url.params.multi_items())
    expected_hash_b64 = SourceAddress.compose(
        full_name="irrelevant", engine=sqlite_warehouse
    ).warehouse_hash_b64
    assert param_set == sorted(
        [
            ("target_full_names", "test.target1"),
            ("target_full_names", "test.target2"),
            ("target_warehouse_hashes_b64", expected_hash_b64),
            ("target_warehouse_hashes_b64", expected_hash_b64),
            ("source_full_name", "test.source_config"),
            ("source_warehouse_hash_b64", expected_hash_b64),
            ("source_pk", "pk1"),
            ("resolution_name", "foo"),
        ]
    )


def test_match_404_resolution(matchbox_api: MockRouter, sqlite_warehouse: Engine):
    """The client can handle a resolution not found error."""
    # Set up mocks
    matchbox_api.get("/match").mock(
        return_value=Response(
            404,
            json=NotFoundError(
                details="Resolution 42 not found",
                entity=BackendRetrievableType.RESOLUTION,
            ).model_dump(),
        )
    )

    # Use match function
    source = select({"test.source_config": ["a", "b"]}, engine=sqlite_warehouse)
    target = select({"test.target1": ["a", "b"]}, engine=sqlite_warehouse)

    with pytest.raises(MatchboxResolutionNotFoundError, match="42"):
        match(
            target,
            source=source,
            source_pk="pk1",
            resolution_name="foo",
        )


def test_match_404_source(matchbox_api: MockRouter, sqlite_warehouse: Engine):
    """The client can handle a source not found error."""
    # Set up mocks
    matchbox_api.get("/match").mock(
        return_value=Response(
            404,
            json=NotFoundError(
                details="SourceConfig 42 not found",
                entity=BackendRetrievableType.SOURCE,
            ).model_dump(),
        )
    )

    # Use match function
    source = select({"test.source_config": ["a", "b"]}, engine=sqlite_warehouse)
    target = select({"test.target1": ["a", "b"]}, engine=sqlite_warehouse)

    with pytest.raises(MatchboxSourceNotFoundError, match="42"):
        match(
            target,
            source=source,
            source_pk="pk1",
            resolution_name="foo",
        )
