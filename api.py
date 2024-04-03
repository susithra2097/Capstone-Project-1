from sqlalchemy import create_engine
import pandas as pd
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
import mysql.connector
from mysql.connector import Error
from streamlit_option_menu import option_menu
import streamlit as st
from datetime import datetime
import re
import plotly.express as px

# API connect Function

def Api_connect():
  api = "AIzaSyDQKvXpGEBeZICpldWWxa6HgeeBugW_Uuk"
  api_service_name = "youtube"
  api_version = "v3"
  

  youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=api)
  
  return youtube
youtube = Api_connect()


# get channel information


def channel_info(id):
  request = youtube.channels().list(
    part="snippet,contentDetails,statistics",
    id=id
  )
  response = request.execute()

  for i in response ["items"]:
    data = dict (channel_name = i["snippet"]["title"] ,
    channel_id = i["id"],
    Subscription_Count = i["statistics"]["subscriberCount"],
    Channel_Views = i["statistics"]["viewCount"],
    Channel_Description = i["snippet"]["description"],
    Playlist_Id = i["contentDetails"]["relatedPlaylists"]["uploads"])

  return (data)



## get playlist Info

def get_videos_id(id):

  video_ids=[]

  response = youtube.channels().list(id=id,part = 'contentDetails').execute()

  playlist_id=response ["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

  next_page_token=None

  while True:
    response1 = youtube.playlistItems().list(
        part ='snippet',
        playlistId=playlist_id,
        maxResults=50,
        pageToken=next_page_token
    ).execute()

    for i in range(len(response1['items'])):
      video_ids.append(response1['items'][i]['snippet']['resourceId']['videoId'])
    next_page_token=response1.get('nextPageToken')

    if next_page_token is None:
      break
  
  #pprint.pprint(video_ids)
  return video_ids
  



def parse_duration(duration_str):
    # Regular expression to extract hours, minutes, and seconds
    pattern = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
    match = pattern.match(duration_str)

    if match:
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        total_seconds = hours * 3600 + minutes * 60 + seconds
        return total_seconds
    else:
        return None

def get_video_info(video_ids):
    video_data = []
    for video_id in video_ids:
        try:
            request = youtube.videos().list(
                part="snippet,ContentDetails,statistics",
                id=video_id
            )
            response = request.execute()

            for item in response["items"]:
                # Convert datetime format
                published_date = datetime.strptime(item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')

                # Parse duration
                duration_seconds = parse_duration(item['contentDetails']['duration'])

                data = dict(
                    Channel_Name=item['snippet']['channelTitle'],
                    Channel_Id=item['snippet']['channelId'],
                    Video_Id=item['id'],
                    Title=item['snippet']['title'],
                    Description=item['snippet'].get('description'),
                    Tags=item['snippet'].get('tags'),
                    Published_Date=published_date if isinstance(published_date, datetime) else None,  # Check if datetime is valid
                    Views=item['statistics'].get('viewCount'),
                    Likes=item['statistics'].get('likeCount'),
                    DisLikes=item['statistics'].get('dislikeCount'),
                    Favorite_Count=item['statistics']['favoriteCount'],
                    Comments=item['statistics'].get('commentCount'),
                    Duration=duration_seconds,  # Use parsed duration in seconds
                    Thumbnail=item['snippet']['thumbnails']['default']['url'],
                    Definition=item['contentDetails']['definition'],
                    Caption_Status=item['contentDetails']['caption']
                )
                video_data.append(data)
        except Exception as e:
            st.error(f"Error processing video {video_id}: {e}")
    return video_data


#get comment information
def get_comment_info(video_ids):
    Comment_data=[]
    try:
        for video_id in video_ids:
            request=youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=50
            )
            response=request.execute()

            for item in response['items']:
                data=dict(Comment_Id=item['snippet']['topLevelComment']['id'],
                        Video_Id=item['snippet']['topLevelComment']['snippet']['videoId'],
                        Comment_Text=item['snippet']['topLevelComment']['snippet']['textDisplay'],
                        Comment_Author=item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        Comment_Published=item['snippet']['topLevelComment']['snippet']['publishedAt'])
                
                Comment_data.append(data)
                
    except:
        pass
    return Comment_data


#get_playlist_details

def get_playlist_details(id):
        next_page_token=None
        All_data=[]
        while True:
                request=youtube.playlists().list(
                        part='snippet,contentDetails',
                        channelId=id,
                        maxResults=50,
                        pageToken=next_page_token
                )
                response=request.execute()

                for item in response['items']:
                        data=dict(Playlist_Id=item['id'],
                                Title=item['snippet']['title'],
                                Channel_Id=item['snippet']['channelId'],
                                Channel_Name=item['snippet']['channelTitle'],
                                PublishedAt=item['snippet']['publishedAt'],
                                Video_Count=item['contentDetails']['itemCount'])
                        All_data.append(data)

                next_page_token=response.get('nextPageToken')
                if next_page_token is None:
                        break
        return All_data


# Define function to create tables in SQL database
def sql_create_tables():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="guvicapstone"
        )

        mycursor = mydb.cursor()

        # Create table for channel data
        mycursor.execute("CREATE TABLE IF NOT EXISTS channel (\
                            channel_name VARCHAR(255),\
                            channel_id VARCHAR(255) PRIMARY KEY,\
                            Subscription_Count INT,\
                            Channel_Views INT,\
                            Channel_Description TEXT,\
                            Playlist_Id VARCHAR(255))")

        # Create table for video data
        mycursor.execute("CREATE TABLE IF NOT EXISTS videos (\
                            Channel_Name VARCHAR(255),\
                            Channel_Id VARCHAR(255),\
                            Video_Id VARCHAR(255) PRIMARY KEY,\
                            Title VARCHAR(255),\
                            Description TEXT,\
                            Tags TEXT,\
                            Published_Date DATETIME,\
                            Views INT,\
                            Likes INT,\
                            DisLikes INT,\
                            Favorite_Count INT,\
                            Comments INT,\
                            Duration TIME,\
                            Thumbnail VARCHAR(255),\
                            Definition VARCHAR(255),\
                            Caption_Status VARCHAR(255))")

        # Create table for comments data
        mycursor.execute("CREATE TABLE IF NOT EXISTS comments (\
                            Comment_Id VARCHAR(255) PRIMARY KEY,\
                            Video_Id VARCHAR(255),\
                            Comment_Text TEXT,\
                            Comment_Author VARCHAR(255),\
                            Comment_Published DATETIME)")

        mydb.commit()
        mycursor.close()
        mydb.close()
        st.success("Tables created successfully.")
    except Error as e:
        st.error(f"Error creating tables: {e}")


