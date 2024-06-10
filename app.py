import streamlit as st
import re
import os
import shutil
import json
from streamlit_option_menu import option_menu
from primarydata import process_url
from viewdatabase import view_database
from mergedData import merge_data
from download import manage_downloads, clean_recycle_bin

# Function to validate YouTube playlist URL
def is_valid_youtube_playlist_url(url):
    playlist_pattern = re.compile(r'^https:\/\/www\.youtube\.com\/playlist\?list=[A-Za-z0-9_-]+$')
    return bool(playlist_pattern.match(url))

# Streamlit App
def main():
    # Apply some CSS for custom styling
    st.markdown("""
        <style>
        .sidebar .sidebar-content {
            background-color: #f0f2f6;
        }
        .sidebar .sidebar-content .element-container {
            padding: 0.5rem;
        }
        .reportview-container .markdown-text-container {
            text-align: center;
        }
        .reportview-container .element-container .stButton button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            transition-duration: 0.4s;
            cursor: pointer;
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar Navigation
    with st.sidebar:
        choice = option_menu("Navigation", ["Home", "View Database", "Merge Data", "Download Database"],
                             icons=["house", "table", "upload", "download"],
                             menu_icon="cast", default_index=0)

    if choice == "Home":
        st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Welcome to YouTube Playlist Validator</h1>", unsafe_allow_html=True)
        st.write("""
        **Note:** Please ensure the URL is a public YouTube playlist.
        """)

        # URL input
        url = st.text_input("Enter YouTube Playlist URL")

        if url:
            if is_valid_youtube_playlist_url(url):
                st.success("The URL is a valid YouTube playlist URL!")
                if st.button("Start Extracting"):
                    clean_recycle_bin()
                    process_url(url)
                    st.info(f"Your URL is: {url}. Metadata is being processed.")
            else:
                st.error("Invalid URL. Please enter a valid YouTube playlist URL.")

    elif choice == "View Database":
        view_database()

    elif choice == "Merge Data":
        merge_data()

    elif choice == "Download Database":
        manage_downloads()

if __name__ == "__main__":
    main()
