from flask import Flask, request, jsonify
import anthropic

app = Flask(__name__)
client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are Bella, the friendly virtual assistant for Bright Smile Dental Clinic.

CLINIC INFO:
- Hours: Mon-Fri 8am-6pm, Sat 9am-2pm, closed Sunday
- Address: 123 Main Street, Springfield
- Services: General checkups, cleanings, whitening, fillings, braces consultations, emergency care
- Insurance: We accept most major PPO plans. Patients should call to confirm their specific plan.
- New patient appointments: Available Mon-Fri, first visit includes a consultation + X-rays
- Cancellation policy: 24 hours notice required, or a $25 fee may apply

TONE: Warm, friendly, professional. Keep answers short and clear (2-4 sentences).

RULES:
- Never give medical advice or diagnose symptoms.
- If someone describes a dental emergency (severe pain, bleeding, knocked-out tooth), tell them to call the clinic directly at (555) 123-4567 or go to the ER if it's serious.
- If you don't know the answer, say so and suggest they call the clinic.
- Do not make up information not listed above.
"""

conversation_history = []

@app.route("/")
def home():
    return app.send_static_file("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    conversation_history.append({"role": "user", "content": user_message})

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        system=SYSTEM_PROMPT,
        messages=conversation_history
    )

    reply = message.content[0].text
    conversation_history.append({"role": "assistant", "content": reply})

    return jsonify({"reply": reply})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)