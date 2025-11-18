# AIChatbot.py
# Full, copy-paste ready chatbot including "ask to generate prescription" feature.
# Requires: prescription_generator.py in same folder with generate_prescription_file() function.
# Also requires google-generativeai installed and configured, and python-docx for prescription generation.

import google.generativeai as genai
import random
import re

# ---------- IMPORT THE PRESCRIPTION MODULE (Step 1: top import) ----------
from prescription_generator import generate_prescription_file

# -----------------------------------------------------
# Configure Gemini API Key - replace with your key
# -----------------------------------------------------
genai.configure(api_key="##############################")   # <-- put your key here

# -----------------------------------------------------
# System Instruction
# -----------------------------------------------------
system_instruction = (
    "You are a Doctor. Use a professional and clinical tone. "
    "Ask one question at a time. First ask for symptoms, then duration, then allergies. "
    "Keep responses short (1–3 lines). "
    "Use the local medical knowledge base to suggest medicines. "
    "If the user is allergic, avoid allergens and suggest alternatives. "
    "If no match is found, analyze symptoms using concise clinical reasoning."
)

# -----------------------------------------------------
# Medical Knowledge Base (with stored allergy conflicts)
# You can expand this JSON with more diseases, ingredients, alternatives, dosage, med_days.
# -----------------------------------------------------
MEDICAL_DB = [
    {
        "disease": "viral fever",
        "keywords": ["fever", "weakness", "body pain", "temperature"],
        "min_days": 2,
        "max_days": 3,
        "medicine": "Dolo 650",
        "ingredients": ["paracetamol", "acetaminophen"],
        "allergy_conflicts": ["paracetamol", "acetaminophen"],
        "alternative_medicine": "Ibuprofen 200mg",
        # optional dosage info (used for prescription generation)
        "dosage": "Take 1 tablet every 8 hours after food.",
        "med_days": 3
    },
    {
        "disease": "fever with cold and cough",
        "keywords": ["fever", "cold", "cough", "high temperature"],
        "min_days": 5,
        "max_days": 6,
        "medicine": "ABC Tablet",
        "ingredients": ["abc-compound"],
        "allergy_conflicts": ["abc-compound"],
        "alternative_medicine": "Crocin 500",
        "dosage": "Take 1 tablet every 8 hours after food.",
        "med_days": 5
    }
]

# -----------------------------------------------------
# Helper: simple keyword extractor (keeps raw text normalized)
# -----------------------------------------------------
def extract_keywords(text):
    return text.lower().strip()

# -----------------------------------------------------
# Duration extractor (supports "2 to 3 days", "from two to three days", "2 days", "yesterday")
# -----------------------------------------------------
def extract_duration(text):
    text = text.lower().strip()

    word_to_num = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
    }

    # digits first
    nums = re.findall(r"\d+", text)
    if nums:
        return int(nums[0])

    # number words
    words = re.findall(r"\b(one|two|three|four|five|six|seven|eight|nine|ten)\b", text)
    if words:
        return word_to_num[words[0]]

    # fallback common terms
    if "yesterday" in text:
        return 1
    if "today" in text and "since" in text:
        return 1
    if "day before yesterday" in text:
        return 2

    return None

# -----------------------------------------------------
# Match disease with keyword substring match + duration range
# -----------------------------------------------------
def match_disease(user_text, duration):
    for entry in MEDICAL_DB:
        # check whether any of the DB keywords appear in the user's text
        if any(keyword in user_text for keyword in entry["keywords"]):
            if entry["min_days"] <= duration <= entry["max_days"]:
                return entry
    return None

# -----------------------------------------------------
# Check allergy conflicts against stored allergy_conflicts in DB entry
# -----------------------------------------------------
def check_allergy_conflict(allergy_text, entry):
    allergy_text = (allergy_text or "").lower()
    for allergen in entry.get("allergy_conflicts", []):
        if allergen in allergy_text:
            return True  # conflict found
    return False  # no conflict

# -----------------------------------------------------
# Diagnosis sentence variations (professional style)
# -----------------------------------------------------
DIAGNOSIS_LINES = [
    "These findings suggest {disease}. {medicine} is appropriate.",
    "The symptoms and duration align with {disease}. {medicine} may be used.",
    "This pattern matches {disease}. {medicine} is suitable.",
    "This condition is indicative of {disease}. {medicine} can be taken.",
    "Based on the provided details, {disease} is likely. {medicine} is recommended."
]

