from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.1-70b-versatile",
            groq_api_key="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",
            temperature=0,
        )
    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input = {"page_data": cleaned_text})
        try:
            json_parser =JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big, Unable to parse jobs")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links, skills, user_name, user_specialization, user_job_role, user_about):
        prompt_email = PromptTemplate.from_template(
            """
            You are an expert **job application writer** with experience in crafting tailored cold emails for job roles.
            
            ### JOB DESCRIPTION:
            {job_description}
            
            ### USER DETAILS:
            - Name: {user_name}  
            - About: {user_about}  
            - Role: {user_job_role}  
            - Specialization: {user_specialization}  
            - Professional Strengths: {key_skills}  
            
            ### INSTRUCTION:
            Based on the provided job description and user details, write a **cold email** tailored to the client.  
            The email should:  
            1. Highlight the user's skills and achievements relevant to the job.  
            2. Showcase the user's ability to solve challenges mentioned in the job description.  
            3. Include the most relevant portfolio/project links:  
                {project_links}  
            
            Make sure the email:  
            - Is professional and concise.  
            - Avoids preamble like "I am writing this email to..."  
            - Directly addresses the client's requirements.  
            
            ### EMAIL OUTPUT:
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            "job_description": str(job),
            "project_links": links,
            "user_name":user_name,
            "user_specialization":user_specialization,
            "user_job_role":user_job_role,
            "user_about": user_about,
            "key_skills": skills
        })
        return res.content