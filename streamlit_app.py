"""Streamlit app entrypoint for Agent Court."""

import streamlit as st

from core.orchestrator import run_debate
from ui.components import (
    inject_styles,
    render_debate_page,
    render_header,
    render_inputs,
    render_verdict_summary,
    set_page,
)


def main() -> None:
    set_page()
    inject_styles()

    # show inputs only if we haven't run a debate yet
    if not st.session_state.get("show_debate"):
        render_header()
        topic, context, run_clicked = render_inputs()

        if run_clicked:
            if not topic.strip():
                st.error("Please enter a debate topic.")
                return

            with st.spinner("Running Marcus, Colton, and Pierce (Judge) agents..."):
                results = run_debate(topic=topic.strip(), context=context.strip())

            # store results and navigate to debate page
            st.session_state["debate_results"] = results
            st.session_state["show_debate"] = True
            st.rerun()

    # if somebody already ran a debate, show only the results page
    if st.session_state.get("show_debate") and st.session_state.get("debate_results"):
        results = st.session_state["debate_results"]
        marcus_argument = results["marcus_argument"]
        colton_argument = results["colton_argument"]
        verdict = results["verdict"]

        render_verdict_summary(verdict)
        render_debate_page(marcus_argument, colton_argument, verdict)


if __name__ == "__main__":
    main()
