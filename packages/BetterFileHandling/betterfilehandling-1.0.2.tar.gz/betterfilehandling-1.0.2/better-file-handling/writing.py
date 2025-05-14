def write_text(file:str, text:str,clear:bool=False):
    try:
        keyword = ''
        if clear:
            keyword = 'w'
        else:
            keyword = 'a'
        with open(file, keyword, encoding='utf-8') as towrite:
            towrite.write(text)
    except FileNotFoundError:
        raise FileNotFoundError(f'No file found with the name - "{file}"')
    except Exception as e:
        raise RuntimeError(f"An error occured while writing to the file - '{file}' : {str(e)}")

def write_lines(file:str, lines:list, clear:bool=False):
    try:
        mode = ''
        if clear:
            mode = 'w'
        else:
            mode = 'a'
        with open(file, mode, encoding='utf-8') as towrite:
            for line in lines:
                towrite.write(f'{str(line)}\n')
    except FileNotFoundError:
        raise FileNotFoundError(f'No file found with the name - "{file}"')
    except Exception as e:
        raise RuntimeError(f"An error occured while writing to the file - '{file}' : {str(e)}")

def write_json(file: str, data: dict):
    try:
        import json
        with open(file, 'w', encoding='utf-8') as towrite:
            json.dump(data, towrite, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        raise FileNotFoundError(f'No file found with the name - "{file}"')
    except TypeError as e:
        raise TypeError(f"Provided data is not serializable to JSON: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while writing to the file - '{file}': {str(e)}")