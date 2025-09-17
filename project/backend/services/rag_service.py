import openai
from django.conf import settings

# Set the API key
openai.api_key = settings.OPENAI_API_KEY

def generate_answer(query: str, context: str):
    """
    Calls OpenAI API with query + context and returns the answer.
    Updated for openai>=1.0.0
    """
    try:
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant that answers questions based on provided context."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}\n\nAnswer based on the context:"}
            ],
            temperature=0,
            max_tokens=500
        )
        
        answer = response.choices[0].message.content.strip()
        return answer
        
    except Exception as e:
        return f"Error generating answer: {str(e)}"