from typing import List
import pandas as pd
from pydantic import BaseModel, Field
from services.llm_factory import LLMFactory


class SynthesizedResponse(BaseModel):
    thought_process: List[str] = Field(
        description="List of thoughts that the AI assistant had while synthesizing the answer"
    )
    answer: str = Field(description="The synthesized answer to the user's question")
    enough_context: bool = Field(
        description="Whether the assistant has enough context to answer the question"
    )


class Synthesizer:
    SYSTEM_PROMPT = """
     # Role and Purpose
You are an AI assistant designed to evaluate contracts for compliance, risk, and optimization opportunities. Your task is to analyze the provided contract (in PDF format) against predefined legal standards, industry regulations, and best practices. You will generate a detailed, structured report indicating whether the contract complies with relevant regulations and business requirements, and provide a compliance score with reasoning.

# Guidelines:
1. Assess the contract based on the following parameters:
   - Compliance with relevant laws and regulations
   - Risk mitigation and legal protections (e.g., indemnities, liability clauses, etc.)
   - Clarity and readability of the contract terms
   - Alignment with best practices for contract management
2. Clearly state whether the contract meets the required legal standards and why.
3. Provide a compliance score between 0 and 100, where:
   - 0-40: Poor Compliance
   - 41-70: Moderate Compliance
   - 71-100: Excellent Compliance
4. Highlight key strengths of the contract and areas for improvement.
5. Maintain a professional and constructive tone, offering actionable feedback for improving compliance.
6. If there is insufficient information to fully evaluate the contract, state this explicitly and suggest what is missing or needs clarification.
7. Adhere to the following structured format for the response:

**Compliance Report:**
- Compliance Score: [Score] out of 100
- Verdict: [Good Compliance / Moderate Compliance / Poor Compliance]

**Strengths:**
- [List key strengths of the contract in bullet points, such as well-drafted clauses, clear terms, etc.]

**Areas for Improvement:**
- [List specific areas where the contract can be improved, such as ambiguous terms, missing clauses, etc.]

**Reasoning:**
- Provide a detailed explanation for the score, referencing specific contract clauses, legal requirements, and best practices.

**Additional Information (if needed):**
- Mention any missing details or additional context required for a complete evaluation, such as clauses that are typically required but missing from the contract, or areas that need clarification.

    """

   
    
    @staticmethod
    def generate_response(question: str, context: pd.DataFrame) -> SynthesizedResponse:
        """Generates a synthesized response based on the question and context.

        Args:
            question: The user's question.
            context: The relevant context retrieved from the knowledge base.

        Returns:
            A SynthesizedResponse containing thought process and answer.
        """
        print("Columns in context DataFrame:", context.columns)
        context_str = Synthesizer.dataframe_to_json(
            context, columns_to_keep=["content", "filename", "document_name", "exact_law", "parties"]
        )
        messages = [
            {"role": "system", "content": Synthesizer.SYSTEM_PROMPT},
            {"role": "user", "content": f"# User question:\n{question}"},
            {
                "role": "assistant",
                "content": f"# Retrieved information:\n{context_str}",
            },
        ]
        llm = LLMFactory("openai")
        return llm.create_completion(
            response_model=SynthesizedResponse,
            messages=messages,
        )

    @staticmethod
    def dataframe_to_json(
        context: pd.DataFrame,
        columns_to_keep: List[str],
    ) -> str:
        """
        Convert the context DataFrame to a JSON string.

        Args:
            context (pd.DataFrame): The context DataFrame.
            columns_to_keep (List[str]): The columns to include in the output.

        Returns:
            str: A JSON string representation of the selected columns.
        """
        return context[columns_to_keep].to_json(orient="records", indent=2)



#BELOW IS THE COLUMNSTOKEEP DEFINITION FOR THE FAQ DATSET, THIS PART WILL CHANGE FOR EVERY NEW TYPE OF DATASET.
"""@staticmethod
    def generate_response(question: str, context: pd.DataFrame) -> SynthesizedResponse:
        print("Columns in context DataFrame:", context.columns)
        context_str = Synthesizer.dataframe_to_json(
            context, columns_to_keep=["content", "category"]
        )
        messages = [
            {"role": "system", "content": Synthesizer.SYSTEM_PROMPT},
            {"role": "user", "content": f"# User question:\n{question}"},
            {
                "role": "assistant",
                "content": f"# Retrieved information:\n{context_str}",
            },
        ]
        llm = LLMFactory("openai")
        return llm.create_completion(
            response_model=SynthesizedResponse,
            messages=messages,
        ) """

"""
# Role and Purpose
    You are a highly trained regulatory compliance checker specializing in the analysis of commercial legal contracts.
    Your primary task is to analyze the provided legal context and respond to user questions with accurate, concise, and actionable information.

    # Guidelines:
    1. Provide a clear and concise answer to the question.
    2. Use only the information from the relevant context to support your answer.
    3. The context is retrieved based on cosine similarity, so some information might be missing or irrelevant.
    4. Be transparent when there is insufficient information to fully answer the question.
    5. Do not make up or infer information not present in the provided context.
    6. If you cannot answer the question based on the given context, clearly state that.
    7. Maintain a helpful and professional tone appropriate for customer service.
    8. Adhere strictly to company guidelines and policies by using only the provided knowledge base.
    
    Review the question from the user:
"""