from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types
from components.vector_db import vector_memory
from components.config import Config

class Agent:
    def __init__(
        self,
        name: str,
        goal: str,
        backstory: str,
        tools: List[Any],
        client: genai.Client,
        model: str = Config.DEFAULT_MODEL,
        max_memory: int = 10
    ):
        self.name = name
        self.goal = goal
        self.backstory = backstory
        self.tools = tools
        self.client = client
        self.model = model
        self.max_memory = max_memory
        self.memory: List[Dict[str, str]] = []

    def add_to_memory(self, role: str, content: str):
        """Add message to short-term memory."""
        self.memory.append({"role": role, "content": content})
        if len(self.memory) > self.max_memory * 2: # Keep conversation window
            self.memory = self.memory[-self.max_memory * 2:]

    def get_memory_context(self) -> str:
        """Format short-term memory for the prompt."""
        return "\n".join([f"{m['role']}: {m['content']}" for m in self.memory])

    def _parse_gemini_response(self, response) -> dict:
        """Extract text, tool calls, and usage from Gemini response."""
        parsed = {
            "text": None,
            "tool_calls": [],
            "tool_results": [],
            "usage": {}
        }

        try:
            parsed["text"] = response.candidates[0].content.parts[0].text
        except (AttributeError, IndexError):
            parsed["text"] = "I encountered an issue processing the response."

        try:
            history = getattr(response, "automatic_function_calling_history", [])
            for item in history:
                for part in item.parts:
                    if hasattr(part, "function_call") and part.function_call:
                        fc = part.function_call
                        parsed["tool_calls"].append({
                            "tool_name": getattr(fc, "name", None),
                            "args": getattr(fc, "args", {}),
                        })
                    if hasattr(part, "function_response") and part.function_response:
                        fr = part.function_response
                        parsed["tool_results"].append({
                            "tool_name": getattr(fr, "name", None),
                            "response": getattr(fr, "response", {}),
                        })
        except Exception as e:
            print(f"⚠️ Error parsing tool history: {e}")

        try:
            usage = response.usage_metadata
            parsed["usage"] = {
                "prompt_tokens": usage.prompt_token_count,
                "completion_tokens": usage.candidates_token_count,
                "total_tokens": usage.total_token_count,
            }
        except AttributeError:
            pass

        return parsed

    def run(self, query: str) -> str:
        """Execute the agent loop for a given query."""
        self.add_to_memory("User", query)
        memory_context = self.get_memory_context()

        prompt = f"""
        You are {self.name}.
        Goal: {self.goal}
        Backstory: {self.backstory}

        Conversation History:
        {memory_context}

        Instructions:
        - Use tools only when necessary.
        - Be accurate, logical, and concise.
        - Use long-term memory via tools if relevant to the query.
        - Do not hallucinate.

        Current Task: {query}
        """

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=self.tools,
                temperature=0.3,
                max_output_tokens=2048,
            )
        )

        output = self._parse_gemini_response(response)
        
        # Store in long-term memory
        vector_memory.add(output, query)
        
        # Update short-term memory with agent's text response
        self.add_to_memory("Agent", output["text"] if output["text"] else "Command executed.")

        return response