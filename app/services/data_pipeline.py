"""Data Pipeline Services that retrieves the data from the MySQL Database"""
import mysql.connector
from typing import List, Dict


class DataPipelineService:
    """
    The Datapipeline Service retrieves the data from a local MySQL database *At the moment*
    Future state: public api

    """
    word_bank: List[Dict]
    api_endpoint: str
    cache: Dict


    # def fetch_words(self) -> List[Dict]:

    # def fetch_by_category
    # def fetch_by_theme