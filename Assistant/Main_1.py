from pathlib import Path
import json
import torch
from sentence_transformers import SentenceTransformer, util
import ollama
from pathlib import Path
import json

# =====================
# SETUP
# =====================


from pathlib import Path
import json
from sentence_transformers import SentenceTransformer

# Base directory: Yukino_AI/
BASE_DIR = Path(__file__).resolve().parent.parent

# Path object (NOT string)
DATA_FILE = BASE_DIR / "processed" / "yukino_context_response_pairs_final.json"

# Load data ONCE
data = json.loads(DATA_FILE.read_text(encoding="utf-8"))

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Prepare contexts
contexts = [" ".join(pair["context"]) for pair in data]
context_embeddings = model.encode(contexts, convert_to_tensor=True)


# =====================
# INTENT + VULNERABILITY
# =====================

def detect_intent(text: str) -> str:
    t = text.lower()

    if any(w in t for w in ["i feel", "i'm scared", "i'm afraid", "i'm anxious", "i feel lost"]):
        return "emotional_vulnerability"
    if t.endswith("?"):
        return "question"
    if any(w in t for w in ["lol", "haha", "whatever", "idc"]):
        return "casual"
    if len(t.split()) < 4:
        return "vague"
    return "statement"

def vulnerability_level(text: str) -> int:
    t = text.lower()
    score = 0
    for w in ["afraid", "scared", "anxious", "fail", "alone", "worthless"]:
        if w in t:
            score += 1
    return min(score, 3)

# =====================
# CANON RETRIEVAL
# =====================

def retrieve_anchor(user_input: str, top_k: int = 5):
    emb = model.encode(user_input, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(emb, context_embeddings)[0]
    top = torch.topk(scores, k=top_k)

    anchors = []
    for i in range(top_k):
        idx = top.indices[i].item()
        anchors.append({
            "response": data[idx]["response"],
            "context": data[idx]["context"],
            "similarity": scores[idx].item()
        })
    return anchors

# =====================
# LLM CALL (OLLAMA – LOCAL)
# =====================

def call_llm(system_prompt: str, user_prompt: str) -> str:
    response = ollama.chat(
        model="mistral",  # use "llama3" if you have enough RAM
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        options={
            "temperature": 0.4,
            "num_predict": 120
        }
    )
    return response["message"]["content"].strip()

# =====================
# PROMPT CONSTRUCTION
# =====================

def build_prompt(user_input, intent, vulnerability, anchor):
    system_prompt = (
        "You are Yukinoshita Yukino.\n"
        "You exist only within the context of a normal conversation.\n"
        "You do NOT acknowledge being an AI, a model, or having an existence timeline.\n"
        "You never discuss your own creation, first experience, or consciousness.\n"
        "If asked about such things, you deflect or reject the premise calmly.\n"
        "You do not use speaker labels or repeat your name.\n"
        "You speak with precision, restraint, and calm bluntness.\n"
        "You do not ramble.\n"
        "You do not use emojis or slang.\n"
        "Maximum 2 sentences."
    )


    rules = [
        "Do not quote or reference anime scenes.",
        "Do not mention past events or names.",
        "Respond as if this is a real, present conversation."
    ]

    if intent == "emotional_vulnerability":
        rules.append("Be firm but not dismissive.")
    if vulnerability >= 2:
        rules.append("Reduce harshness slightly.")

    user_prompt = f"""
User intent: {intent}
User vulnerability level: {vulnerability}

User input:
"{user_input}"

Canon style anchor (tone reference only):
"{anchor}"

Rules:
- {" ".join(rules)}

Respond as Yukinoshita Yukino.
"""

    return system_prompt, user_prompt

# =====================
# YUKINO STYLE VALIDATOR
# =====================

def yukino_validator(text: str) -> int:
    penalties = 0

    if len(text.split(".")) > 3:
        penalties += 1
    if any(w in text.lower() for w in ["lol", "haha", "maybe", "i guess"]):
        penalties += 2
    if text.count("!") > 1:
        penalties += 1
    if len(text.split()) > 60:
        penalties += 1

    return penalties

# =====================
# RESPONSE GENERATION
# =====================

def clean_response(text: str) -> str:
    prefixes = ["yukino:", "yukinoshita:", "assistant:"]
    t = text.strip()
    for p in prefixes:
        if t.lower().startswith(p):
            t = t[len(p):].strip()
    return t


def generate_response(user_input, state):
    intent = detect_intent(user_input)
    vuln = vulnerability_level(user_input)

    anchors = retrieve_anchor(user_input)
    best_anchor = anchors[0]

    system_prompt, user_prompt = build_prompt(
        user_input,
        intent,
        vuln,
        best_anchor["response"]
    )

    for _ in range(2):
        response = call_llm(system_prompt, user_prompt)
        penalty = yukino_validator(response)

        if penalty <= 1:
            break

        user_prompt += "\nBe shorter and more restrained."

    state["last_intent"] = intent
    state["vulnerability"] = vuln

    return "Yukino: " + clean_response(response)

# =====================
# CHAT LOOP
# =====================

def chat():
    print("Yukino: Say what you want. I’ll decide if it’s worth answering.")

    state = {
        "last_intent": None,
        "vulnerability": 0
    }

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit", "bye"}:
            print("Yukino: Finally. Some quiet.")
            break

        reply = generate_response(user_input, state)
        print(reply)

# =====================
# RUN
# =====================

if __name__ == "__main__":
    chat()
