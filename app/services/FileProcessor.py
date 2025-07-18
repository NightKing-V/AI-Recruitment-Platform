import streamlit as st
import fitz  # PyMuPDF
import docx

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
