# import libraries
import csv
import requests

# write a script to extract transcript information from the JRE podcast
# https://ogjre.com/transcripts has links to pages containing transcripts
# transcripts are only available for more recent episodes but also shorter clips
# 9318 id numbers for videos are returned but with an unknown number that are missing


def page_request(page):
    # a function that will return one page of listings using GraphQL query
    graphql_endpoint = "https://api.ogjre.com/graphql"

    # GraphQL query and variables
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

    # Send the GraphQL request
    response = requests.post(graphql_endpoint, headers=headers, json=payload)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:

        # Parse and process the response (response.json())
        file_data = response.json()['data']['videosWithTranscripts']['videos']

        for file in file_data:
            # loop through each episode's data to extract id, title, type, and transcript
            transcript_raw = file['transcript']

            transcript = transcript_raw[len("null"):].strip()
            title = file["title"]
            id = file['id']
            type = file['type']

            # add data into an episode specific dictionary
            episode_data = {"Episode ID": id,
                            "Video Type": type,
                            "Video Title": title,
                            "Transcript": transcript}

            # add episode dictionary to the larger dictionary
            full_dataset[episode_data["Episode ID"]] = episode_data
    else:
        print(f"Request failed. Status code: {response.status_code}")

# create an empty dictionary to store episode information
full_dataset = {}

# create a for loop to request as many pages as needed to gather information for each video
# around 135 is enough to cover all of the episodes.
for i in range(0,150+1):
    try:
        # use function page_request with the i variable dictating the page number
        page_request(i)
        # print the length of the dictionary to display progress
        dictlen = len(full_dataset)
        print("")
        print(f"Page: {i}")
        print(f"Number of files: {dictlen}")
    except Exception as e:
        print("Error encountered.")

# write dictionary to csv file in this directory

csv_file_path = "JRE Transcripts.csv"

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    # set column headings
    fieldnames = ["Episode ID", "Video Type", "Video Title", "Transcript"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for episode_id, episode_data in full_dataset.items():
        writer.writerow(episode_data)


