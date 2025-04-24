import streamlit as st
from openai import OpenAI
import os

# Set up OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Sidebar Configuration ---
st.sidebar.title("🛠️ LLM Configuration")

model = st.sidebar.selectbox("Model", ["gpt-4.1", "gpt-3.5-turbo"], index=0)
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.3, 0.1)
max_tokens = st.sidebar.slider("Max Tokens", 100, 1000, 500, 50)
show_prompt = st.sidebar.checkbox("Show Prompt", value=True)

# --- Main UI ---
st.title("🩺 Clinical Note ➜ SOAP Formatter")
st.markdown("Paste a raw clinical note and click 'Format Note' to see the LLM generate a structured SOAP format.")

note_input = st.text_area("📄 Clinical Note Input", height=200, placeholder="e.g. Pt here for f/u on HTN...")

if st.button("🧠 Format Note"):
    if not note_input.strip():
        st.warning("Please enter a clinical note first.")
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
                max_tokens=max_tokens
            )

            output = response.output_text

        st.markdown("### 🧾 Formatted SOAP Note:")
        st.code(output)

        if show_prompt:
            st.markdown("### 📦 Prompt Sent to API")
            st.code(f"{instructions.strip()}\n\n{input_text.strip()}")
