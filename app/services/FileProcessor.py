import streamlit as st
import fitz  # PyMuPDF
import docx
import io

class FileProcessor:
    
    @staticmethod
    def extract_text_from_pdf(uploaded_file) -> str:
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
        if not jobs:
            st.warning("No jobs available to download.")
            return None

        # Create a new PDF with A4 size
        pdf = fitz.open()
        page = pdf.new_page(width=595, height=842)  # A4 dimensions in points
        
        # Define colors (RGB values 0-1)
        primary_color = (0.2, 0.3, 0.6)      # Dark blue
        secondary_color = (0.4, 0.5, 0.7)    # Light blue
        accent_color = (0.9, 0.4, 0.2)       # Orange
        text_color = (0.2, 0.2, 0.2)         # Dark gray
        light_gray = (0.9, 0.9, 0.9)         # Light gray
        
        # Page margins and dimensions
        margin_left = 50
        margin_right = 545  # 595 - 50
        margin_top = 50
        page_width = 545  # margin_right - margin_left
        
        def add_header(page, y_pos):
            """Add header with title and date"""
            # Header background rectangle
            header_rect = fitz.Rect(margin_left - 20, y_pos - 10, margin_right + 20, y_pos + 40)
            page.draw_rect(header_rect, color=primary_color, fill=primary_color)
            
            # Title
            page.insert_text((margin_left, y_pos + 20), "Job Recommendations Report", 
                            fontsize=18, color=(1, 1, 1))
            
            # Date
            from datetime import datetime
            current_date = datetime.now().strftime("%B %d, %Y")
            page.insert_text((margin_right - 150, y_pos + 20), f"Generated: {current_date}", 
                            fontsize=10, color=(1, 1, 1))
            
            return y_pos + 60
        
        def add_summary_box(page, y_pos, total_jobs):
            # """Add summary information box"""
            # Summary box
            summary_rect = fitz.Rect(margin_left, y_pos, margin_right, y_pos + 40)
            page.draw_rect(summary_rect, color=light_gray, fill=light_gray)
            
            summary_text = f"Total Recommendations: {total_jobs} | Sorted by Match Score"
            page.insert_text((margin_left + 10, y_pos + 25), summary_text, 
                            fontsize=12, color=text_color)
            
            return y_pos + 60
        
        def wrap_text(text, max_width, fontsize=10):
            # """Simple text wrapping function"""
            words = text.split()
            lines = []
            current_line = ""
            
            for word in words:
                test_line = current_line + " " + word if current_line else word
                # Approximate character width (rough estimation)
                if len(test_line) * (fontsize * 0.6) <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
            
            return lines
        
        def add_job_card(page, job, score, rank, y_pos):
            # """Add a formatted job card"""
            card_height = 140
            similarity_pct = score * 100
            
            # Check if we need a new page
            if y_pos + card_height > 780:  # Near bottom of page
                return None, y_pos  # Signal for new page needed
            
            # Job card background
            card_rect = fitz.Rect(margin_left, y_pos, margin_right, y_pos + card_height)
            page.draw_rect(card_rect, color=(0.98, 0.98, 0.98), fill=(0.98, 0.98, 0.98), width=1)
            
            # Rank circle
            circle_center = fitz.Point(margin_left + 25, y_pos + 25)
            page.draw_circle(circle_center, 15, color=primary_color, fill=primary_color)
            page.insert_text((margin_left + 20, y_pos + 30), str(rank), 
                            fontsize=12, color=(1, 1, 1))
            
            # Job title (large, bold)
            job_title = job.get('job_title', 'N/A')[:50] + ('...' if len(job.get('job_title', '')) > 50 else '')
            page.insert_text((margin_left + 50, y_pos + 20), job_title, 
                            fontsize=14, color=primary_color)
            
            # Company name
            company = job.get('company', 'N/A')[:40] + ('...' if len(job.get('company', '')) > 40 else '')
            page.insert_text((margin_left + 50, y_pos + 40), f"at {company}", 
                            fontsize=12, color=text_color)
            
            # Match score badge
            score_text = f"{similarity_pct:.1f}% Match"
            score_rect = fitz.Rect(margin_right - 100, y_pos + 10, margin_right - 10, y_pos + 35)
            
            # Color code the match score
            if similarity_pct >= 80:
                badge_color = (0.2, 0.7, 0.3)  # Green
            elif similarity_pct >= 60:
                badge_color = accent_color       # Orange
            else:
                badge_color = (0.7, 0.3, 0.3)  # Red
                
            page.draw_rect(score_rect, color=badge_color, fill=badge_color)
            page.insert_text((margin_right - 85, y_pos + 27), score_text, 
                            fontsize=10, color=(1, 1, 1))
            
            # Job details in two columns
            col1_x = margin_left + 50
            col2_x = margin_left + 280
            details_y = y_pos + 60
            
            # Column 1
            location = job.get('location', 'N/A')[:25] + ('...' if len(job.get('location', '')) > 25 else '')
            page.insert_text((col1_x, details_y), f"Location: {location}", 
                            fontsize=10, color=text_color)
            
            experience = job.get('experience_level', 'N/A')
            page.insert_text((col1_x, details_y + 15), f"Experience: {experience}", 
                            fontsize=10, color=text_color)
            
            # Column 2
            employment_type = job.get('employment_type', 'N/A')
            page.insert_text((col2_x, details_y), f"Type: {employment_type}", 
                            fontsize=10, color=text_color)
            
            # Skills (limit to avoid overflow)
            skills = job.get('required_skills', [])
            skills_text = ', '.join(skills[:4]) + ('...' if len(skills) > 4 else '')
            if len(skills_text) > 35:
                skills_text = skills_text[:32] + "..."
            page.insert_text((col2_x, details_y + 15), f"Skills: {skills_text}", 
                            fontsize=10, color=text_color)
            
            # Description (wrapped text)
            description = job.get('summary', 'No description available.')
            if len(description) > 200:
                description = description[:197] + "..."
            
            desc_lines = wrap_text(description, page_width - 100, 9)
            desc_y = details_y + 35
            
            for i, line in enumerate(desc_lines[:2]):  # Limit to 2 lines
                page.insert_text((col1_x, desc_y + i * 12), line, 
                                fontsize=9, color=(0.4, 0.4, 0.4))
            
            return page, y_pos + card_height + 20
        
        # Start building the PDF
        current_y = margin_top
        
        # Add header
        current_y = add_header(page, current_y)
        
        # Add summary box
        current_y = add_summary_box(page, current_y, len(jobs))
        
        # Add jobs
        for i, (job, score) in enumerate(zip(jobs, scores), 1):
            result_page, new_y = add_job_card(page, job, score, i, current_y)
            
            if result_page is None:  # Need new page
                # Add page number
                page.insert_text((margin_right - 50, 820), f"Page {pdf.page_count}", 
                                fontsize=8, color=(0.5, 0.5, 0.5))
                
                # Create new page
                page = pdf.new_page(width=595, height=842)
                current_y = margin_top + 30
                result_page, new_y = add_job_card(page, job, score, i, current_y)
            
            current_y = new_y
        
        # Add final page number
        page.insert_text((margin_right - 50, 820), f"Page {pdf.page_count}", 
                        fontsize=8, color=(0.5, 0.5, 0.5))
        
        # Add footer to last page
        footer_y = 800
        footer_text = "Generated by Job Recommendation System"
        page.insert_text((margin_left, footer_y), footer_text, 
                        fontsize=8, color=(0.6, 0.6, 0.6))
        
        # Save to memory buffer
        pdf_buffer = io.BytesIO()
        pdf.save(pdf_buffer)
        pdf_buffer.seek(0)
        pdf.close()
        
        return pdf_buffer