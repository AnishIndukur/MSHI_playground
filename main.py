import streamlit as st
from openai import OpenAI
import os

# Set up OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Page Configuration ---
st.set_page_config(page_title="MSHI LLM Playground", page_icon="🤖", layout="wide")
st.sidebar.title("🛠️ LLM Configuration")


model = st.sidebar.selectbox("Model", ["gpt-4.1", "gpt-4o", "gpt-o4-mini"], index=0)
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.3, 0.1)
max_tokens = st.sidebar.slider("Max Tokens", 100, 1000, 500, 50)
top_p = st.sidebar.slider("Top P", 0.0, 1.0, 0.9, 0.1)
show_prompt = st.sidebar.checkbox("Show Prompt", value=True)

# --- Main UI ---
st.title("LLM Playground")
st.markdown("Paste your prompt below and click 'Get Response' to send to OpenAI.")

note_input = st.text_area("📄 Prompt Input", height=200, placeholder="e.g. Pt here for f/u on HTN...")

if st.button("🧠 Format Note"):
    if not note_input.strip():
        st.warning("Please enter a prompt first.")
    else:
        with st.spinner("Formatting with LLM..."):

            instructions = """
                You are a medical assistant helping to format clinical notes into a structured SOAP format.

                Return the result in this layout:

                S: <Subjective content>
                O: <Objective content>
                A: <Assessment>
                P: <Plan>

                Do not include any extra text or explanations.
            """

            input_text = f"Format this clinical note into a SOAP format:\n{note_input}"

            response = client.responses.create(
                model=model,
                instructions=instructions,
                input=input_text,
                temperature=temperature,
                tools=[],
                max_output_tokens=max_tokens,
                top_p=top_p,
            )

            output = response.output_text

        st.markdown("Response:")
        st.code(output)

        if show_prompt:
            st.markdown("### 📦 Prompt Sent to API")
            st.code(f"{instructions.strip()}\n\n{input_text.strip()}")
