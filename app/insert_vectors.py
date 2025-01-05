# %%
from datetime import datetime
import pandas as pd
from database.vector_store import VectorStore
from timescale_vector.client import uuid_from_time

# Initialize VectorStore
vec = VectorStore()

# Read the CSV file
#df = pd.read_csv("/data/faq_dataset.csv", sep=";")
df = pd.read_csv(r"D:\INFOSYS\pgvectorscale-rag-solution\pgvectorscale-rag-solution\data\faq_dataset.csv",sep=";")
#df = pd.read_csv("D:\INFOSYS\pgvectorscale-rag-solution\pgvectorscale-rag-solution\data\faq_dataset.csv",sep=";")
print(df.head())


# Prepare data for insertion
def prepare_record(row):
    
    content = f"Question: {row['question']}\nAnswer: {row['answer']}"
    embedding = vec.get_embedding(content)
    return pd.Series(
        {
            "id": str(uuid_from_time(datetime.now())),
            "metadata": {
                "category": row["category"],
                "created_at": datetime.now().isoformat(),
            },
            "contents": content,
            "embedding": embedding,
        }
    )
records_df = df.apply(prepare_record, axis=1)
print("records_df value showing ")
print(records_df)

"""print("Performing a search query to verify insertion...")
search_results = vec.search(query_text="What is your return policy?")
print("Search results:")
print(search_results) """


# Create tables and insert data
print("Creating tables...")
vec.create_tables()
print("Tables created successfully.")
print("Creating index...")
vec.create_index()  # DiskAnnIndex
print("Index created successfully.")
print("Upserting records into the database...")
vec.upsert(records_df) 
print("Records inserted successfully.") 

# %%  




"""Prepare a record for insertion into the vector store.


    This function creates a record with a UUID version 1 as the ID, which captures
    the current time or a specified time.

    Note:
        - By default, this function uses the current time for the UUID.
        - To use a specific time:
          1. Import the datetime module.
          2. Create a datetime object for your desired time.
          3. Use uuid_from_time(your_datetime) instead of uuid_from_time(datetime.now()).

        Example:
            from datetime import datetime
            specific_time = datetime(2023, 1, 1, 12, 0, 0)
            id = str(uuid_from_time(specific_time))

        This is useful when your content already has an associated datetime.
    """

"""from datetime import datetime
import pandas as pd
from database.vector_store import VectorStore
from timescale_vector.client import uuid_from_time

# Initialize VectorStore
vec = VectorStore()

# Read the CSV file
input_csv_path = r"D:\INFOSYS\pgvectorscale-rag-solution\pgvectorscale-rag-solution\data\faq_dataset.csv"
output_csv_path = r"D:\INFOSYS\pgvectorscale-rag-solution\pgvectorscale-rag-solution\data\processed_faq_dataset.csv"

df = pd.read_csv(input_csv_path, sep=";")
print("Original DataFrame:")
print(df.head())

# Prepare data for insertion
def prepare_record(row):
    content = f"Question: {row['question']}\nAnswer: {row['answer']}"
    embedding = vec.get_embedding(content)
    return pd.Series(
        {
            "id": str(uuid_from_time(datetime.now())),
            "metadata": {
                "category": row["category"],
                "created_at": datetime.now().isoformat(),
            },
            "contents": content,
            "embedding": embedding,
        }
    )

# Apply the function to prepare records
records_df = df.apply(prepare_record, axis=1)
print("Prepared Records DataFrame:")
print(records_df)

# Save records_df to a CSV file
records_df["embedding"] = records_df["embedding"].apply(lambda x: str(x))  # Convert embeddings to strings for CSV storage
records_df["metadata"] = records_df["metadata"].apply(lambda x: str(x))    # Convert metadata to strings for CSV storage
records_df.to_csv(output_csv_path, index=False)

print(f"Processed data saved to {output_csv_path}") """

