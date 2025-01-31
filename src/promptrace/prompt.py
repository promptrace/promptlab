import re
from dataclasses import dataclass
from pathlib import Path
import os

@dataclass
class Prompt:
    prompt_template: str
    system_prompt: str = None
    user_prompt: str = None

    def __post_init__(self):
        try:
            prompt_template = self.prompt_template.replace("\t", "\\t")
            with open((prompt_template), 'r', encoding='utf-8') as file:
                prompt_content = file.read()

            pattern = r'<<system>>\s*(.*?)\s*<<user>>\s*(.*?)\s*(?=<<|$)'    
            matches = re.findall(pattern, prompt_content, re.DOTALL)
            
            if not matches:
                raise ValueError("No valid prompt format found in template")
                
            self.system_prompt = matches[0][0].strip()
            self.user_prompt = matches[0][1].strip()
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt template file not found: {self.prompt_template}")
        except Exception as e:
            raise ValueError(f"Error parsing prompt template: {str(e)}")

    def prepare_prompts(self, item):
        system_prompt = self.system_prompt
        user_prompt = self.user_prompt
        for item_part in item:
            placeholder = f'<{item_part["title"]}>'
            replacement = f'<{item_part["value"]}>'
            system_prompt = system_prompt.replace(placeholder, replacement)
            user_prompt = user_prompt.replace(placeholder, replacement)
        return system_prompt, user_prompt
    
    def get_prompts(self) -> tuple[str, str]:
        return self.system_prompt, self.user_prompt