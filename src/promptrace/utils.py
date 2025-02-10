import os


def sanitize_path(value: str) -> str:  
    if any(char in value for char in '<>"|?*'):
        raise ValueError('Invalid characters in file path')

    if not value:
        raise ValueError('prompt_template cannot be empty')
    
    value = os.path.normpath(
                    value.replace("\t", "\\t")
                )
    value = os.path.normpath(value)

    return value