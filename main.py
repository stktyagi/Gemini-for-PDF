import pdfplumber
import google.generativeai as genai

genai.configure(api_key="api key here")

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)


def extract_pdf_pages(pathname):
    parts = []
    with pdfplumber.open(pathname) as pdf:
        page_number = 1
        for page in pdf.pages:
            text = page.extract_text()
            parts.append(f"--- PAGE {page_number} ---\n{text}")
            page_number += 1
    return parts

convo = model.start_chat(
    history=[
  {
    "role": "user",
    "parts": extract_pdf_pages("file path here")
  },
])
inp=input("Enter your question: ")
convo.send_message(inp)
print(convo.last.text)
