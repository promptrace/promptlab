import os
import sqlite3


class Deployment:
    @staticmethod
    def deploy(experiment_id: str, deployment_dir:str, db_server:str) -> None:

        SELECT_ASSET = '''
            SELECT asset_name, asset_binary FROM assets 
            WHERE asset_id = (SELECT DISTINCT asset_id FROM experiments WHERE experiment_id = ?)
            '''

        UPDATE_EXPERIMENT = '''UPDATE experiments SET is_deployed = 1, deployment_time = CURRENT_TIMESTAMP WHERE experiment_id = ?'''

        connection = sqlite3.connect(db_server)
        try:
            cursor = connection.cursor()
            cursor.execute(SELECT_ASSET, (experiment_id,))
            row = cursor.fetchone()
            
            if row:
                asset_name, asset = row
                asset_path = os.path.join(deployment_dir, asset_name)
                with open(asset_path, 'wb') as file:
                    file.write(asset)

                connection.execute(UPDATE_EXPERIMENT, (experiment_id,))
                connection.commit()
            else:
                raise ValueError(f"No experiment found with ID: {experiment_id}")
                
        finally:
            connection.close()