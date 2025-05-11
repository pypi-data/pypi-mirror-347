from anthropic import AnthropicError
from mirascope.core import anthropic


@anthropic.call("claude-3-5-sonnet-20240620", stream=True)
def recommend_book(genre: str) -> str:
    return f"Recommend a {genre} book"


try:
    for chunk, _ in recommend_book("fantasy"):
        print(chunk.content, end="", flush=True)
except AnthropicError as e:
    print(f"Error: {str(e)}")
