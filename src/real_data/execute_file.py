import neo as neo_connection
import sys

neo = neo_connection.Neo4jConnection(
    uri="bolt://100.26.49.182:32994",
    user="neo4j",
    pwd="logs-odds-superstructures")

for line in sys.stdin:
	print(neo.query(line.replace("\n","")))

