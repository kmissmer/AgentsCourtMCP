"""
Judge agent: weighs arguments and renders a verdict.
"""

from .common import client, deployment


def judge_agent(topic: str, researcher_arg: str, skeptic_arg: str, context: str = "") -> dict:
	"""
	Agent that acts as a judge.
	Weighs both arguments, identifies stronger logic, and renders judgment.
	"""
	print("\n" + "=" * 80)
	print("JUDGE AGENT - Weighing Arguments and Rendering Judgment")
	print("=" * 80)

	# Prompt the judge to evaluate both arguments
	messages = [
		{
			"role": "system",
			"content": """You are an impartial judge evaluating a debate. Your job is to:
1. Carefully analyze both arguments
2. Assess the quality of evidence and reasoning
3. Identify strengths and weaknesses in each position
4. Consider logical consistency and validity
5. Weigh the merits of each side fairly
6. Render a judgment on which side has the stronger case

You must be objective, thorough, and justify your reasoning with specific examples from the arguments.""",
		},
		{
			"role": "user",
			"content": f"""Topic: {topic}

RESEARCHER'S ARGUMENT (In Favor):
{researcher_arg}

---

SKEPTIC'S ARGUMENT (Against):
{skeptic_arg}

{f"Additional context: {context}" if context else ""}

Please evaluate both arguments and provide:
1. Analysis of the Researcher's argument (strengths and weaknesses)
2. Analysis of the Skeptic's argument (strengths and weaknesses)
3. Key differences and points of contention
4. Your verdict: Which side has the stronger case?
5. Justification for your verdict with specific reasoning""",
		},
	]

	response = client.chat.completions.create(
		messages=messages,
		max_tokens=1500,
		temperature=0.7,
		top_p=1.0,
		model=deployment,
	)

	judgment = response.choices[0].message.content
	print("\n[JUDGE'S VERDICT]")
	print(judgment)

	# Extract a simple verdict (Pro, Con, or Neutral)
	judgment_lower = judgment.lower()
	if "researcher" in judgment_lower and (
		"stronger" in judgment_lower
		or "prevail" in judgment_lower
		or "favors" in judgment_lower
		or "support" in judgment_lower
	):
		verdict = "PRO"
	elif "skeptic" in judgment_lower and (
		"stronger" in judgment_lower or "prevail" in judgment_lower or "favors" in judgment_lower
	):
		verdict = "CON"
	else:
		verdict = "NEUTRAL/MIXED"

	return {
		"judgment": judgment,
		"verdict": verdict,
		"topic": topic,
	}
