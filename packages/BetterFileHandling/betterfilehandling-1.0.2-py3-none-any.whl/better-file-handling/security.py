import base64

def encode_file(file: str, encoding: str = 'utf-8'):
    """
    Encodes a file with the specified encoding.

    Args:
        file (str): Path to the file to be encoded.
        encoding (str): The encoding to use for the file content. Default is 'utf-8'.

    Raises:
        FileNotFoundError: If the file does not exist.
        RuntimeError: If encoding fails.
    """
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = f.read()
            encoded_data = data.encode(encoding)
        
        with open(file, 'wb') as f1:  # 'wb' = write binary
            f1.write(encoded_data)
    except FileNotFoundError:
        raise FileNotFoundError(f"No file found with the name - '{file}'")
    except UnicodeEncodeError:
        raise ValueError(f"Encoding failed for file '{file}' with encoding '{encoding}'")
    except Exception as e:
        raise RuntimeError(f'An error occurred while encoding the file - "{file}": {str(e)}')

def decode_file(file: str, encoding: str = 'utf-8'):
    """
    Decodes a file with the specified encoding.

    Args:
        file (str): Path to the file to be decoded.
        encoding (str): The encoding to use for the file content. Default is 'utf-8'.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If decoding fails.
        RuntimeError: If the process fails.
    """
    try:
        with open(file, 'rb') as f:  # read as binary
            encoded_data = f.read()
            decoded_data = encoded_data.decode(encoding)
        
        with open(file, 'w', encoding='utf-8') as f1:  # save as plain text
            f1.write(decoded_data)
    except FileNotFoundError:
        raise FileNotFoundError(f"No file found with the name - '{file}'")
    except UnicodeDecodeError:
        raise ValueError(f"Cannot decode file '{file}' with encoding '{encoding}'")
    except Exception as e:
        raise RuntimeError(f'An error occurred while decoding the file - "{file}": {str(e)}')

def encode_file_base64(file_path: str) -> str:
    """
    Encodes a file to Base64.

    Args:
        file_path (str): Path to the file to be encoded.

    Returns:
        str: The base64 encoded string.

    Raises:
        FileNotFoundError: If the file does not exist.
        RuntimeError: If encoding fails.
    """
    try:
        with open(file_path, 'rb') as file:
            encoded_bytes = base64.b64encode(file.read())
            return encoded_bytes.decode('utf-8')
    except FileNotFoundError:
        raise FileNotFoundError(f"No file found at: '{file_path}'")
    except Exception as e:
        raise RuntimeError(f"Failed to encode file: {str(e)}")

def decode_file_base64(encoded_data: str, output_path: str):
    """
    Decodes a Base64 encoded string and writes it to a file.

    Args:
        encoded_data (str): The base64 encoded string.
        output_path (str): Path to save the decoded file.

    Raises:
        RuntimeError: If decoding or writing the file fails.
    """
    try:
        decoded_bytes = base64.b64decode(encoded_data)
        with open(output_path, 'wb') as file:
            file.write(decoded_bytes)
    except Exception as e:
        raise RuntimeError(f"Failed to decode and write file: {str(e)}")