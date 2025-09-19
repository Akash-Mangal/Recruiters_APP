import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import Runnable
from pydantic_model import ResumeMetadata, QuerySkills
from dotenv import loadenv

loadenv()
def extract_metadata(resume_text):
    # 1. Setup your OpenAI API key


    llm = ChatOpenAI(
        base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["OPENAI_API_KEY"],
    model="llama-3.3-70b-versatile",  # or "llama3-8b-8192"
    temperature=0)
    llm_struct = llm.with_structured_output(ResumeMetadata)

    # 2. Load resume text (assume you already extracted it)
    # resume_text = extract_text("/path/to/resume.pdf")


    parser = JsonOutputParser(pydantic_object=ResumeMetadata)

    # 3. Define a prompt for metadata extraction
    prompt = PromptTemplate(
        # input_variables=["resume"],
        template="""
        {format_instructions}
    Extract the following information from the resume below:
    - Full Name
    - Email
    - Phone Number
    - Skills
    - Companies Worked At
    - Years of Experience
    - Education Institutions
    - Summary

    Resume:
    {resume}


    """,
    partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    # 4. Create the LangChain chain
    chain: Runnable = prompt | llm | parser


    # 5. Run the chain
    # metadata = chain.invoke("resume", "{resume_text}")
    metadata = chain.invoke({"resume": resume_text})

    return metadata



def extract_skills(resume_text):
    # 1. Setup your OpenAI API key
    

    llm = ChatOpenAI(
        base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["OPENAI_API_KEY"],
    model="llama-3.3-70b-versatile",  # or "llama3-8b-8192"
    temperature=0)
    llm_struct = llm.with_structured_output(ResumeMetadata)

    # 2. Load resume text (assume you already extracted it)
    # resume_text = extract_text("/path/to/resume.pdf")


    parser = JsonOutputParser(pydantic_object=QuerySkills)

    # 3. Define a prompt for metadata extraction
    prompt = PromptTemplate(
        # input_variables=["resume"],
        template="""
        {format_instructions}
    Extract the following information from the job description below:
    - Skills

    Job description:
    {resume}


    """,
    partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    # 4. Create the LangChain chain
    chain: Runnable = prompt | llm | parser


    # 5. Run the chain
    # metadata = chain.invoke("resume", "{resume_text}")
    metadata = chain.invoke({"resume": resume_text})


    return metadata




def fetch_and_rank_resumes_with_llm(resumes, job_description):
    
    llm = ChatOpenAI(
        base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["OPENAI_API_KEY"],
    model="llama-3.3-70b-versatile",  # or "llama3-8b-8192"
    temperature=0)


    parser = JsonOutputParser(pydantic_object=ResumeRankingList)


    candidates_str = ""
    for i in range (len(resumes['ids'][0])):
        candidate_str = f"{i+1}. index: {i}\nsummary: {resumes['documents'][0][i]}\nExperience: {resumes['metadatas'][0][i]['experience_years']}\n\n"
        # print(candidate_str)
        candidates_str += candidate_str

    ranking_prompt = PromptTemplate(template="""
                                   {format_instructions}
You are a recruitment assistant. Based on the following job description:

\"\"\"{job_description}\"\"\"


Candidates:
{candidates_str}
""",
partial_variables={"format_instructions": parser.get_format_instructions()})


    chain : Runnable = ranking_prompt | llm | parser
        
    responses = chain.invoke({"candidates_str": candidates_str,"job_description":job_description})
    
    results = []
    for response in responses['ranks']:
        ind = response['index']
        response['id'] = resumes['ids'][0][ind]
        response['name'] = resumes['metadatas'][0][ind]['name']
        response['summary'] = resumes['documents'][0][ind]
        response['file_path'] = resumes['metadatas'][0][ind]['file_path']
        response.pop('index')
        results.append(response)

    
    # return {"ranks":"bj"}
    return results