import re
import sqlite3

from promptrace.db.db import get_rows
from promptrace.db.sql_query import SQLQuery


class PromptTemplate:

    def __init__(self, id: str=None, name: str=None, description: str=None, version: int = 0, system_prompt: str=None, user_prompt: str=None):
        
            self.id = id
            self.name = name
            self.description = description
            self.version = version
            self.system_prompt = system_prompt
            self.user_prompt = user_prompt
   
            
    def get(sql_connection: sqlite3.Connection, prompt_template_id: str):

        pts = get_rows(sql_connection, SQLQuery.SELECT_ASSET_QUERY, (prompt_template_id,))
        pt = pts[0]
        prompt_template = PromptTemplate(
            id=prompt_template_id,
            name=pt['asset_name'],
            description=pt['asset_description'],
            version=pt['asset_version'],
        )

        pattern = r'<<system>>\s*(.*?)\s*<<user>>\s*(.*?)\s*(?=<<|$)'    
        matches = re.findall(pattern, pt['asset_binary'], re.DOTALL)
        
        if not matches:
            raise ValueError("No valid prompt format found in template")
            
        prompt_template.system_prompt = matches[0][0].strip()
        prompt_template.user_prompt = matches[0][1].strip()

        system_prompt_varaibles = re.findall(r'<(.*?)>', prompt_template.system_prompt)
        user_prompt_varaibles = re.findall(r'<(.*?)>', prompt_template.user_prompt)
        prompt_template.variables = system_prompt_varaibles + user_prompt_varaibles
        prompt_template.variables = list(set(prompt_template.variables))

    
        return prompt_template
    
    def save_or_update(self, sql_connection: sqlite3.Connection):
        pass

    def prepare_prompts(self, item):
        system_prompt = self.system_prompt
        user_prompt = self.user_prompt

        for variable in self.variables:
            placeholder = f'<{variable}>'
            replacement = f'<{item[variable]}>'

            system_prompt = system_prompt.replace(placeholder, replacement)
            user_prompt = user_prompt.replace(placeholder, replacement)

        return system_prompt, user_prompt