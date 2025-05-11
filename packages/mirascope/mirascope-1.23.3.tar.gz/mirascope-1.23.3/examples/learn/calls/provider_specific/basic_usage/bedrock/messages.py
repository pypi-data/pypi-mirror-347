from mirascope.core import Messages, bedrock


@bedrock.call("amazon.nova-lite-v1:0")
def recommend_book(genre: str) -> Messages.Type:
    return Messages.User(f"Recommend a {genre} book")


response: bedrock.BedrockCallResponse = recommend_book("fantasy")
print(response.content)
