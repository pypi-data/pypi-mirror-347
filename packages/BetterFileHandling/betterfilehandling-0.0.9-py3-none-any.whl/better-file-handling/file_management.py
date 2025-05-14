import os
import shutil
import datetime

def file_exist(file:str) -> bool:
    return os.path.isfile(file)

def get_file_extension(file: str) -> str:
    try:
        if not file_exist(file):
            raise FileNotFoundError(f"File '{file}' not found.")
    
        return os.path.splitext(file)[1]
    except Exception as e:
        raise RuntimeError(f"An Error Occured - {str(e)}")

def get_file_size(file:str) -> int:
    if not file_exist(file):
        raise FileNotFoundError(f"Error : File '{file}' not found!")
    
    return os.path.getsize(file)

def get_file_info(file:str) -> dict:
    if not file_exist(file):
        raise FileNotFoundError(f"Error : File '{file}' not found!")
    
    file_info = {
        "size": get_file_size(file),
        "creation-date": datetime.fromtimestamp(os.path.getctime(file)).strftime("%Y-%m-%d %H:%M:%S"),
        "last-modified-time": datetime.fromtimestamp(os.path.getmtime(file)).strftime("%Y-%m-%d %H:%M:%S")
    }

    return file_info

def delete_file(file:str):
    try:
        if not file_exist(file):
            raise FileNotFoundError(f"Error : File '{file}' not found!")
    
        os.remove(file)
    
    except Exception as e:
        raise RuntimeError(f"An Error Occured - {str(e)}")

def rename_file(file:str, new_name:str):
    try:
        if not file_exist(file):
            raise FileNotFoundError(f"Error : File '{file}' not found!")

        new_file_path = os.path.join(os.path.dirname(file), new_name)
        os.rename(file, new_file_path)
    
    except Exception as e:
        raise RuntimeError(f"An Error Occured - {str(e)}")

def copy_file(source:str, destination:str):
    try:
        if not file_exist(source):
            raise FileNotFoundError(f"Error : File '{source}' not found!")
        
        shutil.copy2(source, destination)
    
    except Exception as e:
        raise RuntimeError(f"An Error Occured - {str(e)}")

def move_file(source:str, destination:str):
    try:
        if not file_exist(source):
            raise FileNotFoundError(f"Error : File '{source}' not found!")

        shutil.move(source, destination)
    
    except Exception as e:
        raise RuntimeError(f"An Error Occured - {str(e)}")

def create_directory(path:str):
    try:
        if os.path.exists(path):
            raise FileExistsError(f"Directory '{path}' already exists.")
        
        os.makedirs(path)
    
    except Exception as e:
        raise RuntimeError(f"An Error Occured - {str(e)}")

def list_files_in_directory(path: str, extension: str = None) -> list:
    try:
        if not os.path.isdir(path):
            raise FileNotFoundError(f"Directory '{path}' not found.")
    
        files = os.listdir(path)
        if extension:
            files = [f for f in files if f.endswith(extension)]
        
        return files
    except Exception as e:
        raise RuntimeError(f"An Error Occured - '{str(e)}'")
