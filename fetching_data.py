import hashlib
import time
import requests

import os

# Load environment variables from .env file


public_key = os.getenv('MARVEL_PUBLIC_KEY')
private_key = os.getenv('MARVEL_PRIVATE_KEY')

def search_characters(name):
    # Generate a timestamp
    ts = str(int(time.time()))

    # Generate a hash
    hash_value = hashlib.md5((ts + private_key + public_key).encode('utf-8')).hexdigest()

    # Construct the request URL
    url = "http://gateway.marvel.com/v1/public/characters"

    params = {
        "name": name,
        "apikey": public_key,
        "ts": ts,
        "hash": hash_value,
    }

    try:
        # Make the request
        response = requests.get(url, params=params)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the response JSON
            return response.json()
        else:
            # Return an error message if the request failed
            return {"error": response.text}
    except Exception as e:
        # Return an error message if an exception occurs
        return {"error": str(e)}

def search_stories_by_character(character_name):
    # Search for the character by name
    characters_response = search_characters(character_name)
    if not characters_response or 'error' in characters_response:
        return {"error": "Character not found or error in fetching character data"}

    characters = characters_response.get('data', {}).get('results', [])
    if not characters:
        return {"error": "No characters found"}

    # Get the character ID
    character_id = characters[0]['id']

    # Generate a timestamp
    ts = str(int(time.time()))

    # Generate a hash
    hash_value = hashlib.md5((ts + private_key + public_key).encode('utf-8')).hexdigest()

    # Construct the request URL for stories
    url = f"http://gateway.marvel.com/v1/public/characters/{character_id}/stories"

    params = {
        "ts": ts,
        "apikey": public_key,
        "hash": hash_value,
    }

    try:
        # Make the request
        response = requests.get(url, params=params)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the response JSON
            return response.json()
        else:
            # Return an error message if the request failed
            return {"error": response.text}
    except Exception as e:
        # Return an error message if an exception occurs
        return {"error": str(e)}

# Example usage
def fetch_stories(character_name):
    filtered_stories = []
    stories_response = search_stories_by_character(character_name)
    
    if 'error' in stories_response:
        print(f"Error: {stories_response['error']}")
        filtered_stories.append({"error": stories_response['error']})
        return filtered_stories
    else:
        stories = stories_response.get('data', {}).get('results', [])
        for story in stories:
            if story.get('description'):
                filtered_stories.append({"Title": story['title'], "Description": story['description']})
        return filtered_stories

def search_events_by_character(character_name):
    # Search for the character by name
    characters_response = search_characters(character_name)
    if not characters_response or 'error' in characters_response:
        return {"error": "Character not found or error in fetching character data"}

    characters = characters_response.get('data', {}).get('results', [])
    if not characters:
        return {"error": "No characters found"}

    # Get the character ID
    character_id = characters[0]['id']

    # Generate a timestamp
    ts = str(int(time.time()))

    # Generate a hash
    hash_value = hashlib.md5((ts + private_key + public_key).encode('utf-8')).hexdigest()

    # Construct the request URL for events
    url = f"http://gateway.marvel.com/v1/public/characters/{character_id}/events"

    params = {
        "ts": ts,
        "apikey": public_key,
        "hash": hash_value,
    }

    try:
        # Make the request
        response = requests.get(url, params=params)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the response JSON
            return response.json()
        else:
            # Return an error message if the request failed
            return {"error": response.text}
    except Exception as e:
        # Return an error message if an exception occurs
        return {"error": str(e)}

def fetch_filtered_events(character_name):
    filtered_events = []
    events_response = search_events_by_character(character_name)
    
    if 'error' in events_response:
        print(f"Error: {events_response['error']}")
        filtered_events.append({"error": events_response['error']})
        return filtered_events
    else:
        events = events_response.get('data', {}).get('results', [])
        for event in events:
            if event.get('description'):
                # Extracting relevant data
                event_data = {
                    "Event Title": event['title'],
                    "Description": event['description'],
                    "Characters": [],
                    "Related Events": []
                }
                
                # Extracting character data
                characters = event.get('characters', {}).get('items', [])
                for character in characters:
                    # Adjusting for correct structure
                    if character.get('role'):
                        character_data = {
                            "Name": character.get('name', 'Unknown'),
                            "Role": character.get('role', 'Unknown')
                        }
                        event_data["Characters"].append(character_data)
                

                # Extracting related events data
                related_events = event.get('events', {}).get('items', [])
                for related_event in related_events:
                    related_event_data = {
                        "Event Title": related_event.get('name', 'Unknown')
                    }
                    event_data["Related Events"].append(related_event_data)
                
                filtered_events.append(event_data)
                
        return filtered_events

def search_series_by_character(character_name):
    characters_response = search_characters(character_name)
    if not characters_response or 'error' in characters_response:
        return {"error": "Character not found or error in fetching character data"}

    characters = characters_response.get('data', {}).get('results', [])
    if not characters:
        return {"error": "No characters found"}

    character_id = characters[0]['id']
    ts = str(int(time.time()))
    hash_value = hashlib.md5((ts + private_key + public_key).encode('utf-8')).hexdigest()

    url = f"http://gateway.marvel.com/v1/public/characters/{character_id}/series"

    params = {
        "ts": ts,
        "apikey": public_key,
        "hash": hash_value,
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.text}
    except Exception as e:
        return {"error": str(e)}

def fetch_filtered_series(character_name):
    filtered_series = []
    series_response = search_series_by_character(character_name)
    
    if 'error' in series_response:
        print(f"Error: {series_response['error']}")
        filtered_series.append({"error": series_response['error']})
        return filtered_series
    else:
        series = series_response.get('data', {}).get('results', [])
        for serie in series:
            if serie.get('description'):
                filtered_series.append({"Title": serie['title'], "Description": serie['description']})
        return filtered_series


def fetch_character_extra_data(character_name):
    series = fetch_filtered_series(character_name)
    stories = fetch_stories(character_name)
    events = fetch_filtered_events(character_name)
    return {"Series": series, "Stories": stories, "Events": events}

#Example usage
#print(fetch_character_extra_data("Thor"))