ALTERNATIVE_LINES = [
    "Considering the allergy, {alt_medicine} is appropriate.",
    "The symptoms and allergy profile align better with {alt_medicine}.",
    "To avoid allergic conflict, {alt_medicine} is suitable.",
    "Based on the provided allergy details, {alt_medicine} is recommended.",
    "This condition remains manageable, and {alt_medicine} is a safer option."
]

# -----------------------------------------------------
# Helper: ask user if they want a prescription file (Step 2 helper)
# (This is the small function you add near other helpers)
# -----------------------------------------------------
def user_wants_prescription():
    choice = input("Chatbot: Would you like a prescription for this? (yes/no): ").strip().lower()
    return choice in ["yes", "y", "sure", "ok", "yes please", "yesplease", "ofcourse", "off course"]

# -----------------------------------------------------
# Initialize Gemini model (no web tools used here)
# -----------------------------------------------------
model = genai.GenerativeModel(
    model_name="models/gemini-flash-latest",
    system_instruction=system_instruction
)

chat = model.start_chat(history=[])

# -----------------------------------------------------
# Main conversation loop
# -----------------------------------------------------
print("Medical Chatbot Activated. Type 'exit' to quit.\n")
print("Chatbot: Hello. How can I assist you today?\n")

stage = "ask_symptoms"     # stages: ask_symptoms -> ask_duration -> ask_allergy
user_text = ""
user_duration = None
user_allergy = ""

