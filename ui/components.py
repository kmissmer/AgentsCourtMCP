"""
Reusable Streamlit UI components for Agent Court.
"""

from pathlib import Path

import streamlit as st


def set_page() -> None:
    st.set_page_config(page_title="Agent Court", page_icon="⚖️", layout="wide")


def inject_styles(css_path: str = "ui/styles.css") -> None:
    css_file = Path(css_path)
    if css_file.exists():
        css = css_file.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_header() -> None:
    st.title("⚖️ Agent Court")
    st.caption("Researcher (FOR) vs Skeptic (AGAINST), decided by Judge")


def render_inputs() -> tuple[str, str, bool]:
    topic = st.text_input(
        "Debate topic",
        value="Remote work is better than office work",
        help="Enter a single proposition to debate.",
    )
    context = st.text_area(
        "Optional context",
        value="Consider productivity, work-life balance, collaboration, and employee satisfaction.",
        height=100,
    )
    run_clicked = st.button("Run Debate", type="primary", use_container_width=True)
    return topic, context, run_clicked


def render_sources(sources) -> None:
    if not sources:
        st.caption("No sources returned.")
        return

    for index, source in enumerate(sources, start=1):
        st.markdown(f"**{index}. {source.title}**")
        st.write(f"Domain: {source.domain}")
        st.write(source.snippet)
        st.link_button("Open source", source.url)


def render_verdict_summary(verdict) -> None:
    st.success(f"Winner: {verdict.winner}")


def render_debate_tabs(researcher_argument, skeptic_argument, verdict) -> None:
    tab_for, tab_against, tab_judge = st.tabs(["Researcher (FOR)", "Skeptic (AGAINST)", "Judge"])

    with tab_for:
        st.subheader(researcher_argument.headline_claim)
        st.markdown("**Key Points**")
        for point in researcher_argument.key_points:
            st.write(f"- {point}")
        st.markdown("**Full Report**")
        st.write(researcher_argument.full_report)
        st.markdown("**Sources**")
        render_sources(researcher_argument.sources)

    with tab_against:
        st.subheader(skeptic_argument.headline_claim)
        st.markdown("**Key Points**")
        for point in skeptic_argument.key_points:
            st.write(f"- {point}")
        st.markdown("**Full Report**")
        st.write(skeptic_argument.full_report)
        st.markdown("**Sources**")
        render_sources(skeptic_argument.sources)

    with tab_judge:
        st.markdown("**Judge Reasoning**")
        st.write(verdict.judge_reasoning)
        st.markdown("**Closing Summary**")
        st.info(verdict.closing_summary)
