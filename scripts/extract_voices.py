import os
import re

subtitle_dir = "/Users/prashanth/Documents/Yukino_AI/new_sub_files"
dialogue_output_path = "/Users/prashanth/Documents/Yukino_AI/output/yukino_dialogues.txt"
context_output_path = "/Users/prashanth/Documents/Yukino_AI/output/yukino_context.txt"

yukino_lines = []
yukino_context_lines = []


def extract_season_episode(filename):
    match = re.search(r"S(\d+)_EP(\d+)", filename)
    if match:
        season = int(match.group(1))
        episode = int(match.group(2))
        return season, episode
    return float('inf'), float('inf')


# Sort .ass files like S1_EP2, S2_EP4 etc.
ass_files = sorted(
    [f for f in os.listdir(subtitle_dir) if f.endswith(".ass")],
    key=extract_season_episode
)

for filename in ass_files:
    filepath = os.path.join(subtitle_dir, filename)
    with open(filepath, "r", encoding="latin-1") as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("Dialogue"):
            parts = line.strip().split(",", 9)
            if len(parts) == 10:
                dialogue_text = parts[9]

                # Match Yukino's name (case-insensitive)
                if re.search(r"\bYukino\b", dialogue_text, re.IGNORECASE):
                    yukino_lines.append(dialogue_text)

                    # Identify if it's a contextual/thought line
                    if "{\\i1}" in dialogue_text or "(" in dialogue_text or "..." in dialogue_text:
                        yukino_context_lines.append(dialogue_text)

# Ensure output directory exists
output_dir = os.path.dirname(dialogue_output_path)
os.makedirs(output_dir, exist_ok=True)

# Save full Yukino dialogues
with open(dialogue_output_path, "w", encoding="utf-8") as f:
    for d in yukino_lines:
        f.write(d + "\n")

# Save only contextual/thought-like lines
with open(context_output_path, "w", encoding="utf-8") as f:
    for d in yukino_context_lines:
        f.write(d + "\n")

print(f"✅ Extracted {len(yukino_lines)} Yukino dialogue lines to: {dialogue_output_path}")
print(f"🧠 Extracted {len(yukino_context_lines)} contextual/thought lines to: {context_output_path}")
