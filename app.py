# from langchain.document_loaders import PyPDFLoader
# from langchain.indexes import VectorstoreIndexCreator
# from langchain.chains import retrieval_qa
# from langchain.embeddings import HuggingFaceBgeEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter

import streamlit as st
import openai

treatment_plan = """Treatment Plan
1. [Treatment Name or Medication]

Purpose: [Explain what it does in simple language]

How to take/use: [e.g., "Take 1 tablet by mouth once daily after dinner"]

Duration: [e.g., "For 10 days" or "Until symptoms improve"]

Side Effects: [List common side effects briefly and reassuringly]

Precautions: [e.g., "Do not drive if feeling dizzy"]

2. [Treatment Name or Lifestyle Change]

Purpose:

How to follow:

Duration:

Expected Benefits:

Tips for Success:

(Repeat for additional treatments…)"""

client = openai(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

st.title('Ask Ved')

# Set your OpenAI API Key here or set it in environment variables
#openai.api_key = "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"

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display previous messages in chat
for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])

# User input prompt
prompt = st.chat_input('Pass your Prompt here')

if prompt:
    st.chat_message('user').markdown(prompt)
    st.session_state.messages.append({'role' : 'user', 'content': prompt})

    # Prepare messages for OpenAI chat completion API
    # To keep context, send all messages stored so far to API
    completion = client.chat.completions.create(
        extra_body={},
        model="google/gemma-3n-e4b-it:free",
        messages=[
            {
            "role": "user",
            "content": "You are a Ayurveda expert and doctor, so when the I ask you questions, I want you to response as an Ayurveda doctor and expert." +
                        "I want you to follow this format : " + treatment_plan + prompt
            }
        ]
    )

    #print(completion.choices[0].message.content)
    assistant_reply = completion.choices[0].message.content

    st.chat_message('assistant').markdown(assistant_reply)
    st.session_state.messages.append({'role': 'assistant', 'content': assistant_reply})

