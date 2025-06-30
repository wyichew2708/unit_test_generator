import os
import streamlit as st

from utils.feedback_loop import FeedbackLoop, UserInput


def list_files(repo_path: str):
    files = []
    for root, _, filenames in os.walk(repo_path):
        for name in filenames:
            if name.endswith('.py'):
                files.append(os.path.relpath(os.path.join(root, name), repo_path))
    return files


st.title("AI Test Script Generator")

repo_path = st.text_input("Link to repository", value=".")
files = list_files(repo_path) if os.path.isdir(repo_path) else []
if files:
    target_file = st.selectbox("Target file", options=files)
else:
    target_file = st.text_input("Target file path")

test_types = st.multiselect("Types of tests", ["unit", "integration"], default=["unit"])
language = st.selectbox("Target language", ["Python", "C#"], index=0)
framework = st.text_input("Preferred testing framework", value="pytest")
output_mode = st.selectbox("Target output", ["download", "show"], index=0)
user_prompt = st.text_area("Additional prompt", "")
config_path = st.text_input("Config file", value="ollama_config.json")

if st.button("Generate Tests") and target_file:
    loop = FeedbackLoop(config_path=config_path)
    input_data = UserInput(
        repo_path=repo_path,
        target_file=target_file,
        test_types=list(test_types) if test_types else ["unit"],
        language=language.lower(),
        framework=framework,
        output_mode=output_mode,
        user_prompt=user_prompt,
        output_path="generated_tests/test_generated.py",
    )
    test_code = loop.run(input_data)
    if output_mode == "download":
        st.download_button("Download test script", test_code, file_name="test_generated.py")
    else:
        st.code(test_code, language="python")
