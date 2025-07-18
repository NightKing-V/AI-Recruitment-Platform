

class PromptTemplates:

    @staticmethod
    def resume_extraction_prompt(self, resume_text: str) -> str:
            """Construct a detailed prompt for resume data extraction"""
            
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