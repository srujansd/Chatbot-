import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

st.title("OpenRouter Chatbot with LangChain and Streamlit")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant. Give clear, concise answers."),
    ("human", "Question: {question}")
])

st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your OpenRouter API Key:", type="password")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
tokens = st.sidebar.slider("Max Tokens", 50, 500, 150)
engine = st.sidebar.selectbox("Model", ["openai/gpt-4o-mini", "openai/gpt-4-turbo", "meta-llama/llama-3-70b-instruct"])

st.write("Enter your question below to get started!")
user_input = st.text_input("Ask anything you want:")

def get_response(question, api_key, temperature, tokens, engine):
    chat_model = ChatOpenAI(
        model=engine,
        temperature=temperature,
        max_tokens=tokens,
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"  #  key change for OpenRouter
    )
    parser = StrOutputParser()
    chain = prompt | chat_model | parser
    return chain.invoke({"question": question})

if user_input and api_key:
    try:
        answer = get_response(user_input, api_key, temperature, tokens, engine)
        st.success(answer)
    except Exception as e:
        st.error(f"An error occurred: {e}")
elif user_input and not api_key:
    st.warning("Please enter your OpenRouter API key in the sidebar.")
else:
    st.write("Please enter a question to get started!")
