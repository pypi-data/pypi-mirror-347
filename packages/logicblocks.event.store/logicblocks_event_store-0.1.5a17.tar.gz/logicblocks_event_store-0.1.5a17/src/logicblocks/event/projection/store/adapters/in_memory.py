from collections.abc import Callable, Sequence
from dataclasses import dataclass
from functools import reduce
from typing import Any, Self

from logicblocks.event.types import (
    JsonPersistable,
    JsonValue,
    JsonValueType,
    Projection,
    deserialise_projection,
    serialise_projection,
    serialise_to_json_value,
)

from ..query import (
    Clause,
    FilterClause,
    KeySetPagingClause,
    Lookup,
    OffsetPagingClause,
    Operator,
    PagingDirection,
    Path,
    Query,
    Search,
    SortClause,
    SortField,
    SortOrder,
)
from .base import ProjectionStorageAdapter

type ProjectionResultSet = Sequence[Projection[JsonValue, JsonValue]]
type InMemoryProjectionResultSetTransformer = Callable[
    [ProjectionResultSet], ProjectionResultSet
]
type InMemoryClauseConverter[C: Clause] = Callable[
    [C], InMemoryProjectionResultSetTransformer
]


def compose_transformers(
    functions: Sequence[InMemoryProjectionResultSetTransformer],
) -> InMemoryProjectionResultSetTransformer:
    def accumulator(
        f: InMemoryProjectionResultSetTransformer,
        g: InMemoryProjectionResultSetTransformer,
    ) -> InMemoryProjectionResultSetTransformer:
        def handler(projections: ProjectionResultSet) -> ProjectionResultSet:
            return g(f(projections))

        return handler

    def initial(projections: ProjectionResultSet) -> ProjectionResultSet:
        return projections

    return reduce(accumulator, functions, initial)


def lookup_projection_path(
    projection: Projection[JsonValue, JsonValue], path: Path
) -> Any:
    attribute_name = path.top_level
    remaining_path = path.sub_levels

    try:
        attribute = getattr(projection, attribute_name)
    except AttributeError:
        raise ValueError(f"Invalid projection path: {path}.")

    value = attribute
    for path_segment in remaining_path:
        try:
            value = value[path_segment]
        except KeyError:
            raise ValueError(f"Invalid projection path: {path}.")

    return value


def filter_clause_converter(
    clause: FilterClause,
) -> InMemoryProjectionResultSetTransformer:
    def matches(
        projection: Projection[JsonValue, JsonValue],
    ) -> bool:
        comparison_value = clause.value
        resolved_value = lookup_projection_path(projection, clause.path)

        match clause.operator:
            case Operator.EQUAL:
                return resolved_value == comparison_value
            case Operator.NOT_EQUAL:
                return not resolved_value == comparison_value
            case Operator.GREATER_THAN:
                return resolved_value > comparison_value
            case Operator.GREATER_THAN_OR_EQUAL:
                return resolved_value >= comparison_value
            case Operator.LESS_THAN:
                return resolved_value < comparison_value
            case Operator.LESS_THAN_OR_EQUAL:
                return resolved_value <= comparison_value
            case Operator.IN:
                return resolved_value in comparison_value
            case Operator.CONTAINS:
                return comparison_value in resolved_value
            case _:  # pragma: no cover
                raise ValueError(f"Unknown operator: {clause.operator}.")

    def handler(
        projections: Sequence[Projection[JsonValue, JsonValue]],
    ) -> Sequence[Projection[JsonValue, JsonValue]]:
        return list(
            projection for projection in projections if matches(projection)
        )

    return handler


def sort_clause_converter(
    clause: SortClause,
) -> InMemoryProjectionResultSetTransformer:
    def accumulator(
        projections: Sequence[Projection[JsonValue, JsonValue]],
        field: SortField,
    ) -> Sequence[Projection[JsonValue, JsonValue]]:
        result = sorted(
            projections,
            key=lambda projection: lookup_projection_path(
                projection, field.path
            ),
            reverse=(field.order == SortOrder.DESC),
        )
        return result

    def handler(
        projections: Sequence[Projection[JsonValue, JsonValue]],
    ) -> Sequence[Projection[JsonValue, JsonValue]]:
        return reduce(accumulator, reversed(clause.fields), projections)

    return handler


def key_set_paging_clause_converter(
    clause: KeySetPagingClause,
) -> InMemoryProjectionResultSetTransformer:
    @dataclass
    class NotFound:
        pass

    @dataclass
    class NotProvided:
        pass

    @dataclass
    class Found:
        index: int

    def determine_last_index(
        projections: Sequence[Projection[JsonValue, JsonValue]],
        last_id: str | None,
    ) -> Found | NotFound | NotProvided:
        if last_id is None:
            return NotProvided()

        last_indices = [
            index
            for index, projection in enumerate(projections)
            if projection.id == last_id
        ]
        if len(last_indices) != 1:
            return NotFound()

        return Found(last_indices[0])

    def handler(
        projections: Sequence[Projection[JsonValue, JsonValue]],
    ) -> Sequence[Projection[JsonValue, JsonValue]]:
        last_index_result = determine_last_index(projections, clause.last_id)
        direction = clause.direction
        item_count = clause.item_count

        match (last_index_result, direction):
            case (
                (NotFound(), PagingDirection.FORWARDS)
                | (NotFound(), PagingDirection.BACKWARDS)
                | (NotProvided(), PagingDirection.BACKWARDS)
            ):
                return []
            case (NotProvided(), PagingDirection.FORWARDS):
                return projections[:item_count]
            case (Found(last_index), PagingDirection.FORWARDS):
                return projections[
                    last_index + 1 : last_index + 1 + item_count
                ]
            case (Found(last_index), PagingDirection.BACKWARDS):
                resolved_start_index = max(last_index - item_count, 0)
                return projections[resolved_start_index:last_index]
            case _:  # pragma: no cover
                raise ValueError("Unreachable state.")

    return handler


