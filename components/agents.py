from typing import List, Dict, Any
from google import genai
from google.genai import types

from components.vector_db import vector_memory


class Agent:
    def __init__(
        self,
        name: str,
        goal: str,
        backstory: str,
        tools: List[Any],
        client: genai.Client,
        model: str = "gemini-3-flash-preview",
        max_memory: int = 8
    ):
        """
        Initialize an intelligent agent.

        Args:
            name (str): Agent name
            goal (str): Primary objective of the agent
            backstory (str): Background context for behavior
            tools (List[Any]): Available tools
            client (genai.Client): Gemini client
            model (str): Model name
        """

        self.name = name
        self.goal = goal
        self.backstory = backstory
        self.tools = tools
        self.client = client
        self.model = model
        self.max_memory = max_memory

        # 🧠 Internal memory (short-term)
        self.memory: List[Dict[str, str]] = []

    # -----------------------------
    # Memory Handling
    # -----------------------------
    def add_to_memory(self, role: str, content: str):
        """Add message to memory."""
        self.memory.append({"role": role, "content": content})



    def get_memory_context(self) -> str:
        """Convert memory into prompt-friendly string."""
        return "\n".join([f"{m['role']}: {m['content']}" for m in self.memory[-self.max_memory:]])
    # -----------------------------
    # Agent Response Parse
    # -----------------------------
    def _parse_gemini_response(self, response) -> dict:
        """
        Parse Gemini response and extract:
        - final text
        - tool calls
        - tool results
        - usage info
        """

        parsed = {
            "text": None,
            "tool_calls": [],
            "tool_results": [],
            "usage": {}
        }

        # -----------------------------
        # Final response text
        # -----------------------------
        try:
            parsed["text"] = response.candidates[0].content.parts[0].text
        except Exception:
            parsed["text"] = None

        # -----------------------------
        # Tool calls + responses
        # -----------------------------
        try:
            history = response.automatic_function_calling_history

            for item in history:
                for part in item.parts:

                    # ✅ Tool call
                    if hasattr(part, "function_call") and part.function_call:
                        fc = part.function_call
                        parsed["tool_calls"].append({
                            "tool_name": getattr(fc, "name", None),
                            "args": getattr(fc, "args", {}),
                            "id": getattr(fc, "id", None),
                        })

                    # ✅ Tool response
                    if hasattr(part, "function_response") and part.function_response:
                        fr = part.function_response
                        parsed["tool_results"].append({
                            "tool_name": getattr(fr, "name", None),
                            "response": getattr(fr, "response", {}),
                        })

        except Exception as e:
            print("⚠️ Parsing history failed:", e)

        # -----------------------------
        # Token usage
        # -----------------------------
        try:
            usage = response.usage_metadata
            parsed["usage"] = {
                "prompt_tokens": getattr(usage, "prompt_token_count", None),
                "completion_tokens": getattr(usage, "candidates_token_count", None),
                "total_tokens": getattr(usage, "total_token_count", None),
            }
        except Exception:
            pass

        return parsed
    # -----------------------------
    # Core Agent Execution
    # -----------------------------
    def run(self, query: str) -> str:
        """
        Run the agent on a given query.

        Args:
            query (str): User input

        Returns:
            str: Agent response
        """

        # store user input
        self.add_to_memory("User", query)

        memory_context = self.get_memory_context()

        prompt = f"""
            You are {self.name}.

            Goal:
            {self.goal}

            Backstory:
            {self.backstory}

            Conversation History:
            {memory_context}

            Instructions:
            - Use tools only when necessary
            - Don't use unnecessary tool call
            - Be accurate and logical
            - Be concise but complete
            - Use long term memory when realy needed
            - Do not hallucinate

            Current Task:
            {query}
        """

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=self.tools,
                temperature=0.3,
                max_output_tokens=1024 * 10,
            )
        )

        output = self._parse_gemini_response(response)
        vector_memory.add(output, query)

        # store response
        self.add_to_memory("Agent", output)

        return response