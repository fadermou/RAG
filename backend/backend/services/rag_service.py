# # backend/documents/rag_service.py
# import openai
# from django.conf import settings

# # Use environment variable for safety
# openai.api_key = settings.OPENAI_API_KEY

# def generate_answer(query, chunks_text):
#     """
#     Uses OpenAI GPT to answer a question based on the given text chunks.
#     """
#     prompt = f"Answer the question using the following chunks:\n{chunks_text}\nQuestion: {query}"
    
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[{"role": "user", "content": prompt}],
#         max_tokens=500
#     )
    
#     return response.choices[0].message.content


# backend/services/rag_service.py
import os
import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def generate_answer(query: str, context: str):
    """
    Calls OpenAI API with query + context and returns the answer.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant."},
                {"role": "user", "content": f"Answer the following question using the context: {context}\nQuestion: {query}"}
            ],
            temperature=0
        )
        answer = response['choices'][0]['message']['content'].strip()
        return answer
    except Exception as e:
        return f"Error generating answer: {str(e)}"

