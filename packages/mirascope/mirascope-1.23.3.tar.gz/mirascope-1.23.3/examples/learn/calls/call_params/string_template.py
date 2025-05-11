from mirascope import llm, prompt_template


@llm.call(provider="openai", model="gpt-4o-mini", call_params={"max_tokens": 512})
@prompt_template("Recommend a {genre} book")
def recommend_book(genre: str): ...


response: llm.CallResponse = recommend_book("fantasy")
print(response.content)
