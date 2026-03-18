import os
import re

# Folder containing .ass subtitle files
subtitle_dir = "/Users/prashanth/Documents/Yukino_AI/SE3"

# Output files
dialogue_output = "/Users/prashanth/Documents/Yukino_AI/output/yukino_SE3_dialogues.txt"
context_output = "/Users/prashanth/Documents/Yukino_AI/output/yukino_SE3_context.txt"

# List of keywords to detect Yukino
yukino_keywords = [
    "yukino", "yukinon", "yukinoshita", "yukinoshita yukino", 
    "雪ノ下", "雪乃", "ゆきのん", "ゆきの"
]

# Markers that imply contextual/internal monologue lines
context_markers = ["{\\i1}", "(", "...", "—", "--", "–", "…"]

# Storage for matches
dialogues = []
contexts = []

# Function to check if line is Yukino's
def is_yukino_line(text):
    return any(re.search(rf"\b{kw}\b", text, re.IGNORECASE) for kw in yukino_keywords)

# Sort files by season and episode order
def extract_season_episode(filename):
    match = re.search(r"S(\d+)_EP(\d+)", filename)
    if match:
        season = int(match.group(1))
        episode = int(match.group(2))
        return (season, episode)
    return (float('inf'), float('inf'))

ass_files = sorted(
    [f for f in os.listdir(subtitle_dir) if f.endswith(".ass")],
    key=extract_season_episode
)

# Process each file
for file in ass_files:
    filepath = os.path.join(subtitle_dir, file)
    with open(filepath, "r", encoding="latin-1") as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("Dialogue:"):
            parts = line.strip().split(",", 9)
            if len(parts) == 10:
                text = parts[9]

                if is_yukino_line(text):
                    dialogues.append(text)
                    if any(marker in text for marker in context_markers):
                        contexts.append(text)

print(f"✅ Found {len(dialogues)} Yukino dialogue lines.")
print(f"🧠 Found {len(contexts)} contextual lines.")

# Write outputs
os.makedirs(os.path.dirname(dialogue_output), exist_ok=True)

with open(dialogue_output, "w", encoding="utf-8") as f:
    for line in dialogues:
        f.write(line + "\n")

with open(context_output, "w", encoding="utf-8") as f:
    for line in contexts:
        f.write(line + "\n")

print(f"✅ Output saved to:\n- {dialogue_output}\n- {context_output}")
