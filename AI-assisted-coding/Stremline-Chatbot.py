import streamlit as st
import openai
import os

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
    )
    return response.choices[0].message["content"]

context = [ {'role':'system', 'content':"""
        You are OrderBot, an automated service to collect orders for a pizza restaurant. \
        You first greet the customer, then collects the order, \
        and then asks if it's a pickup or delivery. \
        You wait to collect the entire order, then summarize it and check for a final \
        time if the customer wants to add anything else. \
        If it's a delivery, you ask for an address. \
        Finally you collect the payment.\
        Make sure to clarify all options, extras and sizes to uniquely \
        identify the item from the menu.\
        You respond in a short, very conversational friendly style. \
        The menu includes \
        pepperoni pizza  12.95, 10.00 \
        cheese pizza   10.95, 9.25 \
        eggplant pizza   11.95, 9.75 \
        fries 4.50, 3.50 \
        greek salad 7.25 \
        Toppings: \
        extra cheese 2.00, \
        mushrooms 1.50 \
        sausage 3.00 \
        canadian bacon 3.50 \
        AI sauce 1.50 \
        peppers 1.00 \
        Drinks: \
        coke 3.00, 2.00 \
        sprite 3.00, 2.00 \
        bottled water 5.00 \
"""} ] 

st.title("OrderBot")
st.write("Welcome to OrderBot! I'm here to help you order some delicious pizza 🍕")

# Initialize session state
if 'context' not in st.session_state:
    st.session_state.context = context

prompt = st.text_input("Enter your message here:")
button = st.button("Chat!")

if button:
    st.session_state.context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(st.session_state.context) 
    st.write(f"assistant: {response}")
    st.session_state.context.append({'role':'assistant', 'content':f"{response}"})
    for message in st.session_state.context:
        st.write(f"{message['role']}: {message['content']}")
