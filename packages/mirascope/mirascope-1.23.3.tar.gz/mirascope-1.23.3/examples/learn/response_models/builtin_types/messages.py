from mirascope import Messages, llm


@llm.call(provider="openai", model="gpt-4o-mini", response_model=list[str])
def extract_book(texts: list[str]) -> Messages.Type:
    return Messages.User(f"Extract book titles from {texts}")


book = extract_book(
    [
        "The Name of the Wind by Patrick Rothfuss",
        "Mistborn: The Final Empire by Brandon Sanderson",
    ]
)
print(book)
# Output: ["The Name of the Wind", "Mistborn: The Final Empire"]
