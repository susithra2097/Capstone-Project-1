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

-   **API_connect:**

    -   Establishes connection with the YouTube Data API using the
        provided API key.

-   **channel_info:**

    -   Retrieves information about a specific YouTube channel,
        including basic details and related playlists.

-   **get_videos_id:**

    -   Retrieves the video IDs from the uploads playlist of a given
        channel.

-   **parse_duration:**

    -   Parses the duration string of a video into total seconds.

-   **get_video_info:**

    -   Retrieves detailed information about each video, including
        metadata and statistics.

-   **get_comment_info:**

    -   Retrieves comments for each video using the video IDs.

-   **get_playlist_details:**

    -   Retrieves details of all playlists associated with a given
        channel.

-   **sql_create_tables:**

    -   Creates database tables for storing channel data, video data,
        and comment data.

-   **channel_data_upload:**

    -   Uploads channel data to the MySQL database.

-   **video_data_upload:**

    -   Uploads video data to the MySQL database.

-   **comment_data_upload:**

    -   Uploads comment data to the MySQL database.

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
