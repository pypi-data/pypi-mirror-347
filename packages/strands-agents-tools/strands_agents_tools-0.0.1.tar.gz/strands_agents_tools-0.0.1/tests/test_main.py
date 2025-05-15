"""Tests for the main module."""

from strands_agents_tools import main

def test_tools_hello():
    """Test the tools_hello function."""
    assert main.tools_hello() == "Hello from strands-agents-tools!"

def test_get_agent_greeting():
    """Test the get_agent_greeting function."""
    assert main.get_agent_greeting() == "Hello from strands-agents!"
