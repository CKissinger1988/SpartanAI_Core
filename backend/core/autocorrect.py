import re

def normalize_text(text):
    # Enforce case-insensitive standards
    text = text.lower()
    
    # Simple autocorrect dictionary - expandable to full RAG model
    corrections = {
        "jarvis": "Jarvis",
        "hexstrike": "Hexstrike"
    }
    
    for word, correct in corrections.items():
        text = text.replace(word, correct)
    
    return text
