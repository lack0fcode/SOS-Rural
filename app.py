import streamlit as st
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

lex_client = boto3.client(
    'lexv2-runtime',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

if 'history' not in st.session_state:
    st.session_state['history'] = []

st.title("SOS Rural - Chat de Primeiros Socorros")

user_input = st.text_input("Digite sua pergunta:")

if st.button("Enviar") and user_input:
    response = lex_client.recognize_text(
        botId=os.getenv('LEX_BOT_ID'),
        botAliasId=os.getenv('LEX_BOT_ALIAS_ID'),
        localeId=os.getenv('LEX_BOT_LOCALE_ID', 'pt_BR'),
        sessionId='usuario_local',
        text=user_input
    )

    
    message = ''
    if 'messages' in response:
        message = ' '.join([m.get('content', '') for m in response['messages']])

    st.session_state['history'].append({"user": user_input, "bot": message})

for chat in st.session_state['history']:
    st.markdown(f"**Você:** {chat['user']}")
    st.markdown(f"**IA:** {chat['bot']}")
