"""
SHL Assessment Recommendation System - Streamlit Web Application

This is the main web interface for the assessment recommendation system.
It provides an intuitive interface for recruiters to get assessment recommendations.
"""

import streamlit as st
import yaml
import sys
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

# Load environment variables first
load_dotenv(Path(__file__).parent / ".env")

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.recommendation.recommender import AssessmentRecommender

# Page configuration
st.set_page_config(
    page_title="SHL Assessment Recommendation System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme Settings in Sidebar
with st.sidebar:
    st.markdown("### 🎨 Theme Settings")
    
    theme = st.radio(
        "Select theme",
        ["Light", "Dark"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    primary_color = st.color_picker(
        "Primary Color",
        value="#1E3A8A"
    )
    
    text_color = st.color_picker(
        "Text Color",
        value="#0F172A"
    )
    
    bg_color = st.color_picker(
        "Background Color",
        value="#F8FAFC" if theme == "Light" else "#1E293B"
    )

# Custom CSS
# Custom CSS
st.markdown(f"""
<style>
    .main-header {{
        font-size: 2.5rem;
        color: {primary_color};
        font-weight: bold;
        margin-bottom: 0.5rem;
    }}
    .sub-header {{
        font-size: 1.2rem;
        color: #64748B;
        margin-bottom: 2rem;
    }}
    .assessment-card {{
        background-color: {bg_color};
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid {primary_color};
        margin-bottom: 1rem;
        color: {text_color};
    }}
    .assessment-name {{
        font-size: 1.3rem;
        font-weight: bold;
        color: {primary_color};
        margin-bottom: 0.5rem;
    }}
    .similarity-badge {{
        display: inline-block;
        background-color: #10B981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        font-weight: 600;
    }}
    .info-label {{
        font-weight: 600;
        color: {text_color};
    }}
    .recommendation-box {{
        background-color: {bg_color};
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid {primary_color};
        margin-top: 1rem;
        color: {text_color};
    }}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_recommender():
    """Load the recommendation system (cached)."""
    try:
        # First, ensure vector DB is built
        import json
        from src.embeddings.build_vector_db import VectorDBBuilder
        
        # Check if vector DB is empty and rebuild if needed
        try:
            recommender = AssessmentRecommender()
            # Try to query to see if DB has data
            test_results = recommender.retriever.collection.count()
            if test_results == 0:
                st.info("📊 Building vector database... This may take a minute")
                builder = VectorDBBuilder()
                with open('data/raw/shl_catalog.json', 'r', encoding='utf-8') as f:
                    assessments = json.load(f)
                builder.build(assessments)
                st.success("✅ Vector database built successfully!")
        except:
            # If error occurs, rebuild from scratch
            st.info("📊 Initializing vector database... This may take a minute")
            builder = VectorDBBuilder()
            with open('data/raw/shl_catalog.json', 'r', encoding='utf-8') as f:
                assessments = json.load(f)
            builder.build(assessments)
            st.success("✅ Vector database initialized successfully!")
        
        recommender = AssessmentRecommender()
        if recommender.client is None:
            st.warning("⚠️ OpenAI API key not configured. LLM features will be disabled.")
        return recommender
    except Exception as e:
        import traceback
        st.error(f"Error loading recommendation system: {str(e)}")
        st.error("Full error details:")
        st.code(traceback.format_exc())
        st.info("Please ensure:\n"
                "1. .env file exists with OPENAI_API_KEY\n"
                "2. Data pipeline has been run:\n"
                "   - python src/scraper/scrape_shl.py\n"
                "   - python src/scraper/parser.py\n"
                "   - python src/embeddings/build_vector_db.py")
        return None


def display_assessment_card(assessment: dict, show_full: bool = True):
    """Display an assessment in a card format."""
    
    # Format similarity score with color coding
    similarity = assessment.get('similarity_score', 0.0)
    # Clamp for display: 0–100%
    display_score = max(0.0, similarity)
    score_pct = int(round(display_score * 100))
    
    # UI-level relevance bands
    if score_pct >= 70:
        badge_color = "#10B981"  # Green
        badge_text = f"Match: {score_pct}% (High)"
    elif score_pct >= 30:
        badge_color = "#F59E0B"  # Amber
        badge_text = f"Match: {score_pct}% (Medium)"
    else:
        badge_color = "#3B82F6"  # Blue
        badge_text = f"Match: {score_pct}% (Low)"
    
    st.markdown(f"""
    <div class="assessment-card">
        <div class="assessment-name">{assessment['name']}</div>
        <span style="display: inline-block; background-color: {badge_color}; color: white; padding: 0.3rem 0.8rem; border-radius: 1rem; font-size: 0.875rem; font-weight: 600;">
            {badge_text}
        </span>
        <br><br>
        <span class="info-label">Category:</span> {assessment['category']}<br>
        <span class="info-label">Duration:</span> {assessment['duration']}<br>
        <span class="info-label">Experience Level:</span> {assessment['experience_level']}
    </div>
    """, unsafe_allow_html=True)
    
    if show_full:
        with st.expander("📋 Full Details"):
            st.write("**Description:**")
            st.write(assessment['description'])
            st.write("**Skills Measured:**")
            st.write(assessment['skills_measured'])
            st.write("**Job Suitability:**")
            st.write(assessment['job_suitability'])
            st.write("**Delivery Method:**")
            st.write(assessment['delivery_method'])
            
            # Show detailed score
            st.divider()
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write("**Similarity Score:**")
            with col2:
                st.metric("", f"{score_pct}%", delta=None)


def main():
    """Main application function."""
    
    # Header
    st.markdown('<div class="main-header">🎯 SHL Assessment Recommendation System</div>', 
                unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-powered assessment recommendations for your hiring needs</div>', 
                unsafe_allow_html=True)
    
    # Load recommender
    recommender = load_recommender()
    if recommender is None:
        return
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/200x80/1E3A8A/FFFFFF?text=SHL", 
                 use_column_width=True)
        st.markdown("## About")
        st.info(
            "This system uses Retrieval-Augmented Generation (RAG) to recommend "
            "the most suitable SHL assessments based on your job requirements."
        )
        
        st.markdown("## Features")
        st.markdown("""
        - 🔍 Semantic search across 20+ assessments
        - 🤖 AI-powered recommendations
        - 📊 Detailed assessment information
        - ⚡ Fast and accurate matching
        """)
        
        st.markdown("## How it works")
        st.markdown("""
        1. Enter job details and requirements
        2. System retrieves relevant assessments
        3. AI generates personalized recommendations
        4. Review matches with explanations
        """)
    
    # Main content area
    tab1, tab2 = st.tabs(["🎯 Get Recommendations", "📚 Browse Catalog"])
    
    with tab1:
        st.markdown("### Enter Job Requirements")
        
        col1, col2 = st.columns(2)
        
        with col1:
            job_title = st.text_input(
                "Job Title *",
                placeholder="e.g., Software Engineer, Sales Manager, HR Business Partner",
                help="Enter the job title or role you're hiring for"
            )
            
            experience_level = st.selectbox(
                "Experience Level *",
                ["Entry", "Mid", "Senior", "Executive"],
                help="Select the experience level required for this role"
            )
        
        with col2:
            skills_input = st.text_area(
                "Required Skills *",
                placeholder="Enter skills separated by commas\ne.g., Python, Problem Solving, Team Leadership",
                height=100,
                help="List the key skills and competencies required"
            )
            
            additional_context = st.text_area(
                "Additional Context (Optional)",
                placeholder="Any additional information about the role or hiring goals",
                height=100,
                help="Provide any additional context that might help"
            )
        
        # Recommendation options
        with st.expander("⚙️ Advanced Options"):
            use_llm = st.checkbox(
                "Use AI-generated explanations", 
                value=True,
                help="Generate detailed explanations using AI (requires OpenAI API key)"
            )
            show_retrieval_scores = st.checkbox(
                "Show similarity scores",
                value=True,
                help="Display similarity scores for each recommendation"
            )
        
        # Generate recommendations button
        if st.button("🚀 Get Recommendations", type="primary", use_container_width=True):
            if not job_title or not skills_input:
                st.error("⚠️ Please fill in Job Title and Required Skills")
            else:
                # Parse skills
                skills = [s.strip() for s in skills_input.split(',') if s.strip()]
                
                with st.spinner("🔍 Analyzing requirements and retrieving assessments..."):
                    try:
                        # Generate recommendations
                        result = recommender.recommend(
                            job_title=job_title,
                            skills=skills,
                            experience_level=experience_level,
                            additional_context=additional_context if additional_context else None,
                            use_llm=use_llm
                        )
                        
                        # Display results
                        st.markdown("---")
                        st.markdown("## 📊 Recommendations")
                        
                        # Summary
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Assessments Found", result['retrieval_count'])
                        with col2:
                            st.metric("Job Title", result['job_title'])
                        with col3:
                            st.metric("Experience Level", result['experience_level'])

                        # Balanced Recommendation summary (K vs P)
                        tech_count = 0
                        beh_count = 0
                        for a in result.get('retrieved_assessments', []):
                            cat = (a.get('category') or '').lower()
                            if 'personality' in cat or 'behavior' in cat:
                                beh_count += 1
                            else:
                                tech_count += 1
                        balanced_text = "✔ Balanced across skill domains" if tech_count and beh_count else "⚠ Consider including both technical and behavioral tests"
                        st.info(f"Recommendation Summary\nTechnical Tests: {tech_count} | Behavioral Tests: {beh_count}\n{balanced_text}")
                        
                        # AI-generated recommendations
                        if result.get('llm_recommendations'):
                            st.markdown("### 🤖 AI-Generated Recommendations")
                            st.markdown(f"""
                            <div class="recommendation-box">
                            {result['llm_recommendations'].replace(chr(10), '<br>')}
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Retrieved assessments (cards only, with normalized display scores)
                        st.markdown("### 📋 Detailed Assessment Information")
                        if result['retrieved_assessments']:
                            scores = [a.get('similarity_score', 0.0) for a in result['retrieved_assessments']]
                            min_s, max_s = (min(scores), max(scores)) if scores else (0.0, 0.0)
                            span = max_s - min_s
                            normalized = []
                            for a in result['retrieved_assessments']:
                                s = a.get('similarity_score', 0.0)
                                if span > 1e-6:
                                    disp = (s - min_s) / span  # 0..1 relative within this result set
                                else:
                                    disp = 0.3 if s > 0 else 0.1  # gentle default when all equal/zero
                                a = {**a, 'similarity_score': disp}
                                normalized.append(a)
                            for assessment in normalized:
                                display_assessment_card(assessment, show_full=True)
                        else:
                            st.warning("No assessments found matching your criteria. Try adjusting your requirements.")
                        
                        # Download option
                        if result['retrieved_assessments']:
                            st.markdown("---")
                            df = pd.DataFrame(result['retrieved_assessments'])
                            csv = df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download Recommendations (CSV)",
                                data=csv,
                                file_name=f"shl_recommendations_{job_title.replace(' ', '_')}.csv",
                                mime="text/csv"
                            )
                    
                    except Exception as e:
                        st.error(f"Error generating recommendations: {str(e)}")
                        st.info("If you're seeing OpenAI API errors, make sure your API key is set in the .env file.")
    
    with tab2:
        # Catalog header banner
        st.markdown("## 📚 SHL Assessment Catalog")
        st.caption("Explore all available assessments")
        st.markdown("### 🔍 Search Assessment Catalog")
        st.caption("Search by role, skill, or assessment type")
        
        search_query = st.text_input(
            "Search by role, skills, or assessment type",
            placeholder="e.g., cognitive ability, sales, leadership",
            help="Enter keywords to search the catalog"
        )
        
        if search_query:
            with st.spinner("Searching catalog..."):
                try:
                    # Get recommendations using semantic search
                    results = recommender.recommend_simple(
                        query=search_query,
                        use_llm=False
                    )
                    
                    # Extract assessments from the result
                    if isinstance(results, dict):
                        # recommend_simple() returns a dict with 'retrieved_assessments' key
                        assessments = results.get('retrieved_assessments', [])
                    elif isinstance(results, list):
                        assessments = results
                    else:
                        assessments = []
                    
                    if assessments:
                        st.markdown(f"### 📋 Found {len(assessments)} matching assessments")
                        
                        # Display as cards
                        for i, assessment in enumerate(assessments):
                            display_assessment_card(assessment, show_full=True)
                    else:
                        st.warning("❌ No assessments found matching your search. Try different keywords!")
                
                except Exception as e:
                    st.error(f"Error searching catalog: {e}")
                    import traceback
                    st.info("Troubleshooting: Check that vector database is built and contains assessments")
        else:
            # Show all assessments if no search query
            st.info("👆 Enter a search query to find assessments, or browse all below:")
            
            try:
                # Load all assessments from file
                import json
                with open('data/raw/shl_catalog.json', 'r', encoding='utf-8') as f:
                    all_assessments = json.load(f)
                
                if all_assessments:
                    st.markdown(f"### 📚 All {len(all_assessments)} Available Assessments")
                    
                    # Add filter by type
                    col1, col2 = st.columns(2)
                    with col1:
                        type_filter = st.selectbox(
                            "Filter by Test Type",
                            ["All"] + list(set([a.get('test_type', 'Unknown') for a in all_assessments]))
                        )
                    
                    with col2:
                        sort_by = st.selectbox(
                            "Sort by",
                            ["Name (A-Z)", "Duration", "Test Type"]
                        )
                    
                    # Filter and sort
                    filtered = all_assessments
                    if type_filter != "All":
                        filtered = [a for a in filtered if a.get('test_type') == type_filter]
                    
                    if sort_by == "Name (A-Z)":
                        filtered = sorted(filtered, key=lambda x: x.get('name', ''))
                    elif sort_by == "Duration":
                        filtered = sorted(filtered, key=lambda x: x.get('duration_minutes', 0))
                    elif sort_by == "Test Type":
                        filtered = sorted(filtered, key=lambda x: x.get('test_type', ''))
                    
                    st.markdown(f"Showing {len(filtered)} assessments")
                    
                    # Display all assessments
                    for assessment in filtered:
                        display_assessment_card(assessment, show_full=False)
                else:
                    st.warning("No assessments found in database")
            except Exception as e:
                st.info("Load assessments from database to browse catalog")

    # Evaluation info box
    st.info("ℹ Recommendations are generated using semantic similarity and evaluated using Recall@K on benchmark queries.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748B; font-size: 0.875rem;">
        <p>SHL Assessment Recommendation System | Powered by RAG & AI</p>
        <p>Built with Streamlit, ChromaDB, Sentence Transformers, and OpenAI</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
