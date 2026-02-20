import streamlit as st
import yaml
import os
from datetime import datetime

def render():
    # Custom CSS for admin view
    st.markdown("""
    <style>
        .admin-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
        }
        
        .card-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid #f3f4f6;
        }
        
        .card-icon {
            font-size: 1.5rem;
        }
        
        .card-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: #1f2937;
            margin: 0;
        }
        
        .card-description {
            color: #6b7280;
            font-size: 0.875rem;
            margin-top: 0.25rem;
        }
        
        .skill-chip {
            display: inline-block;
            background: #dbeafe;
            color: #1e40af;
            padding: 0.25rem 0.75rem;
            border-radius: 16px;
            font-size: 0.875rem;
            margin: 0.25rem;
            font-weight: 500;
        }
        
        .weight-display {
            background: #f0fdf4;
            border: 2px solid #86efac;
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
            margin: 0.5rem 0;
        }
        
        .weight-value {
            font-size: 2rem;
            font-weight: 700;
            color: #15803d;
            margin: 0;
        }
        
        .weight-label {
            color: #166534;
            font-size: 0.875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .info-box {
            background: #eff6ff;
            border-left: 4px solid #3b82f6;
            padding: 1rem;
            border-radius: 4px;
            margin: 1rem 0;
        }
        
        .warning-box {
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 1rem;
            border-radius: 4px;
            margin: 1rem 0;
        }
        
        .success-animation {
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from {
                transform: translateY(-10px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    config_path = "data/config.yaml"
    
    # Load current config with error handling
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        st.error("⚠️ Configuration file not found. Please ensure data/config.yaml exists.")
        return
    except yaml.YAMLError as e:
        st.error(f"⚠️ Error parsing configuration file: {e}")
        return
    
    # Ensure required keys exist with defaults
    if 'taxonomy' not in config:
        config['taxonomy'] = {}
    
    if 'scoring_weights' not in config:
        config['scoring_weights'] = {
            'cosine': 0.5,
            'jaccard': 0.5
        }
        st.info("ℹ️ Scoring weights not found in config. Using default values (50/50).")
    
    # Ensure both weights exist
    if 'cosine' not in config['scoring_weights']:
        config['scoring_weights']['cosine'] = 0.5
    if 'jaccard' not in config['scoring_weights']:
        config['scoring_weights']['jaccard'] = 0.5
    
    # Info banner
    st.markdown("""
    <div class="info-box">
        <strong>ℹ️ About System Configuration</strong><br>
        Changes made here will affect how the AI evaluates resumes. Make sure to test thoroughly after updates.
    </div>
    """, unsafe_allow_html=True)
    
    # === SECTION 1: SKILL TAXONOMY ===
    st.markdown("""
    <div class="admin-card">
        <div class="card-header">
            <span class="card-icon">📚</span>
            <div>
                <h3 class="card-title">Skill Taxonomy Management</h3>
                <p class="card-description">Define and organize skills by category for intelligent matching</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    updated_taxonomy = {}
    
    # Create expandable sections for each category
    if not config['taxonomy']:
        st.warning("⚠️ No skill categories found in configuration. Add categories below:")
        # Provide a way to add new categories
        new_category = st.text_input("New Category Name", placeholder="e.g., technical, soft_skills")
        new_skills_input = st.text_area("Skills (comma-separated)", placeholder="e.g., python, java, communication")
        if st.button("Add Category") and new_category and new_skills_input:
            config['taxonomy'][new_category] = [s.strip().lower() for s in new_skills_input.split(",") if s.strip()]
            st.success(f"Added category: {new_category}")
            st.rerun()
    
    for idx, (category, skills) in enumerate(config['taxonomy'].items()):
        with st.expander(f"🏷️ {category.upper()} ({len(skills)} skills)", expanded=(idx == 0)):
            st.markdown(f"**Current Skills:**")
            # Display current skills as chips
            chips_html = "".join([f'<span class="skill-chip">{skill}</span>' for skill in skills])
            st.markdown(f'<div style="margin: 0.5rem 0;">{chips_html}</div>', unsafe_allow_html=True)
            
            # Edit field
            new_skills = st.text_area(
                f"Edit {category} skills (comma-separated)",
                value=", ".join(skills),
                height=100,
                key=f"taxonomy_{category}",
                help=f"Add or remove skills for {category}. Separate multiple skills with commas."
            )
            updated_taxonomy[category] = [s.strip().lower() for s in new_skills.split(",") if s.strip()]
            
            # Show count
            new_count = len(updated_taxonomy[category])
            old_count = len(skills)
            if new_count != old_count:
                delta = new_count - old_count
                st.caption(f"📊 Skills count: {old_count} → {new_count} ({'+' if delta > 0 else ''}{delta})")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # === SECTION 2: SCORING WEIGHTS ===
    st.markdown("""
    <div class="admin-card">
        <div class="card-header">
            <span class="card-icon">⚖️</span>
            <div>
                <h3 class="card-title">AI Scoring Weights</h3>
                <p class="card-description">Adjust the balance between semantic context and exact keyword matching</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Explanation of scoring methods
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.markdown("""
        **🧠 Cosine Similarity (Semantic)**
        - Understands context and meaning
        - Better for varied terminology
        - More intelligent matching
        """)
    with col_info2:
        st.markdown("""
        **🎯 Jaccard Index (Keywords)**
        - Exact skill matching
        - Precise requirements
        - Better for specific terms
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Weight sliders with visual feedback
    col1, col2 = st.columns(2)
    
    with col1:
        new_cos = st.slider(
            "Cosine Weight (Semantic Context)",
            min_value=0.0,
            max_value=1.0,
            value=float(config['scoring_weights']['cosine']),
            step=0.05,
            help="Higher values prioritize understanding context over exact keywords"
        )
        st.markdown(f"""
        <div class="weight-display">
            <p class="weight-value">{new_cos:.0%}</p>
            <p class="weight-label">Semantic Weight</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        new_jac = 1.0 - new_cos
        st.markdown(f"""
        <div style="margin-top: 2.2rem;"></div>
        """, unsafe_allow_html=True)
        st.metric(
            label="Jaccard Weight (Auto-calculated)",
            value=f"{new_jac:.0%}",
            delta=None,
            help="Automatically balances to ensure weights sum to 100%"
        )
        st.markdown(f"""
        <div class="weight-display">
            <p class="weight-value">{new_jac:.0%}</p>
            <p class="weight-label">Keyword Weight</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Visual indicator of balance
    st.markdown("<br>", unsafe_allow_html=True)
    
    if new_cos > 0.7:
        recommendation = "⚠️ High semantic weight - good for diverse job descriptions"
        box_class = "warning-box"
    elif new_cos < 0.3:
        recommendation = "⚠️ High keyword weight - good for technical exact matches"
        box_class = "warning-box"
    else:
        recommendation = "✅ Balanced configuration - recommended for most use cases"
        box_class = "info-box"
    
    st.markdown(f'<div class="{box_class}">{recommendation}</div>', unsafe_allow_html=True)
    
    # === SECTION 3: SAVE CONFIGURATION ===
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])
    
    with col_btn1:
        save_button = st.button(
            "💾 Save Configuration",
            type="primary",
            use_container_width=True,
            help="Apply changes to the system"
        )
    
    with col_btn2:
        if st.button("🔄 Reset to Default", use_container_width=True):
            st.warning("Reset functionality - implement default config restore")
    
    with col_btn3:
        if st.button("📋 Preview Changes", use_container_width=True):
            with st.expander("📊 Configuration Preview", expanded=True):
                st.json({
                    "taxonomy": updated_taxonomy,
                    "scoring_weights": {
                        "cosine": new_cos,
                        "jaccard": new_jac
                    }
                })
    
    # Save logic
    if save_button:
        try:
            config['taxonomy'] = updated_taxonomy
            config['scoring_weights']['cosine'] = float(new_cos)
            config['scoring_weights']['jaccard'] = float(new_jac)
            
            # Backup old config
            backup_path = f"{config_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            with open(config_path, 'r') as f:
                with open(backup_path, 'w') as backup:
                    backup.write(f.read())
            
            # Save new config
            with open(config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            
            st.markdown("""
            <div class="success-animation">
            </div>
            """, unsafe_allow_html=True)
            
            st.success("✅ Configuration updated successfully!")
            st.info(f"💾 Backup saved to: {backup_path}")
            
            # Show what changed
            with st.expander("📝 Change Summary"):
                total_skills = sum(len(skills) for skills in updated_taxonomy.values())
                st.write(f"**Total Skills Configured:** {total_skills}")
                st.write(f"**Semantic Weight:** {new_cos:.0%}")
                st.write(f"**Keyword Weight:** {new_jac:.0%}")
                st.write(f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            st.error(f"❌ Error saving configuration: {str(e)}")
            st.exception(e)