from pydantic import BaseModel, Field
from typing import List, Optional



class ResumeMetadata(BaseModel):
    name: Optional[str] = Field(description="Full name of the candidate")
    email: Optional[str] = Field(description="Email address of the candidate")
    phone: Optional[str] = Field(description="Phone number of the candidate")
    skills: List[str] = Field(default_factory=list, description="List of key technical or soft skills all in title case")
    companies: List[str] = Field(default_factory=list, description="Companies or organizations the candidate has worked at")
    experience_years: Optional[str] = Field(description="Total years of professional experience")
    education: List[str] = Field(default_factory=list, description="Educational institutions attended by the candidate")
    summary: str = Field(description= "Write a concise, skill-focused professional summary that clearly highlights the candidate’s most relevant technical and soft skills, experience, "
        "and achievements. Exclude generic phrases and irrelevant details. The summary will be stored in a vector database and used for matching candidates "
        "to job descriptions, so focus on clarity, precision, and search relevance.")
    
class QuerySkills(BaseModel):
    skills: List[str] = Field(default_factory=list, description="List all the technical or soft skills mentioned in job description. Do not include any foreign. It must be in single word. Example: Python Development is Python.")

class ResumeRanking(BaseModel):
    score: float = Field(description="Score the resume on the basis of Job description and Resume summary.on the scale of 0 to 10")
    rank: int = Field(description="Rank number of resume among the given resumes on the basis of Job description and Resume summary.")
    ids: str = Field(description= "Provide ids of resume from the given data")
    comment: str = Field(description= "Justify the score and rank given to the candidate. Also give reason for the same")

class ResumeRankingList(BaseModel):
    ranks: List[ResumeRanking] = Field("Json format of each resume.")