from typing import TypedDict, Literal, Union


class MutationVariables(TypedDict):
    datasetPath: Union[str, None]
    configPath: Union[str, None]
    id: str


class ExecuteGraphQLParams(TypedDict):
    mutation: Literal["createSharedView", "updateSharedView"]
    variables: dict[Literal["input"], MutationVariables]
    token: str
    api_url: str
