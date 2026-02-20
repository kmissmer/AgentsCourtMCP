"""
agent_debate.py — Test runner for the Agents Court debate system.

Use this to run and validate the full debate pipeline.
Streamlit app will eventually be built, but if you wanna test the agents 
on the backend this will be how for now. Only works in a jupyter interactive window 
because thats how we code lol.

Usage:
    python agent_debate.py
"""

from agents.researcher import researcher_agent
from agents.skeptic import skeptic_agent
from agents.judge import judge_agent
from core.models import Argument


def run_debate(topic: str, context: str = "") -> dict:
    """
    Run a full debate cycle: Researcher → Skeptic → Judge.

    This is the core orchestration function. The Streamlit app will
    call this directly — do not change the return shape.

    Args:
        topic:   The proposition being debated
        context: Optional framing or constraints for the agents

    Returns:
        {
            "topic":               str,
            "context":             str,
            "researcher_argument": Argument,
            "skeptic_argument":    Argument,
            "verdict":             Verdict,
        }
    """
    print(f"\n{'#' * 80}")
    print(f"# AGENTS COURT: '{topic}'")
    print(f"{'#' * 80}")

    # Round 1: Researcher builds the FOR case
    researcher_argument = researcher_agent(topic, context)
    
    # Validate researcher_argument
    if not isinstance(researcher_argument, Argument):
        raise TypeError(f"Researcher agent failed. Expected Argument object, got {type(researcher_argument)}: {researcher_argument}")

    # Round 2: Skeptic sees the FOR case and builds the AGAINST case
    skeptic_argument = skeptic_agent(topic, context)
    
    # Validate skeptic_argument
    if not isinstance(skeptic_argument, Argument):
        raise TypeError(f"Skeptic agent failed. Expected Argument object, got {type(skeptic_argument)}: {skeptic_argument}")

    # Round 3: Judge reads both and renders a verdict (no tools, reasoning only)
    verdict = judge_agent(topic, researcher_argument, skeptic_argument)

    results = {
        "topic": topic,
        "context": context,
        "researcher_argument": researcher_argument,
        "skeptic_argument": skeptic_argument,
        "verdict": verdict,
    }

    # Print summary
    print(f"\n{'=' * 80}")
    print("DEBATE COMPLETE")
    print(f"{'=' * 80}")
    print(f"Topic:   {topic}")
    print(f"Winner:  {verdict.winner}")
    print(f"Summary: {verdict.closing_summary}")
    print(f"{'=' * 80}")

    return results