import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.MCQ_Generator.utils import read_file, get_table_data
import streamlit as st
from langchain_community.callbacks import get_openai_callback
from src.MCQ_Generator.MCQ_Generate import generate_evaluate_chain
from src.MCQ_Generator.logger import logging

# Load environment variables (Make sure your .env or Streamlit Secrets are set)
load_dotenv()

# Loading json file safely using the correct file descriptor variable
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, 'Response.json')

with open(json_path, 'r') as file:
    RESPONSE_JSON = json.load(file)

# Creating a title for the application
st.title("MCQs Generator Application with LangChain 🦜🔗")

# Creating a form using st.form
with st.form("user_inputs"):
    # File Upload
    uploaded_file = st.file_uploader("Upload a PDF or TXT File")

    # Input Fields
    mcq_count = st.number_input("Number of MCQs: ", min_value=3, max_value=50)

    # Subject
    subject = st.text_input("Insert the Subject: ", max_chars=20)

    # Quiz Tone
    tone = st.text_input("Complexity Level of Questions", max_chars=20, placeholder="SIMPLE")

    # Add Button
    button = st.form_submit_button("Generate MCQs")

# Logic execution outside the UI form layout block
if button and uploaded_file is not None and mcq_count and subject and tone:
    with st.spinner("GENERATING...."):
        try:
            text = read_file(uploaded_file)
            
            # Keep all token data tracking inside the active callback context manager window
            with get_openai_callback() as cb:
                response = generate_evaluate_chain(
                    {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    }
                )
                
            # Log backend metrics straight to your cloud server terminal console
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost: {cb.total_cost}")

            # Process the response output metrics safely
            if isinstance(response, dict):
                quiz = response.get("quiz", None)
                if quiz is not None:
                    table_data = get_table_data(quiz)
                    if table_data is not None:
                        df = pd.DataFrame(table_data)
                        df.index = df.index + 1
                        st.table(df)

                        # Display the evaluation review in a textbox
                        st.text_area(label="Review", value=response.get("review", ""))
                    else:
                        st.error("Error structural layout discrepancy in the Table Data processing!")
                else:
                    st.write(response)

        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("An internal error occurred during the LangChain compilation sequence.")
