"""Streamlit app entrypoint for Agent Court."""

import streamlit as st

from agent_debate import run_debate
from ui.components import (
    inject_styles,
    render_debate_tabs,
    render_header,
    render_inputs,
    render_verdict_summary,
    set_page,
)


def main() -> None:
    set_page()
    inject_styles()
    render_header()
    topic, context, run_clicked = render_inputs()

    if run_clicked:
        if not topic.strip():
            st.error("Please enter a debate topic.")
            return

        with st.spinner("Running researcher, skeptic, and judge agents..."):
            results = run_debate(topic=topic.strip(), context=context.strip())

        researcher_argument = results["researcher_argument"]
        skeptic_argument = results["skeptic_argument"]
        verdict = results["verdict"]

        render_verdict_summary(verdict)
        render_debate_tabs(researcher_argument, skeptic_argument, verdict)


if __name__ == "__main__":
    main()
