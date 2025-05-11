from anthropic import AsyncAnthropic
from mirascope.core import anthropic, prompt_template


@anthropic.call("claude-3-5-sonnet-20240620")
@prompt_template("Recommend a {genre} book")
async def recommend_book(genre: str) -> anthropic.AsyncAnthropicDynamicConfig:
    return {
        "client": AsyncAnthropic(),
    }
