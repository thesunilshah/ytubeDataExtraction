import os
import json
import random
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image

# Function to load metadata
def load_metadata(json_file="database/metadata.json"):
    with open(json_file, "r") as f:
        metadata = json.load(f)
    return metadata

# Function to get a random sample of 12 images and their metadata
def get_random_sample(metadata, sample_size=12):
    return random.sample(metadata, min(sample_size, len(metadata)))

# Function to display images in a grid format using Matplotlib
def display_images(sample):
    fig, axs = plt.subplots(4, 3, figsize=(15, 15))
    axs = axs.flatten()
    for ax, data in zip(axs, sample):
        img = Image.open(data['thumbnail_details']['path'])
        ax.imshow(img)
        ax.set_title(data['title_analysis']['title'], fontsize=10)
        ax.axis('off')
    for ax in axs[len(sample):]:
        ax.axis('off')
    st.pyplot(fig)

# Function to display metadata in a table format
def display_metadata(sample):
    metadata_df = pd.DataFrame([
        {
            "Unique ID": data['unique_id'],
            "Category": data['category'],
            "Views": data['video_views'],
            "Title": data['title_analysis']['title'],
            "Title Length": data['title_analysis']['title_length'],
            "Word Count": data['title_analysis']['word_count'],
            "BERT Tokens": data['title_analysis']['num_tokens_bert'],
            "GPT Tokens": data['title_analysis']['num_tokens_gpt'],
            "Thumbnail Path": data['thumbnail_details']['path'],
            "Thumbnail Width": data['thumbnail_details']['width'],
            "Thumbnail Height": data['thumbnail_details']['height'],
            "Aspect Ratio": data['thumbnail_details']['aspect_ratio'],
         
        }
        for data in sample
    ])
    st.write("Metadata Table:")
    st.dataframe(metadata_df)

# Function to show data and memory usage
def show_data_statistics(metadata):
    df = pd.DataFrame(metadata)
    st.write("### Data and Memory Usage Statistics")
    st.write(f"**Total Data Entries:** {len(metadata)}")
    st.write(f"**Memory Usage:** {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    # Graph: Category Distribution
    st.write("#### Category Distribution")
    category_counts = df['category'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 5))
    category_counts.plot(kind='bar', ax=ax)
    ax.set_xlabel("Category")
    ax.set_ylabel("Count")
    ax.set_title("Category Distribution")
    st.pyplot(fig)

    # Graph: Views Distribution
    st.write("#### Views Distribution")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(df['video_views'], bins=20, edgecolor='black')
    ax.set_xlabel("Views")
    ax.set_ylabel("Frequency")
    ax.set_title("Views Distribution")
    st.pyplot(fig)

    # Graph: Title Length Distribution
    st.write("#### Title Length Distribution")
    title_lengths = df.apply(lambda row: row['title_analysis']['title_length'], axis=1)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(title_lengths, bins=20, edgecolor='black')
    ax.set_xlabel("Title Length")
    ax.set_ylabel("Frequency")
    ax.set_title("Title Length Distribution")
    st.pyplot(fig)

# Main function to handle view database functionality
def view_database():
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>View Database</h1>", unsafe_allow_html=True)

    # Load metadata
    metadata = load_metadata()

    # Display a random sample of 12 images in grid format
    sample = get_random_sample(metadata)
    display_images(sample)

    # Display metadata in table format
    display_metadata(sample)

    # Show data and memory usage
    show_data_statistics(metadata)
