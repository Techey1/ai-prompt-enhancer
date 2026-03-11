import streamlit as st
from transformers import pipeline
import re

st.set_page_config(page_title="AI Prompt Enhancer")
st.title("🧠 AI Prompt Enhancer")

prompt = st.text_area("Enter your prompt", height=120)

@st.cache_resource
def load_model():
    pipe = pipeline(
        "text2text-generation",
        model="t5-small",
        tokenizer="t5-small"
    )
    return pipe

generator = load_model()

def get_custom_reason(text_lower):
    """Customizable reason detection - MODIFY THIS DICTIONARY"""
    reason_map = {
        'sick': ['sick', 'ill', 'fever', 'not well', 'unwell', 'health issue'],
        'family': ['family', 'kid', 'child', 'home', 'emergency'],
        'weather': ['rain', 'storm', 'weather', 'flood'],
        'transport': ['traffic', 'bus', 'train', 'car broke', 'vehicle'],
        'medical': ['doctor', 'dentist', 'hospital', 'appointment'],
        'tired': ['tired', 'exhausted', 'fatigue']
    }
    
    for reason_key, keywords in reason_map.items():
        if any(keyword in text_lower for keyword in keywords):
            # CUSTOMIZE THESE PHRASES HERE
            reason_phrases = {
                'sick': 'high fever and body pain',
                'family': 'family medical emergency', 
                'weather': 'heavy rainfall',
                'transport': 'major traffic congestion',
                'medical': 'dental appointment',
                'tired': 'extreme fatigue'
            }
            return reason_phrases.get(reason_key, reason_key.replace('_', ' ').title())
    
    return "urgent personal matter"  # YOUR DEFAULT

def enhance_prompt(text):
    text = text.strip()
    
    instruction = f"""Improve vague prompts into clear instructions.

boss sick → Write polite message to boss about being sick and taking leave today.
global warming → Explain global warming: causes, effects, solutions.
assignment → Help write assignment with structure and examples.

{text} →"""

    result = generator(
        instruction,
        max_new_tokens=60,
        num_beams=2,
        repetition_penalty=2.0,
        do_sample=False,
        early_stopping=True
    )

    output = result[0]["generated_text"].strip()

    original_text = text.lower()
    words = original_text.split()
    for word in words:
        pattern = re.escape(word)
        output = re.sub(f'\\\\b{pattern}\\\\b.{1,3}', '', output, count=3)
    output = re.sub(r'→.*|→', '', output).strip()

    text_lower = text.lower()
    key_words = [w for w in words if len(w) > 2]  # Filter short words
    
    if any(word in text_lower for word in ['boss', 'msg', 'office', 'sick','hello','email','manager']):
        reason = get_custom_reason(text_lower)
        output = f"""Write a professional message to my boss explaining {reason}. 
        Include polite greeting, brief explanation, work coverage plan, expected return time, and courteous closing."""
    
    elif any(word in text_lower for word in ['global', 'warming', 'climate']):
        output = f"""Explain {text} comprehensively: causes (CO2 emissions, deforestation), effects 
        (temperature rise, extreme weather), evidence (scientific data), solutions (renewable energy, 
        policy changes), and current global impact."""
    
    elif any(word in text_lower for word in ['assign', 'homework', 'study', 'exam', 'teacher']):
        topic = text if len(text.split()) > 1 else "this subject"
        output = f"""Help me complete my {topic}: provide clear step-by-step guidance, relevant examples, 
        simple explanations, logical structure, key concepts, and practice questions."""
    
    else:
        topic = text.title()
        output = f"""Provide detailed explanation of {topic} covering: definition, key components, 
        real-world examples, benefits/challenges, current trends, and practical applications."""
    
    return output

def analyze_prompt(text):
    words = len(text.split())
    return min(words * 0.8, 10), min(words / 5, 10), 5

if st.button("✨ Enhance Prompt", type="primary"):
    if not prompt.strip():
        st.warning("Please enter a prompt")
    else:
        with st.spinner("Enhancing..."):
            enhanced = enhance_prompt(prompt)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📝 Original")
            st.code(prompt, language="text")
        with col2:
            st.subheader("✨ Enhanced")
            st.success(enhanced)

        clarity, specificity, _ = analyze_prompt(prompt)
        st.metric("Quality Score", f"{(clarity + specificity)/2:.1f}/10")
