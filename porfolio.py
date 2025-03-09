import pandas as pd
import chromadb
import uuid


class Portfolio:

    def __init__(self,file="app/resources/tech_stack_portfolio.csv"):
        self.file = file
        self.data=pd.read_csv(file)
        self.chroma_Client=chromadb.PersistentClient()
        self.collection=self.chroma_Client.get_or_create_collection(name="portfolio")
        
    def load_portfolio(self):
        if self.collection.count():
            for _,row in self.data.iterrows():
                self.collection.add(documents=row["Tech Stack"],
                            metadatas={'links':row["Portfolio Links"]},
                            ids=[str(uuid.uuid4())])
    def query_links(self,skills):
        return self.collection.query(query_texts=skills,n_results=2).get('metadatas',[])
    