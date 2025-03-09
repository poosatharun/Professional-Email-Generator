import re

def clean_text(text):
    # Remove URLs and links
    text = re.sub(r'http[s]?://\S+', '', text)  
    text = re.sub(r'www\.\S+', '', text)  

    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)  

    # Remove special characters (except alphanumeric and spaces)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  

    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()  

    return text