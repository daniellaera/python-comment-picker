from collections import Counter
import os
import random
from googleapiclient.discovery import build
import re

# Set up your YouTube Data API credentials
api_key = 'Replace with your API key'  # Replace with your API key
youtube = build('youtube', 'v3', developerKey=api_key)

# Define your YouTube channel ID
channel_id = 'Replace with your channel ID'  # Replace with your channel ID

def get_latest_video_comments(video_id):
    comments = []
    response = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText',
        maxResults=100  # You can adjust the number of comments to fetch
    ).execute()
    
    while response:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            username = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            comments.append((username, comment))
        try:
            # Try to fetch the next page of comments
            next_page_token = response['nextPageToken']
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                textFormat='plainText',
                maxResults=100,
                pageToken=next_page_token
            ).execute()
        except KeyError:
            # No more pages of comments
            break
    
    return comments

def select_random_topic(video_ids):
    # Fetch comments from the latest videos
    comments = []
    for video_id in video_ids:
        video_comments = get_latest_video_comments(video_id)
        comments.extend(video_comments)

    # Pick a random comment as the selected topic
    selected_topic = random.choice(comments)
    
    return selected_topic

def select_most_popular_topic(video_ids):
    # Fetch comments from the latest videos
    comments = []
    for video_id in video_ids:
        video_comments = get_latest_video_comments(video_id)
        comments.extend(video_comments)

    # Count comment occurrences
    comment_counter = Counter(comments)

    # Find the most popular comment
    most_popular_comment, frequency = comment_counter.most_common(1)[0]

    return most_popular_comment, frequency

if __name__ == '__main__':
    # List the video IDs of the latest videos on your channel
    latest_video_ids = [
        'video_id',
        'video_id',
        'video_id',
        'video_id',
        'video_id',
        'video_id'
    ]  # Replace with your video IDs
    
    # Select a random topic from the latest videos' comments
    topic = select_random_topic(latest_video_ids)

    # Find the most popular topic from the latest videos' comments
    popular_topic, frequency = select_most_popular_topic(latest_video_ids)

    print("Selected Topic:")
    print(topic)
    print("Most Popular Topic:")
    print(popular_topic)
    print(f"Frequency: {frequency} times")