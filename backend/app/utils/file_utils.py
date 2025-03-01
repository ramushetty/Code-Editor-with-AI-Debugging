import os
from pathlib import Path
from app.core.config import settings

def save_code_file(filename: str, content: str, user_id: int):
    # Create user-specific directory if it doesn't exist
    user_dir = Path(settings.FILE_STORAGE_DIR) / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)

    # Save the file
    file_path = user_dir / filename
    with open(file_path, "w") as file:
        file.write(content)

    return file_path

def read_code_file(filename: str, user_id: int):
    file_path = Path(settings.FILE_STORAGE_DIR) / str(user_id) / filename
    if not file_path.exists():
        raise FileNotFoundError("File not found")
    with open(file_path, "r") as file:
        return file.read()

def delete_code_file(filename: str, user_id: int):
    file_path = Path(settings.FILE_STORAGE_DIR) / str(user_id) / filename
    if not file_path.exists():
        raise FileNotFoundError("File not found")
    os.remove(file_path)