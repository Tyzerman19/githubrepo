import csv
import time

import requests
import pandas as pd

# 9318 id numbers with some missing



def page_request(page):
    graphql_endpoint = "https://api.ogjre.com/graphql"

    # Define the GraphQL query and variables
    graphql_query = """
      query VideosWithTranscripts($limit: Int, $offsetMultiplier: Int) {
        videosWithTranscripts(limit: $limit, offsetMultiplier: $offsetMultiplier) {
          hasMore
          offsetMultiplier
          videos {
            transcript
            ...VideoSnippet
            __typename
          }
          __typename
        }
      }
    
      fragment VideoSnippet on Video {
        id
        title
        episodeNumber
        type
        # ... other fields ...
        __typename
      }
    """

    variables = {
        "limit": 50,
        "offsetMultiplier": page
    }

    # Set the request headers
    headers = {
        'Content-Type': 'application/json',
    }

    # Construct the request payload
    payload = {
        'query': graphql_query,
        'variables': variables
    }
    # episodes_listing_url = "https://ogjre.com/transcripts"

    # make html request
    # response = requests.get(episodes_listing_url)

    # Send the GraphQL request
    response = requests.post(graphql_endpoint, headers=headers, json=payload)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse and process the response (response.json())
        file_data = response.json()['data']['videosWithTranscripts']['videos']
        # print(response.json())

        # print(transcript)

        for file in file_data:
            transcript = file['transcript']
            transcript_real = transcript[len("null"):].strip()
            title = file["title"]
            id = file['id']
            type = file['type']

            episode_data = {"Episode ID": id,
                            "Video Type": type,
                            "Video Title": title,
                            "Transcript": transcript_real}

            full_dataset[episode_data["Episode ID"]] = episode_data
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

full_dataset = {}

counter = 0
for i in range(0,130+1):
    try:
        page_request(i)
        counter += 50
        # print(counter)
        print(len(full_dataset))
    except Exception as e:
        print("No more episodes?")

# write to csv

csv_file_path = "JRE Transcripts.csv"

with open(csv_file_path, 'w', newline='') as csvfile:
    fieldnames = ["Episode ID", "Video Type", "Video Title", "Transcript"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for episode_id, episode_data in full_dataset.items():
        writer.writerow(episode_data)


