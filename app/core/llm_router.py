from langchain_google_genai import ChatGoogleGenerativeAI
import os

def fast_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.3,
        max_output_tokens=2048 
    )