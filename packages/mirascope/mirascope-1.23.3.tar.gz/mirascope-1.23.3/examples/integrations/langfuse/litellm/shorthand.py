from mirascope.core import litellm
from mirascope.integrations.langfuse import with_langfuse


@with_langfuse()
@litellm.call("gpt-4o-mini")
def recommend_book(genre: str) -> str:
    return f"Recommend a {genre} book"


print(recommend_book("fantasy"))
