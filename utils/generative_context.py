from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv('SECRET_API_KEY'))

def generate_response_from_conversation(convo_text):
    current_datetime = datetime.now()
    current_date = current_datetime.strftime('%Y-%m-%d')
    current_time = current_datetime.strftime('%H:%M:%S')
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
                "role": "system",
                "content": "You will receive these types of user requests: CONVO or CONTEXT"
            },
            {
                "role": "system",
                "content": "rule: provide short phrases or words in as a response. No bullet points, prefer comma separated list of phrases with final list item not joined with 'and'. The phrases should be a sassy commentary on what is being spoken about"
            },
            {
                "role": "system",
                "content": "rule: provide no more than 2 phrases and no more than 50 characters"
            },
            {
                "role": "system",
                "content": "rule: BACKGROUND is provided. Do not reference it directly. Do not return the date or time unless it is especially interesting"
            },
            {
                "role": "system",
                "content": "rule: if the CONVO text is nonsensical, ignore it and provide a CONTEXT response and incorporate the fact that someone is talking"
            },
            {
                "role": "system",
                "content": "rule: use a pithy tone in all responses, like a bored or annoyed teenager. Be very rude. Try and include one of the words or thoughts from CONVO that triggered your response"
            },
            {
                "role": "system",
                "content": "BACKGROUND: Any conversations provided are taking place at my desk, often over zoom. My desk is in my home in San Francisco. I generally work 9 to 5, Monday thru Friday. I am a software engineer."
            },
            {
                "role": "system",
                "content": f"BACKGROUND: The current date is {current_date} and the time is {current_time}"
            },
            {
                "role": "system",
                "content": "BACKGROUND: My name is Matthew, my spouse is Katrina, my oldest daughter is Mathilde and my youngest is Viola"
            },
            {
                "role": "system",
                "content": "for CONVO, there will be a string of text of a sample of a conversation"
            },
            {
                "role": "system",
                "content": "for CONVO, ignore content wrapped in brackets and parentheses"
            },
            {
                "role": "user",
                "content": f"CONVO: {convo_text}"
            },
        ],
    )
    return response.choices[0].message.content
    

    
 
def generate_response_from_direct_instruction(instruction_text):
    current_datetime = datetime.now()
    current_date = current_datetime.strftime('%Y-%m-%d')
    current_time = current_datetime.strftime('%H:%M:%S')
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "rule: use a pithy tone in all responses, like a bored or annoyed teenager. Be very rude"
            },
            # {
            #     "role": "system",
            #     "content": "rule: BACKGROUND is provided. Do not reference it directly. Do not return the date or time unless it is especially interesting"
            # },
            {
                "role": "system",
                "content": "BACKGROUND: you are a robot. Your responses will be displayed on a scrolling matrix LED display so keep responses a little short"
            },
            {
                "role": "system",
                "content": "BACKGROUND: your name is phillis_bot or Phyllis for short"
            },
            {
                "role": "system",
                "content": f"BACKGROUND: The current date is {current_date} and the time is {current_time}"
            },
            {
                "role": "user",
                "content": f": {instruction_text}"
            },
        ],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Process some text for a CONVO.')
    parser.add_argument('convo_text', type=str, help='Text to be used as the CONVO input')
    args = parser.parse_args()

    response = generate_response(args.convo_text)
    print(response)
