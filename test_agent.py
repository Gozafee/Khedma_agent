import pytest
from agent import KhedmaAgent

def test_collect_all_data():
    agent = KhedmaAgent()
    agent.run("اسمي يوسف، رقم هويتي 123456، أريد تجديد الجواز للسفر، أنا في الخرطوم")
    assert agent.state["done"] is True
    assert len(agent.state["collected_fields"]) == 4

def test_stops_after_5_turns():
    agent = KhedmaAgent()
    for _ in range(6):
        agent.run("أنا يوسف")
    assert "Max turns" in agent.run("أنا يوسف")

def test_token_budget():
    agent = KhedmaAgent()
    agent.token_usage = 6000
    assert "Budget" in agent.run("اسمي يوسف")

def test_hallucination_detection():
    agent = KhedmaAgent()
    result = agent.run("هالوسة")
    assert agent.state["hallucination_triggered"] is True
    assert "Hallucination" in result