# Define function to upload channel data to SQL database
def channel_data_upload(data_channel):
    try:
        engine = create_engine("mysql+mysqlconnector://root:root@localhost/guvicapstone")
        
        # Check if channel ID already exists in the database
        existing_channel_ids = pd.read_sql("SELECT channel_id FROM channel", engine)
        new_channel_ids = data_channel['channel_id'].unique()
        new_channel_ids = set(new_channel_ids) - set(existing_channel_ids['channel_id'])
        
        # Filter out rows with existing channel IDs
        data_channel = data_channel[data_channel['channel_id'].isin(new_channel_ids)]
        
        # Upload filtered data to the database
        if not data_channel.empty:
            data_channel.to_sql(name="channel", con=engine, if_exists='append', index=False)
            st.success("Data uploaded successfully.")
        else:
            st.warning("No new data to upload.")
    except Exception as e:
        st.error(f"Error uploading data: {e}")



def video_data_upload(video_data):
    try:
        engine = create_engine("mysql+mysqlconnector://root:root@localhost/guvicapstone")
        
        # Convert Duration to HH:MM:SS format
        video_data['Duration'] = video_data['Duration'].apply(lambda x: pd.to_datetime(x, unit='s').strftime('%H:%M:%S') if not pd.isnull(x) else None)
        
        # Convert Tags from list to string
        video_data['Tags'] = video_data['Tags'].apply(lambda x: ', '.join(x) if x is not None else '')
        
        # Upload video data to the database
        if video_data is not None and not video_data.empty:
            video_data.to_sql(name="videos", con=engine, if_exists='append', index=False)
            st.success("Video data uploaded successfully.")
        else:
            st.warning("No video data to upload.")
    except Exception as e:
        st.error(f"Error uploading video data: {e}")



# Define function to upload comment data to SQL database
def comment_data_upload(comment_data):
    try:
        engine = create_engine("mysql+mysqlconnector://root:root@localhost/guvicapstone")
        
        # Check for duplicate entries
        existing_comments = pd.read_sql("SELECT Comment_Id FROM comments", engine)
        comment_data = comment_data[~comment_data['Comment_Id'].isin(existing_comments['Comment_Id'])]
        
        # Convert Comment_Published to the correct datetime format
        comment_data['Comment_Published'] = pd.to_datetime(comment_data['Comment_Published'])
        
        # Upload comment data to the database
        if comment_data is not None and not comment_data.empty:
            comment_data.to_sql(name="comments", con=engine, if_exists='append', index=False)
            st.success("Comment data uploaded successfully.")
        else:
            st.warning("No comment data to upload.")
    except Exception as e:
        st.error(f"Error uploading comment data: {e}")


# Streamlit part
st.set_page_config(layout="wide")
st.title("YOUTUBE DATA HARVESTING")

with st.sidebar:
    opt = option_menu("MENU", ['HOME' , 'EXTRACT DATA', 'QUESTIONS'])

# Inside the main function where the data extraction and upload occur
if opt == 'HOME':
    st.write("""
    # Welcome to YouTube Data Harvesting App
    
    This app allows you to extract and analyze data from YouTube channels.
    
    To get started, select one of the options from the sidebar.
    """)
