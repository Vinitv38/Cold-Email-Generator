import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key= os.getenv('GROQ_API_KEY'),
            model_name="llama-3.1-70b-versatile"

        )

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(

            """
            ### SCRAPPED TEST FROM WEBSITE:
            {page_data}
            ### INSTRUCTION 
            The scrapped text is from the career's page of a website.
            Yor job is to extract the job postings and return them in JSON fromat containing following keys: `role`, `expereience`, `skills`, and `description`.
            Only return the purely valid JSON.
            ### VALID JSON (NO PREAMBLE):"""

        )

        chain_extract = prompt_extract | self.llm | JsonOutputParser()
        res = chain_extract.invoke(input={'page_data':cleaned_text})
        print(res)
        return res if isinstance(res,list) else [res]
    
    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            '''
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Vinit Lathiwala currently studying in Final year pusunig B.Tech in CSE with AI-ML.
            You are an AI/ML developer with expertise in building and fine-tuning machine learning models. Your specialties include natural language processing (NLP), computer vision, and creating AI-powered solutions. You are skilled in Python, TensorFlow, scikit-learn, Flask, and frontend technologies like HTML, CSS, and JavaScript. You excel at solving complex problems, collaborating in teams, and integrating AI into practical applications
            Your job is to write a cold email to the client regarding the job mentioned above mentioning ahat how you are gooin aligning with the skills they require
            Also add  the most relevant ones from the follwing links to showcase the your portfolio: {link_list}.
            Remember you are Vinit Lathiwala.
            ### Email (NO PREAMBLE):
        '''
        )

        chain_email = prompt_email | self.llm 
        res = chain_email.invoke({'job_description': str(job), "link_list":links})
        return res.content