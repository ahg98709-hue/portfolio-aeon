
import os
from groq import Groq
from aeon.config import AEON_MODEL, GROQ_API_KEY

class LLM:
    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment variables.")
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = AEON_MODEL

    def chat(self, prompt: str, system_prompt: str = "You are AEON, an advanced digital intelligence.") -> str:
        """
        Sends a chat request to the LLM.
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error communicating with LLM: {str(e)}"

    def generate_code(self, prompt: str) -> str:
        """
        Specialized method for code generation prompts.
        """
        system_prompt = "You are a Python coding expert. Output only valid Python code without markdown backticks."
        return self.chat(prompt, system_prompt)
