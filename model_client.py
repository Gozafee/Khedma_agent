from abc import ABC, abstractmethod

class ModelClient(ABC):
    @abstractmethod
    def generate(self, messages: list, **kwargs) -> str:
        pass
    
    @abstractmethod
    def get_token_count(self) -> int:
        pass

class MockModelClient(ModelClient):
    def __init__(self):
        self.tokens = 0
        
    def generate(self, messages: list, **kwargs) -> str:
        self.tokens += 50
        user_msg = messages[-1]["content"] if messages else ""
        
        if "my name" in user_msg or "name" in user_msg.lower():
            return '{"name": "Yousif", "national_id": "123456", "reason": "travel", "location": "Khartoum"}'
        else:
            return "Missing fields: name, national_id, reason, location"
    
    def get_token_count(self) -> int:
        return self.tokens
