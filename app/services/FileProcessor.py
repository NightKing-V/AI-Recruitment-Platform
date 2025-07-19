import streamlit as st
import fitz  # PyMuPDF
import docx
import io

class FileProcessor:
    """Handles file upload and text extraction from different file formats"""
    
    @staticmethod
    def extract_text_from_pdf(uploaded_file) -> str:
        """Extract text from PDF file using PyMuPDF"""
        try:
            # Reset file pointer to beginning
            uploaded_file.seek(0)
            
            # Read the file content
            pdf_content = uploaded_file.read()
            
            # Open PDF document from bytes
            pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
            
            text = ""
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text += page.get_text() + "\n"
            
            pdf_document.close()
            return text.strip()
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return ""
    
    @staticmethod
    def extract_text_from_docx(uploaded_file) -> str:
        """Extract text from DOCX file"""
        try:
            # Reset file pointer to beginning
            uploaded_file.seek(0)
            doc = docx.Document(uploaded_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            st.error(f"Error reading DOCX: {str(e)}")
            return ""
    
    @staticmethod
    def extract_text_from_txt(uploaded_file) -> str:
        """Extract text from TXT file"""
        try:
            # Reset file pointer to beginning
            uploaded_file.seek(0)
            # Convert bytes to string
            text = uploaded_file.read().decode('utf-8')
            return text.strip()
        except Exception as e:
            st.error(f"Error reading TXT: {str(e)}")
            return ""
    
    @classmethod
    def process_file(cls, uploaded_file) -> str:
        """Process uploaded file and extract text based on file type"""
        if uploaded_file is None:
            return ""
        
        file_type = uploaded_file.type
        
        if file_type == "application/pdf":
            return cls.extract_text_from_pdf(uploaded_file)
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return cls.extract_text_from_docx(uploaded_file)
        elif file_type == "text/plain":
            return cls.extract_text_from_txt(uploaded_file)
        else:
            st.error(f"Unsupported file type: {file_type}")
            return ""

    @staticmethod
    def download_jobs_as_pdf(jobs: list, scores: list):
        """
        Generate a downloadable PDF containing job recommendations using PyMuPDF.
        """
        if not jobs:
            st.warning("No jobs available to download.")
            return None

        # Create a new PDF
        pdf = fitz.open()
        page = pdf.new_page()

        # Starting position
        y = 50
        x = 50

        # Title
        title = "Job Recommendations"
        page.insert_text((x, y), title, fontsize=16, fontname="helv", fill=(0, 0, 0))
        y += 30

        for i, (job, score) in enumerate(zip(jobs, scores), 1):
            similarity_pct = score * 100  # convert to percentage

            text = (
                f"{i}. {job['job_title']} at {job['company']}\n"
                f"Match Score: {similarity_pct:.2f}%\n"
                f"Location: {job['location']}\n"
                f"Experience: {job['experience_level']}\n"
                f"Job Type: {job['employment_type']}\n"
                f"Required Skills: {', '.join(job['required_skills'])}\n"
                f"Description: {job['summary']}...\n"
            )

            # Check for page overflow
            if y > page.rect.height - 100:
                page = pdf.new_page()
                y = 50

            page.insert_text((x, y), text, fontsize=10, fontname="helv", fill=(0, 0, 0))
            y += 100  # spacing between jobs

        # Save to memory buffer
        pdf_buffer = io.BytesIO()
        pdf.save(pdf_buffer)
        pdf_buffer.seek(0)

        return pdf_buffer
