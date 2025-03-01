# from transformers import GPTNeoForCausalLM, GPT2Tokenizer

# # Load GPT-Neo model and tokenizer
# model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")
# tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")

# def analyze_code(code: str):
#     inputs = tokenizer(code, return_tensors="pt")
#     outputs = model.generate(**inputs, max_length=200)
#     return tokenizer.decode(outputs[0], skip_special_tokens=True)


# import openai
# from app.core.config import settings

# # Set up OpenAI API
# openai.api_key = settings.OPENAI_API_KEY

# def analyze_code(code: str):
#     """
#     Analyze the code using OpenAI Codex and return suggestions.
#     """
#     try:
#         response = openai.Completion.create(
#             engine="code-davinci-002",  # Use the Codex model
#             prompt=f"Analyze the following code for syntax errors, performance issues, and provide suggestions:\n\n{code}\n\nAnalysis:",
#             max_tokens=200,  # Limit the response length
#             temperature=0.5,  # Control creativity (0 = deterministic, 1 = creative)
#         )
#         return response.choices[0].text.strip()
#     except Exception as e:
#         return f"Error analyzing code: {str(e)}"
    
    
# from transformers import pipeline

# # Load a code analysis model
# code_analyzer = pipeline("text-generation", model="microsoft/CodeGPT-small-py")

# def analyze_code(code: str):
#     """
#     Analyze the code using Hugging Face Transformers and return suggestions.
#     """
#     try:
#         result = code_analyzer(code)
#         return result[0]["generated_text"]
#     except Exception as e:
#         return f"Error analyzing code: {str(e)}"

import google.generativeai as genai
from app.core.config import settings  # Assuming you have a settings module

# Configure Gemini API
genai.configure(api_key=settings.GOOGLE_API_KEY)  # Replace with your actual key name

def analyze_code(code: str):
    """
    Analyze the code using Google Gemini and return suggestions.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')  # Or 'gemini-pro-vision' if you need image input.
        prompt = f"Analyze the following code for syntax errors, performance issues, and provide suggestions:\n\n{code}\n\nAnalysis:"

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error analyzing code: {str(e)}"