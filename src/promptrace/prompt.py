import re
from dataclasses import dataclass
import sqlite3
from typing import List


@dataclass
class Prompt:
    prompt_template: str
    db_server: str
    system_prompt: str = None
    user_prompt: str = None
    variables: List[str] = None

    SELECT_ASSETS_QUERY = '''SELECT asset_name, asset_binary FROM assets WHERE asset_id = ?'''

    def __post_init__(self):
        try:
            conn = sqlite3.connect(str(self.db_server))
            cursor = conn.cursor()
            
            cursor.execute(self.SELECT_ASSETS_QUERY,  (self.prompt_template,))
            
            prompts = cursor.fetchall()                    
            if prompts:
                for asset_name, asset_binary in prompts:
                    prompt_content = asset_binary
                    
            cursor.close()
            conn.close()

            pattern = r'<<system>>\s*(.*?)\s*<<user>>\s*(.*?)\s*(?=<<|$)'    
            matches = re.findall(pattern, prompt_content, re.DOTALL)
            
            if not matches:
                raise ValueError("No valid prompt format found in template")
                
            self.system_prompt = matches[0][0].strip()
            self.user_prompt = matches[0][1].strip()

            system_prompt_varaibles = re.findall(r'<(.*?)>', self.system_prompt)
            user_prompt_varaibles = re.findall(r'<(.*?)>', self.user_prompt)
            self.variables = system_prompt_varaibles + user_prompt_varaibles
            self.variables = list(set(self.variables))
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt template file not found: {self.prompt_template}")
        except Exception as e:
            raise ValueError(f"Error parsing prompt template: {str(e)}")

    def prepare_prompts(self, item):
        system_prompt = self.system_prompt
        user_prompt = self.user_prompt

        for variable in self.variables:
            placeholder = f'<{variable}>'
            replacement = f'<{item[variable]}>'

            system_prompt = system_prompt.replace(placeholder, replacement)
            user_prompt = user_prompt.replace(placeholder, replacement)

        return system_prompt, user_prompt
    
    def get_prompts(self) -> tuple[str, str]:
        return self.system_prompt, self.user_prompt