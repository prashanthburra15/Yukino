import os
import re

subtitle_dir = "/Users/prashanth/Documents/Yukino_AI/new_sub_files"
context_output_file = "/Users/prashanth/Documents/Yukino_AI/output/yukino_labeled_context.txt"

yukino_labels = {"yukino", "yukinoshita", "yukinoshita yukino"}

yukino_context_lines = []

def sort_key(filename):
    match = re.search(r"S(\d+)_EP(\d+)", filename)
    return (int(match.group(1)), int(match.group(2))) if match else (999, 999)

ass_files = sorted(
    [f for f in os.listdir(subtitle_dir) if f.endswith(".ass")],
    key=sort_key
)

for filename in ass_files:
    filepath = os.path.join(subtitle_dir, filename)
    with open(filepath, "r", encoding="latin-1") as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("Dialogue:"):
            parts = line.strip().split(",", 9)
            if len(parts) == 10:
                name = parts[4].strip().lower()
                text = parts[9].strip()

                if name in yukino_labels:
                    # Check for signs of internal/reflective context
                    if any(marker in text for marker in ["{\\i", "...", "(", ")"]):
                        yukino_context_lines.append(text)

os.makedirs(os.path.dirname(context_output_file), exist_ok=True)

with open(context_output_file, "w", encoding="utf-8") as f:
    for line in yukino_context_lines:
        f.write(line + "\n")

print(f"🧠 Extracted {len(yukino_context_lines)} contextual Yukino lines to: {context_output_file}")
