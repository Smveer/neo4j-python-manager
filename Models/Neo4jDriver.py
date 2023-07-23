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

    def get_finals(self) -> list:
        finals = []
        q = "MATCH (f:Final) RETURN f;"
        records, summary, keys = self.driver.execute_query(q)

        for item in records:
            element = item.data()["f"]
            finals.append(element)
        return finals

    def get_final_teams(self) -> list:
        final_teams = []
        q = "MATCH (t:Team) RETURN t;"
        records, summary, keys = self.driver.execute_query(q)

        for item in records:
            element = item.data()["t"]
            final_teams.append(element)
        return final_teams

    def get_year_results(
            self,
            year: int
    ) -> list:
        year_results = []
        q = "MATCH (f:Final where f.year=$year)-[r:PLAY_FINAL]-(t:Team) return f, t, r.winner"
        records, summary, keys = self.driver.execute_query(q, year=year)
        for item in records:
            element = item.data()
            year_results.append(element)
        return year_results

    def get_team_results(
            self,
            team: str
    ) -> list:
        team_results = []
        q = "MATCH (t:Team where t.name=$team)-[r:PLAY_FINAL]-(f:Final) return t, f, r.winner"
        records, summary, keys = self.driver.execute_query(q, team=team)
        for item in records:
            element = item.data()
            team_results.append(element)
        return team_results
