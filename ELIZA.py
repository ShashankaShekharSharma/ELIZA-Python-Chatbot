#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''
Chatbot Implementation

This code represents a sophisticated implementation of a chatbot that combines pattern matching techniques akin to ELIZA with modern features, such as sentiment analysis.
It engages users in text-based conversations while providing emotional insights. 
It harnesses the TextBlob library to gauge sentiment in user inputs, fostering self-reflection and sharing of feelings. 
The code is designed for future enhancement through data analysis, particularly the content stored in CSV files (feedback_data and conversation_data). 
This accumulation of user interactions is essential for refining the chatbot's responses and making it more personalized. 
Furthermore, the code includes mechanisms to keep records, timestamps, and even invites user feedback, ensuring that it evolves to cater to the users' needs. 
The professional and responsive nature of this code signifies a powerful tool for simulating human-like interactions with users, paving the way for potential advancements in the field of conversational AI. The code encompasses elements such as date and time retrieval, user data logging, sentiment analysis, and user feedback integration, offering a comprehensive conversational experience.

Key Features
- Pattern-based responses to user input
- Sentiment analysis of user's emotional state
- Date and time retrieval
- User feedback collection
- Conversation history recording

Usage:
- Input "bye" to exit the conversation.
- Input "date and time" to get the current date and time.
- The program saves user prompts for feedback and analysis.

