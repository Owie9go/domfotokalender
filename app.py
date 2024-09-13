import streamlit as st
from PIL import Image
import os
from datetime import date, timedelta

# Directory to save images
IMAGES_DIR = "uploaded_images"

# Ensure the directory exists
if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

# Secret key for authentication
SECRET_KEY = "MayonaiseIsEenInstrument"

# Function to save the uploaded image
def save_image(uploaded_file, save_path):
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

# Get the current week (Monday to Sunday)
def get_current_week():
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())  # Monday of the current week
    end_of_week = start_of_week + timedelta(days=6)          # Sunday of the current week
    return start_of_week, end_of_week

# Function to display images for a given date range
def display_images(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        # Define the image path for the current date
        image_path = os.path.join(IMAGES_DIR, f"{current_date}.png")

        # If the image exists, display it
        if os.path.exists(image_path):
            st.write(f"Image for {current_date}")
            st.image(Image.open(image_path), caption=f"Image for {current_date}")
        else:
            st.write(f"No image found for {current_date}")

        # Move to the next day
        current_date += timedelta(days=1)

# Page selection in the sidebar (default is "View Images")
page = st.sidebar.selectbox("Choose a page", ["View Images", "Upload Image"])

if page == "View Images":
    # Default page: View Images
    st.title("DroneXpress blijf het langst op de DIF, en dit is het bewijs!")
    st.subheader("Iedere dag uploaden wij een foto, van een lege ID ruimte!")

    # Get the current week dates (initial display)
    if "week_offset" not in st.session_state:
        st.session_state.week_offset = 0

    # Calculate the start and end of the current week based on the offset
    start_of_week, end_of_week = get_current_week()
    start_of_week += timedelta(weeks=st.session_state.week_offset)
    end_of_week += timedelta(weeks=st.session_state.week_offset)

    # Display the images for the current week
    st.write(f"Displaying images from **{start_of_week}** to **{end_of_week}**")
    display_images(start_of_week, end_of_week)

    # Navigation buttons for previous and next weeks
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("<< Previous Week"):
            st.session_state.week_offset -= 1

    with col2:
        if st.button("Next Week >>"):
            st.session_state.week_offset += 1

elif page == "Upload Image":
    # Upload Image page
    st.title("Date-based Image Uploader")

    # Prompt the user to enter the secret key
    entered_key = st.text_input("Enter the secret key to upload images:", type="password")

    # Check if the entered key matches the secret key
    if entered_key == SECRET_KEY:
        st.success("Authentication successful! You can upload images now.")

        # Date input (calendar)
        selected_date = st.date_input("Select a date", date.today())

        # Display the selected date
        st.write(f"Selected Date: {selected_date}")

        # File uploader for images
        uploaded_file = st.file_uploader("Upload an image for this date", type=["png", "jpg", "jpeg"])

        # Define the image path based on selected date
        image_path = os.path.join(IMAGES_DIR, f"{selected_date}.png")

        # If the user uploads a file
        if uploaded_file:
            # Save the image
            save_image(uploaded_file, image_path)
            st.success(f"Image for {selected_date} uploaded successfully!")

        # Display the image if it exists for the selected date
        if os.path.exists(image_path):
            st.image(Image.open(image_path), caption=f"Image for {selected_date}")
    else:
        st.error("Invalid key! Please enter the correct key to upload images.")
