from datetime import datetime
import json
import sqlite3
from typing import Union, overload, TypeVar
import uuid
from promptrace.asset.dataset import Dataset
from promptrace.asset.prompt_template import PromptTemplate
from promptrace.db.db import insert_or_update
from promptrace.enums import AssetType
from promptrace.db.sql_query import SQLQuery

T = TypeVar('T', Dataset, PromptTemplate)

class Asset:

    def __init__(self, connection: sqlite3.Connection):
        
        self.connection = connection
    
    @overload
    def create_or_update(self, asset: Dataset) -> Dataset:
        ...
    
    @overload
    def create_or_update(self, asset: PromptTemplate) -> PromptTemplate:
        ...
    
    def create_or_update(self, asset: T) -> T:
        if isinstance(asset, Dataset):
            return self._handle_dataset(asset)
        elif isinstance(asset, PromptTemplate):
            return self._handle_prompt_template(asset)
        else:
            raise TypeError(f"Unsupported asset type: {type(asset)}")
    
    def _handle_dataset(self, dataset: Dataset) -> Dataset:
        timestamp = datetime.now().isoformat()
        if dataset.id is not None:
            pass
        else:        
            dataset.id = str(uuid.uuid4())
            dataset.version = 1

            binary = {
                "file_path": dataset.file_path
            }

        insert_or_update(self.connection, SQLQuery.INSERT_ASSETS_QUERY, (dataset.id, dataset.name, dataset.description, dataset.version, AssetType.PROMPT_TEMPLATE.value, json.dumps(binary), timestamp))

        return dataset
    
    def _handle_prompt_template(self, template: PromptTemplate) -> PromptTemplate:
        timestamp = datetime.now().isoformat()

        if template.id is not None:
            pass
        else:
            template.id = str(uuid.uuid4())
            template.version = 1

            binary = f'''
                <<system>>
                    {template.system_prompt}
                <<user>>
                    {template.user_prompt}
            '''
            
        insert_or_update(self.connection, SQLQuery.INSERT_ASSETS_QUERY, (template.id, template.name, template.description, template.version, AssetType.PROMPT_TEMPLATE.value,  binary, timestamp))

        return template
    
