from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gemma-3-4b-it",
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    temperature=0.3,
    streaming=True
)