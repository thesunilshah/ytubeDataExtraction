import os
import re
import json
import requests
from pytube import Playlist
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from transformers import BertTokenizer, GPT2Tokenizer

# Initialize tokenizers
bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
gpt_tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# Function to validate image format and resize to (256, 256)
def check_image(image_path):
    valid_formats = ["jpeg", "jpg", "png"]
    try:
        img = Image.open(image_path)
        if img.format.lower() not in valid_formats:
            os.remove(image_path)
            return False
        
        img.save(image_path)
        return True
    except Exception as e:
        print(f"An error occurred while processing the image: {str(e)}")
        os.remove(image_path)
        return False

# Function to download and validate thumbnail
def download_thumbnail(video_id, images_folder):
    try:
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        response = requests.get(thumbnail_url)
        if response.status_code == 200:
            thumbnail_path = os.path.join(images_folder, f'{video_id}.jpg')
            with open(thumbnail_path, 'wb') as img_file:
                img_file.write(response.content)
            if check_image(thumbnail_path):
                return thumbnail_path
            else:
                return None
        else:
            print(f"Failed to download thumbnail for {video_id}.")
            return None
    except Exception as e:
        print(f"An error occurred while downloading the thumbnail: {str(e)}")
        return None



# Function to get video category
def get_video_category(video_url):
    try:
        response = requests.get(video_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            category_element = soup.find('meta', attrs={'itemprop': 'genre'})
            if category_element:
                return category_element.get('content')
        return "Unknown"
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return "Unknown"

# Function to analyze the title
def analyze_title(title):
    title_length = len(title)
    word_count = len(title.split())
    num_tokens_bert = len(bert_tokenizer.tokenize(title))
    num_tokens_gpt = len(gpt_tokenizer.tokenize(title))
    return {
        "title": title,
        "title_length": title_length,
        "word_count": word_count,
        "num_tokens_bert": num_tokens_bert,
        "num_tokens_gpt": num_tokens_gpt
    }

# Function to extract thumbnail details
def get_thumbnail_details(image_path):
    try:
        img = Image.open(image_path)
        width, height = img.size
        aspect_ratio = f"{width}:{height}"
        
        
          
        return {
            "path": image_path,
            "width": width,
            "height": height,
            "aspect_ratio": aspect_ratio,
            
        }
    except Exception as e:
        print(f"An error occurred while getting thumbnail details: {str(e)}")
        return {}



# Function to process URL and save metadata
def process_url(url):
    playlist = Playlist(url)
    metadata = []
    unique_id = 1
    images_folder = "database/images"
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    for video in playlist.videos:
        video_title = video.title
        video_url = video.watch_url
        video_views = video.views
        video_id = video.video_id
        thumbnail_path = download_thumbnail(video_id, images_folder)
        unique_id = video_id
        
        if thumbnail_path:
            category = get_video_category(video_url)
            title_analysis = analyze_title(video_title)
            thumbnail_details = get_thumbnail_details(thumbnail_path)

            # Append video metadata
            metadata.append({
                "unique_id": unique_id,
                "category": category,
                "thumbnail_details": thumbnail_details,
                "video_views": video_views,
                "title_analysis": title_analysis
            })
            

    # Save metadata to JSON file
    with open("database/metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)

    print(f"Processed {len(metadata)} videos. Metadata saved to metadata.json")
