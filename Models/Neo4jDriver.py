import json
import sys
from neo4j import GraphDatabase


class Neo4jDriver:
    driver = None
    data_json = {}

    def __init__(
            self,
            json_file_path: str = ""
    ):
        if json_file_path != "":
            with open(json_file_path) as f:
                self.data_json = json.load(f)
                self.URI = self.data_json["NEO4J_URI"]
                self.user = self.data_json["NEO4J_USERNAME"]
                self.pwd = self.data_json["NEO4J_PASSWORD"]

        if self.URI and self.user and self.pwd:

            with GraphDatabase.driver(self.URI, auth=tuple([self.user, self.pwd])) as self.driver:
                try:
                    self.driver.verify_connectivity()
                    print(f"Connected to Database URI : {self.URI}\n")
                except Exception as e:
                    print(f"Failed to connect to {self.URI} due to {e}\n")
                    sys.exit(1)
