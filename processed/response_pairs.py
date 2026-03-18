from pathlib import Path
import json

# Input subtitle text files (update paths if needed)
context_files = [
    "/Users/prashanth/Documents/Yukino_AI/yukino_output/Yukino_All_Context.txt"
]

# Output path
output_file = Path("/Users/prashanth/Documents/Yukino_AI/processed/yukino_context_response_pairs_final.json")

def is_yukino(speaker):
    return speaker.lower().strip() in {"yukino", "yukinoshita", "yuki"}

def extract_speaker(line):
    return line.split(":", 1)[0].strip() if ":" in line else ""

def clean_line(line):
    return line.strip()

def is_duplicate_line(line, context):
    return line in context

def all_same_speaker(context_lines):
    speakers = [extract_speaker(l) for l in context_lines]
    return len(set(speakers)) == 1

all_pairs = []

for file_path in context_files:
    lines = Path(file_path).read_text(encoding="utf-8").splitlines()

    for i in range(len(lines)):
        line = lines[i].strip()
        if ":" not in line:
            continue

        speaker = extract_speaker(line)
        if not is_yukino(speaker):
            continue  # only generate for Yukino lines

        response = clean_line(line)
        context = []
        seen_lines = set()

        # Backtrack for up to 3 valid non-Yukino context lines
        for j in range(i - 1, -1, -1):
            prev_line = lines[j].strip()
            if ":" not in prev_line:
                continue

            prev_speaker = extract_speaker(prev_line)
            if is_yukino(prev_speaker):
                continue  # skip Yukino's previous replies

            if prev_line in seen_lines:
                continue  # avoid duplicate lines
            seen_lines.add(prev_line)

            context.insert(0, clean_line(prev_line))
            if len(context) >= 3:
                break

        # Skip context with no variety (e.g., all Hiratsuka 3 times)
        if not context or all_same_speaker(context):
            continue

        all_pairs.append({
            "context": context,
            "response": response
        })

# Save to file
output_file.parent.mkdir(parents=True, exist_ok=True)
output_file.write_text(json.dumps(all_pairs, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"✅ Generated {len(all_pairs)} high-quality Yukino context-response pairs.")
print(f"📁 Output saved to: {output_file}")