while True:
    try:
        user_msg = input("You: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nChatbot: Session ended.")
        break

    if not user_msg:
        # if empty input, re-prompt relevant question
        if stage == "ask_symptoms":
            print("Chatbot: Please describe the symptoms.")
        elif stage == "ask_duration":
            print("Chatbot: Please specify the duration in days.")
        elif stage == "ask_allergy":
            print("Chatbot: Please specify allergies (or 'none').")
        continue

    if user_msg.lower() in ["exit", "quit", "bye"]:
        print("Chatbot: Thank you. Session closed.")
        break

    # ---------------------------
    # Stage 1: Gather symptoms
    # ---------------------------
    if stage == "ask_symptoms":
        
        # User's first message is just the problem description.
        # Bot must NOT treat it as symptoms directly.
        print("Chatbot:", random.choice([
            "Please describe all symptoms clearly.",
            "Kindly list the symptoms you are experiencing.",
            "Tell me the symptoms you have noticed."
        ]))
        
        # Move to next stage where actual symptoms will be given
        stage = "collect_symptoms"
        continue

    # NEW BLOCK
    if stage == "collect_symptoms":
        user_text = extract_keywords(user_msg)
        
        print("Chatbot:", random.choice([
            "How many days have these symptoms been present?",
            "Specify the duration in days.",
            "For how long have these symptoms continued?"
        ]))
        
        stage = "ask_duration"
        continue


    # ---------------------------
    # Stage 2: Gather duration
    # ---------------------------
    if stage == "ask_duration":
        duration = extract_duration(user_msg)
        if duration is None:
            print("Chatbot:", random.choice([
                "Mention the duration in days.",
                "Please specify the number of days.",
                "State for how many days this has been happening."
            ]))
            continue
        user_duration = duration

        # Now ask allergy information
        print("Chatbot:", random.choice([
            "Do you have any known allergies?",
            "Please mention if you are allergic to any medicine or ingredient.",
            "Specify allergies, if any."
        ]))
        stage = "ask_allergy"
        continue

    # ---------------------------
    # Stage 3: Gather allergies & Analyze
    # ---------------------------
    if stage == "ask_allergy":
        user_allergy = user_msg.lower().strip()
        # Attempt to match in local DB
        result = match_disease(user_text, user_duration)

        if result:
            # Check allergy conflict
            conflict = check_allergy_conflict(user_allergy, result)

            if not conflict:
                # -------------- CASE A: Matched + safe medicine --------------
                reply = random.choice(DIAGNOSIS_LINES).format(
                    disease=result["disease"],
                    medicine=result["medicine"]
                )
                print("\nChatbot:", reply, "\n")

                # ---------- ASK whether to generate prescription (Step 3: prescription prompt) ----------
                if user_wants_prescription():
                    # Use dosage and med_days from DB if available, else defaults
                    dosage_instruction = result.get("dosage", "Take 1 tablet every 8 hours after food.")
                    medication_days = result.get("med_days", 3)

                    patient_name = input("Chatbot: Please enter the patient's name for the prescription: ").strip()
                    file_path = generate_prescription_file(
                        patient_name=patient_name or "Patient",
                        symptoms=user_text,
                        duration=user_duration,
                        allergy=user_allergy,
                        diagnosis=result["disease"],
                        medicine=result["medicine"],
                        dosage=dosage_instruction,
                        med_days=medication_days
                    )
                    print(f"Chatbot: Your prescription has been generated: {file_path}\n")
                else:
                    print("Chatbot: Alright. Let me know if you need anything else.\n")

            else:
                # -------------- CASE B: Matched but allergy conflict -> recommend alternative --------------
                alt_reply = random.choice(ALTERNATIVE_LINES).format(
                    alt_medicine=result["alternative_medicine"]
                )
                print("\nChatbot:", alt_reply, "\n")

                # ---------- ASK whether to generate prescription for the alternative ----------
                if user_wants_prescription():
                    dosage_instruction = result.get("dosage", "Take 1 tablet every 8 hours after food.")
                    medication_days = result.get("med_days", 3)

                    patient_name = input("Chatbot: Please enter the patient's name for the prescription: ").strip()
                    file_path = generate_prescription_file(
                        patient_name=patient_name or "Patient",
                        symptoms=user_text,
                        duration=user_duration,
                        allergy=user_allergy,
                        diagnosis=result["disease"],
                        medicine=result["alternative_medicine"],
                        dosage=dosage_instruction,
                        med_days=medication_days
                    )
                    print(f"Chatbot: A safe prescription has been generated based on your allergy: {file_path}\n")
                else:
                    print("Chatbot: Understood. Let me know if you need anything else.\n")

            # Reset state after handling
            stage = "ask_symptoms"
            user_text = ""
            user_duration = None
            user_allergy = ""
            print("Chatbot: How else may I assist you?\n")
            continue

        # ---------------------------
        # No local match — Agentic LLM fallback
        # ---------------------------
        print("Chatbot: Analyzing medically...")

        agentic_prompt = (
            "You are a medical diagnosis system. Do NOT ask any follow-up questions. "
            "Provide a short, professional conclusion in 2–3 lines: likely condition, one-line rationale, and a recommended medicine. "
            f"Symptoms: {user_text}\n"
            f"Duration: {user_duration} days\n"
            f"Allergies: {user_allergy}\n"
        )

        # Use model.generate_content for your SDK version
        response = model.generate_content(agentic_prompt)
        agentic_reply = response.text.strip()

        # Print agentic reply
        print("Chatbot:", agentic_reply, "\n")

        # Ask if user wants a prescription based on agentic reply
        if user_wants_prescription():
            # we will ask patient name; medicine/dosage are not structured here
            # so we use the LLM reply text as 'diagnosis' and 'medicine' field
            patient_name = input("Chatbot: Please enter the patient's name for the prescription: ").strip()
            # default dosage and med_days for an LLM-produced recommendation
            dosage_instruction = "Take medication as advised: follow the prescription instructions."
            medication_days = 3

            file_path = generate_prescription_file(
                patient_name=patient_name or "Patient",
                symptoms=user_text,
                duration=user_duration,
                allergy=user_allergy,
                diagnosis=agentic_reply.splitlines()[0] if agentic_reply else "Clinical summary",
                medicine="Refer to LLM suggestion (see above).",
                dosage=dosage_instruction,
                med_days=medication_days
            )
            print(f"Chatbot: Prescription generated: {file_path}\n")
        else:
            print("Chatbot: Alright. Let me know if you need anything else.\n")

        # reset state
        stage = "ask_symptoms"
        user_text = ""
        user_duration = None
        user_allergy = ""
        print("Chatbot: How else may I assist you?\n")
        continue

    # default fallback outside of main states
    print("Chatbot: I did not understand that. Please describe symptoms, duration, or say 'exit' to quit.")
