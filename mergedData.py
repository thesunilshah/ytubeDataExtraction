import os
import json
import shutil
import streamlit as st

def load_metadata(json_file="database/metadata.json"):
    with open(json_file, "r") as f:
        metadata = json.load(f)
    return metadata

def save_metadata(metadata, json_file="database/metadata.json"):
    with open(json_file, "w") as f:
        json.dump(metadata, f, indent=4)

def merge_metadata(new_metadata, existing_metadata):
    existing_ids = {item["unique_id"] for item in existing_metadata}
    merged_metadata = existing_metadata + [item for item in new_metadata if item["unique_id"] not in existing_ids]
    return merged_metadata

def merge_images(source_folder, dest_folder="database/images"):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    for filename in os.listdir(source_folder):
        source_path = os.path.join(source_folder, filename)
        dest_path = os.path.join(dest_folder, filename)
        shutil.copy(source_path, dest_path)  # Overwrite existing images

def merge_database(uploaded_zip_path):
    with st.spinner("Merging database..."):
        # Unzip the uploaded file into the upload_database folder
        zip_folder = "upload_database"
        shutil.unpack_archive(uploaded_zip_path, zip_folder)

        # Ensure the expected structure
        metadata_file = os.path.join(zip_folder, "metadata.json")
        images_folder = os.path.join(zip_folder, "images")

        if not os.path.exists(metadata_file) or not os.path.exists(images_folder):
            st.error("The uploaded zip file must contain 'metadata.json' and an 'images' folder.")
            shutil.rmtree(zip_folder)  # Clean up
            return

        # Merge metadata
        new_metadata = load_metadata(metadata_file)
        existing_metadata = load_metadata()
        merged_metadata = merge_metadata(new_metadata, existing_metadata)
        save_metadata(merged_metadata)

        # Merge images
        merge_images(images_folder)

        # Clean up the uploaded files
        shutil.rmtree(zip_folder)

        st.success("Database merged successfully!")

def merge_data():
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Merge Database</h1>", unsafe_allow_html=True)
    st.write("Upload a zip file containing the new database (metadata.json and images folder) to merge it with the existing database.")

    uploaded_file = st.file_uploader("Choose a zip file", type="zip")

    if uploaded_file is not None:
        upload_folder = "upload_database"
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        uploaded_zip_path = os.path.join(upload_folder, "uploaded_database.zip")
        
        # Save the uploaded zip file in the upload_database folder
        with open(uploaded_zip_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Start the merging process
        merge_database(uploaded_zip_path)

# Uncomment below lines if running outside of Streamlit
# if __name__ == "__main__":
#     merge_data()
