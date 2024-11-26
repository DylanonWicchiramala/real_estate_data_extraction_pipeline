import csv
from tqdm import tqdm
import json
import pymongo.collection
import pymongo
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings


# Function to concatenate all text fields into one string
def concatenate_fields(document:dict, fields:list[str], with_field_name:bool=True) -> str:
    fields = fields if fields else list(document.keys())
    if with_field_name:
        return "\n".join([ f"{field} : {document.get(field)}" for field in fields if document.get(field)])
    else:
        return "\n".join([ f"{document.get(field)}" for field in fields if document.get(field)])


def populate_embedding_for_dict(
    data: dict, 
    fields_to_embed: list[str], 
    embedding: OpenAIEmbeddings,
    embedding_key: str = "embedding", 
) -> dict:
    """Generate embedding for a single data dictionary and add it to the dictionary."""
    
    # Concatenate all relevant fields
    combined_text = concatenate_fields(data, fields_to_embed)
    
    # Generate the embedding for the combined text
    embedded = embedding.embed_query(combined_text)

    # Update the dictionary with the generated embedding
    data[embedding_key] = embedded

    return data


# Function to generate embeddings and update the MongoDB collection
def populate_embeddings(
    collection: pymongo.collection.Collection, 
    fields_to_embeded:list[str], 
    embedding: OpenAIEmbeddings,
    embedding_key:str="embedding",
) -> pymongo.collection.Collection:
    """ generate embedding of all of data in collection in mongo db database. this function will create field `embedding` in database. """
    
    documents = collection.find()
    documents = list(documents)
    
    for doc in tqdm(documents, desc="Updating embeded data to db collection."):
        # Concatenate all relevant fields
        combined_text = concatenate_fields(doc, fields_to_embeded)
        
        # Generate the embedding for the combined text
        data_with_embeded = populate_embedding_for_dict(
                data = doc,
                fields_to_embed = fields_to_embeded,
                embedding = embedding,
                embedding_key = embedding_key,
            )

        # Update the document with the generated embedding
        collection.update_one(
            {"_id": doc["_id"]},
            {"$set": data_with_embeded}
        )
    return collection


def add_from_json(path: str, add_function):
    """ push new data(many) from json file to mongodb collection.
    """
    # Load data from the provided JSON file
    with open(path) as file:
        data = json.load(file)
        
    # Upsert (insert or replace) each document in the collection
    for record in data:
        add_function(record)
    
    print(f"Upserted {len(data)} records into the collection.")
    

def add_from_csv(path: str, add_function, delimiter:str=",", newline='', encoding='utf-8'):
    """Create data collection from CSV file.
    
    Args:
        path (str): Path to the CSV file.
        collection (pymongo.collection.Collection): MongoDB collection to insert/update data.
    """
    # Open the CSV file
    with open(path, newline=newline, encoding=encoding) as file:
        # Read the CSV content using the csv module
        reader = csv.DictReader(file, delimiter=delimiter)
        
        # Upsert (insert or replace) each document in the collection
        for record in reader:
            add_function(record)
    
    print(f"Upserted {reader.line_num} records into the collection.")