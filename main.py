from flask import Flask, request, jsonify
import os

from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI

app = Flask(__name__)

# 1) Configure your OpenAI key in the environment
#    export OPENAI_API_KEY="sk-..."
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable")

# 2) Initialize the Chat LLM
chat = ChatOpenAI(
    openai_api_key=openai_api_key,
    model_name="gpt-4o",    # or "gpt-4"
    temperature=0.2,
)

# 3) Define a prompt template (system + user)
template = """You are a Manim code generator.
Generate a *minimal* Python script defining a Manim Scene subclass
that fulfills the user’s request.  Respond **only** with valid code.

User Request:
{user_prompt}

"""
prompt = PromptTemplate(
    input_variables=["user_prompt"],
    template=template
)

# 4) Assemble the chain
chain = LLMChain(llm=chat, prompt=prompt)

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.json or {}
    user_prompt = data.get("prompt", "").strip()
    if not user_prompt:
        return jsonify(error="No prompt provided"), 400

    try:
        # 5) Run the chain
        code = chain.run(user_prompt).strip()
        return jsonify(code=code)
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)
