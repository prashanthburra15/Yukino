import os
from pathlib import Path

def clean_line(line):
    line = line.strip()
    if not line or ":" not in line:
        return None

    speaker, dialogue = line.split(":", 1)
    speaker = speaker.strip()
    dialogue = dialogue.replace("\\N", " ").strip()

    # Filter system lines or metadata
    if speaker.lower() in ["text", "title"]:
        return None

    # Replace unknown or missing names
    if speaker in ["?", "？", ""]:
        speaker = "Unknown"

    return f"{speaker}: {dialogue}" if dialogue else None

def clean_txt_file(input_path: Path, output_path: Path):
    lines = input_path.read_text(encoding="utf-8").splitlines()
    cleaned_lines = [clean_line(line) for line in lines]
    cleaned_lines = [line for line in cleaned_lines if line]  # Remove None
    output_path.write_text("\n".join(cleaned_lines), encoding="utf-8")
    print(f"✔ Cleaned: {input_path.name} → {output_path.name}")

# 🗂 Set your folders here
input_folder = Path("/Users/prashanth/Documents/Yukino_AI/data/cleaned_txts")  # Folder with SE2_EPxx.txt files
output_folder = Path("/Users/prashanth/Documents/Yukino_AI/data/cleaned_files")
output_folder.mkdir(exist_ok=True)

# 🔁 Batch process all .txt files
for file in input_folder.glob("*.txt"):
    output_file = output_folder / f"{file.stem}.txt"
    clean_txt_file(file, output_file)
