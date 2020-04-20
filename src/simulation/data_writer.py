import os
import pandas as pd


class ResultWriter:

    @staticmethod
    def write_to_excel(data: pd.DataFrame, filename, file_path="."):
        full_path = os.path.join(file_path, filename)
        data.to_excel(full_path)
