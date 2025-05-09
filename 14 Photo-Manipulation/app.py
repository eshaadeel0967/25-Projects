import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import io

# Streamlit UI
st.title("🖼️ Photo Manipulation App")

# Upload Image
uploaded_file = st.file_uploader("📤 Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Open Image
    image = Image.open(uploaded_file)
    st.image(image, caption="📷 Original Image", use_column_width=True)

    # Choose filter
    filter_option = st.radio("Choose a filter:", ("Original", "Grayscale", "Blur", "Brightness", "Contrast"))

    # Apply Filters
    if filter_option == "Grayscale":
        image = image.convert("L")
    elif filter_option == "Blur":
        image = image.filter(ImageFilter.GaussianBlur(radius=5))
    elif filter_option == "Brightness":
        enhancer = ImageEnhance.Brightness(image)
        factor = st.slider("Brightness Factor", 0.5, 3.0, 1.0)
        image = enhancer.enhance(factor)
    elif filter_option == "Contrast":
        enhancer = ImageEnhance.Contrast(image)
        factor = st.slider("Contrast Factor", 0.5, 3.0, 1.0)
        image = enhancer.enhance(factor)

    # Show modified image
    st.image(image, caption="🖌️ Modified Image", use_column_width=True)

    # Download button
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    st.download_button("📥 Download Image", buf.getvalue(), "modified_image.png", "image/png")

# Footer
st.markdown("📌 Apply different filters to your images using Python & Streamlit.")
st.write("🔹 Developed by Esha using Streamlit")
