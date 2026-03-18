import os
import re
from pathlib import Path

def clean_dialogue(text):
    # Remove ASS formatting like {\i1}, {\fad(...)}, etc.
    return re.sub(r"{\\.*?}", "", text).strip()

def process_ass_file(file_path: Path, output_dir: Path):
    episode_name = file_path.stem
    output_file = output_dir / f"{episode_name}.txt"
    output_lines = []

    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("Dialogue:"):
                parts = line.split(",", 9)
                if len(parts) == 10:
                    speaker = parts[4].strip() or "Unknown"
                    raw_text = parts[9].strip()
                    clean_text = clean_dialogue(raw_text)
                    if clean_text:
                        output_lines.append(f"{speaker}: {clean_text}")

    output_file.write_text("\n".join(output_lines), encoding="utf-8")
    print(f"Saved: {output_file.name}")

# Folder containing your .ass files
input_folder = Path("/Users/prashanth/Documents/Yukino_AI/Sub_files/SE2")
output_folder = Path("/Users/prashanth/Documents/Yukino_AI/data/cleaned_txts")
output_folder.mkdir(exist_ok=True)

# Process all .ass files
for file in input_folder.glob("*.ass"):
    process_ass_file(file, output_folder)
