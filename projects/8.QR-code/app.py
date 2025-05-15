import streamlit as st
import qrcode
import cv2
import numpy as np
from io import BytesIO
from PIL import Image

# Function to generate QR Code
def generate_qr_code(text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    
    img = qr.make_image(fill="black", back_color="white")
    
    # Convert PIL image to bytes for Streamlit
    img_bytes = BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    
    return img_bytes

# Function to decode QR Code
def decode_qr_code(image):
    image = np.array(image.convert('RGB'))
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(image)
    return data if data else "No QR code detected."

# Streamlit UI
st.title("🔲 QR Code Generator & Decoder")

# Tabs for Generator and Decoder
tab1, tab2 = st.tabs(["Generate QR Code", "Decode QR Code"])

with tab1:
    st.subheader("Generate QR Code")
    user_input = st.text_input("Enter text or URL")
    if st.button("Generate QR Code"):
        if user_input:
            qr_image_bytes = generate_qr_code(user_input)
            st.image(qr_image_bytes, caption="Your QR Code", use_column_width=False)
            
            # Download button
            st.download_button(label="📥 Download QR Code", data=qr_image_bytes, file_name="qr_code.png", mime="image/png")

with tab2:
    st.subheader("Decode QR Code")
    uploaded_file = st.file_uploader("Upload a QR Code Image", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded QR Code", use_column_width=False)
        decoded_text = decode_qr_code(image)
        st.write("🔍 **Decoded Text:** ", decoded_text)

# Footer
st.markdown("📌 Generate & scan QR codes easily using Python & Streamlit.")
st.write("🔹 Developed by Esha")
