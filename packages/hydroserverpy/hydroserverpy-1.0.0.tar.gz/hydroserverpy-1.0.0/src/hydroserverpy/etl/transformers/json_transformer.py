import logging
import pandas as pd
from typing import Dict, Optional, Any, List
from .base import Transformer
import json
import jmespath


class JSONTransformer(Transformer):
    def __init__(
        self,
        query_string: str,
        datastream_ids: Dict[str, str],
        timestamp_format: Optional[str] = "ISO8601",
    ):
        """
        Initializes the JSONTransformer.

        Parameters:
            query_string (str): JMESPath to the data array containing time series data.
            Since JMESPath can natively rename column names, the assumption is the timestamp column
            is always named 'timestamp' or converted to 'timestamp' in the JMESPath query.
            datastream_ids (dict): Mapping from JSON field names to datastream IDs.
            timestamp_format (str, optional): The format of the timestamp, if it needs special parsing.
        """
        self.query_string = query_string
        self.datastream_ids = datastream_ids
        self.timestamp_format = timestamp_format

    def transform(self, data_file):
        """
        Transforms a JSON file-like object into the standard Pandas dataframe format.
        Since JMESPath can natively rename column names, the assumption is the timestamp column
        is always named 'timestamp' for JSON data or converted to 'timestamp' in the JMESPath query.

        Parameters:
            data_file: File-like object containing JSON data.

        Returns:
            pd.DataFrame: pandas DataFrames in the format pd.Timestamp, datastream_id_1, datastream_id_2, ...
        """
        json_data = json.load(data_file)
        data_points = self.extract_data_points(json_data)
        if not data_points:
            logging.warning("No data points found in the JSON data.")
            return None

        df = pd.DataFrame(data_points)

        return self.standardize_dataframe(
            df,
            self.datastream_ids,
            timestamp_format=self.timestamp_format,
        )

    def extract_data_points(self, json_data: Any) -> Optional[List[dict]]:
        """Extracts data points from the JSON data using the data_path."""
        data_points = jmespath.search(self.query_string, json_data)

        if isinstance(data_points, dict):
            data_points = [data_points]
        return data_points
