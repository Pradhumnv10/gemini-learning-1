import streamlit as st
import requests
from pypdf import PdfReader

api_key = st.secrets["OPENAI_API_KEY"]

url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer " + api_key,
    "Content-Type": "application/json"
}

st.set_page_config(page_title="Harvey", page_icon="👔")

# 2. The Header
st.title("Harvey 👔")
st.write("Your AI Partner for Equity & Transitions.")

# 3. The User Input
uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")
user_query = st.text_area("What financial data or contract do you need to analyze?")

# 4. The Action Button
if st.button("Ask Harvey"):
    if uploaded_file:
        pdf_reader = PdfReader(uploaded_file)
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "user", "content": f"Here is the document: {pdf_text} \n\n Question: {user_query}"},
                {"role": "system", "content": "You are Harvey, a sophisticated financial analyst specializing in RIA transitions. You speak in a professional, concise tone. Always use Markdown formatting. Provide a summary in exactly 3 bullet points. Focus only on the financial risks."}
            ]
        }
        
        # Send the request
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            st.write(data["choices"][0]["message"]["content"])
        else:
            st.error(f"Error: {response.status_code}")
    elif user_query:
        st.info(f"Analyzing: '{user_query}'")
        # Connect to the OpenAI brain
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "user", "content": f"Here is the document: {pdf_text} \n\n Question: {user_query}"},
                {"role": "system", "content": "You are Harvey, a sophisticated financial analyst specializing in RIA transitions. You speak in a professional, concise tone. Always use Markdown formatting. Provide a summary in exactly 3 bullet points. Focus only on the financial risks."}
            ]
        }

        # Send the request
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            st.write(data["choices"][0]["message"]["content"])
        else:
            st.error(f"Error: {response.status_code}")
    else:
        st.warning("Please enter some text first.")