import streamlit as st
from openai import OpenAI

# Set up OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Page Configuration ---
st.set_page_config(page_title="MSHI LLM Playground", page_icon="🤖", layout="wide")
st.sidebar.title("🛠️ LLM Configuration")

# --- Sidebar Settings ---
model = st.sidebar.selectbox("Model", ["gpt-4.1", "gpt-4o", "gpt-o4-mini"], index=0)
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.3, 0.1)
max_tokens = st.sidebar.slider("Max Tokens", 100, 1000, 500, 50)
top_p = st.sidebar.slider("Top P", 0.0, 1.0, 0.9, 0.1)
show_prompt = st.sidebar.checkbox("Show Full Request", value=True)

# --- Main UI ---
st.title("🧪 MSHI LLM Playground")
st.markdown("Enter custom **instructions** and a **prompt** to interact with an OpenAI LLM using the Responses API.")

instructions = st.text_area("🧾 Instructions", height=150, placeholder="e.g. Format a clinical note into SOAP format...")
input_text = st.text_area("📝 Prompt", height=200, placeholder="e.g. Pt here for f/u on HTN...")

if st.button("🧠 Get Response"):
    if not input_text.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Calling the LLM..."):

            response = client.responses.create(
                model=model,
                instructions=instructions,
                input=input_text,
                temperature=temperature,
                top_p=top_p,
                max_output_tokens=max_tokens,
            )

            output = response.output_text

        st.markdown("### 🧠 Model Response")
        st.markdown(output)

        if show_prompt:
            st.markdown("### 📦 Full Request Sent")
            st.code(f"INSTRUCTIONS:\n{instructions.strip()}\n\nINPUT:\n{input_text.strip()}", language="text")
