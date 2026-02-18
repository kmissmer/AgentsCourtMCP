"""
Researcher agent: argues in favor.
"""

from .common import client, deployment, search_for_information


def researcher_agent(topic: str, context: str = "") -> str:
	"""
	Agent that argues IN FAVOR of a cause/topic.
	Searches for supporting evidence and builds the best case.
	"""
	print("\n" + "=" * 80)
	print("RESEARCHER AGENT - Building the case IN FAVOR")
	print("=" * 80)

	# Search for supporting evidence (from both Reddit and Wikipedia)
	search_query = f"{topic} benefits advantages positive"
	search_results = search_for_information(search_query, max_results=5, source="both")

	print("\n[Search Results]")
	print(search_results)

	# Prompt the researcher to build the best case
	messages = [
		{
			"role": "system",
			"content": """You are a skilled advocate arguing IN FAVOR of a position. Your job is to:
1. Review the evidence provided
2. Build the strongest possible case for supporting this position
3. Highlight key benefits, advantages, and positive outcomes
4. Anticipate and preemptively address counterarguments
5. Use logical reasoning and evidence to support your position

Be persuasive, well-reasoned, and cite the evidence provided. Present your argument in a clear, structured format.""",
		},
		{
			"role": "user",
			"content": f"""Topic: {topic}

Evidence from community discussions and research:
{search_results}

{f"Additional context: {context}" if context else ""}

Please present your strongest argument IN FAVOR of this position. Be comprehensive but concise (500-800 words).""",
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
	print("\n[RESEARCHER'S ARGUMENT]")
	print(argument)

	return argument
