from docs_listener import extract_text_from_doc
from gemini_nlp_extractor import extract_journal_info
from calendar_task_sync import create_calendar_event, create_task
import os,re
import json
from dotenv import load_dotenv

load_dotenv()

def extract_plain_text_from_doc(doc):
    """
    Extracts plain text from a full Google Docs API document dictionary.
    """
    text = ""
    for element in doc.get("body", {}).get("content", []):
        if "paragraph" in element:
            for p_element in element["paragraph"].get("elements", []):
                text += p_element.get("textRun", {}).get("content", "")
    return text.strip()

def main():
    # Get Google Doc ID from environment variables
    doc_id = "11NjQ6cJG7D-pQVwi76f6d0gxXo87Yw3zK7oBXIFZGUQ"
    
    # Fetch full Google Doc (dict format)
    doc = extract_text_from_doc(doc_id)

    # Extract plain text from the doc
    note_text = extract_plain_text_from_doc(doc)
    print("📖 Note:\n", note_text)

    # Extract journal information using Gemini NLP
    response_json = extract_journal_info(note_text)
    print("🔍 Gemini Response:\n", response_json)

    # Try parsing the JSON response from Gemini
    try:
        cleaned_json = re.sub(r"```json|```", "", response_json).strip()
        extracted = json.loads(cleaned_json)
    except Exception as e:
        print("⚠️ Unable to parse Gemini response:", e)
        return

    # Create Calendar Events
    for event in extracted.get("events", []):
        link = create_calendar_event(event["description"], event["datetime"])
        print(f"🗓 Event Created: {link}")

    # Create Google Tasks
    for task in extracted.get("tasks", []):
        task_id = create_task(task["description"], task.get("due_date"))
        print(f"✅ Task Created: {task_id}")

    # Ensure logs folder exists
    os.makedirs("logs", exist_ok=True)

    # Log the extracted data into a summary file
    with open("logs/summary.json", "w") as log:
        json.dump(extracted, log, indent=2)
    print("📦 Actions saved to logs/summary.json")

if __name__ == "__main__":
    main()