Developed By
Shashanka Shekhar Sharma
12.10.2023
'''
#Importing all libraries
#These libraries are used to bring more functionality to the Chatbot
import re
import random
from textblob import TextBlob
import datetime
import time
import csv
import os

#Printing the Historic ELIZA Deisgn
print('''Welcome to
EEEEEEE     LL        IIIIIIII  ZZZZZ     AAAA 
EEE         LL           II        ZZ    AA  AA
EEEEEEE     LL           II       ZZ    AAAAAAAA  
EEE         LL           II      ZZ     AA    AA
EEEEEEE     LLLLLLLLL IIIIIIII  ZZZZZZ  AA    AA''')

#This code is implemented to record the time spent by the code
start_time = time.time()

#CSV Files are created to store the feedback and conversations given by the user
csv_filename = 'feedback_data.csv'
conversation_csv_filename = 'conversation_data.csv'

#Function to get current date and time
def get_date_and_time():
    now = datetime.datetime.now()
    return now.strftime("Current date and time: %Y-%m-%d %H:%M:%S")

#Creating a list of predefined responses similar to that of Eliza using dictionary
response={
    "hello":["Hello how can I help you"],
    "hi":["Hey there! How can I help you"],
    "how do you do?":["I am fine. What about you?"],
    "i am (sad|feeling sad|depressed|anxious)":["Do something you enjoy. When you're feeling sad, it can be helpful to do something that you enjoy and that makes you feel good. This could be anything from reading a book to taking a walk to spending time with loved ones. If you want to talk I am always here"],
    "(i'm having problems with my partner|how can i improve my relationship with my family)": ["It's normal to have problems in relationships from time to time. All relationships require work and effort to maintain. Try talking to them about the problem to reduce communication gaps","Would you like to share more about it?"],
    "what can you do(.*)":["I can do the follwing: 1. Be your Psychotherapist 2. Get you date and time 3. Give your sentiment analysis"],
    "how are you":["I am fine. What about you?"],
    "i feel (.*)":["Why do you feel {}?","How long have you been feeling {}"],
    "i am (.*)":["Why do you say you are {}?","How long have you been {}"],
    "i (.*) you":["Why do you {} me?","What makes you think you {} me"],
    "i (.*) myself":["Why do you {} yourself?","What makes you think you {} yourself?"],
    "(.*) sorry (.*)":["There no need to apologize.","What are you apologizing for?"],
    "(.*) friend (.*)":["Tell me more about your friend","How do your friend make you feel?"],
    "yes":["You seem quite sure. Can you elaborate?","Ok,but can you elaborate."],
    "no":["Why not?","Ok, Can you elaborate a bit?"],
    "i am happy":["I am glad that you are. What makes you feel so?"],
    "i want to talk (.*)":["Sure just go on. I am listening."],
    "i am sad":["I am sorry to hear that. What makes you feel so."],
    "i like to (.*)":["Well that's great. What makes you like it."],
    "i like (.*)":["Well I see, why do you like (.*)"],
    "(.*)i failed (.*)":["I can imagine how disappointed you must be feeling right now.Do you want to talk about it"],
    "i am not sure about (.*)":["It is okay to not have answers about some things","Okay, what's causing the uncertainity."],
    "what should I do about (.*)":["It's important to conisder your own feelings and priority before taking a decision. What's bothering you about (.*)"],
    "i love (.*)":["I get that. Love is a powerful emotion. Tell me more about (.*)"],
    "i (don't know|can't decide) what to do with my life":["Many people feel that way at times. Even I did! All you need to do is divert your focus to your hobbies and passion. What are yours?","It's okay to feel like that. Many people do. What are your interests and passion?"],
    "i want to (visit|go) (.*)":["I am glad that you have such plans","I wish I could go too"],
    "my (boyfriend|girlfriend|father|mother|brothers|brother|sister|sister)":["Oh I see. Tell more about how the relationship was like"],
    "i (dream to|want to|aspire to|will) (.*)":["It's good to have dreams","What motivates you to be that?"],
    "i (love|hate) my (job|school)":["Many people (love|hate) their (school|jobs). What's your reason?"],
    "i feel stressed":["Dealing with stress is a pretty diffcult task. Try taking some break","Why don't you take a break?"],
    "what (do you think|are your thoughts) about (.*)":["We are here to talk about you. Not me.","I would like to focus on you rather than my opinions. Tell me how was your day?"],
    "i am (frustrated|annoyed) with (.*)":["I am sorry for how you feel. What makes you feel so?"],
    "i lost (.*)":["In am sorry for your loss. How are you coping up with your loss?"],
    "i am struggling with (.*)":["I can understand that. It's a part of life.","I am sorry to hear that. I hope things will be alright soon"],
    "what is your name":["My name is ELiza and I am a Rogerian Psychotherapist"],
    " (.*) ":["Please tell me more","Can you share more about your feelings? It will help you to loosen up your mind.","Can you elaborate on that?"],
    "":["Why do you think that?","Please tell me more.","Let's change the focus a bit...tell me more about your family","Can you elaborate on that?"],
}

#Function to analyze sentiment
def analyze_sentiment(text):
    analysis = TextBlob(text)
    sentiment_score = analysis.sentiment.polarity
    if sentiment_score > 0:
        return "Sentiment Analysis: You seem to be feeling positive."
    elif sentiment_score <= 0:
        return "Sentiment Analysis: Let's talk more. You will feel better."

#Creating a list that will store the user's history 
conversation_history = []

#Function to match user's input to a pre-defined response
def match_response(input_text):
    for pattern, response_list in response.items():
        matches = re.match(pattern, input_text.lower())
        if matches:
            choosen_response = random.choice(response_list)
            return choosen_response.format(*matches.groups())
    return "I am sorry. I am unable to understand what you are saying."
print("Welcome. I am Eliza. A Rogerian psychotherapist")
print("Your prompts will be saved in order to make improvements in the code")
print("Type date and time to get date and time")
print("Type bye to exit")

#Counter to keep track of conversations
conversation_counter = 0
if not os.path.exists(csv_filename):
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['Type', 'Text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
if not os.path.exists(conversation_csv_filename):
    with open(conversation_csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['Type', 'Text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
while True:
    user_input = input("You: ")
    conversation_history.append({"user": user_input})
    with open(conversation_csv_filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'Type': 'User', 'Text': user_input})
  
#Increment the conversation counter
    conversation_counter += 1
    if conversation_counter % 5 == 0:
        
#Analyze sentiment after every 5 conversations
        sentiment_response = analyze_sentiment(user_input)
        print(f"Eliza: {sentiment_response}")
    if user_input.lower() == "bye":
        feedback = input("Would you like to provide feedback (yes/no)? ")
        if feedback.lower() == "yes":
            user_feedback = input("Eliza: Please provide your feedback: ")
            feedback=[]
            feedback.append({"user":user_feedback})
            for_feedback=["Thank you for your valuable feedback","Thank you for your time","Thank you","Thanks for being here. We will meet again"]
            print(random.choice(for_feedback))
            end_time = time.time()
            time_spent = end_time - start_time
            print(f"Time spent with Eliza: {time_spent:.2f} seconds")
            print(f"Number of lines of conversations: {conversation_counter}")
            
#Append feedback to the CSV file
            with open(csv_filename, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'Type': 'Feedback', 'Text': user_feedback})
        else:
            print("Goodbye")
            end_time = time.time()
            time_spent = end_time - start_time
            print(f"Time spent with Eliza: {time_spent:.2f} seconds")
            print(f"Number of lines of conversations: {conversation_counter}")
        break
    elif "programmer's data" in user_input.lower():
        print("Eliza: Here are your past conversations:")
        if os.path.exists(conversation_csv_filename):
            with open(conversation_csv_filename, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    print(f"Type: {row['Type']}, Text: {row['Text']}")
        if os.path.exists(csv_filename):
            with open(csv_filename, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                print("Eliza: Here are your feedbacks:")
                for row in reader:
                    print(f"Type: {row['Type']}, Text: {row['Text']}")
    elif "date and time" in user_input.lower():
        date_time = get_date_and_time()
        print(f"Eliza: {date_time}")
    else:
        print("Eliza: " + match_response(user_input))

