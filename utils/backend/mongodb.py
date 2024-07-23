from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def get_mongo_connection():
    client = MongoClient(os.getenv('MONGODB_HOST', 'localhost'), int(os.getenv('MONGODB_PORT', 27017)))
    return client[os.getenv('MONGODB_DATABASE', 'academicworld')]

def mongo_get_faculty():
    try:
        db = get_mongo_connection()
        cursor = db.faculty.find({
            "name": { "$ne": None, "$ne": "" }
        }, { "id": 1, "name": 1, "_id": 0 })
        faculty_options = [{'label': faculty['name'], 'value': str(faculty['id'])} for faculty in cursor]
        return faculty_options
    except Exception as e:
        print(f"An error occurred while attempting to retrieve faculty members: {e}")
        return []

def mongo_get_faculty_keywords(faculty_id):
    try:
        db = get_mongo_connection()
        faculty = db.faculty.find_one(
            { "id": int(faculty_id) },
            { "keywords.name": 1, "keywords.score": 1, "_id": 0 }
        )
        return faculty.get('keywords', [])
    except Exception as e:
        print(f"An error occurred while attempting to retrieve keywords: {e}")
        return []
    
def mongo_get_publications(faculty_id):
    try:
        db = get_mongo_connection()
        faculty = db.faculty.find_one(
            { "id": faculty_id },
            { "publications": 1, "_id": 0 }
        )
        publication_ids = faculty.get('publications', [])
        publications = db.publications.find(
            { "id": { "$in": publication_ids } },
            { "title": 1, "numCitations": 1, "_id": 0 }
        )
        return list(publications)
    except Exception as e:
        print(f"An error occurred while attempting to retrieve publications: {e}")
        return []

