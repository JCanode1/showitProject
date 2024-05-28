import os

def generate_user_card(name, image_url, description):
    if len(description) > 30:
        description = description[:30] + "..."
    
    html_content = f"""
    <div class="card-container">
        <img class="round" src="{image_url}" alt="user" />
        <h3>{name}</h3>
        <p>{description}</p>
    </div>
    """
    return html_content
    


def remove_files_from_directory(directory="html"):
    files = os.listdir(directory)
    for file in files:
        os.remove(os.path.join(directory, file))

def create_html_page(characters):
    html = """ 
    
        <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Scrollable Menu with User Card</title>
    <style>
    div.scrollmenu {
    background-color: #333;
    overflow: auto;
    white-space: nowrap;
    padding: 10px;
    }

    div.scrollmenu > * {
    display: inline-block;
    color: white;
    text-align: center;
    padding: 14px;
    text-decoration: none;
    vertical-align: top;
    }

    div.scrollmenu img {
    height: 100px;
    }

    div.scrollmenu p {
    margin: 0;
    }

    .card-container {
    text-align: center;
    margin: 20px;
    padding: 20px;
    background-color: white;
    border-radius: 2rem;
    box-shadow: 0px 1rem 1.5rem rgba(0, 0, 0, 0.5);
    color: #404040;
    display: inline-block;
    vertical-align: top;
    }

    .card-container img.round {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    margin-top: 20px;
    border: 5px solid #ffd01a;
    }

    .card-container h3 {
    margin: 10px 0;
    color: #404040;
    }

    .card-container p {
    color: #404040;
    margin-bottom: 0;
    max-width: 200px; /* Adjust the maximum width as needed */
    overflow-wrap: break-word; /* Allow the text to wrap */
    }

    .discription {
    width:200px;
    word-wrap: break-word;
    }



    </style>
    </head>
    <body>

    <div class="scrollmenu">
    """

    for character in characters:
        name = character['name']
        description = character['description']
        thumbnail = character['thumbnail']
        image_url = f"{thumbnail['path']}.{thumbnail['extension']}"
        
        html += generate_user_card(name, image_url, description)
        
    ending = """
        </div>
        </div>
        </div>

        </body>
        </html>
            
        """
        
    html += ending
    
    return html