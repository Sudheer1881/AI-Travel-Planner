import streamlit as st
import google.generativeai as genai
import wikipediaapi
import time
import base64

# Set Streamlit page configuration
st.set_page_config(page_title="AI Travel Planner", layout="wide")

# Set up Gemini API
GOOGLE_API_KEY = "AIzaSyAKe_6ORpIx0jypFs-UrxbRfRn5JyL5EXM"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Set up Wikipedia API
wiki_wiki = wikipediaapi.Wikipedia(language="en", user_agent="AI_Travel_Planner/1.0")

def get_wikipedia_summary(destination):
    """Fetch a short summary about the destination from Wikipedia."""
    page = wiki_wiki.page(destination)
    return page.summary[:500] if page.exists() else "No Wikipedia information available."

def get_ai_travel_plan(start_location, destination, days, budget, purpose, travel_style, preferences):
    """Generate a travel itinerary using Gemini AI."""
    prompt = f"""
    Create a {days}-day travel itinerary from {start_location} to {destination}.
    Budget: {budget} INR
    Purpose: {purpose}
    Travel Style: {travel_style}
    Additional Preferences: {preferences}
    Include travel options, attractions, food recommendations, and travel tips.
    """
    response = model.generate_content(prompt)
    return response.text if response else "Could not generate itinerary."

# Function to encode image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Set paths for images
bg_image_path = "C:/Users/HP/OneDrive/Desktop/Ai_Travel_Planner/Gemini_Generated_Image_uf0g94uf0g94uf0g.jpg"
sidebar_image_path = "C:/Users/HP/OneDrive/Desktop/Ai_Travel_Planner/Gemini_Generated_Image_8sbuoz8sbuoz8sbu.jpg"

# Convert the background image to base64
bg_image_base64 = get_base64_image(bg_image_path)

# Apply CSS for background and text styling
st.markdown(
    f"""
    <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{bg_image_base64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .subheader {{
            color: white;
            background-color: #FFB6C1; /* Light Pink */
            font-size: 24px;
            font-weight: bold;
            padding: 5px;
            border-radius: 5px;
        }}
        .ai-generated-text {{
            background-color: #FFB6C1; /* Light Pink */
            padding: 10px;
            border-radius: 10px;
            font-size: 18px;
            color: black;
        }}
        .stMarkdown, .stTextInput, .stNumberInput, .stSelectbox, .stTextArea {{
            font-size: 20px;
            color: white;
        }}
        .stButton>button {{
            font-size: 20px;
            background-color: #FFB6C1 !important; /* Light Pink */
            color: white !important;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for user inputs
with st.sidebar:
    st.image(sidebar_image_path, use_column_width=True)
    st.title("Travel Details 🌍")

    start_location = st.text_input("Enter your starting location:")
    destination = st.text_input("Enter your destination:")
    days = st.number_input("Duration (days):", min_value=1, value=5)
    budget = st.number_input("Enter your budget (in INR):", min_value=5000, step=1000)
    purpose = st.selectbox("Purpose of travel:", ["Friendly Trip", "Family Trip", "Business Trip", "Adventure Trip", "Cultural Exploration Trip"])
    travel_style = st.selectbox("Preferred travel style:", ["Famous Places", "Offbeat Locations", "Mixed"])
    preferences = st.text_area("Any specific preferences or requirements?", "", height=100)

# Main content
st.markdown('<h1 class="title">AI Travel Planner ✈️</h1>', unsafe_allow_html=True)

if st.button("Generate Itinerary ✨"):
    if start_location and destination:
        with st.spinner("Generating your personalized itinerary... 🚀"):
            time.sleep(5)  # Simulating loading time

        st.markdown('<h2 class="subheader">📍 About Destination</h2>', unsafe_allow_html=True)
        st.write(get_wikipedia_summary(destination))

        st.markdown('<h2 class="subheader">📅 Your Personalized Itinerary</h2>', unsafe_allow_html=True)
        with st.spinner("Finalizing your itinerary... 🎉 Meanwhile, pack your bags!"):
            time.sleep(10)  # Simulating loading time

        itinerary = get_ai_travel_plan(start_location, destination, days, budget, purpose, travel_style, preferences)
        st.markdown(f'<div class="ai-generated-text">{itinerary}</div>', unsafe_allow_html=True)
    else:
        st.warning("Please enter both starting location and destination.")
