import numpy as np
import cv2
import streamlit as st
from skimage import color
from PIL import Image

# Page configuration
st.set_page_config(page_title="White Spot Detection with Binary Imaging", layout="wide")

# Header
st.markdown("<h1 style='text-align: center;'>White Spot Detection (Binary Imaging)</h1>", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

# White color reference in LAB space (pure white)
white_lab = np.array([100, 0, 0])  # L=100, A=0, B=0 for pure white in LAB color space

def calculate_delta(c1, c2):
    """Calculate Euclidean distance (delta) between two LAB colors."""
    return np.sqrt(np.sum((c1 - c2) ** 2))

if uploaded_file is not None:
    # Load the image using PIL
    image = Image.open(uploaded_file)
    image = image.convert("RGB")  # Ensure the image is in RGB mode
    image_np = np.array(image)

    # Convert RGB to Lab color space using skimage
    lab_image = color.rgb2lab(image_np)

    # Initialize an empty mask for white spots based on delta threshold
    delta_threshold = 25  # Set a threshold for white spot detection based on delta value (adjustable)

    # Create a binary mask based on delta calculation
    binary_mask = np.zeros(lab_image.shape[:2], dtype=bool)  # Initialize a mask of the same size as the image

    delta_values = []  # List to store delta values for each detected white spot

    for i in range(lab_image.shape[0]):  # Iterate over rows
        for j in range(lab_image.shape[1]):  # Iterate over columns
            # Calculate the delta between each pixel and white color (pure white)
            delta = calculate_delta(lab_image[i, j], white_lab)
            
            # If the delta is less than the threshold, mark it as a white spot
            if delta < delta_threshold:
                binary_mask[i, j] = True
                delta_values.append(delta)

    # Convert the binary mask to binary image (0 and 255)
    binary_image = (binary_mask * 255).astype(np.uint8)

    # Calculate percentage of white spots
    total_pixels = image_np.shape[0] * image_np.shape[1]
    white_pixel_count = np.sum(binary_mask)
    white_percentage = (white_pixel_count / total_pixels) * 100

    # Calculate average delta of white spots
    if delta_values:
        average_delta = np.mean(delta_values)
    else:
        average_delta = 0.0

    # Overlay white spots on the original image (mark in red)
    annotated_image = image_np.copy()
    annotated_image[binary_mask] = [255, 0, 0]  # Mark white spots with red color

    # Display the annotated image with reduced size
    st.image(annotated_image, caption="Detected White Spots (Marked in Red)", use_container_width=True)

    # Show binary image only when button is clicked
    show_binary_image = st.button("Show Binary Image")

    if show_binary_image:
        # Display the binary image with reduced size
        st.image(binary_image, caption="Binary Image (White Spots)", use_container_width=True, channels="GRAY")

    # Display percentage of white spots clearly
    st.subheader(f"White Spot Percentage: {white_percentage:.2f}%")

    # Display the average delta value
    st.subheader(f"Average Delta of White Spots: {average_delta:.2f}")

    # Save the binary and annotated images when the button is clicked
    with st.expander("Save Images"):
        if st.button("Save Images"):
            # Convert to PIL Image for saving
            binary_image_pil = Image.fromarray(binary_image)
            annotated_image_pil = Image.fromarray(annotated_image)

            # Save the images
            binary_image_pil.save("binary_image.png")
            annotated_image_pil.save("annotated_image.png")

            st.success("Images saved successfully!")
            st.write("You can download them from the following links:")

            # Provide download buttons for saved images
            st.download_button("Download Binary Image", data=open("binary_image.png", "rb"), file_name="binary_image.png", mime="image/png")
            st.download_button("Download Annotated Image", data=open("annotated_image.png", "rb"), file_name="annotated_image.png", mime="image/png")

# Footer
st.markdown("<hr><p style='text-align: center;'>Developed by Prabhanjan</p>", unsafe_allow_html=True)
