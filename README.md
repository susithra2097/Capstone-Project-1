# YouTube Data Harvesting and Analysis

**Overview:**

The YouTube Data Harvesting App is a Python application built to
extract, analyze, and visualize data from YouTube channels. It utilizes
the YouTube Data API to gather information such as channel details,
video metadata, and comments, and stores the extracted data into a MySQL
database. The app also provides functionality to perform various
analytical queries on the stored data.

**Requirements:**

-   Python 3.x

-   Streamlit

-   Pandas

-   MySQL Connector

-   SQLAlchemy

-   Google API Client Library

**Features:**

-   **Data Extraction:**

    -   Extracts channel information including name, ID, subscriber
        count, views, description, and uploads playlist ID.

    -   Retrieves video metadata such as title, description, tags,
        published date, views, likes, dislikes, comments, duration,
        thumbnail, definition, and caption status.

    -   Gathers comments for each video, including comment ID, video ID,
        text, author, and publish date.

-   **Database Integration:**

    -   Creates MySQL tables to store channel data, video data, and
        comment data.

    -   Utilizes SQLAlchemy for database connection and management.

-   **Analytics:**

    -   Provides various analytical queries to analyze the stored data.

    -   Queries include top videos by views, likes, comments, most
        active channels, average video duration per channel, etc.

-   **User Interface:**

    -   Built using Streamlit to provide an interactive web-based
        interface.

    -   Users can input channel IDs, initiate data extraction, and
        perform analytical queries from the sidebar menu.

**Functions Overview:**

Functions:
1.	Api_connect():
•	Purpose: Establishes a connection to the YouTube Data API using the developer key.
•	Returns: An instance of the YouTube Data API client.
2.	channel_info(id):
•	Purpose: Retrieves information about a YouTube channel based on its ID.
•	Parameters: id (string) - YouTube channel ID.
•	Returns: A dictionary containing channel details such as name, ID, subscriber count, views, etc.
3.	get_videos_id(id):
•	Purpose: Retrieves video IDs from a YouTube channel's uploads playlist.
•	Parameters: id (string) - YouTube channel ID.
•	Returns: A list of video IDs.
4.	parse_duration(duration_str):
•	Purpose: Parses duration string (e.g., "PT5M30S") and converts it to seconds.
•	Parameters: duration_str (string) - Duration string in ISO 8601 format.
•	Returns: Total duration in seconds.
5.	get_video_info(video_ids):
•	Purpose: Retrieves detailed information about videos using their IDs.
•	Parameters: video_ids (list) - List of YouTube video IDs.
•	Returns: A list of dictionaries containing video details such as title, description, views, likes, dislikes, etc.
6.	get_comment_info(video_ids):
•	Purpose: Retrieves comments for videos using their IDs.
•	Parameters: video_ids (list) - List of YouTube video IDs.
•	Returns: A list of dictionaries containing comment details such as comment ID, video ID, text, author, etc.
7.	get_playlist_details(id):
•	Purpose: Retrieves details of playlists associated with a YouTube channel.
•	Parameters: id (string) - YouTube channel ID.
•	Returns: A list of dictionaries containing playlist details such as ID, title, channel ID, published date, etc.
8.	sql_create_tables():
•	Purpose: Creates database tables if they don't exist.
•	Returns: None.
9.	channel_data_upload(data_channel):
•	Purpose: Uploads channel data to a MySQL database.
•	Parameters: data_channel (DataFrame) - DataFrame containing channel data.
•	Returns: None.
10.	video_data_upload(video_data):
•	Purpose: Uploads video data to a MySQL database.
•	Parameters: video_data (DataFrame) - DataFrame containing video data.
•	Returns: None.

11.	comment_data_upload(comment_data):
•	Purpose: Uploads comment data to a MySQL database.
•	Parameters: comment_data (DataFrame) - DataFrame containing comment data.
•	Returns: None.


**Usage:**

-   Upon launching the application, users are presented with a sidebar
    menu offering options to navigate through the app.

-   Users can input a YouTube channel ID to extract data, which will
    then be uploaded to the MySQL database.

-   Analytical queries can be performed by selecting the corresponding
    option from the sidebar menu.

## 

## **Setup Instructions**

1.  **Install Dependencies**: Ensure that you have installed the
    required Python packages, including Streamlit, pandas, SQLAlchemy,
    and MySQL Connector.

2.  **API Key**: Obtain a YouTube Data API key from the Google Developer
    Console and replace the placeholder in the code with your API key.

3.  **Database Setup**: Set up a MySQL database with the required tables
    for storing channel data, video details, and comments.

4.  **Run the Application**: Execute the provided Python script to start
    the Streamlit web application. Access the application via the
    provided URL in your web browser.

5.  **Extract and Analyze Data**: Enter the YouTube channel ID in the
    application and click the \"Extract And Upload Data\" button to
    retrieve and store channel information. Explore the available
    options to query and analyze the stored data.

## 

## **References**

-   [YouTube Data API
    Documentation](https://developers.google.com/youtube/v3/getting-started)

-   [Streamlit
    Documentation](https://docs.streamlit.io/library/api-reference)

-   [MySQL Documentation](https://dev.mysql.com/doc/)

-   [Pandas Documentation](https://pandas.pydata.org/docs/)
