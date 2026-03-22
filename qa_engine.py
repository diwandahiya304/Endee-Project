import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def answer_question(question, context_chunks):
    context = "\n\n---\n\n".join(context_chunks)

    prompt = f"""You are a helpful assistant that answers questions based on a document.
Use ONLY the information provided in the context below to answer the question.
If the answer is not in the context, say "I couldn't find this information in the document."

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""

    response = groq_client.chat.completions.create(
       model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=512
    )

    return response.choices[0].message.content.strip()