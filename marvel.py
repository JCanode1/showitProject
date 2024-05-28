import requests
import time
import hashlib
import csv
import os

public_key = "8c1b9e7280938f443a2603a6e92bd6a8"
private_key = "7da56872f4db95cfe9442631a136507057318f06"


def character_added(name, description, ID):
    file_path = 'characterData.csv'
    
    # Prepare the new row
    new_row = {
        'id': ID,
        'name': name,
        'description': description if description else 'No description available.'
    }
    
    # Write the new row to the CSV file
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ['id', 'name', 'description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write the header if the file is empty
        if file.tell() == 0:
            writer.writeheader()
        
        # Write the new row
        writer.writerow(new_row)



    

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
        
        

def search_id(ID):
    
    # Generate a timestamp
    ts = str(int(time.time()))

    # Generate a hash
    hash_value = hashlib.md5((ts + private_key + public_key).encode('utf-8')).hexdigest()

    # Construct the request URL
    url = "http://gateway.marvel.com/v1/public/characters"

    params = {
        "id": ID,
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
    
    
## Example usage
# result = search_characters("thor")
# print(result)

# result = search_id(1009664)
# print(result)


