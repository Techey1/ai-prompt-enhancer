# AI Prompt Enhancer

This project improves vague prompts and converts them into clear and structured AI instructions.

## Problem
Short prompts like "boss sick" or "write email" often produce poor AI results because they lack context and structure.
Focused area is office and education.
eg1: msg to boss sick leave take
eg2: climate changes

## Solution
This system enhances user prompts by automatically adding:
- Audience
- Tone
- Format
- Additional details

## AI Tools Used
- Hugging Face Transformers
- T5-small model
- Streamlit

## How to Run
1. Install libraries
pip install -r requirements.txt

2. Run the app
streamlit run app.py
