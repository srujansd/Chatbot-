import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


st.title("OpenRouter Chatbot")

#OpenRouter API key 
OPENROUTER_API_KEY = "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"

# Message format for the chatbot
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    ("human", "Question: {question}")
])

# Sidebar settings
st.sidebar.title("Settings")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
tokens = st.sidebar.slider("Max Tokens", 50, 500, 150)
engine = st.sidebar.selectbox(
    "Model",
    ["openai/gpt-4o-mini", "openai/gpt-4-turbo", "meta-llama/llama-3-70b-instruct"]
)

# Asking the user for input
st.write("Enter your question below to get started!")
user_input = st.text_input("Ask anything you want:")

# Function to get response from model
def get_response(question, temperature, tokens, engine):
    chat_model = ChatOpenAI(
        model=engine,
        temperature=temperature,
        max_tokens=tokens,
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )
    parser = StrOutputParser()
    chain = prompt | chat_model | parser
    return chain.invoke({"question": question})

# Display answer
if user_input:
    try:
        answer = get_response(user_input, temperature, tokens, engine)
        st.success(answer)
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please enter a question to get started!")
