import os
from dotenv import load_dotenv
from smolagents import CodeAgent, LiteLLMModel, tool
from tools import MathVerificationTool

load_dotenv()

model = LiteLLMModel(
    model_id="huggingface/Qwen/Qwen2.5-Coder-32B-Instruct",
    api_key=os.getenv("HF_TOKEN")
)

@tool
def final_answer(steps_working: str, tool_verification_log: str, absolute_final_answer: str) -> str:
    """Provides the final structured answer to the user containing full step-by-step math workings.

    Args:
        steps_working: The detailed step-by-step algebraic manipulation or breakdown. Provide steps separated by new lines.
        tool_verification_log: A summary note explaining how the results were validated.
        absolute_final_answer: The final simplified mathematical result (e.g., 'y = 7').
    """
    return f"""### **Mathematical Derivation**

{steps_working}

---

### **Verification & Validation**
* {tool_verification_log}

---

### **Conclusion**
**{absolute_final_answer}**"""

agent = CodeAgent(
    tools=[MathVerificationTool(), final_answer],
    model=model,
    additional_authorized_imports=["sympy", "matplotlib.pyplot", "numpy", "pandas"],
    name="MathFirstPrinciplesTutor"
)