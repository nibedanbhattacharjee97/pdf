import streamlit as st
import PyPDF2
import requests

# Function to process the PDF into a list of shortcuts
def extract_shortcuts_from_pdf(file_path):
    shortcuts = []
    try:
        with open(file_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                text = page.extract_text()
                lines = text.split("\n")
                for line in lines:
                    if "Displays" in line or "Toggles" in line or "Moves" in line:
                        parts = line.split(maxsplit=1)
                        if len(parts) == 2:
                            shortcut, description = parts
                            shortcuts.append((shortcut.strip(), description.strip()))
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return shortcuts

# Function to fetch a related YouTube video link
def get_youtube_video(query):
    try:
        api_key = "YOUR_YOUTUBE_API_KEY"  # Replace with your YouTube Data API key
        search_url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": query,
            "key": api_key,
            "type": "video",
            "maxResults": 1,
        }
        response = requests.get(search_url, params=params)
        if response.status_code == 200:
            video_info = response.json()
            if video_info["items"]:
                video_id = video_info["items"][0]["id"]["videoId"]
                return f"https://www.youtube.com/watch?v={video_id}"
    except Exception as e:
        st.error(f"Error fetching YouTube video: {e}")
    return None

# Load the Excel shortcuts from the uploaded PDF
pdf_path = "Excel_shortcuts_cheat_sheet.pdf"
shortcuts = extract_shortcuts_from_pdf(pdf_path)

# Streamlit app
st.title("Excel Shortcut Assistant")
st.write("Ask any Excel shortcut question, and I'll help you!")

# Input for the user's query
query = st.text_input("Enter your question (e.g., 'Moves to the previous')", "")

if query:
    query_lower = query.lower()
    results = []

    # Search for the user's query across all shortcuts
    for shortcut, description in shortcuts:
        if query_lower in description.lower() or any(keyword in description.lower() for keyword in query_lower.split()):
            results.append((shortcut, description))
    
    # Display results
    if results:
        st.write(f"Found {len(results)} matching shortcuts:")
        for shortcut, description in results:
            st.success(
                f"**Shortcut**: `{shortcut}`\n\n**Description**: {description}\n\n"
            )
    else:
        st.error("Sorry, I couldn't find a shortcut for your query.")
