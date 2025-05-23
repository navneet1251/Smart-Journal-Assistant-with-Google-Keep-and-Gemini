import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_journal_info(note_text):
    prompt = f"""
Extract the following from this journal entry:

1. Tasks (with due dates if mentioned)
2. Calendar events (with datetime)
3. Tags - generate relevant hashtags like #todo, #meeting, #reminder, #idea based on the context. Even if they are not explicitly written, infer them.


Journal:
\"\"\"
{note_text}
\"\"\"

Return as JSON with keys: tasks, events, tags. Extract tasks and events from the journal in this strict JSON format only without backticks or explanation.
"""
    response = model.generate_content(prompt)
    return response.text

# Example usage:
if __name__ == "__main__":
    sample_note = "Team call Friday at 10am. Need to book flight by Wednesday. Think about project X."
    print(extract_journal_info(sample_note))
