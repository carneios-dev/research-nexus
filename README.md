# Research Nexus

## Purpose

Research Nexus is designed to facilitate exploration and usage of the Academic World dataset. The application targets researchers, academic professionals, and university administrators, allowing them to analyze academic publications, faculty information, and related data. The primary objectives are to provide insights into research trends, faculty expertise, and institutional collaborations.

## Demo

[Link to Video Demo](https://mediaspace.illinois.edu/media/t/1_fhdjqy7v)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/CS411DSO-SU24/ScottSwanson.git
    cd ScottSwanson
    ```

1. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows: venv\Scripts\activate
    ```

1. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

1. Create a `.env` file in the root directory of your project and add your database connection details:

    ```text
    MYSQL_HOST=localhost
    MYSQL_USER=myuser
    MYSQL_PASSWORD=mypassword
    MYSQL_DATABASE=mydatabase
    ```

    Make sure to replace `myuser`, `mypassword`, and `mydatabase` with your actual MySQL credentials.

1. Run the application:

    ```bash
    python app.py
    ```

## Usage

To use the Research Nexus:

1. Start the application by following the installation steps.
2. Open a web browser and navigate to `http://127.0.0.1:61443`.
3. Use the dashboard to explore various academic metrics, including faculty details, publication statistics, and keyword analysis.

## Design

The application is designed using the Dash framework. The overall architecture consists of:

- **Frontend:** A web-based dashboard built with Dash for interactive data visualization.
- **Backend:** Data is stored in three databases - MySQL, MongoDB, and Neo4j.
- **Components:**
  - `app.py`: Initializes and runs the Dash application.
  - `utils/`: Contains database utility functions for MySQL, MongoDB, and Neo4j.
  - `assets/`: Contains the stylesheet and icon for the application.
  - `.gitignore`: Specifies what files and directories to ignore when committing to the remote repository.
  - `requirements.txt`: Specifies the dependencies to install when installing a new virtual Python environment, i.e., `venv`.
  - `.env`: Environment variables for Python to read database credentials, connection information, and other configuration data from.
- **Widgets:**
  - MySQL
    - Faculty Research Output Summary
      - **Purpose**: Provide an overview of the research output of faculty members in terms of the number of publications and citation counts.
      - **Input**: Allow users to select a faculty member from a dropdown list.
      - **Output**: Display the number of publications and the total citation count for the selected faculty member.
      - **Queries**: This widget performs `SELECT` queries to aggregate publication counts and citation counts from the relevant tables in the MySQL database.
      - **Usage**: Users can quickly get an overview of the research productivity of any faculty member, helping them identify prolific researchers or potential collaborators.
    - University Research Trends
      - **Purpose**: Visualize the research trends within a specific university over time.
      - **Input**: Allow users to select a university from a dropdown list.
      - **Output**: Generate a line graph showing the number of publications per year by the selected university.
      - **Queries**: This widget performs `SELECT` queries to count publications per year, grouped by university.
      - **Usage**: Users can analyze how research output in different universities has evolved over time, which can be useful for academic planning and identifying emerging research areas.
  - MongoDB
    - Faculty Research Interests Visualization
      - **Purpose**: Provide a detailed visualization of a faculty member's research interests based on their associated keywords.
      - **Input**: Allow users to select a faculty member from a dropdown list.
      - **Output**: Display a word cloud of the keywords associated with the selected faculty member, highlighting the scores to indicate the prominence of each research interest.
      - **Queries**: This widget would query the `faculty` collection to retrieve the keywords and their scores for the selected faculty member.
      - **Usage**: Users can quickly understand the main research areas and expertise of a faculty member, which is useful for identifying experts in specific fields or potential collaborators.
    - Publication Impact Analysis
      - **Purpose**: Analyze and display the impact of publications by a faculty member based on citation counts.
      - **Input**: Allow users to select either a specific faculty member.
      - **Output**: Display a table or chart showing the titles of the publications along with their citation counts, sorted by the number of citations.
      - **Queries**: This widget would first query the `faculty` collection to get the list of publication IDs for the selected faculty member, and then query the `publications` collection to retrieve the titles and citation counts for these publications.
      - **Usage**: Users can identify highly cited papers and gauge the impact of the research conducted by a faculty member, which is useful for performance reviews and academic assessments.
  - Neo4j
    - Research Collaboration Network
      - **Purpose**: Visualize the collaboration network between faculty members based on their co-authorship of publications.
      - **Input**: Allow users to select a faculty member.
      - **Output**: Display a graph showing the selected faculty member and their co-authors, with edges representing the co-authorship relationships.
      - **Queries**: This widget would query the `PUBLISH` relationships to identify connections between faculty members who have co-authored publications.
      - **Usage**: Users can see the collaboration network of a faculty member, helping them understand research partnerships and potential collaborators within the institution.
    - Keyword-Based Research Analysis
      - **Purpose**: Analyze and visualize the research focus areas of the most prolific faculty members based on the 50 most popular keywords associated with their publications.
      - **Input**: Allow users to select a keyword from a list of the top 50 most popular keywords.
      - **Output**: Display a pie graph of the top 10 faculty members who have published work related to the selected keyword, along with the proportionof publications related to the selected keyword (as a percentage).
      - **Queries**: This widget would query the `LABEL_BY` relationships to find publications labeled with the selected keyword and then find the faculty members associated with those publications.
      - **Usage**: Users can identify faculty members who are active in the most popular research areas, aiding in discovering experts and potential collaborators for interdisciplinary research.

## Implementation

- Frontend
  - [Dash](https://dash.plotly.com/): Used for most of the UI and visualization development.
  - [wordcloud](https://pypi.org/project/wordcloud/): Used to create the word cloud for one of the widgets.
  - [networkx](https://networkx.org/): Used to create the custom scatter plot graph to describe relationships between authors and co-authors in one of the widgets.
- Backend
  - [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/): The database connector between Python and MySQL.
  - [pymongo](https://pymongo.readthedocs.io/en/stable/): The database connector between Python and MongoDB.
  - [neo4j](https://pypi.org/project/neo4j/): The database connector between Python and Neo4j.

## Database Techniques

The application employs various database techniques:

- Views
  - `valid_faculty_view`
    - This is the view we use in our stored procedures to ensure we select from non-null and empty faculty members to populate the dropdown in the UI.
  - `valid_university_view`
    - This is the view we use in our stored procedures to ensure we select from non-null and empty universities to populate the dropdown in the UI.
- Stored Procedures
  - `get_faculty`
    - This is the query to retrieve a list of the faculty members with valid names for the dropdown box.
  - `get_faculty_pubs_cites`
    - This is the query that takes in a faculty member's name as input, and retrieves that faculty member's publication and citation counts.
  - `get_universities`
    - This is the query to retrieve a list of valid universities for the dropdown box.
  - `get_university_pubs_per_year`
    - This is the query that takes in a university name as input, and retrieves the research numbers by faculty members per year over time.
- Indexing
  - `idx_faculty_name`
    - This is on the `name` column in the `faculty` table.
  - `idx_university_name`
    - This is on the `name` column in the `university` table.
  - `idx_publication_id_year`
    - This is on the `id` and `year` columns in the `publication` table.
  - These indexes improve the performance of the MySQL stored procedures.
    - Not including the primary and foreign key indexes created.

## Contributions

- **Scott Swanson**: Developed the entire solution. Spent approximately 40 hours on these tasks.
