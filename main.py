
import requests
import json
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "ab47a001-f539-4ff6-b2fc-88f37b49c4a8"
FLOW_ID = "69c709fc-e116-4ef1-a363-b8b135c45458"
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ENDPOINT = "customer" # The endpoint name of the flow

  

def run_flow(message: str) -> dict:
    
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()


def main():
    st.title("Customer Service Assistant")

    message = st.text_area("Message",placeholder="We are here to help you. Please type your question.")
    
    if st.button("Run Flow"):
        if not message.strip():
            st.error("Please enter a message.")
            return
        
        try:
            with st.spinner("Running flow..."):
                response = run_flow(message)
            
            response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            st.markdown(response)
        except Exception as e:
            st.error(str(e))



if __name__ == "__main__":
    main()