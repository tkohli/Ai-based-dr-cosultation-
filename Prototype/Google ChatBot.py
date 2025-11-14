import google.generativeai as genai

# -------------------------------------------------
#  Configure Gemini API Key
# -------------------------------------------------
genai.configure(api_key="###")

# -------------------------------------------------
#  System instruction (medical chatbot personality)
# -------------------------------------------------
system_instruction = (
    "You are a medical assistant chatbot. "
    "Provide general information about symptoms, causes, and basic home remedies. "
    "Do not prescribe strong medicines or treatments. "
    "Encourage consulting a certified doctor when needed."
)

# -------------------------------------------------
#  Choose the correct model (from your list)
# -------------------------------------------------
MODEL_NAME = "models/gemini-flash-latest"
# Alternative (more powerful): MODEL_NAME = "models/gemini-pro-latest"

# Initialize chatbot
model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    system_instruction=system_instruction
)

chat = model.start_chat(history=[])

print("Medical Chatbot is now active. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Chatbot: Take care! Goodbye.")
        break

    try:
        response = chat.send_message(user_input)
        print("Chatbot:", response.text)
    except Exception as e:
        print("Error:", e)
