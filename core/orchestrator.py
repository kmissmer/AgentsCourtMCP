"""
Core orchestration for the Agents Court debate system.

This module exports the `run_debate` function which executes a full
round of the debate: Kaleb takes the first option, Alan takes the second,
and the judge issues a verdict.  Other parts of the application (Streamlit UI,
CLI tools, tests, etc.) should import from here rather than the
legacy script.
"""

from agents.marcus import marcus_agent
from agents.colton import colton_agent
from agents.judge import judge_agent
from core.models import Argument


def run_debate(topic: str, context: str = "") -> dict:
    """Run a full debate cycle: Kaleb -> Alan -> Judge.

    Args:
        topic:   The proposition being debated (typically two options)
        context: Optional framing or constraints for the agents

    Returns:
        {
            "topic":             str,
            "context":           str,
            "marcus_argument":   Argument,
            "colton_argument":   Argument,
            "verdict":           Verdict,
        }
    """
    print(f"\n{'#' * 80}")
    print(f"# AGENTS COURT: '{topic}'")
    print(f"{'#' * 80}\n")

    # Round 1: Marcus builds the case for the first option
    marcus_argument = marcus_agent(topic, context)
    if not isinstance(marcus_argument, Argument):
        raise TypeError(
            f"Marcus failed. Expected Argument object, got {type(marcus_argument)}: {marcus_argument}"
        )

    # Round 2: Colton builds the case for the second option
    colton_argument = colton_agent(topic, context)
    if not isinstance(colton_argument, Argument):
        raise TypeError(
            f"Colton failed. Expected Argument object, got {type(colton_argument)}: {colton_argument}"
        )

    # Round 3: Judge (Pierce) reads both and renders a verdict
    verdict = judge_agent(topic, marcus_argument, colton_argument)

    results = {
        "topic": topic,
        "context": context,
        "marcus_argument": marcus_argument,
        "colton_argument": colton_argument,
        "verdict": verdict,
    }

    # Print summary to console
    print(f"\n{'=' * 80}")
    print("DEBATE COMPLETE")
    print(f"{'=' * 80}")
    print(f"Topic:   {topic}")
    print(f"Winner:  {verdict.winner}")
    print(f"Summary: {verdict.closing_summary}")
    print(f"{'=' * 80}\n")

    return results
