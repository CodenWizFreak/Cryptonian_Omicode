import streamlit as st
import random
from PIL import Image
import os

def load_puzzle_images():
    return [
        ("Taj Mahal", "assets/artifact_images/taj_mahal.jpeg"),
        ("Konark Sun Temple", "assets/artifact_images/konark_temple.jpeg"),
        ("Qutub Minar", "assets/artifact_images/qutub_minar.jpeg")
    ]

def scramble_image(image_path, grid_size=3):
    image = Image.open(image_path)
    width, height = image.size
    piece_width = width // grid_size
    piece_height = height // grid_size
    pieces = []
    for i in range(grid_size):
        for j in range(grid_size):
            piece = image.crop((j * piece_width, i * piece_height, (j + 1) * piece_width, (i + 1) * piece_height))
            pieces.append(piece)
    random.shuffle(pieces)
    return pieces, (piece_width, piece_height)

def app(wallet_address):
    st.title("🧩 Artifact Assembler: Piece it Together!")
    st.write("Reassemble the artifact by arranging the pieces in the correct order!")
    
    artifacts = load_puzzle_images()
    selected_artifact = st.selectbox("Choose an artifact to assemble:", [name for name, _ in artifacts])
    artifact_image = next(path for name, path in artifacts if name == selected_artifact)
    
    grid_size = st.selectbox("Select difficulty:", [2, 3, 4], index=1)
    pieces, (pw, ph) = scramble_image(artifact_image, grid_size)
    
    st.write("Drag and drop the pieces into the correct order:")
    
    cols = st.columns(grid_size)
    user_order = []
    for i in range(grid_size):
        for j in range(grid_size):
            idx = i * grid_size + j
            user_order.append(st.selectbox(f"Piece {idx+1}", list(range(len(pieces))), key=f"piece_{idx}"))
            cols[j].image(pieces[idx], use_container_width=True)
    
    if st.button("Check Order"):
        correct_order = list(range(len(pieces)))
        if user_order == correct_order:
            st.success("🎉 Correct! You've assembled the artifact!")
            st.write(f"About the {selected_artifact}: This is a historical marvel of India!")
        else:
            st.error("❌ Incorrect! Try again.")
