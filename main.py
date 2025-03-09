import streamlit as st
from chains import Chain
from utils import clean_text
from porfolio import Portfolio
from langchain_community.document_loaders import WebBaseLoader

def create_streamlit_app(llm,portfolio,clean_text):
    st.title("Job Application Assistant")
    st.write("This app helps you extract job postings from a website and generate a cold email for job applications.")
    st.write("Enter the text from the careers page of a website and click the 'Extract Jobs' button to get started.")
    
    url_input = st.text_input("Enter the text from the careers page of a website:",value="https://www.example.com/careers")
    submit_button = st.button("Submit")

    if submit_button:

        loader=WebBaseLoader([url_input])
        data=clean_text(loader.load().pop().page_content)
        portfolio.load_portfolio()
        jobs=llm.extract_jobs(data)
        for job in jobs:
            skills=job.get('skills',[])
            links=portfolio.query_links(skills)
            email=llm.generate_email(job,links)
            st.markdown(f"""
    <div style='white-space: pre-wrap; word-wrap: break-word; font-size: 16px; line-height: 1.6;'>
        {email}
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    chain=Chain()
    portfolio=Portfolio()
    st.set_page_config(page_title="Job Application Assistant",page_icon="📝")
    create_streamlit_app(chain,portfolio,clean_text)

