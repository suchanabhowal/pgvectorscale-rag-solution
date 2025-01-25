import streamlit as st
import pandas as pd
#from synthesizer import Synthesizer, SynthesizedResponse  # Import your Synthesizer class
#from similarity_search import VectorSearch  # Assuming vec.search is part of this module
from database.vector_store import VectorStore
from services.synthesizer import Synthesizer,SynthesizedResponse

# Initialize the vector search (replace this with your actual setup)
vec = VectorStore()  # Adjust with the actual implementation

# Streamlit App Title
st.title("Legal Contract Query Assistant")
st.subheader("Analyze and answer questions about commercial legal contracts.")

# Input Section
user_query = st.text_input("Enter your query:", placeholder="E.g., Explain the discrepancy of ...")

# Submit Button
if st.button("Get Answer"):
    if not user_query.strip():
        st.warning("Please enter a query before submitting.")
    else:
        with st.spinner("Processing your query..."):
            try:
                # Perform the vector search
                results = vec.search(user_query, limit=3)

                # Log the columns in the context DataFrame
                st.write("Context DataFrame Columns:", results.columns.tolist())

                # Generate a response using the Synthesizer
                response: SynthesizedResponse = Synthesizer.generate_response(
                    question=user_query, context=results
                )
                # Display the results
                st.subheader("Synthesized Response")
                st.write(response.answer)

                st.subheader("Thought Process")
                for thought in response.thought_process:
                    st.write("- ", thought)

                st.subheader("Context Used")
                st.json(Synthesizer.dataframe_to_json(results, columns_to_keep=[
                    "content", "filename", "document_name", "exact_law", "parties"
                ]))

            except Exception as e:
                st.error(f"An error occurred: {e}")

# Footer
st.markdown("---")
st.markdown("Powered by **Streamlit** and **OpenAI**")
