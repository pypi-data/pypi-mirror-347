def read_text(file:str, limit:int=0):
    try:
        with open(file, 'r', encoding='utf-8') as toRead:
            if limit == 0:
                return toRead.read()
            else:
                return toRead.read(limit)
    except FileNotFoundError:
        raise FileNotFoundError(f"No File Found with the name: '{file}'")
    except Exception as e:
        raise RuntimeError(f'failed to read file: {str(e)}')

def readline(file: str, line: int):
    try:
        with open(file, 'r', encoding='utf-8') as toread:
            for current_line, content in enumerate(toread, start=1):
                if current_line == line:
                    return content
            raise IndexError(f"Line {line} does not exist in the file: '{file}'")
    except FileNotFoundError:
        raise FileNotFoundError(f"No file found with the name: '{file}'")
    except IndexError as e:
        raise e
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the file '{file}': {str(e)}")
    
def read_lines(file:str, start:int=1, end:int=-1):
    try:
        with open(file, 'r', encoding='utf-8') as toread:
            lines = toread.readlines()
            if end == -1:
                return lines[start-1:]
            else:
                return lines[start-1:end]
    except FileNotFoundError:
        raise FileNotFoundError(f"No file found with the name: '{file}'")
    except Exception as e:
        raise RuntimeError(f"Error reading the file-'{file}' : {str(e)}")

def read_all_lines(file:str):
    try:
        with open(file, 'r', encoding='utf-8') as toread:
            return toread.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"No file found with the name: '{file}'")
    except Exception as e:
        raise RuntimeError(f"Error while reading the file - '{file}' : {str(e)}")

def read_until(file: str, keyword: str):
    import string
    try:
        with open(file, 'r', encoding='utf-8') as toread:
            content = toread.read().split()
            data = []
            for word in content:
                clean_word = word.strip(string.punctuation)
                if clean_word == keyword:
                    return ' '.join(data)
                data.append(word)
            raise ValueError(f"Keyword '{keyword}' not found in file: '{file}'")
    except FileNotFoundError:
        raise FileNotFoundError(f"No file found with the name: '{file}'")
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the file '{file}': {str(e)}")