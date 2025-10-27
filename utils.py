import trafilatura
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

def clean_html_to_text(html):
    try:
        extracted = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=False,
            include_formatting=True
        )
        if extracted:
            return extracted
        else:
            return "Could not extract text from the provided HTML content."

    except Exception as e:
        return "{e} - Could not extract text from the provided HTML content."
    


def response_with_llm(user_prompt, system_prompt, model):

    llm = Groq()

    response = llm.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        model=model,
    )

    
    return response.choices[0].message.content
    
    
