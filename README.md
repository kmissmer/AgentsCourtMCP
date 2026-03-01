# Agent Court

A multi-agent debate system where AI agents argue different sides of a proposition, with an impartial judge evaluating and rendering a verdict. Built with Azure OpenAI, Streamlit, and the Model Context Protocol (MCP).

## Overview

Agent Court automates structured debates by orchestrating three specialized agents:

- **Marcus** – Argues for the first option presented in the debate topic
- **Colton** – Argues for the second option presented in the debate topic  
- **Pierce (Judge)** – Evaluates both arguments and renders an impartial verdict

Each agent can search the web, Reddit, and Wikipedia to gather evidence and build compelling cases. The system returns structured arguments with key points, sources, and a detailed report.

## Features

- **Multi-agent debate orchestration** – Three independent agents argue their respective sides
- **Tool-augmented reasoning** – Agents can search for evidence across multiple sources
- **Streamlit UI** – User-friendly interface for running debates and viewing results
- **Structured output** – Debate results include claims, key points, sources, and full reports
- **Flexible topics** – Handle two-choice debates, propositions, or single-topic rebuttals

## File Structure

```
AgentsCourtMCP/
├── README.md                           # This file
├── LICENSE                             # MIT License
├── requirements.txt                    # Python dependencies
├── config.py                           # Configuration and API credentials
├── agent_debate.py                     # Legacy CLI entry point (deprecated)
│
├── agents/
│   ├── __init__.py
│   ├── marcus.py                       # First-option debater agent
│   ├── colton.py                       # Second-option debater agent
│   └── judge.py                        # Pierce (judge) agent
│
├── core/
│   ├── __init__.py
│   ├── models.py                       # Pydantic models (Argument, Verdict, Source)
│   ├── prompts.py                      # System prompts for all agents
│   └── orchestrator.py                 # Main debate orchestration logic
│
├── mcp/
│   ├── __init__.py
│   ├── server.py                       # MCP server and tool registry
│   └── tools/
│       ├── __init__.py
│       ├── search_reddit.py            # Reddit search tool (via Tavily)
│       └── search_wikipedia.py         # Wikipedia search tool (via Tavily)
│
├── ui/
│   ├── __init__.py
│   ├── components.py                   # Streamlit UI components
│   └── styles.css                      # Custom CSS styling
│
└── streamlit_app.py                    # Main Streamlit application entry point
```

## Installation

### Prerequisites

- Python 3.9+
- Azure OpenAI API key
- Tavily API key (for web search tools)

### Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd AgentsCourt
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create .env file in teh same structure as .env.example**
- This requires the Azure OpenAI API key, Endpoint, API Version, and Model Deployment
- It also requires the Tavily API Key

## Usage

### Streamlit UI

Run the interactive web interface:

```bash
streamlit run streamlit_app.py
```

1. Enter a debate topic (e.g., "remote work vs in-office work")
2. Optionally add context or constraints
3. Click **Run Debate**
4. View Marcus's argument, Colton's argument, and Pierce's verdict on separate tabs


## Architecture

### Data Models

**Argument** – Produced by Marcus and Colton agents:
- `side` – "Marcus" or "Colton"
- `headline_claim` – Short summary of the main argument
- `key_points` – List of 3 key supporting points
- `sources` – List of Source objects (title, URL, snippet, domain)
- `full_report` – 300–500 word detailed argument

**Verdict** – Produced by Pierce (judge):
- `winner` – "Marcus", "Colton", or "DRAW"
- `judge_reasoning` – Detailed analysis of both arguments
- `closing_summary` – 2–3 sentence plain English verdict

**Source** – Evidence reference:
- `title` – Source title/article headline
- `url` – Link to the source
- `snippet` – Quote or summary from the source
- `domain` – Website domain

### Agent Flow

1. **Input** – User provides a debate topic and optional context
2. **Marcus** → Searches for evidence supporting the first option
3. **Colton** → Searches for evidence supporting the second option
4. **Pierce** → Reads both arguments and evaluates them objectively
5. **Output** → Structured debate results with verdict

### Tool Integration (MCP)

Agents can call two search tools via the Model Context Protocol:

- **search_reddit** – Community opinions and discussions
- **search_wikipedia** – Factual background and encyclopedic knowledge

## Prompts

All agent system prompts are defined in `core/prompts.py`:

- **MARCUS_PROMPT** – Instructs Marcus to take the first option
- **COLTON_PROMPT** – Instructs Colton to take the second option
- **JUDGE_PROMPT** – Instructs Pierce to evaluate objectively

Modify these prompts to adjust agent behavior, tone, or reasoning style.

## Future Developments

- Adding new search tools
- Full MCP integration

## Where Copilot Helped
-  Copilot allowed us to speed up development time greatly. A project that wouldve likely taken weeks without it took days instead. An example of a tedious task Copilot was able to speed up was when we wanted to change the agents names at the end of our project. Normally that would be a boring tedious tasks that would take a while because we would have to go through every file and make sure every name is changed correctly. However, Copilot was able to compelte this tedious task for us in seconds.
-  Copilot helped us brainstorm ideas for this project. For example, we asked Copilot advice on file structure to hear other opinions on how the project can be as maintainable as possible.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