elif opt == 'EXTRACT DATA':
    c1, c2, c3 = st.columns(3)
    with c1:
        id = st.text_input("Enter your channel ID")

    if st.button("Extract And Upload data"):
        if id.strip() == "":
            st.warning("Please enter a valid channel ID.")
        else:
            st.info("Extracting and uploading data...")
            try:
                sql_create_tables()
                data_channel = channel_info(id)
                if data_channel:
                    data_channel = pd.DataFrame(data_channel, index=[0])
                    #st.write("Channel data:", data_channel)
                    
                    video_ids = get_videos_id(id)
                    #st.write("Video IDs:", video_ids)
                    
                    video_data = pd.DataFrame(get_video_info(video_ids))
                    #st.write("Video data:", video_data)
                    
                    comment_data = pd.DataFrame(get_comment_info(video_ids))
                    #st.write("Comment data:", comment_data)
                    
                    channel_data_upload(data_channel)
                    video_data_upload(video_data)
                    comment_data_upload(comment_data)
                else:
                    st.warning("No data found for the provided channel ID.")
            except Exception as e:
                st.error(f"Error: {e}")

elif opt == 'QUESTIONS':
    questions = st.selectbox("Choose Your Question", [
        "Choose your Questions...",
        '1. What are the names of all videos and their corresponding channels?',
        '2. Which channels have the most number of videos, and how many videos do they have?',
        '3. What are the top 10 most viewed videos and their respective channels?',
        '4. How many comments were made on each video, and what are their corresponding video names?',
        '5. Which videos have the highest number of likes, and what are their corresponding channel names?',
        '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
        '7. What is the total number of views for each channel, and what are their corresponding channel names?',
        '8. What are the names of all the channels that have published videos in the year 2022?',
        '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?',
        '10. Which videos have the highest number of comments, and what are their corresponding channel names?'
    ], index=0)

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="guvicapstone"
    )

    mycursor = mydb.cursor()
    query = None

    if questions.startswith('1. What are the names of all videos and their corresponding channels?'):
        query = """
                SELECT Title, Channel_Name 
                FROM videos
                """
    elif questions.startswith('2. Which channels have the most number of videos, and how many videos do they have?'):
        query = """
                SELECT Channel_Name, COUNT(*) AS Video_Count 
                FROM videos 
                GROUP BY Channel_Name 
                ORDER BY Video_Count DESC 
                LIMIT 10
                """
    elif questions.startswith('3. What are the top 10 most viewed videos and their respective channels?'):
        query = """
                SELECT Title, Channel_Name, Views 
                FROM videos 
                ORDER BY Views DESC 
                LIMIT 10
                """
    elif questions.startswith('4. How many comments were made on each video, and what are their corresponding video names?'):
        query = """
                SELECT v.Title, COUNT(c.Comment_Id) AS Comment_Count
                FROM videos v
                LEFT JOIN comments c ON v.Video_Id = c.Video_Id
                GROUP BY v.Title
                """
    elif questions.startswith('5. Which videos have the highest number of likes, and what are their corresponding channel names?'):
        query = """
                SELECT Title, Channel_Name, Likes 
                FROM videos 
                ORDER BY Likes DESC 
                LIMIT 10
                """
    elif questions.startswith('6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?'):
        query = """
                SELECT Title, SUM(Likes) AS Total_Likes, SUM(DisLikes) AS Total_Dislikes 
                FROM videos 
                GROUP BY Title
                """
    elif questions.startswith('7. What is the total number of views for each channel, and what are their corresponding channel names?'):
        query = """
                SELECT Channel_Name, SUM(Views) AS Total_Views 
                FROM videos 
                GROUP BY Channel_Name 
                ORDER BY Total_Views DESC 
                LIMIT 10
                """
    elif questions.startswith('8. What are the names of all the channels that have published videos in the year 2022?'):
        query = """
                SELECT DISTINCT Channel_Name 
                FROM videos 
                WHERE YEAR(Published_Date) = 2022
                """
    elif questions.startswith('9. What is the average duration of all videos in each channel, and what are their corresponding channel names?'):
        query = """
                SELECT Channel_Name, AVG(Duration) AS Average_Duration 
                FROM videos 
                GROUP BY Channel_Name
                """
    elif questions.startswith('10. Which videos have the highest number of comments, and what are their corresponding channel names?'):
        query = """
                SELECT v.Title, v.Channel_Name, COUNT(c.Comment_Id) AS Comment_Count 
                FROM videos v 
                LEFT JOIN comments c ON v.Video_Id = c.Video_Id 
                GROUP BY v.Title, v.Channel_Name 
                ORDER BY Comment_Count DESC 
                LIMIT 10
                """
    
    if query is not None:
        try:
            mycursor.execute(query)
            df = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
            st.write(df)
        
            # Plotting the result if applicable
            if questions.startswith(('2.', '3.', '5.',  '7.', '10.')):
                fig = px.bar(df, x=df.columns[0], y=df.columns[1:], title=None)
                st.plotly_chart(fig)
            elif questions.startswith(('4.', '6.')):
                fig = px.pie(df, names=df.columns[1], title=None)
                st.plotly_chart(fig)
            elif questions.startswith(('8.', '9.')):
                fig = px.line(df, x=df.columns[0], y=df.columns[1],
                  labels={df.columns[0]: 'Number of Comments', df.columns[1]: 'Video id'},
                  title='Number of Comments on Each Video')
                st.plotly_chart(fig)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please select a question.")
