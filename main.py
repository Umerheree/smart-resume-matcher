import os
from src.pdf_reader import extract_text_from_pdf
from src.text_cleaner import clean_text
from src.matcher import calculate_match
from src.skills import extract_skills  # <--- NEW IMPORT

def main():
    # --- SETUP PATHS ---
    base_dir = os.path.dirname(os.path.abspath(__file__))
    resumes_dir = os.path.join(base_dir, 'data', 'resumes')
    jd_path = os.path.join(base_dir, 'data', 'job_description.txt')

    # --- 1. READ JOB DESCRIPTION ---
    if not os.path.exists(jd_path):
        print("❌ Error: data/job_description.txt not found.")
        return

    with open(jd_path, 'r', encoding='utf-8') as f:
        raw_jd = f.read()

    # --- 2. READ RESUMES ---
    resume_files = [f for f in os.listdir(resumes_dir) if f.endswith('.pdf')]
    resume_texts = []
    valid_filenames = []

    for filename in resume_files:
        path = os.path.join(resumes_dir, filename)
        text = extract_text_from_pdf(path)
        if text.strip():
            resume_texts.append(clean_text(text))
            valid_filenames.append(filename)

    # --- 3. RUN MATCHING ---
    cleaned_jd = clean_text(raw_jd)
    scores = calculate_match(cleaned_jd, resume_texts)
    
    # --- 4. EXTRACT SKILLS (NEW) ---
    jd_skills = extract_skills(cleaned_jd)
    print(f"\n🔍 Job Requires: {', '.join(jd_skills).upper()}")

    # --- 5. DISPLAY RESULTS ---
    final_results = []
    for i, filename in enumerate(valid_filenames):
        # Find skills in this specific resume
        resume_skills = extract_skills(resume_texts[i])
        # Calculate how many JD skills the candidate has
        skills_matched = set(resume_skills).intersection(set(jd_skills))
        
        final_results.append({
            "name": filename,
            "score": scores[i]['total'],
            "skills_found": resume_skills,
            "skills_matched": skills_matched
        })

    final_results.sort(key=lambda x: x['score'], reverse=True)

    print("\n" + "="*50)
    print(" 🏆 RESUME MATCHING REPORT (WITH SKILLS)")
    print("="*50)
    
    for item in final_results:
        print(f"📄 {item['name']}")
        print(f"   ✅ Match Score: {item['score']}%")
        # Show skills
        matched_str = ", ".join(item['skills_matched']).upper() if item['skills_matched'] else "None"
        print(f"   🎯 Skills Matched: {matched_str}")
        print("-" * 30)

if __name__ == "__main__":
    main()