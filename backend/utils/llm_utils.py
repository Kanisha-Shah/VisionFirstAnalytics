# utils/llm_utils.py
import os
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    api_key=api_key,
    model="gpt-4",
    temperature=0.6,
    max_tokens=100
)

prompt_template = PromptTemplate.from_template(
    """
    You are a UX behavior analyst.

    Based on the user's session data:

    Screen Elements: {screen_elements}
    User Actions: {user_actions}
    Anomalies: {anomalies}
    Timestamps: {timestamps}

    Please answer:
    1. What is the user likely trying to do?
    2. What are the signs of friction or confusion?
    3. What suggestions would you give to the product/design team to improve this experience?
        """
)

chain = LLMChain(llm=llm, prompt=prompt_template)

def get_prediction(summary):
    try:
        print("---------OpenAI Called--------")
        response = chain.invoke({
            "screen_elements": ", ".join(summary["screen_elements"]),
            "user_actions": ", ".join(summary["user_actions"]),
            "anomalies": ", ".join(summary["anomalies"]),
            "timestamps": ", ".join(map(str, summary["timestamps"]))
        })
        return response.content if hasattr(response, 'content') else str(response)
    except Exception as e:
        return f"LLM error: {str(e)}"
