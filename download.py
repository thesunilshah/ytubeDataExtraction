import os
import shutil
import streamlit as st

RECYCLE_BIN = "recyclebin"
DATABASE_FOLDER = "database"
METADATA_FILE = "metadata.json"
IMAGE_FOLDER = "images"

# Create recycle bin folder if it doesn't exist
if not os.path.exists(RECYCLE_BIN):
    os.makedirs(RECYCLE_BIN)

# Calculate the size of the database
def get_database_size():
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(DATABASE_FOLDER):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size / (1024 * 1024)  # Convert to MB

# Create a zip file of the database
def create_database_zip():
    shutil.make_archive("database_backup", 'zip', DATABASE_FOLDER)
    return "database_backup.zip"

# Download the database as a zip file
def download_database():
    zip_file = create_database_zip()
    with open(zip_file, "rb") as f:
        st.download_button("Download Database", f, file_name="database_backup.zip")
    os.remove(zip_file) # deleting the zip file after download 

# Move the database to recycle bin
def delete_database():
    if os.path.exists(DATABASE_FOLDER):
        shutil.move(DATABASE_FOLDER, RECYCLE_BIN)
        st.success("Database moved to recycle bin.")
    else:
        st.error("No database found to delete.")

# Restore the database from recycle bin
def restore_database():
    recycle_path = os.path.join(RECYCLE_BIN, DATABASE_FOLDER)
    if os.path.exists(recycle_path):
        shutil.move(recycle_path, ".")
        st.success("Database restored from recycle bin.")
    else:
        st.error("No database found in recycle bin to restore.")

# Check and clean recycle bin when extracting new URL
def clean_recycle_bin():
    recycle_path = os.path.join(RECYCLE_BIN, DATABASE_FOLDER)
    if os.path.exists(recycle_path):
        shutil.rmtree(recycle_path)

def manage_downloads():
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Download Database</h1>", unsafe_allow_html=True)
    db_size = get_database_size()
    st.write(f"Current database size: {db_size:.2f} MB")

    if db_size > 1024:
        st.warning("The database size exceeds the maximum limit for direct download. Please contact support for a custom download.")
    else:
        if st.button("Download Database"):
            download_database()

    if st.button("Delete Database"):
        delete_database()

    if os.path.exists(os.path.join(RECYCLE_BIN, DATABASE_FOLDER)):
        if st.button("Restore Database"):
            restore_database()
