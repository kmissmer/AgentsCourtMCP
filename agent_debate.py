"""
Multi-agent debate system: Researcher vs Skeptic with Judge arbitration.

Three agents discuss a topic:
1. Researcher Agent - argues in favor
2. Skeptic Agent - argues against
3. Judge Agent - weighs both arguments and renders judgment
"""

import json

from agents.researcher import researcher_agent
from agents.skeptic import skeptic_agent
from agents.judge import judge_agent


def run_debate(topic: str, context: str = "") -> dict:
    """
    Run a full debate cycle: Proponent -> Opponent -> Judge.
    
    Args:
        topic: The topic/cause to debate
        context: Optional additional context for the debate
        
    Returns:
        Dictionary containing full debate results
    """
    print(f"\n{'#'*80}")
    print(f"# AGENT COURT: DEBATE ON '{topic}'")
    print(f"{'#'*80}")
    
    # Round 1: Researcher builds case
    researcher_argument = researcher_agent(topic, context)

    # Round 2: Skeptic responds
    skeptic_argument = skeptic_agent(topic, researcher_argument, context)

    # Round 3: Judge renders verdict
    judgment = judge_agent(topic, researcher_argument, skeptic_argument, context)
    
    # Compile results
    results = {
        "topic": topic,
        "context": context,
        "researcher_argument": researcher_argument,
        "skeptic_argument": skeptic_argument,
        "judge_verdict": judgment["judgment"],
        "judge_decision": judgment["verdict"],
    }
    
    print("\n" + "="*80)
    print("DEBATE SUMMARY")
    print("="*80)
    print(f"Topic: {topic}")
    print(f"Judge's Decision: {judgment['verdict']}")
    print("="*80)
    
    return results


if __name__ == "__main__":
    # Example: Debate about remote work
    topic = "Remote work is better than office work"
    context = "Consider productivity, work-life balance, collaboration, and employee satisfaction."
    
    results = run_debate(topic, context)
    
    # Save results to file
    with open("debate_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n✓ Debate complete! Results saved to debate_results.json")
