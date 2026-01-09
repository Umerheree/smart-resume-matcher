import streamlit as st
import os
from src.pdf_reader import extract_text_from_pdf
from src.text_cleaner import clean_text
from src.matcher import calculate_match
from src.skills import extract_skills

# --- PAGE CONFIG (Must be first) ---
st.set_page_config(page_title="AI Resume Matcher", page_icon="✨", layout="wide")

# --- CUSTOM CSS FOR "PREMIUM" LOOK ---
st.markdown("""
    <style>
    /* Remove standard Streamlit padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Custom Card Style */
    .stCard {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border-left: 5px solid #4CAF50;
    }
    /* Hide the default Streamlit menu/footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=50)
    st.title("Settings")
    
    st.markdown("### 1. Job Description")
    jd_input = st.text_area("Paste JD here:", height=250, help="Copy paste the job description from LinkedIn/Indeed.")
    
    if st.button("📄 Load Example JD"):
        try:
            with open("data/job_description.txt", "r", encoding='utf-8') as f:
                jd_input = f.read()
                st.toast("Example JD Loaded!", icon="✅")
        except:
            st.error("File not found.")

# --- MAIN LAYOUT ---
st.title("✨ Smart Resume Matcher")
st.markdown("##### Upload resumes to rank them by **AI relevance**.")

uploaded_files = st.file_uploader("Drop PDF Resumes Here", type=["pdf"], accept_multiple_files=True)

if st.button("Analyze Candidates 🚀", type="primary"):
    if not jd_input:
        st.warning("⚠️ Please provide a Job Description in the sidebar.")
    elif not uploaded_files:
        st.warning("⚠️ Upload at least one resume.")
    else:
        with st.spinner("Reading & Comparing..."):
            # 1. Processing
            cleaned_jd = clean_text(jd_input)
            jd_skills = extract_skills(cleaned_jd)
            
            resume_texts = []
            filenames = []
            
            for f in uploaded_files:
                text = extract_text_from_pdf(f)
                if text:
                    resume_texts.append(clean_text(text))
                    filenames.append(f.name)
            
            if resume_texts:
                scores = calculate_match(cleaned_jd, resume_texts)
                
                # 2. Structure Data
                results = []
                for i, filename in enumerate(filenames):
                    resume_skills = extract_skills(resume_texts[i])
                    matched_skills = set(resume_skills).intersection(set(jd_skills))
                    score = scores[i]['total']
                    
                    results.append({
                        "name": filename,
                        "score": score,
                        "matched_skills": list(matched_skills),
                        "missing_skills": list(set(jd_skills) - matched_skills)
                    })
                
                # Sort by score
                results.sort(key=lambda x: x['score'], reverse=True)
                
                # 3. DISPLAY RESULTS (The Premium Part)
                st.success(f"Analyzed {len(results)} candidates successfully!")
                
                st.subheader("🏆 Top Candidates")
                
                for res in results:
                    # Create a "Card" using Columns
                    with st.container():
                        c1, c2, c3 = st.columns([1, 4, 2])
                        
                        with c1:
                            st.markdown(f"## {res['score']}%")
                            st.caption("Match Score")
                        
                        with c2:
                            st.markdown(f"### 📄 {res['name']}")
                            if res['matched_skills']:
                                st.write("✅ **Skills:** " + ", ".join([s.upper() for s in res['matched_skills']]))
                            else:
                                st.write("⚠️ No specific skills matched.")
                                
                        with c3:
                            # Visual Progress Bar
                            st.progress(res['score'] / 100)
                            if res['score'] > 75:
                                st.markdown("🌟 **Excellent Match**")
                            elif res['score'] > 50:
                                st.markdown("👍 **Good Match**")
                            else:
                                st.markdown("📉 **Low Match**")
                        
                        st.divider()