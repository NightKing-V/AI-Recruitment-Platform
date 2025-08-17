

class PromptTemplates:

    @staticmethod
    def resume_extraction_prompt(resume_text: str, existing_json: str) -> str:
        prompt = f"""
    You are an expert resume parser analyzing a multi-page resume.

    You are given:
    1. The current extracted JSON (from previous pages), if available.
    2. The new page content.

    Your task:
    - Update the JSON with any new information found in the page.
    - Do NOT remove or overwrite existing information unless the new data is clearly more accurate.
    - Append new items to arrays (skills, experience, education, certifications, languages, projects).
    - Avoid duplicates in arrays (e.g., no repeating skills, jobs, or project entries).

    STRICT RULES:
    1. Return ONLY valid JSON. Do NOT include any explanations or extra text.
    2. Keep missing information as empty arrays [] or empty strings "".
    3. EXPERIENCE: Include ONLY paid professional jobs, internships, or official roles. Do NOT include projects, personal work, academic assignments, or hobbies.
    4. Do NOT put projects them under 'experience'.
    5. SKILLS: Include both technical and soft skills. Avoid duplicates.
    6. EDUCATION: Include degrees, diplomas if available.
    7. CERTIFICATIONS: List professional certifications.
    8. LANGUAGES: List all languages mentioned.
    9. Maintain the exact JSON structure below and do not add extra fields.

    Required JSON structure (must always be followed):
    [
        {{
            "name": "Full Name",
            "location": "City, Country",
            "summary": "Professional summary or objective",
            "skills": ["skill1", "skill2"],
            "experience": [
                {{
                    "title": "Job Title",
                    "company": "Company Name", 
                    "duration": "X years/months"
                }}
            ],
            "education": [
                {{
                    "degree": "Degree Name"
                }}
            ],
            "certifications": ["certification1"],
            "languages": ["language1"]
        }}
    ]

    Current JSON:
    {existing_json}

    New page content:
    {resume_text}

    Return the UPDATED JSON following all rules above:
    """

        return prompt

        
        
    @staticmethod
    def job_generator_prompt(job_num, job_domains: list[str]) -> str:
        domains_str = ", ".join(job_domains)
        prompt = f"""
    You are an expert job description writer.

    STRICT INSTRUCTIONS:
    - Output ONLY a JSON array (no headings, no explanations, no markdown, no extra fields).
    - Do NOT include any text outside the JSON.
    - Generate {job_num} unique, detailed job descriptions for each of these domains: {domains_str}.

    Each job object must have:
    [
        {{
            "job_title": "Job Title",
            "job_domain": "Job Domain",
            "summary": "Brief overview of the role",
            "responsibilities": ["Responsibility 1", "Responsibility 2", "Responsibility 3"],
            "required_skills": ["Skill 1", "Skill 2", "Skill 3"],
            "qualifications": ["Qualification 1", "Qualification 2"],
            "experience_level": "Entry-level / Mid-level / Senior",
            "company": "Company Name",
            "location": "City, Country",
            "employment_type": "Full-time / Part-time / Contract"
        }}
    ]

    Now output ONLY the JSON array:
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

