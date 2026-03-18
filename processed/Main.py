from pathlib import Path
import json
import torch
from sentence_transformers import SentenceTransformer, util

# === SETUP ===

# Load semantic model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load context-response pairs
DATA_FILE = "/Users/prashanth/Documents/Yukino_AI/processed/yukino_context_response_pairs_final.json"
data = json.loads(Path(DATA_FILE).read_text(encoding="utf-8"))

# Precompute embeddings for all contexts
contexts = [" ".join(pair["context"]) for pair in data]
context_embeddings = model.encode(contexts, convert_to_tensor=True)

# Yukino-style keywords to boost personality accuracy
yukino_keywords = [
    "refuse", "nonsense", "common sense", "pathetic", "I see", "so you think",
    "how foolish", "why would I", "you should", "petty", "lecherous", "I don’t", "do you think",
    "shallow", "don’t assume", "stop pretending", "unnecessary", "delusional"
]

# === HELPER FUNCTIONS ===

def score_response(response: str) -> float:
    """
    Scores a response based on length and Yukino-style tone markers.
    """
    score = len(response) * 0.05  # Favor slightly longer responses
    score += sum(1 for kw in yukino_keywords if kw in response.lower()) * 1.0  # Keyword boost
    return score

def clean_prefix(response: str) -> str:
    """
    Removes multiple speaker name prefixes and adds clean Yukino prefix.
    """
    while any(response.lower().startswith(prefix) for prefix in ("yukino:", "yukinoshita:", "yuki:")):
        response = response.partition(":")[2].strip()
    return "Yukino: " + response

# === CHAT LOOP ===

def chat():
    print("Yukino: Say something or don’t. I’m not here to entertain.")
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit", "bye"}:
            print("Yukino: Finally, some peace and quiet.")
            break

        # Embed user input
        input_embedding = model.encode(user_input, convert_to_tensor=True)

        # Compute similarity with all context embeddings
        cosine_scores = util.pytorch_cos_sim(input_embedding, context_embeddings)[0]

        # Get top 5 matches
        top_k = 5
        top_results = torch.topk(cosine_scores, k=top_k)

        reranked = []
        for i in range(top_k):
            idx = top_results.indices[i].item()
            raw_response = data[idx]["response"]
            cleaned = clean_prefix(raw_response)
            character_score = score_response(cleaned)
            reranked.append((character_score, cleaned, cosine_scores[idx].item()))

        # Rerank by personality score + return best
        reranked.sort(reverse=True)
        best_score, response, similarity_score = reranked[0]

        # Fallback for very poor matches
        if similarity_score < 0.30:
            print("Yukino: That doesn’t even make sense. Try again.")
            continue

        print(f"[DEBUG] Match Score: {similarity_score:.2f} | Rerank Score: {best_score:.2f}")
        print(response)

# === RUN ===

if __name__ == "__main__":
    chat()
