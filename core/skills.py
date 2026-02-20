# A database of tech skills to look for
TECH_SKILLS_DB = {
    "python", "java", "c++", "javascript", "typescript", "html", "css",
    "react", "angular", "vue", "node", "django", "flask",
    "sql", "mysql", "postgresql", "mongodb",
    "aws", "azure", "docker", "kubernetes", "git", "linux",
    "machine learning", "deep learning", "nlp", "tensorflow", "pytorch"
}

def extract_skills(text):
    """
    Scans text and returns a set of found skills from our DB.
    """
    found_skills = set()
    words = text.split()
    
    # Check for single-word skills
    for word in words:
        if word in TECH_SKILLS_DB:
            found_skills.add(word)
            
    # Check for multi-word skills (like 'machine learning')
    for skill in TECH_SKILLS_DB:
        if " " in skill and skill in text:
            found_skills.add(skill)
            
    return list(found_skills)