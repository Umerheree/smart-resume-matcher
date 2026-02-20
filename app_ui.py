import streamlit as st
import pandas as pd
from views import recruiter_dashboard, candidate_feedback, admin_view

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="NexGen AI ATS",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR PROFESSIONAL UI ---
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 2rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%);
    }
    
    [data-testid="stSidebar"] .css-1d391kg, [data-testid="stSidebar"] .st-emotion-cache-1gulkj5 {
        color: white;
    }
    
    /* Sidebar text color */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .st-emotion-cache-16idsys p {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Logo container */
    .logo-container {
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 1rem;
    }
    
    /* Brand styling */
    .brand-title {
        color: white;
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 0.5rem;
        letter-spacing: 0.5px;
    }
    
    .brand-tagline {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.85rem;
        margin-top: 0.25rem;
    }
    
    /* Navigation styling */
    .nav-section {
        margin: 2rem 0 1.5rem 0;
    }
    
    .nav-label {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.75rem;
    }
    
    /* Radio button styling for navigation */
    [data-testid="stSidebar"] .row-widget.stRadio > div {
        gap: 0.5rem;
    }
    
    [data-testid="stSidebar"] .row-widget.stRadio > div > label {
        background: rgba(255, 255, 255, 0.1);
        padding: 0.75rem 1rem;
        border-radius: 8px;
        transition: all 0.3s ease;
        cursor: pointer;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] .row-widget.stRadio > div > label:hover {
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.3);
        transform: translateX(4px);
    }
    
    [data-testid="stSidebar"] .row-widget.stRadio > div > label[data-baseweb="radio"] > div:first-child {
        background-color: rgba(255, 255, 255, 0.2);
    }
    
    /* Divider styling */
    [data-testid="stSidebar"] hr {
        margin: 1.5rem 0;
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    /* Footer styling - removed absolute positioning to prevent overlap */
    
    /* Page header */
    .page-header {
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #e5e7eb;
    }
    
    .page-title {
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .page-description {
        color: #6b7280;
        font-size: 1rem;
    }
    
    /* Icons for navigation items */
    .nav-icon {
        margin-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    # Logo and branding
    st.markdown("""
        <div class="logo-container">
            <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="70" style="filter: brightness(0) invert(1);">
            <div class="brand-title">NexGen AI ATS</div>
            <div class="brand-tagline">Intelligent Talent Acquisition</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation section
    st.markdown('<div class="nav-label">🎯 WORKSPACE</div>', unsafe_allow_html=True)
    
    # Navigation menu with icons
    navigation_options = {
        "👥 Recruiter Dashboard": "Recruiter Dashboard",
        "📊 Candidate Feedback": "Candidate Feedback",
        "⚙️ System Administration": "System Administration"
    }
    
    selected_display = st.radio(
        "Navigate to",
        list(navigation_options.keys()),
        label_visibility="collapsed"
    )
    
    # Map display name back to internal value
    app_mode = navigation_options[selected_display]
    
    st.markdown("---")
    
    # Help section
    with st.expander("ℹ️ Quick Guide", expanded=False):
        st.markdown("""
        **Recruiter Dashboard**  
        Batch process resumes and rank candidates
        
        **Candidate Feedback**  
        Get AI-powered resume optimization tips
        
        **System Admin**  
        Manage skill taxonomy and scoring weights
        """)
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <p style="color: rgba(255, 255, 255, 0.6); font-size: 0.75rem; margin: 0;">Developed by</p>
            <p style="color: white; font-weight: 600; font-size: 0.85rem; margin: 0.25rem 0 0 0;">Umer Mehboob</p>
        </div>
    """, unsafe_allow_html=True)

# --- DYNAMIC VIEW ROUTING WITH PAGE HEADERS ---
page_info = {
    "Recruiter Dashboard": {
        "title": "Recruiter Dashboard",
        "description": "Batch process resumes, rank candidates, and make data-driven hiring decisions",
        "icon": "👥"
    },
    "Candidate Feedback": {
        "title": "Candidate Feedback Portal",
        "description": "Receive personalized AI-powered recommendations to optimize your resume",
        "icon": "📊"
    },
    "System Administration": {
        "title": "System Administration",
        "description": "Configure skill taxonomy, manage scoring weights, and customize ATS parameters",
        "icon": "⚙️"
    }
}

# Display page header
current_page = page_info[app_mode]
st.markdown(f"""
    <div class="page-header">
        <div class="page-title">{current_page['icon']} {current_page['title']}</div>
        <div class="page-description">{current_page['description']}</div>
    </div>
""", unsafe_allow_html=True)

# Route to appropriate view
if app_mode == "Recruiter Dashboard":
    recruiter_dashboard.render()
elif app_mode == "Candidate Feedback":
    candidate_feedback.render()
elif app_mode == "System Administration":
    admin_view.render()