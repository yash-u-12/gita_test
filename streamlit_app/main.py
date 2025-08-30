import streamlit as st
import sys
import os
import websockets


# Add the project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from database.db_utils import get_db_manager

# Page configuration
st.set_page_config(
    page_title="Gita Guru - Divine Learning",
    page_icon="🕉️",
    layout="wide"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .header-section {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        border-bottom: 1px solid rgba(255,255,255,0.2);
        text-align: center;
        color: white;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 1rem;
    }
    
    .sloka-display {
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .meaning-section {
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    
    .meaning-section:hover {
        transform: translateY(-2px);
    }
    
    .meaning-title {
        font-weight: 600;
        color: white;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
    }
    
    .meaning-icon {
        margin-right: 0.5rem;
        font-size: 1.2rem;
    }
    
    .sloka-text {
        color: white;
        font-size: 1.2rem;
        line-height: 1.8;
        text-align: center;
        font-weight: 500;
    }
    
    .meaning-text {
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.6;
        font-size: 1rem;
    }
    
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
    }
    
    .stSelectbox > div > div > div {
        color: white;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        border: none;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .section-header {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1.5rem 0 1rem 0;
        border-left: 4px solid #667eea;
        backdrop-filter: blur(10px);
    }
    
    .section-header h3 {
        color: white;
        margin: 0;
        font-size: 1.3rem;
        font-weight: 600;
    }
    
    .audio-player {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    .info-box {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ffd700;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    .info-box p {
        color: rgba(255, 255, 255, 0.9);
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize database manager
    db_manager = get_db_manager()
    
    # Header section
    st.markdown("""
    <div class="header-section">
        <div class="main-title">🕉️ Gita Guru</div>
        <div class="subtitle">Bhagavad Gita Sloka Viewer</div>
        <div style="opacity: 0.8;">Explore the divine wisdom of the Bhagavad Gita</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Fetch chapters from Supabase
    chapters = db_manager.get_all_chapters()
    if not chapters:
        st.error("No chapters found in database. Please check your database connection.")
        return
    
    # Chapter selection
    st.markdown("""
    <div class="section-header">
        <h3>📚 Select Chapter</h3>
    </div>
    """, unsafe_allow_html=True)
    
    chapter_options = {f"Chapter {ch['chapter_number']}: {ch['chapter_name']}": ch for ch in chapters}
    selected_chapter_display = st.selectbox(
        "Choose a chapter to explore:",
        ["Select a Chapter"] + list(chapter_options.keys())
    )
    
    if selected_chapter_display != "Select a Chapter":
        selected_chapter = chapter_options[selected_chapter_display]
        
        # Fetch slokas for selected chapter from Supabase
        slokas = db_manager.get_slokas_by_chapter(selected_chapter['id'])
        if not slokas:
            st.markdown("""
            <div class="info-box">
                <p>No slokas found for this chapter.</p>
            </div>
            """, unsafe_allow_html=True)
            return
        
        # Sloka selection
        st.markdown("""
        <div class="section-header">
            <h3>🎯 Select Sloka</h3>
        </div>
        """, unsafe_allow_html=True)
        
        sloka_options = {f"Sloka {sloka['sloka_number']}": sloka for sloka in slokas}
        selected_sloka_display = st.selectbox(
            "Choose a sloka to read:",
            ["Select a Sloka"] + list(sloka_options.keys())
        )
        
        if selected_sloka_display != "Select a Sloka":
            selected_sloka = sloka_options[selected_sloka_display]
            
            # Display sloka content
            st.markdown(f"""
            <div class="section-header">
                <h3>📖 Sloka {selected_sloka['sloka_number']} - Chapter {selected_chapter['chapter_number']}: {selected_chapter['chapter_name']}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Sloka text display
            st.markdown("""
            <div class="sloka-display">
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
<div class="sloka-text">
    {selected_sloka.get('sloka_text_telugu', 'Text not available')}
</div>
""", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Meanings display
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="meaning-section">
                    <div class="meaning-title">
                        <span class="meaning-icon">📖</span>
                        Telugu Meaning
                    </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
<div class="meaning-text">
    {selected_sloka.get('meaning_telugu', 'Meaning not available')}
</div>
""", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="meaning-section">
                    <div class="meaning-title">
                        <span class="meaning-icon">🌍</span>
                        English Meaning
                    </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
<div class="meaning-text">
    {selected_sloka.get('meaning_english', 'Meaning not available')}
</div>
""", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Reference audio section
            st.markdown("""
            <div class="section-header">
                <h3>🎵 Reference Audio</h3>
            </div>
            """, unsafe_allow_html=True)
            
            ref_url = selected_sloka.get("reference_audio_url")
            if ref_url:
                st.markdown("""
                <div class="audio-player">
                """, unsafe_allow_html=True)
                st.audio(ref_url, format="audio/mp3")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="info-box">
                    <p>No reference audio available for this sloka.</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: white; padding: 2rem 0; opacity: 0.8;">
        <p>🕉️ May the divine wisdom guide your path</p>
        <p><small>Gita Guru - Divine Learning Platform</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
