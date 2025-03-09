from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

import os
load_dotenv()


class Chain:
    def __init__(self):
        self.llm=ChatGroq(temperature=0.5,groq_api_key="your_groq_api",model="mixtral-8x7b-32768")

    def extract_jobs(self,cleaned_text):
        
            # Define Prompt Template
            prompt_extract = PromptTemplate.from_template(
                """
                Scraped text from website:
                {page_data}

                ### Instruction:
                The scraped text is from the careers page of a website.
                Your job is to extract job postings and return them in **JSON format** containing
                the following keys: 'role', 'experience', 'skills', 'description'.

                Only return a **valid JSON** (no additional text), and every key should have a **list** as its value.
                
                ### Valid JSON Output (No preamble, only JSON):
                """
            )

            # Create a Chain
            chain_extract = prompt_extract | self.llm

            # Invoke the LLM with the extracted data
            res = chain_extract.invoke({"page_data": cleaned_text}) 

            json_parser=JsonOutputParser()
            res=json_parser.parse(res.content)

            return res if isinstance(res, list) else [res]
    def generate_email(self,job,links):
            prompt_email = PromptTemplate.from_template(
                """
                ### Job Description:
                {description}

                ### Instruction:
                You are Tharun, a softwarre engineer actively looking for job opportunities.  
                Craft a professional cold email expressing interest in this role. The email should:  
                - Start with a personalized greeting.  
                - Briefly introduce Tharun’s background and expertise in Data Science.  
                - Highlight relevant skills and projects aligning with the job description.  
                - Express enthusiasm and request the next steps for further discussion.  
                - Maintain a polite and professional tone.  
                also add two or threee portfolio links from{link_list} in the discription and make it short and impact ful

                Generate a compelling and concise email that maximizes engagement.
                ###Email(no peramble)
                """
            )

            chain_email=prompt_email | self.llm
            res=chain_email.invoke({"description":str(job),"link_list":links})

            return res.content