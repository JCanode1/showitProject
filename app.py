import streamlit as st
import streamlit.components.v1 as components  # Correct import
from marvel import search_characters, character_added
from messyHTML import generate_user_card, create_html_page
from generateStory import generate_story
import os


def main():
        
    # Initialize an empty list to store the superhero team
    if 'superhero_team' not in st.session_state:
        st.session_state.superhero_team = []

    st.title("Marvel Superhero Team Builder")

    # Input for searching a character
    character_name = st.text_input("Search for a Marvel character")

    if character_name:
        # Search for characters using the Marvel API
        result = search_characters(character_name)

        if result is not None:  # Check if result is not None
            if "error" in result:
                st.error(f"An error occurred: {result['error']}")
            else:
                characters = result.get('data', {}).get('results', [])
                if characters:
                    for character in characters:
                        if character['description'] == "":
                            character['description'] = "No description available."
                        st.write(f"**Name:** {character['name']}")
                        st.write(f"**Description:** {character['description']}")
                        thumbnail = character['thumbnail']
                        image_url = f"{thumbnail['path']}.{thumbnail['extension']}"
                        st.image(image_url)
                        
                        # Check if character is already in the team
                        character_ids = [char['id'] for char in st.session_state.superhero_team]
                        if character['id'] in character_ids:
                            st.write(f"{character['name']} is already in the team.")
                        else:
                            if st.button(f"Add {character['name']} to Team"):
                                st.session_state.superhero_team.append(character)
                                character_added(character['name'], character['description'], character['id'])
                                # Generate HTML content for the team
                                html_content = create_html_page(st.session_state.superhero_team)
                                st.session_state.html_content = html_content
                else:
                    st.write("No characters found.")
        else:
            st.error("No data returned from the Marvel API.")
    st.write("Your Team:")


    # Display the current superhero team using the generated HTML
    if 'html_content' in st.session_state:
        components.html(st.session_state.html_content, height=300)

        # Check if there are at least two characters in the team to enable the "Generate Story" button
    if len(st.session_state.superhero_team) >= 2:
        generate_story_button = st.button("Story Maker")
    else:
        generate_story_button = st.button("Story Maker", disabled=True)

    if generate_story_button:
        # Set a session state variable to indicate that the story generation page should be shown
        st.session_state.show_story_page = True

    if 'show_story_page' in st.session_state and st.session_state.show_story_page:
        story_page()


def story_page():
    st.title("Superhero Team Story Generator")

    st.write("Your Team:")
    
    if 'html_content' in st.session_state:
        components.html(st.session_state.html_content, height=300)
    
    problem = st.text_input("Enter a subject or problem for the story:")
    
    if problem:
        st.write("Generated Story:")
        with st.spinner("Generating Story..."):
            # story_text = generate_story(st.session_state.superhero_team, problem)
            with open('storyExample.txt', 'r') as file:
                story_text = file.read()
            st.write(story_text)



    

if __name__ == "__main__":
    main()

