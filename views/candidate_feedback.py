import streamlit as st
from core.parser import ResumeParser
from core.engine import MatchingEngine
from utils.text_utils import clean_text
import yaml
from datetime import datetime

def render():
    # Custom CSS for candidate feedback view
    st.markdown("""
    <style>
        .score-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 3rem 2rem;
            border-radius: 16px;
            text-align: center;
            color: white;
            margin: 2rem 0;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }
        
        .score-display {
            font-size: 5rem;
            font-weight: 800;
            line-height: 1;
            margin: 1rem 0;
            text-shadow: 0 4px 6px rgba(0,0,0,0.2);
        }
        
        .score-label {
            font-size: 1.25rem;
            opacity: 0.95;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 600;
        }
        
        .score-description {
            font-size: 1rem;
            opacity: 0.9;
            margin-top: 0.5rem;
            max-width: 500px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .feedback-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        
        .feedback-card h3 {
            color: #1f2937;
            margin-top: 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .skill-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 0.75rem;
            margin: 1rem 0;
        }
        
        .skill-item {
            background: #f0fdf4;
            border: 2px solid #86efac;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 500;
            color: #166534;
            transition: all 0.2s ease;
        }
        
        .skill-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(134, 239, 172, 0.3);
        }
        
        .skill-item-missing {
            background: #fef2f2;
            border: 2px solid #fca5a5;
            color: #991b1b;
        }
        
        .skill-item-missing:hover {
            box-shadow: 0 4px 12px rgba(252, 165, 165, 0.3);
        }
        
        .suggestion-box {
            background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
            border-left: 4px solid #f59e0b;
            padding: 1.25rem;
            border-radius: 8px;
            margin: 0.75rem 0;
        }
        
        .suggestion-box strong {
            color: #92400e;
            display: block;
            margin-bottom: 0.5rem;
        }
        
        .suggestion-box p {
            color: #78350f;
            margin: 0.25rem 0;
            line-height: 1.6;
        }
        
        .progress-bar-container {
            background: #e5e7eb;
            height: 24px;
            border-radius: 12px;
            overflow: hidden;
            margin: 1rem 0;
            position: relative;
        }
        
        .progress-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #10b981 0%, #059669 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            font-size: 0.875rem;
            transition: width 1s ease-out;
        }
        
        .stat-mini {
            background: #f9fafb;
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
            border: 1px solid #e5e7eb;
        }
        
        .stat-mini-value {
            font-size: 1.75rem;
            font-weight: 700;
            color: #1f2937;
            margin: 0;
        }
        
        .stat-mini-label {
            font-size: 0.75rem;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 0.25rem;
        }
        
        .section-divider {
            height: 2px;
            background: linear-gradient(90deg, transparent 0%, #667eea 50%, transparent 100%);
            margin: 2.5rem 0;
        }
        
        .tip-highlight {
            background: #eff6ff;
            border-left: 3px solid #3b82f6;
            padding: 0.75rem 1rem;
            border-radius: 4px;
            margin: 0.5rem 0;
            font-size: 0.95rem;
        }
        
        .empty-state {
            text-align: center;
            padding: 4rem 2rem;
            color: #9ca3af;
        }
        
        .empty-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
        }
        
        .priority-high {
            background: #fef2f2;
            border-left: 4px solid #ef4444;
            padding: 1rem;
            border-radius: 6px;
            margin: 0.5rem 0;
        }
        
        .priority-medium {
            background: #fffbeb;
            border-left: 4px solid #f59e0b;
            padding: 1rem;
            border-radius: 6px;
            margin: 0.5rem 0;
        }
        
        .priority-low {
            background: #f0fdf4;
            border-left: 4px solid #10b981;
            padding: 1rem;
            border-radius: 6px;
            margin: 0.5rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div class="tip-highlight">
        <strong>🎯 Welcome to AI Resume Analyzer!</strong><br>
        Get instant, personalized feedback on how well your resume matches your target job. 
        Our AI will identify gaps and provide actionable recommendations to improve your chances.
    </div>
    """, unsafe_allow_html=True)
    
    # Input Section
    st.markdown("### 📋 Step 1: Provide Job Details")
    
    target_jd = st.text_area(
        "Target Job Description",
        height=200,
        placeholder="📄 Paste the complete job description here...\n\n• Include all required skills and qualifications\n• The more detailed, the better the analysis\n• Copy directly from the job posting",
        help="Paste the full job description you're applying for. Include requirements, responsibilities, and desired qualifications."
    )
    
    if target_jd:
        word_count = len(target_jd.split())
        st.caption(f"✓ Job description loaded ({word_count} words)")
    
    st.markdown("### 📎 Step 2: Upload Your Resume")
    
    user_resume = st.file_uploader(
        "Upload Your Resume",
        type="pdf",
        help="Upload your resume in PDF format for analysis"
    )
    
    if user_resume:
        st.success(f"✅ Resume uploaded: {user_resume.name} ({user_resume.size / 1024:.1f} KB)")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Action button
    col1, col2 = st.columns([3, 1])
    with col1:
        analyze_button = st.button(
            "✨ Get AI Feedback & Recommendations",
            type="primary",
            use_container_width=True,
            disabled=not (target_jd and user_resume)
        )
    with col2:
        if st.button("🔄 Start Over", use_container_width=True):
            st.rerun()

    # Analysis Logic
    if analyze_button:
        if not target_jd or not user_resume:
            st.warning("⚠️ Please provide both the job description and your resume.")
            return

        parser = ResumeParser()
        engine = MatchingEngine()

        with st.spinner("🤖 AI is analyzing your profile against the job requirements..."):
            try:
                # Parse and segment
                segmented = parser.parse(user_resume)
                cleaned_resume = clean_text(segmented['full_text'])
                cleaned_jd = clean_text(target_jd)

                # Get matching data
                match_data = engine.run_tfidf_match(cleaned_jd, [cleaned_resume])[0]
                
                # Score Display
                score = match_data['score']
                
                # Determine score category
                if score > 80:
                    score_color = "#10b981"
                    score_verdict = "Excellent Match!"
                    score_message = "Your resume is well-optimized for this role. You're a strong candidate!"
                elif score > 60:
                    score_color = "#f59e0b"
                    score_verdict = "Good Match"
                    score_message = "Your resume shows potential. Some optimizations will make it even stronger."
                else:
                    score_color = "#ef4444"
                    score_verdict = "Needs Improvement"
                    score_message = "Your resume needs significant updates to match this job description."
                
                st.markdown(f"""
                <div class="score-container" style="background: linear-gradient(135deg, {score_color} 0%, {score_color}dd 100%);">
                    <div class="score-label">Your ATS Match Score</div>
                    <div class="score-display">{score:.0f}%</div>
                    <div class="score-verdict" style="font-size: 1.5rem; font-weight: 600; margin: 0.5rem 0;">
                        {score_verdict}
                    </div>
                    <div class="score-description">{score_message}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if score > 80:
                    st.balloons()
                
                # Mini Statistics
                st.markdown("### 📊 Quick Statistics")
                col1, col2, col3, col4 = st.columns(4)
                
                keywords_found = len(match_data.get('keywords', []))
                
                with col1:
                    st.markdown(f"""
                    <div class="stat-mini">
                        <div class="stat-mini-value">{score:.0f}%</div>
                        <div class="stat-mini-label">Match Score</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="stat-mini">
                        <div class="stat-mini-value">{keywords_found}</div>
                        <div class="stat-mini-label">Skills Found</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    sections_found = sum([1 for v in segmented.values() if v and v != segmented.get('full_text')])
                    st.markdown(f"""
                    <div class="stat-mini">
                        <div class="stat-mini-value">{sections_found}</div>
                        <div class="stat-mini-label">Sections Parsed</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    confidence = "High" if score > 80 else "Medium" if score > 60 else "Low"
                    st.markdown(f"""
                    <div class="stat-mini">
                        <div class="stat-mini-value">{confidence}</div>
                        <div class="stat-mini-label">Confidence</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
                
                # Gap Analysis
                st.markdown("### 🎯 Skills Gap Analysis")
                
                # Load taxonomy for better suggestions
                try:
                    with open("data/config.yaml", "r") as f:
                        config = yaml.safe_load(f)
                    
                    all_tech_skills = [skill for cat in config.get('taxonomy', {}).values() for skill in cat]
                except:
                    all_tech_skills = []
                
                found_in_jd = [s for s in all_tech_skills if s in cleaned_jd]
                found_in_res = [s for s in all_tech_skills if s in cleaned_resume]
                missing = list(set(found_in_jd) - set(found_in_res))
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### ✅ Skills You Have")
                    if found_in_res:
                        st.markdown('<div class="skill-grid">', unsafe_allow_html=True)
                        for skill in found_in_res[:10]:  # Show top 10
                            st.markdown(f'<div class="skill-item">✓ {skill.upper()}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        if len(found_in_res) > 10:
                            st.caption(f"+ {len(found_in_res) - 10} more skills")
                    else:
                        st.info("No matching skills detected from our taxonomy.")
                
                with col2:
                    st.markdown("#### ❌ Missing Skills")
                    if missing:
                        st.markdown('<div class="skill-grid">', unsafe_allow_html=True)
                        for skill in missing[:10]:  # Show top 10
                            st.markdown(f'<div class="skill-item skill-item-missing">⚠ {skill.upper()}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        if len(missing) > 10:
                            st.caption(f"+ {len(missing) - 10} more missing skills")
                    else:
                        st.success("Great! You have all the key skills mentioned in the job description.")
                
                st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
                
                # Actionable Suggestions
                st.markdown("### 💡 Personalized Improvement Recommendations")
                
                suggestions_count = 0
                
                # Priority: High - Missing Skills
                if len(missing) > 0:
                    suggestions_count += 1
                    st.markdown(f"""
                    <div class="priority-high">
                        <strong>🔴 HIGH PRIORITY: Add Missing Skills</strong><br>
                        The job description requires {len(missing)} skill(s) that weren't found in your resume. 
                        Consider naturally incorporating these into your experience section:
                        <br><br>
                        <strong>Top Missing Skills:</strong> {', '.join([s.upper() for s in missing[:5]])}
                        <br><br>
                        <em>💡 Tip: Don't just list them - show how you've used them in real projects or responsibilities.</em>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Priority: High - Formatting Issues
                if not segmented.get('experience'):
                    suggestions_count += 1
                    st.markdown("""
                    <div class="priority-high">
                        <strong>🔴 HIGH PRIORITY: Resume Structure</strong><br>
                        Our parser couldn't clearly identify an 'Experience' or 'Work History' section in your resume. 
                        <br><br>
                        <strong>Action Items:</strong>
                        <ul style="margin: 0.5rem 0;">
                            <li>Use clear section headers like "Work Experience", "Professional Experience", or "Employment History"</li>
                            <li>Ensure consistent formatting throughout your resume</li>
                            <li>Use a standard, ATS-friendly resume template</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Priority: Medium - Score improvement
                if score < 70:
                    suggestions_count += 1
                    st.markdown("""
                    <div class="priority-medium">
                        <strong>🟡 MEDIUM PRIORITY: Keyword Alignment</strong><br>
                        Your resume seems to use different terminology than the job description.
                        <br><br>
                        <strong>Recommendation:</strong> Review the job posting and mirror its language in your resume. 
                        If they say "project management," use that exact phrase instead of "managed projects."
                        <br><br>
                        <em>💡 Tip: Many companies use ATS (Applicant Tracking Systems) that look for exact keyword matches.</em>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Priority: Medium - Skills section
                if len(found_in_res) < 5:
                    suggestions_count += 1
                    st.markdown("""
                    <div class="priority-medium">
                        <strong>🟡 MEDIUM PRIORITY: Strengthen Skills Section</strong><br>
                        Your resume appears to have limited technical skills listed. Most competitive candidates include 8-12 relevant skills.
                        <br><br>
                        <strong>Action:</strong> Add a dedicated "Skills" or "Technical Skills" section near the top of your resume.
                    </div>
                    """, unsafe_allow_html=True)
                
                # Priority: Low - General optimization
                if score >= 70 and score < 85:
                    suggestions_count += 1
                    st.markdown("""
                    <div class="priority-low">
                        <strong>🟢 LOW PRIORITY: Final Polish</strong><br>
                        Your resume is already good! Here are some optional enhancements:
                        <ul style="margin: 0.5rem 0;">
                            <li>Quantify achievements with numbers and percentages</li>
                            <li>Use strong action verbs (Led, Developed, Implemented, Optimized)</li>
                            <li>Tailor your summary/objective to match this specific role</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                if suggestions_count == 0:
                    st.success("🎉 Excellent! Your resume is well-optimized. No major changes needed.")
                
                st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
                
                # Export Report
                st.markdown("### 📥 Save Your Report")
                
                report_data = f"""
RESUME ANALYSIS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Candidate: {user_resume.name}

MATCH SCORE: {score:.1f}%
Verdict: {score_verdict}

STATISTICS:
- Skills Found: {keywords_found}
- Skills Missing: {len(missing)}
- Sections Parsed: {sections_found}

SKILLS YOU HAVE:
{chr(10).join(['• ' + s.upper() for s in found_in_res])}

MISSING SKILLS:
{chr(10).join(['• ' + s.upper() for s in missing])}

RECOMMENDATIONS:
{suggestions_count} improvement areas identified (see detailed report above)
"""
                
                st.download_button(
                    label="📄 Download Full Analysis Report",
                    data=report_data,
                    file_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"❌ An error occurred during analysis: {str(e)}")
                st.exception(e)
    
    else:
        # Empty state
        if not target_jd or not user_resume:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">🎯</div>
                <h3>Ready to Optimize Your Resume?</h3>
                <p>Upload your job description and resume to get started with AI-powered feedback</p>
                <p style="margin-top: 1rem; font-size: 0.9rem;">
                    <strong>What you'll get:</strong><br>
                    ✓ ATS Match Score<br>
                    ✓ Skills Gap Analysis<br>
                    ✓ Personalized Recommendations<br>
                    ✓ Downloadable Report
                </p>
            </div>
            """, unsafe_allow_html=True)