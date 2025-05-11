from mirascope.core import openai, prompt_template
from openai import OpenAI


@openai.call("gpt-4o-mini", client=OpenAI())
@prompt_template("Recommend a {genre} book")
def recommend_book(genre: str): ...
