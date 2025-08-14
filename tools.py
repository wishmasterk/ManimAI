# This file contains all the functions/Agents which will be used to create a animation video from prompt
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv(override = True)

# --- Agent 1: The Planner ---
def create_animation_plan(user_prompt: str) -> str:
    """
    Takes a user prompt and asks an LLM to create a detailed, step-by-step animation plan.
    """
    system_prompt = """
    You are an expert animation director with a deep understanding of Manim. Your role is to act as a creative partner, translating a user's idea into a clear and effective storyboard plan.

    **Your Goal:**
    Your primary goal is to create a step-by-step animation plan that is so clear and well-structured that a specialized 'Coder AI' can use it as a blueprint to write flawless Manim code.

    **Your Process:**

    1.  **Interpret the User's Vision:** First, use your full intelligence to understand the core idea behind the user's prompt. What is the story they are trying to tell with this animation?

    2.  **Handle Vague Prompts Gracefully:** Users aren't always specific. If a prompt is missing details (like a specific shape, color, or duration), please make a sensible, common-sense choice. For example, if the user says "show a shape," using a `Circle` is a great default. The key is to briefly note the choice you made in the plan.
        * *Example:* "1. Create a Circle object. (Note: Defaulting to Circle as the shape was not specified)."

    3.  **Structure the Plan:** Organize your interpretation into an ordered, step-by-step list. This ensures the animation flows logically from one action to the next.

    **Output Guidelines:**
    To ensure the Coder AI can work effectively, please format your final output as a numbered list titled 'Animation Plan:'. Please focus on the sequence of events and object descriptions, as the Coder AI will handle the specific Manim functions.
    """
    LLM1 = ChatOpenAI(model = 'gpt-4o-mini', temperature = 0.3)
    response = LLM1.invoke(
        [
            SystemMessage(content = system_prompt),
            HumanMessage(content = user_prompt),
        ]
    )
    plan = response.content
    print("--- Planner LLM: Plan created.")
    return plan

# --- Agent 2: The Coder ---
def create_manim_code(plan: str) -> str:
    """
    Takes a detailed animation plan and asks an LLM to write the corresponding Manim code.
    """

    system_prompt = """
    You are a senior Manim programmer with a passion for writing clean, efficient, and error-free code.
    You will be given a highly detailed, step-by-step animation plan. Your task is to translate this plan
    into a complete, runnable Python script that perfectly implements it.

    **Core Directives:**
    1.  **Implement the Plan Exactly:** Adhere strictly to the provided plan. Do not add or omit any steps.
    2.  **Code Quality:** Write high-quality, readable code. Use meaningful variable names (e.g., `title_text`, `main_circle`).
    3.  **Error Prevention (Crucial):**
        * **Object Management:** Ensure every object is added to the scene (`self.add()`) *before* it is used in a `Transform` or other animation that assumes it exists.
        * **Animation Timing:** Use `self.wait()` to create natural pauses between animations, making the final video easy to follow.
        * **Import Everything:** Start the script with `from manim import *` to ensure all necessary classes and functions are available.

    **Strict Output Rules:**
    1.  The main animation class **MUST** be named `GeneratedScene`.
    2.  All animation logic **MUST** be within the `construct(self)` method.
    3.  Your final output **MUST ONLY** be the raw Python code. Do not include any explanations, comments, or markdown formatting.
    """

    user_prompt = f"Based on the following plan, write the Manim code:\n\n{plan}"
    LLM2 = ChatOpenAI(model = 'gpt-5')
    response = LLM2.invoke(
        [
            SystemMessage(content = system_prompt),
            HumanMessage(content = user_prompt),
        ]
    )
    code = response.content
    print("--- Coder LLM: Initial code generated.")
    return code

# --- Agent 3: The Debugger ---
def debug_manim_code(plan: str, broken_code: str, error_message: str) -> str:
    """
    Takes a plan, the code that failed, and the error message, and asks an LLM to fix it.
    """
    system_prompt = """
    You are a senior Manim software engineer specializing in debugging. You are methodical, precise, and an expert at root cause analysis.
    You will be given three pieces of information:
    1. The original 'Animation Plan'.
    2. The 'Broken Code' that failed to execute.
    3. The exact 'Error Message' produced by Manim.

    Your mission is to fix the code by following a strict analytical process:

    1.  **Analyze the Error:** First, carefully analyze the `Error Message` to understand the specific technical failure (e.g., `NameError`, `AttributeError`, an object not being on screen).
    2.  **Consult the Plan:** Cross-reference the error with the `Animation Plan` and the `Broken Code`. Your primary goal is to fix the error while maintaining **100% fidelity** to the original plan. Do not add new animations or remove steps.
    3.  **Minimal Viable Fix:** Implement the smallest, most targeted change possible to resolve the error. Do not refactor or rewrite code unnecessarily.
    4.  **Final Code Output:** Provide only the complete, corrected, raw Python code.

    **Strict Output Rules:**
    - The class must remain `GeneratedScene`.
    - The logic must remain in the `construct(self)` method.
    - Your output must ONLY be the raw Python code, with no explanations or markdown.
    """

    user_prompt = f"""
    The following plan was created:
    --- PLAN ---
    {plan}
    
    This code was generated to execute the plan, but it failed:
    --- BROKEN CODE ---
    {broken_code}

    Here is the error message from Manim:
    --- ERROR MESSAGE ---
    {error_message}

    Please provide the corrected Python code.
    """
    LLM3 = ChatOpenAI(model = 'gpt-5')
    response = LLM3.invoke(
        [
            SystemMessage(content = system_prompt),
            HumanMessage(content = user_prompt),
        ]
    )
    corrected_code = response.content
    print("--- Debugger LLM: Code correction attempted.")
    return corrected_code
