import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv(override = True)

app = Flask(__name__, template_folder='.')

# 2) Initialize Chat LLM
LLM = ChatOpenAI(model = "gpt-4.1")

# 3) Define prompt template
template = """You are a code generator.
So generate code based on the user prompt.

User Request:
{user_prompt}
"""

prompt = PromptTemplate(
    input_variables=["user_prompt"],
    template=template
)

# 4) Create LangChain chain
chain =  prompt | LLM

# 5) Serve frontend
@app.route("/")
def home():
    return render_template("index.html")

# 6) Backend route for generation
@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json()
    user_prompt = data.get("prompt", "")

    if not user_prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        output = (chain.invoke(user_prompt)).content
        return jsonify({"code": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)
