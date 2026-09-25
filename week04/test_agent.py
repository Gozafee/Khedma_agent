"""
Pytest tests for Week 4 - proving failure conditions.
Each test proves a specific control mechanism.
"""
import pytest
from agent import KhedmaAgent


def test_collect_all_data():
    """Happy path: agent collects all 4 required fields."""
    agent = KhedmaAgent()
    agent.run(
        "اسمي يوسف، رقم هويتي 123456، أريد تجديد الجواز للسفر، أنا في الخرطوم"
    )
    assert agent.state["done"] is True
    assert len(agent.state["collected_fields"]) == 4


def test_stops_after_5_turns():
    """Failure control: agent stops at turn cap (runaway loop prevention)."""
    agent = KhedmaAgent()
    for _ in range(6):
        agent.run("أنا يوسف")
    assert "Max turns" in agent.run("أنا يوسف")
    assert agent.turn_count <= agent.max_turns


def test_token_budget():
    """Failure control: agent respects token budget."""
    agent = KhedmaAgent()
    agent.token_usage = 6000
    assert "Budget" in agent.run("اسمي يوسف")


def test_hallucination_detection():
    """Failure control: agent detects hallucinated tool calls."""
    agent = KhedmaAgent()
    result = agent.run("هالوسة")
    assert agent.state["hallucination_triggered"] is True
    assert "Hallucination" in result