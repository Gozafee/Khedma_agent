"""
ModelClient interface for Khedma project.
Provides a swappable seam between Mock, Local (Ollama), and Hosted models.
"""
from abc import ABC, abstractmethod


class ModelClient(ABC):
    """Abstract base class for all model clients."""

    @abstractmethod
    def generate(self, messages: list, **kwargs) -> str:
        """Generate a response given a list of messages."""
        pass

    @abstractmethod
    def get_token_count(self) -> int:
        """Return the total tokens used so far."""
        pass


class MockModelClient(ModelClient):
    """Mock model client for testing without API calls."""

    def __init__(self):
        self.tokens = 0

    def generate(self, messages: list, **kwargs) -> str:
        self.tokens += 50
        user_msg = messages[-1]["content"] if messages else ""

        if "اسمي" in user_msg or "name" in user_msg.lower():
            return (
                '{"name": "Yousif", "national_id": "123456", '
                '"reason": "travel", "location": "Khartoum"}'
            )
        return "Missing fields: name, national_id, reason, location"

    def get_token_count(self) -> int:
        return self.tokens


class OllamaModelClient(ModelClient):
    """Local model client using Ollama with an Arabic-capable model."""

    def __init__(self, model_name: str = "yousif-khedma"):
        self.model_name = model_name
        self.tokens = 0

    def generate(self, messages: list, **kwargs) -> str:
        import ollama
        response = ollama.chat(
            model=self.model_name,
            messages=messages,
            options={
                "temperature": kwargs.get("temperature", 0.1),
                "num_predict": kwargs.get("max_tokens", 300),
            },
        )
        self.tokens += len(response["message"]["content"].split()) * 2
        return response["message"]["content"]

    def get_token_count(self) -> int:
        return self.tokens