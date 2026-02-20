import streamlit as st
import pandas as pd
from core.parser import ResumeParser
from core.engine import MatchingEngine
from utils.text_utils import extract_contact_info, clean_text
from datetime import datetime
import time

def render():
    # Custom CSS for recruiter dashboard
    st.markdown("""
    <style>
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 12px;
            color: white;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
        }
        
        .metric-label {
            font-size: 0.875rem;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 0.5rem;
        }
        
        .candidate-card {
            background: white;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .candidate-card:hover {
            border-color: #667eea;
            box-shadow: 0 8px 16px rgba(102, 126, 234, 0.2);
            transform: translateY(-2px);
        }
        
        .candidate-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        }
        
        .top-talent-badge {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 16px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-block;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .screening-badge {
            background: #e5e7eb;
            color: #6b7280;
            padding: 0.25rem 0.75rem;
            border-radius: 16px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-block;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .score-circle {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            font-weight: 700;
            color: white;
            margin: 0 auto 1rem auto;
        }
        
        .score-high {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        }
        
        .score-medium {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        }
        
        .score-low {
            background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
        }
        
        .skill-tag {
            display: inline-block;
            background: #eff6ff;
            color: #1e40af;
            padding: 0.375rem 0.75rem;
            border-radius: 6px;
            font-size: 0.75rem;
            margin: 0.25rem;
            font-weight: 500;
            border: 1px solid #dbeafe;
        }
        
        .contact-info {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: #6b7280;
            font-size: 0.875rem;
            margin: 0.5rem 0;
        }
        
        .section-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid #e5e7eb;
        }
        
        .section-icon {
            font-size: 1.5rem;
        }
        
        .section-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: #1f2937;
            margin: 0;
        }
        
        .info-banner {
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border-left: 4px solid #3b82f6;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        .progress-bar {
            height: 8px;
            background: #e5e7eb;
            border-radius: 4px;
            overflow: hidden;
            margin: 0.5rem 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s ease;
        }
        
        .empty-state {
            text-align: center;
            padding: 4rem 2rem;
            color: #9ca3af;
        }
        
        .empty-state-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Info banner
    st.markdown("""
    <div class="info-banner">
        <strong>💡 Pro Tip:</strong> Upload multiple resumes at once for efficient batch processing. 
        Our AI will analyze, score, and rank all candidates automatically.
    </div>
    """, unsafe_allow_html=True)
    
    # Input Section
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📋</span>
        <h2 class="section-title">Job Requirements</h2>
    </div>
    """, unsafe_allow_html=True)
    
    jd_text = st.text_area(
        "Target Job Description",
        height=200,
        placeholder="Paste the complete job description here...\n\nInclude:\n• Required skills and qualifications\n• Job responsibilities\n• Experience requirements\n• Technical competencies",
        help="The more detailed your JD, the more accurate the candidate matching will be."
    )
    
    # Character count
    if jd_text:
        char_count = len(jd_text)
        word_count = len(jd_text.split())
        st.caption(f"📊 {char_count} characters • {word_count} words")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Upload Section
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📎</span>
        <h2 class="section-title">Candidate Resumes</h2>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Upload Candidate Resumes",
        type="pdf",
        accept_multiple_files=True,
        help="Upload multiple PDF resumes. Supported format: PDF only"
    )
    
    # Show uploaded files
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} resume(s) uploaded successfully")
        with st.expander("📄 View uploaded files"):
            for idx, file in enumerate(uploaded_files, 1):
                st.text(f"{idx}. {file.name} ({file.size / 1024:.1f} KB)")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        analyze_button = st.button(
            "🚀 Run Batch Analysis",
            type="primary",
            use_container_width=True,
            disabled=not (jd_text and uploaded_files)
        )
    with col2:
        if st.button("🔄 Clear All", use_container_width=True):
            st.rerun()
    with col3:
        if uploaded_files and jd_text:
            st.metric("Ready", f"{len(uploaded_files)} files", delta="Go!")

    # Analysis Logic
    if analyze_button:
        if not jd_text or not uploaded_files:
            st.warning("⚠️ Please provide both a job description and candidate resumes.")
            return

        parser = ResumeParser()
        engine = MatchingEngine()
        
        all_results = []
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            for idx, file in enumerate(uploaded_files):
                progress = (idx + 1) / len(uploaded_files)
                progress_bar.progress(progress)
                status_text.text(f"Analyzing {file.name}... ({idx + 1}/{len(uploaded_files)})")
                
                try:
                    # Parse and segment
                    segmented = parser.parse(file)
                    contact = extract_contact_info(segmented['full_text'])
                    cleaned = clean_text(segmented['full_text'])
                    
                    # Match using Engine
                    match_data = engine.run_tfidf_match(clean_text(jd_text), [cleaned])[0]
                    
                    all_results.append({
                        "Candidate Name": file.name.replace('.pdf', ''),
                        "Match Score": round(match_data['score'], 2),
                        "Email": contact.get('email', 'N/A'),
                        "Phone": contact.get('phone', 'N/A'),
                        "Top Skills Found": ", ".join(match_data.get('keywords', [])[:5]).upper() if match_data.get('keywords') else "N/A",
                        "Status": "🌟 Top Talent" if match_data['score'] > 75 else "📋 Screening",
                        "Skills Count": len(match_data.get('keywords', []))
                    })
                    
                except Exception as e:
                    st.error(f"Error processing {file.name}: {str(e)}")
                    continue
                
                time.sleep(0.1)  # Small delay for visual feedback
            
            progress_bar.empty()
            status_text.empty()
            
            if not all_results:
                st.error("❌ No resumes could be processed successfully.")
                return
            
            # Create DataFrame
            df = pd.DataFrame(all_results).sort_values(by="Match Score", ascending=False)
            
            # Summary Metrics
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div class="section-header">
                <span class="section-icon">📊</span>
                <h2 class="section-title">Analysis Summary</h2>
            </div>
            """, unsafe_allow_html=True)
            
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            
            with metric_col1:
                st.metric(
                    label="Total Candidates",
                    value=len(df),
                    delta=None
                )
            
            with metric_col2:
                top_talent = len(df[df['Match Score'] > 75])
                st.metric(
                    label="Top Talent",
                    value=top_talent,
                    delta=f"{(top_talent/len(df)*100):.0f}%"
                )
            
            with metric_col3:
                avg_score = df['Match Score'].mean()
                st.metric(
                    label="Avg Match Score",
                    value=f"{avg_score:.1f}%",
                    delta=None
                )
            
            with metric_col4:
                best_match = df['Match Score'].max()
                st.metric(
                    label="Best Match",
                    value=f"{best_match:.1f}%",
                    delta="Top Pick"
                )
            
            # Results Table
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div class="section-header">
                <span class="section-icon">🏆</span>
                <h2 class="section-title">Ranked Shortlist</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Style the dataframe
            def highlight_score(val):
                if isinstance(val, (int, float)):
                    if val > 75:
                        return 'background-color: #d1fae5; color: #065f46; font-weight: 600'
                    elif val > 50:
                        return 'background-color: #fef3c7; color: #92400e; font-weight: 600'
                    else:
                        return 'background-color: #f3f4f6; color: #4b5563'
                return ''
            
            styled_df = df.style.applymap(highlight_score, subset=['Match Score'])
            st.dataframe(styled_df, use_container_width=True, height=400)
            
            # Export Options
            col_export1, col_export2 = st.columns(2)
            
            with col_export1:
                csv = df.to_csv(index=False).encode('utf-8')
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                st.download_button(
                    label="📥 Download Full Report (CSV)",
                    data=csv,
                    file_name=f'candidate_shortlist_{timestamp}.csv',
                    mime='text/csv',
                    use_container_width=True
                )
            
            with col_export2:
                top_candidates = df.head(5).to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⭐ Download Top 5 Only (CSV)",
                    data=top_candidates,
                    file_name=f'top_5_candidates_{timestamp}.csv',
                    mime='text/csv',
                    use_container_width=True
                )
            
            # Top Pick Spotlights
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div class="section-header">
                <span class="section-icon">🌟</span>
                <h2 class="section-title">Top Candidate Spotlights</h2>
            </div>
            """, unsafe_allow_html=True)
            
            top_3 = df.head(3)
            cols = st.columns(3)
            
            for idx, (_, row) in enumerate(top_3.iterrows()):
                with cols[idx]:
                    # Score circle
                    score = row['Match Score']
                    if score > 75:
                        score_class = 'score-high'
                    elif score > 50:
                        score_class = 'score-medium'
                    else:
                        score_class = 'score-low'
                    
                    st.markdown(f"""
                    <div class="candidate-card">
                        <div class="score-circle {score_class}">
                            {score:.0f}%
                        </div>
                        <h3 style="text-align: center; margin: 0 0 0.5rem 0;">
                            {row['Candidate Name'][:30]}
                        </h3>
                        <div style="text-align: center; margin-bottom: 1rem;">
                            <span class="{'top-talent-badge' if score > 75 else 'screening-badge'}">
                                {row['Status']}
                            </span>
                        </div>
                        <div class="contact-info">
                            <span>📧</span>
                            <span>{row['Email']}</span>
                        </div>
                        <div class="contact-info">
                            <span>📱</span>
                            <span>{row['Phone']}</span>
                        </div>
                        <div style="margin-top: 1rem;">
                            <strong style="font-size: 0.875rem; color: #4b5563;">Key Skills:</strong>
                            <div style="margin-top: 0.5rem;">
                                {' '.join([f'<span class="skill-tag">{skill.strip()}</span>' for skill in row['Top Skills Found'].split(',')[:3]])}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ An error occurred during analysis: {str(e)}")
            st.exception(e)
    
    else:
        # Empty state when no analysis has been run
        if not uploaded_files or not jd_text:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🎯</div>
                <h3>Ready to Find Top Talent?</h3>
                <p>Upload job description and candidate resumes to get started</p>
            </div>
            """, unsafe_allow_html=True)