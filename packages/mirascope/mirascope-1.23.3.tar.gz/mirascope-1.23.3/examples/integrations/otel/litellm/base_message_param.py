from mirascope.core import BaseMessageParam, litellm
from mirascope.integrations.otel import configure, with_otel

configure()


@with_otel()
@litellm.call("gpt-4o-mini")
def recommend_book(genre: str) -> list[BaseMessageParam]:
    return [BaseMessageParam(role="user", content=f"Recommend a {genre} book")]


print(recommend_book("fantasy"))
