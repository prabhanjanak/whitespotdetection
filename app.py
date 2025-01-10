from PIL import Image
import numpy as np
import streamlit as st
from skimage import color
import cv2

# Page configuration
st.set_page_config(page_title="White Spot Detection with Binary Imaging", layout="wide")

# Header
st.markdown("<h1 style='text-align: center;'>White Spot Detection (Binary Imaging)</h1>", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Load the image using PIL
    image = Image.open(uploaded_file)
    image = image.convert("RGB")  # Ensure the image is in RGB mode
    image_np = np.array(image)

    # Convert RGB to Lab color space
    lab_image = color.rgb2lab(image_np)

    # Define thresholds for white spot detection in Lab space (adjusted for better detection)
    l_threshold = 90  # High lightness (L value, range 0-100)
    a_threshold = 15  # Allow a little more variation for a (red/green)
    b_threshold = 15  # Allow a little more variation for b (yellow/blue)

    # Create a binary mask for white spots
    binary_mask = (
        (lab_image[..., 0] >= l_threshold) &  # High lightness
        (np.abs(lab_image[..., 1]) <= a_threshold) &  # Low a (red/green)
        (np.abs(lab_image[..., 2]) <= b_threshold)    # Low b (yellow/blue)
    )

    # Convert the boolean mask to binary (0 and 255)
    binary_image = (binary_mask * 255).astype(np.uint8)

    # Calculate percentage of white spots
    total_pixels = image_np.shape[0] * image_np.shape[1]
    white_pixel_count = np.sum(binary_mask)
    white_percentage = (white_pixel_count / total_pixels) * 100

    # Overlay white spots on the original image
    annotated_image = image_np.copy()
    annotated_image[binary_mask] = [255, 0, 0]  # Mark white spots with red color

    # Display the annotated image with reduced size
    st.image(annotated_image, caption="Detected White Spots (Marked in Red)", use_column_width=True)

    # Show binary image only when button is clicked
    show_binary_image = st.button("Show Binary Image")

    if show_binary_image:
        # Display the binary image with reduced size
        st.image(binary_image, caption="Binary Image (White Spots)", use_column_width=True, channels="GRAY")

    # Save the binary and annotated images when the button is clicked
    if st.button("Save Images"):
        # Convert to PIL Image for saving
        binary_image_pil = Image.fromarray(binary_image)
        annotated_image_pil = Image.fromarray(annotated_image)

        # Save the images
        binary_image_pil.save("binary_image.png")
        annotated_image_pil.save("annotated_image.png")

        st.success("Images saved successfully!")
        st.write("You can download them from the following links:")
        st.download_button("Download Binary Image", data=open("binary_image.png", "rb"), file_name="binary_image.png", mime="image/png")
        st.download_button("Download Annotated Image", data=open("annotated_image.png", "rb"), file_name="annotated_image.png", mime="image/png")

    # Display the percentage of white spots
    st.write(f"**White Spot Percentage:** {white_percentage:.2f}%")

# Footer
st.markdown("<hr><p style='text-align: center;'>Developed by Prabhanjan</p>", unsafe_allow_html=True)
