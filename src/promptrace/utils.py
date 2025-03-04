import json
import os
from typing import Dict, List

class Utils:

    @staticmethod
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

    @staticmethod
    def load_dataset(dataset_path:str) -> List[Dict]:

        dataset_path = Utils.sanitize_path(dataset_path)

        dataset = []
        with open(dataset_path, 'r') as file:
            for line in file:
                dataset.append(json.loads(line.strip()))
        return dataset