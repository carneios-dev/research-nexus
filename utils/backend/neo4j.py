from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Returns a Tuple containing a Neo4j driver and the database name.
# NOTE: You could argue that it'd be more efficient to create the driver once and
#       reuse it across multiple functions. However, since the user is the one indirectly
#       opening the connection, it's probably more secure to close it after each use.
#       There doesn't seem to be any performance issues with this approach either.
def get_neo4j_connection():
    uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    user = os.getenv('NEO4J_USER', 'neo4j')
    password = os.getenv('NEO4J_PASSWORD')
    return (GraphDatabase.driver(uri, auth=(user, password)), os.getenv('NEO4J_DATABASE', 'academicworld'))

def neo4j_get_faculty():
    QUERY = """
        MATCH (f:FACULTY)
        WHERE f.`name` IS NOT NULL AND TRIM(f.`name`) <> ''
        RETURN f.`name` AS faculty_name
        ORDER BY f.`name`
    """
    (driver, database) = get_neo4j_connection()

    with driver.session(database=database) as session:
        result = session.run(QUERY)
        return [{'label': record['faculty_name'], 'value': record['faculty_name']} for record in result]

def neo4j_get_collaboration_network(faculty_name):
    QUERY = """
        MATCH (f:FACULTY {name: $name})-[:PUBLISH]->(p:PUBLICATION)<-[:PUBLISH]-(co:FACULTY)
        RETURN f.name AS faculty, co.name AS coauthor, COUNT(p) AS collaborations
    """
    (driver, database) = get_neo4j_connection()

    with driver.session(database=database) as session:
        result = session.run(QUERY, name=faculty_name)
        return [
            {"faculty": record["faculty"], "coauthor": record["coauthor"], "collaborations": record["collaborations"]}
            for record in result
        ]

def neo4j_get_popular_keywords():
    QUERY = """
        MATCH (k:KEYWORD)<-[:LABEL_BY]-(p:PUBLICATION)
        WHERE k.`name` IS NOT NULL AND TRIM(k.`name`) <> ''
        WITH k.`name` AS keyword_name, COUNT(p) AS frequency
        ORDER BY frequency DESC
        LIMIT 50
        RETURN keyword_name, frequency
        ORDER BY keyword_name ASC
    """
    (driver, database) = get_neo4j_connection()

    with driver.session(database=database) as session:
        result = session.run(QUERY)
        return [{'label': record['keyword_name'], 'value': record['keyword_name']} for record in result]

def neo4j_get_faculty_keyword_analysis(keyword):
    QUERY = """
        MATCH (k:KEYWORD {name: $keyword})<-[:LABEL_BY]-(p:PUBLICATION)<-[:PUBLISH]-(f:FACULTY)
        RETURN f.name AS faculty_name, COUNT(p) AS publication_count
        ORDER BY publication_count DESC
        LIMIT 10
    """
    (driver, database) = get_neo4j_connection()

    with driver.session(database=database) as session:
        result = session.run(QUERY, keyword=keyword)
        return [
            {"faculty_name": record["faculty_name"], "publication_count": record["publication_count"]}
            for record in result
        ]
