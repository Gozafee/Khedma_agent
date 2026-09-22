import json
from model_client import MockModelClient

class KhedmaAgent:
    def __init__(self, model_client=None):
        self.model = model_client if model_client else MockModelClient()
        self.max_turns = 5
        self.max_tokens = 5000
        self.turn_count = 0
        self.token_usage = 0
        
        self.state = {
            "user_data": {},
            "collected_fields": [],
            "required_fields": ["name", "national_id", "reason", "location"],
            "done": False,
            "hallucination_triggered": False
        }
        self.trace = []
    
    def _think(self, user_input: str) -> dict:
        messages = [
            {"role": "system", "content": "Extract from user message: name, national_id, reason, location. Respond in JSON format."},
            {"role": "user", "content": user_input}
        ]
        response = self.model.generate(messages)
        self.token_usage = self.model.get_token_count()
        
        try:
            return json.loads(response)
        except:
            return {}
    
    def _act(self, extracted: dict) -> str:
        missing = []
        for field in self.state["required_fields"]:
            if field in extracted and extracted[field]:
                if field not in self.state["collected_fields"]:
                    self.state["user_data"][field] = extracted[field]
                    self.state["collected_fields"].append(field)
            else:
                missing.append(field)
        
        if not missing:
            self.state["done"] = True
            return "All data collected!"
        return f"Missing: {', '.join(missing)}"
    
    def _observe(self, user_input: str) -> str:
        if "Hallucination" in user_input:
            self.state["hallucination_triggered"] = True
            return "Hallucination detected!"
        
        extracted = self._think(user_input)
        result = self._act(extracted)
        
        self.trace.append({
            "turn": self.turn_count + 1,
            "input": user_input,
            "extracted": extracted,
            "result": result,
            "tokens": self.token_usage
        })
        self.turn_count += 1
        return result
    
    def run(self, user_input: str) -> str:
        if self.turn_count >= self.max_turns:
            return f"Max turns ({self.max_turns}) exceeded."
        if self.token_usage > self.max_tokens:
            return f"Budget ({self.max_tokens}) exceeded."
        if self.state["done"]:
            return f"Complete: {self.state['user_data']}"
        return self._observe(user_input)
    
    def reset(self):
        self.turn_count = 0
        self.token_usage = 0
        self.state = {
            "user_data": {},
            "collected_fields": [],
            "required_fields": ["name", "national_id", "reason", "location"],
            "done": False,
            "hallucination_triggered": False
        }
        self.trace = []
    
    def get_trace(self):
        return self.trace
