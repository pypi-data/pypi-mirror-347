from mirascope.core import bedrock
from mirascope.integrations.langfuse import with_langfuse


@with_langfuse()
@bedrock.call("anthropic.claude-3-haiku-20240307-v1:0")
def recommend_book(genre: str) -> str:
    return f"Recommend a {genre} book."


print(recommend_book("fantasy"))
