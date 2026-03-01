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
    st.caption("Marcus vs Colton debate, decided by Pierce (Judge)")


def render_inputs() -> tuple[str, str, bool]:
    topic = st.text_input(
        "Debate topic",
        placeholder="e.g. 'Is remote work better than in-office work?'",
        help="Enter a single proposition to debate.",
    )
    context = st.text_area(
        "Optional context",
        placeholder="input any additional context or constraints for the debate here",
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


def render_debate_tabs(marcus_argument, colton_argument, verdict) -> None:
    tab_for, tab_against, tab_judge = st.tabs(["Marcus", "Colton", "Judge"])

    with tab_for:
        st.subheader(marcus_argument.headline_claim)
        st.markdown("**Key Points**")
        for point in marcus_argument.key_points:
            st.write(f"- {point}")
        st.markdown("**Full Report**")
        st.write(marcus_argument.full_report)
        st.markdown("**Sources**")
        render_sources(marcus_argument.sources)

    with tab_against:
        st.subheader(colton_argument.headline_claim)
        st.markdown("**Key Points**")
        for point in colton_argument.key_points:
            st.write(f"- {point}")
        st.markdown("**Full Report**")
        st.write(colton_argument.full_report)
        st.markdown("**Sources**")
        render_sources(colton_argument.sources)

    with tab_judge:
        st.markdown("**Judge Reasoning**")
        st.write(verdict.judge_reasoning)
        st.markdown("**Closing Summary**")
        st.info(verdict.closing_summary)


def render_debate_page(marcus_argument, colton_argument, verdict) -> None:
    if "debate_view" not in st.session_state:
        st.session_state.debate_view = "Marcus"

    # Top row with a right-aligned back button
    top_cols = st.columns([1, 8, 1])
    with top_cols[2]:
        if st.button("Run another debate"):
            st.session_state.pop("debate_results", None)
            st.session_state["show_debate"] = False
            st.rerun()

    left_col, main_col, right_col = st.columns([1, 3, 1], gap="small")

    with left_col:
        if st.button("Marcus", use_container_width=True):
            st.session_state.debate_view = "Marcus"
        if st.button("Colton", use_container_width=True):
            st.session_state.debate_view = "Colton"
        if st.button("Judge", use_container_width=True):
            st.session_state.debate_view = "Judge"

    choice = st.session_state.debate_view

    with main_col:
        if choice == "Marcus":
            st.subheader(marcus_argument.headline_claim)
            st.markdown("**Key Points**")
            for point in marcus_argument.key_points:
                st.write(f"- {point}")
            st.markdown("**Full Report**")
            st.write(marcus_argument.full_report)

        elif choice == "Colton":
            st.subheader(colton_argument.headline_claim)
            st.markdown("**Key Points**")
            for point in colton_argument.key_points:
                st.write(f"- {point}")
            st.markdown("**Full Report**")
            st.write(colton_argument.full_report)

        else:
            st.markdown("**Judge Reasoning**")
            st.write(verdict.judge_reasoning)
            st.markdown("**Closing Summary**")
            st.write(verdict.closing_summary)

    with right_col:
        if choice == "Marcus":
            st.markdown("**Sources**")
            for index, source in enumerate(marcus_argument.sources or [], start=1):
                st.link_button(f"{index}. {source.title}", source.url, use_container_width=True)

        elif choice == "Colton":
            st.markdown("**Sources**")
            for index, source in enumerate(colton_argument.sources or [], start=1):
                st.link_button(f"{index}. {source.title}", source.url, use_container_width=True)

        else:
            st.caption("No sources for judge.")