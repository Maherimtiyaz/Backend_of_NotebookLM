# Storage service for handling file operations
# This service abstracts away the details of file storage, allowing us to easily switch between different storage backends (e.g., local filesystem, cloud storage) without affecting the rest of the application.
import os

# function to store file
async def store_file(file, document_id) -> bool:
    try:
        # Create a directory for storing files if it doesn't exist
        os.makedirs("storage", exist_ok=True)
        if "." not in file.filename:
            raise ValueError("Invalid file name")
        
        # Extract the file extension
        extension = file.filename.split(".")[-1]
        file_path = f"storage/{document_id}.{extension}"
        
        # Save the uploaded file to the storage directory
        with open(file_path, "wb") as buffer:
            # Read the file in chunks to handle large files efficiently
            while True:
                chunk = await file.read(1024)  # Read 1KB at a time
                if not chunk:
                    break
                buffer.write(chunk)
        
        return True
    except Exception as e:
        raise Exception(f"Error storing file: {str(e)}")

# function to delete file
async def delete_file(document_id: str) -> bool:
    try:
        for filename in os.listdir("storage"):
            if filename.startswith(document_id):
                file_path = os.path.join("storage", filename)
                os.remove(file_path)
        return True
    except Exception as e:
        raise Exception(f"Error deleting file: {str(e)}")
    except Exception as e:  
        raise Exception(f"Error deleting file: {str(e)}")
    
# function to read file
async def read_file(document_id: str) -> str:
        try:
            for filename in os.listdir("storage"):
                if filename.startswith(document_id):
                    file_path = os.path.join("storage", filename)
                    with open(file_path, "r") as file:
                        return file.read()
            raise FileNotFoundError("File not found")
        except Exception as e:
            raise Exception(f"Error reading file: {str(e)}")
    