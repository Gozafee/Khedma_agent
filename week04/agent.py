"""
KhedmaAgent - Week 4
Implements a manual ReAct loop with:
- Turn cap (max 5 turns)
- Token budget (max 5000 tokens)
- Explicit stopping conditions
- Failure detection (hallucination)
- Full audit trail
"""
import json
from model_client import MockModelClient


class KhedmaAgent:
    """ReAct agent for Sudanese passport renewal assistance."""

    def __init__(self, model_client=None):
        # Default to MockModelClient (no API calls)
        self.model = model_client if model_client else MockModelClient()

        # Reliability controls
        self.max_turns = 5
        self.max_tokens = 5000
        self.turn_count = 0
        self.token_usage = 0

        # Agent state
        self.state = {
            "user_data": {},
            "collected_fields": [],
            "required_fields": ["name", "national_id", "reason", "location"],
            "done": False,
            "hallucination_triggered": False,
        }

        # Audit trail
        self.trace = []

    def _think(self, user_input: str) -> dict:
        """Reasoning step: extract structured data from user input."""
        messages = [
            {
                "role": "system",
                "content": (
                    "Extract from user message these fields: "
                    "name, national_id, reason, location. "
                    "Respond in JSON format."
                ),
            },
            {"role": "user", "content": user_input},
        ]
        response = self.model.generate(messages)
        self.token_usage = self.model.get_token_count()

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {}

    def _act(self, extracted: dict) -> str:
        """Action step: update state with extracted data."""
        missing = []
        for field in self.state["required_fields"]:
            if field in extracted and extracted[field]:
                if field not in self.state["collected_fields"]:
                    self.state["user_data"][field] = extracted[field]
                    self.state["collected_fields"].append(field)
            elif field not in self.state["collected_fields"]:
                missing.append(field)

        if not missing:
            self.state["done"] = True
            return "All data collected successfully!"
        return f"Missing fields: {', '.join(missing)}"

    def _observe(self, user_input: str) -> str:
        """Observation step: process input and update state."""
        # Trigger hallucination detection (test keyword)
        if "هالوسة" in user_input:
            self.state["hallucination_triggered"] = True
            return "Hallucination detected!"

        extracted = self._think(user_input)
        result = self._act(extracted)

        # Log to trace
        self.trace.append({
            "turn": self.turn_count + 1,
            "input": user_input,
            "extracted": extracted,
            "result": result,
            "tokens": self.token_usage,
        })

        self.turn_count += 1
        return result

    def run(self, user_input: str) -> str:
        """Main ReAct loop with explicit stopping conditions."""
        # Stop condition 1: Turn limit exceeded
        if self.turn_count >= self.max_turns:
            return (
                f"Max turns ({self.max_turns}) exceeded. "
                "Please visit the nearest passport office."
            )

        # Stop condition 2: Token budget exceeded
        if self.token_usage > self.max_tokens:
            return (
                f"Budget ({self.max_tokens}) exceeded. "
                "Please start a new session."
            )

        # Stop condition 3: Task complete
        if self.state["done"]:
            return f"Complete: {self.state['user_data']}"

        # Execute the loop
        return self._observe(user_input)

    def get_trace(self) -> list:
        """Return the full audit trail."""
        return self.trace

    def reset(self):
        """Reset the agent for a new session."""
        self.turn_count = 0
        self.token_usage = 0
        self.state = {
            "user_data": {},
            "collected_fields": [],
            "required_fields": ["name", "national_id", "reason", "location"],
            "done": False,
            "hallucination_triggered": False,
        }
        self.trace = []
        self.model = MockModelClient()