def offset_paging_clause_converter(
    clause: OffsetPagingClause,
) -> InMemoryProjectionResultSetTransformer:
    def handler(
        projections: Sequence[Projection[JsonValue, JsonValue]],
    ) -> Sequence[Projection[JsonValue, JsonValue]]:
        offset = clause.offset
        item_count = clause.item_count

        return projections[offset : offset + item_count]

    return handler


class InMemoryQueryConverter:
    def __init__(self):
        self._registry: dict[type[Clause], InMemoryClauseConverter[Any]] = {}

    def with_default_clause_converters(self) -> Self:
        return (
            self.register_clause_converter(
                FilterClause, filter_clause_converter
            )
            .register_clause_converter(SortClause, sort_clause_converter)
            .register_clause_converter(
                KeySetPagingClause, key_set_paging_clause_converter
            )
            .register_clause_converter(
                OffsetPagingClause, offset_paging_clause_converter
            )
        )

    def register_clause_converter[C: Clause](
        self, clause_type: type[C], converter: InMemoryClauseConverter[C]
    ) -> Self:
        self._registry[clause_type] = converter
        return self

    def convert_clause(
        self, clause: Clause
    ) -> InMemoryProjectionResultSetTransformer:
        if clause.__class__ not in self._registry:
            raise ValueError(f"No converter registered for clause: {clause}")
        return self._registry[clause.__class__](clause)

    def convert_query(
        self, query: Query
    ) -> InMemoryProjectionResultSetTransformer:
        match query:
            case Search(filters, sort, paging):
                return compose_transformers(
                    [
                        self.convert_clause(clause)
                        for clause in (list(filters) + [sort] + [paging])
                        if clause is not None
                    ]
                )
            case Lookup(filters):
                return compose_transformers(
                    [self.convert_clause(clause) for clause in filters]
                )
            case _:
                raise ValueError(f"Unsupported query type: {query}.")


class InMemoryProjectionStorageAdapter[
    ItemQuery: Query = Lookup,
    CollectionQuery: Query = Search,
](ProjectionStorageAdapter[ItemQuery, CollectionQuery]):
    def __init__(self, query_converter: InMemoryQueryConverter | None = None):
        self._projections: dict[
            tuple[str, str], Projection[JsonValue, JsonValue]
        ] = {}
        self._query_converter = (
            query_converter
            if query_converter is not None
            else InMemoryQueryConverter().with_default_clause_converters()
        )

    async def save(
        self,
        *,
        projection: Projection[JsonPersistable, JsonPersistable],
    ) -> None:
        projection_key = (projection.name, projection.id)
        existing = self._projections.get(projection_key, None)
        if existing is not None:
            self._projections[projection_key] = Projection[
                JsonValue, JsonValue
            ](
                id=existing.id,
                name=existing.name,
                source=existing.source,
                state=serialise_to_json_value(projection.state),
                metadata=serialise_to_json_value(projection.metadata),
            )
        else:
            self._projections[projection_key] = serialise_projection(
                projection
            )

    async def _find_raw(
        self, query: Query
    ) -> Sequence[Projection[JsonValue, JsonValue]]:
        return self._query_converter.convert_query(query)(
            list(self._projections.values())
        )

    async def find_one[
        State: JsonPersistable = JsonValue,
        Metadata: JsonPersistable = JsonValue,
    ](
        self,
        *,
        lookup: ItemQuery,
        state_type: type[State] = JsonValueType,
        metadata_type: type[Metadata] = JsonValueType,
    ) -> Projection[State, Metadata] | None:
        projections = await self._find_raw(lookup)

        if len(projections) > 1:
            raise ValueError(
                f"Expected single projection for query: {lookup} "
                f"but found {len(projections)} projections: {projections}."
            )
        if len(projections) == 0:
            return None

        projection = projections[0]

        return deserialise_projection(projection, state_type, metadata_type)

    async def find_many[
        State: JsonPersistable = JsonValue,
        Metadata: JsonPersistable = JsonValue,
    ](
        self,
        *,
        search: CollectionQuery,
        state_type: type[State] = JsonValueType,
        metadata_type: type[Metadata] = JsonValueType,
    ) -> Sequence[Projection[State, Metadata]]:
        return [
            deserialise_projection(projection, state_type, metadata_type)
            for projection in (await self._find_raw(search))
        ]
