import json
import sqlite3
from typing import Dict, List

from promptrace.db.db import get_rows
from promptrace.db.sql_query import SQLQuery
from promptrace.utils import sanitize_path

class Dataset:
    def __init__(self, id: str=None, name: str=None, description: str=None, version: int = 0, file_path: str=None, ds: List[Dict]=None):

        self.id = id
        self.name = name
        self.description = description
        self.version = version
        self.file_path = file_path
        self.ds = ds

    def get(sql_connection: sqlite3.Connection, ds_id: str):
        pts = get_rows(sql_connection, SQLQuery.SELECT_ASSET_QUERY, (ds_id,))
        pt = pts[0]
        ds = Dataset(
            id=ds_id,
            name=pt['asset_name'],
            description=pt['asset_description'],
            version=pt['asset_version'],
            file_path= json.loads(pt['asset_binary'])['file_path']
        )

        ds.ds = Dataset.load_dataset(ds.file_path)

        return ds
    
    def load_dataset(dataset_path:str) -> List[Dict]:

        dataset_path = sanitize_path(dataset_path)
        dataset = []
        with open(dataset_path, 'r') as file:
            for line in file:
                dataset.append(json.loads(line.strip()))
        return dataset
