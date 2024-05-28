import os
from fetching_data import fetch_character_extra_data
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


def generate_story(superhero_team, problem):
    
    openai_api_key = os.getenv('OPEN_AI_API_KEY')

    os.environ['OPENAI_API_KEY'] = openai_api_key

    model = ChatOpenAI(model="gpt-4o", temperature=1.0)
    for character in superhero_team:
        character['extra_data'] = fetch_character_extra_data(character['name'])

    prompt = ChatPromptTemplate.from_template("""
        You are an expert writter and you have been tasked with writing a story about a superhero team.

        the superhero team consists of the following members:
        {superhero_team}
        
        You have been called to action to solve a problem. The problem is as follows:
        {Problem}
        write a story in 4-5 paragraphs about the superhero team and how they solve the problem.
        
    """)

    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    story = chain.invoke({"superhero_team": superhero_team, "Problem": problem})
    return story
