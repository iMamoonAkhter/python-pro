import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

from prompt import SYSTEM_PROMPT

# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================

load_dotenv()


def _not_found_app(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8")])
    return [b"Educational AI Assistant"]


app = application = handler = _not_found_app

# =====================================================
# PAGE CONFIG
# =====================================================
def load_css():
    try:
        with open("style.css", "r", encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except FileNotFoundError:
        st.warning("style.css file not found")


def run_streamlit_app():
    st.set_page_config(
        page_title="Educational AI Assistant",
        page_icon="🎓",
        layout="wide"
    )

    load_css()

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

    st.markdown(
        """
        <h1 style='text-align:center;'>
            🎓 Educational AI Assistant
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style='text-align:center; color:gray;'>
            Ask about admissions, courses, fees, schedules, campuses, and more.
        </p>
        """,
        unsafe_allow_html=True
    )

    for message in st.session_state.messages:

        if message["role"] == "system":
            continue

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input(
        "Ask a question..."
    )

    if user_input:

        with st.chat_message("user"):
            st.markdown(user_input)

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        with st.chat_message("assistant"):

            message_placeholder = st.empty()

            try:

                with st.spinner("Thinking..."):

                    response = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=st.session_state.messages,
                        temperature=0.7,
                        max_tokens=1024
                    )

                    bot_reply = response.choices[0].message.content

                    message_placeholder.markdown(bot_reply)

            except Exception as e:

                bot_reply = f"Error: {str(e)}"

                message_placeholder.error(bot_reply)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": bot_reply
            }
        )

    with st.sidebar:

        st.title("🎓 Information")

        st.markdown("---")

        st.markdown("""
        ### Quick Topics

        - Admissions
        - Courses
        - Fees
        - Timings
        - Scholarships
        - Campuses
        - Contact Information
        """)

        st.markdown("---")

        if st.button("🗑 Clear Chat"):

            st.session_state.messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                }
            ]

            st.rerun()

        st.markdown("---")

        st.caption("BRAINS COLLAGE AI ASSISTANT")


if __name__ == "__main__":
    run_streamlit_app()