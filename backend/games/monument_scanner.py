import streamlit as st
from PIL import Image
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
import google.generativeai as genai
from dotenv import load_dotenv
import os
from datetime import datetime
from backend.games.console import *  # Import the same backend functions as other games

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load model and processor once
processor = AutoImageProcessor.from_pretrained("mmgyorke/vit-world-landmarks")
model = AutoModelForImageClassification.from_pretrained("mmgyorke/vit-world-landmarks")

# Achievement definitions matching the pattern
ACHIEVEMENTS = {
    'monument_scanner': {
        'discoverer': {'name': '🏛️ Monument Master', 'desc': 'Scan 10 different landmarks', 'threshold': 10},
        'historian': {'name': '📚 History Buff', 'desc': 'Learn about 5 UNESCO sites', 'threshold': 5},
        'globe_trotter': {'name': '🌍 Globe Trotter', 'desc': 'Scan monuments from 3 different continents', 'threshold': 3}
    }
}

def detect_landmark(image):
    """Detects landmarks in the uploaded image using the ViT model."""
    inputs = processor(image, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    pred_label = torch.argmax(probs, dim=-1).item()
    confidence = float(probs[0][pred_label])  # Get confidence score

    labels = model.config.id2label
    return labels.get(pred_label, "Unknown Landmark"), confidence

def get_landmark_info(landmark_name):
    prompt = f"In about 3 bullet points, give me a short description of the landmark {landmark_name}."
    response = genai.GenerativeModel("gemini-pro").generate_content(prompt)
    return response.text if response else "No info available."

def app(wallet_address):
    st.title("🏛️ Monument Scanner")

    # Initialize session state
    if "scanner_state" not in st.session_state:
        st.session_state.scanner_state = {
            'scanned_monuments': [],
            'total_scans': 0,
            'unique_monuments': set(),
            'game_started': False,
            'start_time': None,
            'saved_scans': []
        }

    # Game Controls matching other games
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🎲 New Session", use_container_width=True):
            if st.session_state.scanner_state['game_started'] and len(st.session_state.scanner_state['scanned_monuments']) > 0:
                saved_session = {
                    'monuments': st.session_state.scanner_state['scanned_monuments'],
                    'unique_count': len(st.session_state.scanner_state['unique_monuments']),
                    'total_scans': st.session_state.scanner_state['total_scans'],
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                update_activity_progress(
                    wallet_address,
                    'Monument Scanner',
                    4,  # Activity type 4 for monument scanner
                    len(st.session_state.scanner_state['scanned_monuments']),
                    10,  # Target number of scans
                    additional_data=saved_session
                )
                st.success("Current session saved! Starting new session...")
            
            st.session_state.scanner_state = {
                'scanned_monuments': [],
                'total_scans': 0,
                'unique_monuments': set(),
                'game_started': True,
                'start_time': datetime.now(),
                'saved_scans': []
            }
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset Scanner", use_container_width=True):
            st.session_state.scanner_state = {
                'scanned_monuments': [],
                'total_scans': 0,
                'unique_monuments': set(),
                'game_started': False,
                'start_time': None,
                'saved_scans': []
            }
            st.rerun()

    with col3:
        if st.button("💾 Save Progress", use_container_width=True):
            if st.session_state.scanner_state['game_started'] and len(st.session_state.scanner_state['scanned_monuments']) > 0:
                saved_session = {
                    'monuments': st.session_state.scanner_state['scanned_monuments'],
                    'unique_count': len(st.session_state.scanner_state['unique_monuments']),
                    'total_scans': st.session_state.scanner_state['total_scans'],
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                update_activity_progress(
                    wallet_address,
                    'Monument Scanner',
                    4,
                    len(st.session_state.scanner_state['scanned_monuments']),
                    10,
                    additional_data=saved_session
                )
                st.success("Session progress saved successfully!")
            else:
                st.warning("No active session to save!")

    # Progress tracking
    st.markdown("### 📊 Scanning Progress")
    progress = min(len(st.session_state.scanner_state['unique_monuments']) / 10, 1.0)  # Progress towards 10 unique monuments
    st.progress(progress)
    
    if st.session_state.scanner_state['start_time']:
        elapsed_time = (datetime.now() - st.session_state.scanner_state['start_time']).seconds
        st.markdown(f"⏱️ Session Time: {elapsed_time//60}m {elapsed_time%60}s")

    # Main scanner interface
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        # Detect landmark with confidence
        landmark_name, confidence = detect_landmark(image)
        landmark_info = get_landmark_info(landmark_name)

        col1, col2 = st.columns(2)
        
        with col1:
            st.image(image, caption="Uploaded Image.", use_container_width=True)

        with col2:
            st.write(f"**Detected Landmark:** {landmark_name}")
            st.write(f"**Confidence Score:** {confidence:.2%}")
            st.write("Description of the landmark:")
            st.write(landmark_info)

            # Update progress tracking
            if not st.session_state.scanner_state['game_started']:
                st.session_state.scanner_state['game_started'] = True
                st.session_state.scanner_state['start_time'] = datetime.now()

            st.session_state.scanner_state['total_scans'] += 1
            st.session_state.scanner_state['unique_monuments'].add(landmark_name)
            
            scan_data = {
                'landmark': landmark_name,
                'confidence': confidence,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'info': landmark_info
            }
            st.session_state.scanner_state['scanned_monuments'].append(scan_data)

            # Check achievements
            if len(st.session_state.scanner_state['unique_monuments']) >= 10:
                update_achievement(wallet_address, 'discoverer')
            
            # Update database
            update_activity_progress(
                wallet_address,
                'Monument Scanner',
                4,
                len(st.session_state.scanner_state['scanned_monuments']),
                10,
                additional_data={
                    'last_scan': scan_data,
                    'unique_count': len(st.session_state.scanner_state['unique_monuments'])
                }
            )

    # Display statistics
    if st.session_state.scanner_state['total_scans'] > 0:
        st.markdown("### 📈 Session Statistics")
        st.write(f"Total Scans: {st.session_state.scanner_state['total_scans']}")
        st.write(f"Unique Monuments: {len(st.session_state.scanner_state['unique_monuments'])}")