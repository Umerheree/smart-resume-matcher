import re
from pypdf import PdfReader

class ResumeParser:
    def __init__(self):
        self.section_map = {
            "experience": r"(experience|work history|employment|professional background)",
            "education": r"(education|academic|certification|degree)",
            "skills": r"(technical skills|competencies|expertise|tools)",
            "projects": r"(projects|personal work|portfolio)"
        }

    def parse(self, pdf_file): # Ensure this name is exactly 'parse'
        """Extracts text and segments it into logical sections."""
        reader = PdfReader(pdf_file)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
        
        segments = {"full_text": full_text, "experience": "", "education": "", "skills": "", "projects": ""}
        current_section = "full_text"
        
        for line in full_text.split('\n'):
            clean_line = line.strip().lower()
            for section, pattern in self.section_map.items():
                if re.search(pattern, clean_line):
                    current_section = section
                    break
            segments[current_section] += line + " "
            
        return segments