import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def get_mysql_connection():
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE', 'academicworld')
    )

def get_faculty():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('get_faculty')
        result = []
        for result_set in cursor.stored_results():
            result.extend(result_set.fetchall())
        return result
    except mysql.connector.Error as e:
        print(f"An error occurred while attempting to retrieve faculty members: {e}")
    finally:
        if conn.is_connected():
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

def get_faculty_pubs_cites(faculty_name):
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('get_faculty_pubs_cites', [faculty_name])
        result = []
        for result_set in cursor.stored_results():
            result.extend(result_set.fetchall())
        return result
    except mysql.connector.Error as e:
        print(f"An error occurred while attempting to retrieve faculty publication and citation counts: {e}")
    finally:
        if conn.is_connected():
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

def get_universities():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('get_universities')
        result = []
        for result_set in cursor.stored_results():
            result.extend(result_set.fetchall())
        return result
    except mysql.connector.Error as e:
        print(f"An error occurred while attempting to retrieve universities: {e}")
    finally:
        if conn.is_connected():
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

def get_university_pubs_per_year(university_name):
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('get_university_pubs_per_year', [university_name])
        result = []
        for result_set in cursor.stored_results():
            result.extend(result_set.fetchall())
        return result
    except mysql.connector.Error as e:
        print(f"An error occurred while attempting to retrieve university publication counts per year: {e}")
    finally:
        if conn.is_connected():
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
