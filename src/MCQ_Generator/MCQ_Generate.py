import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.MCQ_Generator.utils import read_file, get_table_data
from src.MCQ_Generator.logger import logging

#Importing necessary packages from LangChain
# NEW (correct)
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain, SequentialChain

#Loading environment variables from .env file
load_dotenv()

#Access the environment variables via .env file
key=os.getenv("my_openrouter_key")

llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY") or os.getenv("my_openrouter_key"),
    base_url="https://openrouter.ai/api/v1",
    model="openai/gpt-4o-mini",
    temperature=0.7
)


TEMPLATE="""
Text:{text}
You are an expert MCQ generator. Given the above text, it is your job to \ 
create a quiz of {number} Multiple CHoice Question for {subject} in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as guide.\
Ensure to make {number} MCQs.
### RESPONSE_JSON 
{response_json}
""" 

quiz_generation_prompt = PromptTemplate(
    input_variables = {"text","number","subject","tone","response_json"}, #Variables which user will pass in prompt
    template = TEMPLATE
)

quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz",verbose=True) 


TEMPLATE2 = """
You are an expert English grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity.
If the quiz is not at per with the cognitive and analytical abilities of the students,\ 
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student's ability.
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""
quiz_evaluation_prompt=PromptTemplate(input_variables=["subject","quiz"],template=TEMPLATE)

review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

#This is an Overall Chain where we run the two chains in Sequence.
generate_evaluate_chain=SequentialChain(
    chains=[quiz_chain,review_chain],
    input_variables=["text","number","subject","tone","response_json"],
    output_variables=["quiz","review"],
    verbose=True
)
