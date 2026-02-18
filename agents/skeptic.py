"""
Skeptic agent: argues against.
"""

from .common import client, deployment, search_for_information


def skeptic_agent(topic: str, researcher_argument: str, context: str = "") -> str:
	"""
	Agent that argues AGAINST a cause/topic.
	Searches for counterevidence and builds the strongest opposing case.
	"""
	print("\n" + "=" * 80)
	print("SKEPTIC AGENT - Building the case AGAINST")
	print("=" * 80)

	# Search for opposing evidence (from both Reddit and Wikipedia)
	search_query = f"{topic} criticisms risks disadvantages negative concerns"
	search_results = search_for_information(search_query, max_results=5, source="both")

	print("\n[Search Results]")
	print(search_results)

	# Prompt the skeptic to build the strongest opposing case
	messages = [
		{
			"role": "system",
			"content": """You are a skilled critic arguing AGAINST a position. Your job is to:
1. Review the evidence provided
2. Build the strongest possible case against this position
3. Highlight risks, disadvantages, and negative outcomes
4. Address and refute the opposing argument
5. Identify logical fallacies or weaknesses in the other side's reasoning
6. Use evidence to support your counterargument

Be persuasive, well-reasoned, and cite the evidence provided. Present your argument in a clear, structured format.""",
		},
		{
			"role": "user",
			"content": f"""Topic: {topic}

Evidence from community discussions and research:
{search_results}

The Researcher's Argument (which you must counter):
{researcher_argument}

{f"Additional context: {context}" if context else ""}

Please present your strongest argument AGAINST this position and refute the researcher's claims. Be comprehensive but concise (500-800 words).""",
		},
	]

	response = client.chat.completions.create(
		messages=messages,
		max_tokens=1000,
		temperature=0.7,
		top_p=1.0,
		model=deployment,
	)

	argument = response.choices[0].message.content
	print("\n[SKEPTIC'S ARGUMENT]")
	print(argument)

	return argument
