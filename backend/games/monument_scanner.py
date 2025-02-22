import streamlit as st
from PIL import Image
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load model and processor once
processor = AutoImageProcessor.from_pretrained("mmgyorke/vit-world-landmarks")
model = AutoModelForImageClassification.from_pretrained("mmgyorke/vit-world-landmarks")

def detect_landmark(image):
    """Detects landmarks in the uploaded image using the ViT model."""
    inputs = processor(image, return_tensors="pt")  # Convert image to tensor
    with torch.no_grad():
        outputs = model(**inputs)  # Run through model

    # Get the highest confidence class
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    pred_label = torch.argmax(probs, dim=-1).item()

    # Get label names
    labels = model.config.id2label  # Maps label index to landmark name
    return labels.get(pred_label, "Unknown Landmark")


def get_landmark_info(landmark_name):
    prompt = f"In about 3 bullet points, give me a short description of the landmark {landmark_name}."
    response = genai.GenerativeModel("gemini-pro").generate_content(prompt)
    return response.text if response else "No info available."


def app(wallet_address):
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        # st.image(image, caption="Uploaded Image.", use_container_width=True)

        # Detect landmark
        landmark_name = detect_landmark(image)
        # st.write(f"**Detected Landmark:** {landmark_name}")

        landmark_info = get_landmark_info(landmark_name)


        col1, col2 = st.columns(2)
        
        with col1:
            st.image(image, caption="Uploaded Image.", use_container_width=True)

        with col2:
            st.write(f"**Detected Landmark:** {landmark_name}")
            st.write(f"Description of the landmark: ")
            st.write(landmark_info)

