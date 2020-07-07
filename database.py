import sqlite3, logging, traceback


samples_table = """
CREATE TABLE samples (number INT NOT NULL, value INT NOT NULL)
"""
spectrum_table = """
CREATE TABLE spectrum (bucket INT NOT NULL, amplitude INT NOT NULL)
"""


class Database:
    def __init__(self):
        try:
            conn = sqlite3.connect('data.db')
            conn.execute("DROP TABLE samples")
            conn.execute("DROP TABLE spectrum")
            conn.execute(samples_table)
            conn.execute(spectrum_table)
        except Exception as e:
            logging.exception(traceback.format_exc())

    def run(self, pipeline):
        try:
            while not pipeline.should_exit():
                pipeline.consume()
        except Exception as e:
            logging.exception(traceback.format_exc())

