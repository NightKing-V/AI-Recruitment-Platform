

class PromptTemplates:

    @staticmethod
    def resume_extraction_prompt(self, resume_text: str) -> str:
            
            prompt = f"""
    You are an expert resume parser. Analyze the following resume text and extract structured information in valid JSON format.

    IMPORTANT INSTRUCTIONS:
    1. Return ONLY valid JSON, no additional text or explanation
    2. If information is missing, use empty arrays [] or empty strings ""
    3. Extract all relevant information accurately
    4. For experience, include ALL jobs mentioned
    5. For skills, extract both technical and soft skills
    6. For education, include degree, institution, and year if available

    Required JSON structure:
    {{
        "name": "Full Name",
        "email": "email@example.com", 
        "phone": "phone number",
        "location": "City, State/Country",
        "summary": "Professional summary or objective",
        "skills": ["skill1", "skill2", "skill3"],
        "experience": [
            {{
                "title": "Job Title",
                "company": "Company Name", 
                "duration": "Start Date - End Date",
                "location": "City, State",
                "description": "Job description and key achievements"
            }}
        ],
        "education": [
            {{
                "degree": "Degree Name",
                "institution": "Institution Name",
                "year": "Graduation Year",
                "location": "City, State"
            }}
        ],
        "certifications": ["certification1", "certification2"],
        "languages": ["language1", "language2"],
        "projects": [
            {{
                "name": "Project Name",
                "description": "Project description",
                "technologies": ["tech1", "tech2"]
            }}
        ]
    }}

    Resume text to analyze:
    {resume_text}

    Return only the JSON structure with extracted data:
    """
            return prompt
        
        
    @staticmethod
    def job_generator_prompt(job_num, job_domains: list[str]) -> str:
        domains_str = ", ".join(job_domains)
        prompt = f"""
        You are an expert job description writer. Generate highly realistic and detailed job descriptions for the following domains:
        {domains_str}

        IMPORTANT INSTRUCTIONS:
        1. Return ONLY valid JSON, no additional text or explanation.
        2. Generate {job_num} unique job description/s for each domain listed.
        3. Use varied job titles relevant to each domain.
        4. Keep language professional, concise, and recruiter-friendly.
        5. Include all key details that a recruiter would expect.

        Required JSON structure (return as an array):
        [
            {{
                "job_title": "Job Title",
                "job_domain": "Job Domain",
                "summary": "Brief overview of the role",
                "responsibilities": [
                    "Responsibility 1",
                    "Responsibility 2",
                    "Responsibility 3"
                ],
                "required_skills": [
                    "Skill 1",
                    "Skill 2",
                    "Skill 3"
                ],
                "qualifications": [
                    "Qualification 1",
                    "Qualification 2"
                ],
                "experience_level": "e.g., Entry-level / Mid-level / Senior",
                "location": "City, State/Country",
                "employment_type": "Full-time / Part-time / Contract"
            }}
        ]

        Return only the JSON array:
        """
        return prompt
    
    @staticmethod
    def job_extraction_prompt(job_description_text: str) -> str:
        prompt = f"""
        You are a highly skilled information extractor specializing in parsing job descriptions.
        Extract the key information from the following job description text:

        Job Description Text:
        {job_description_text}
        

        IMPORTANT INSTRUCTIONS:
        1. Return ONLY valid JSON, no additional text or explanation.
        2. Extract and fill the following JSON structure exactly as shown.
        3. If any detail is missing or not explicitly mentioned, use an empty string or empty array as appropriate.

        Required JSON structure:
        [
            {{
                "job_title": "",
                "job_domain": "",
                "summary": "",
                "responsibilities": [],
                "required_skills": [],
                "qualifications": [],
                "experience_level": "",
                "location": "",
                "employment_type": ""
            }}
        ]

        Return only the JSON object:
        """
        return prompt

