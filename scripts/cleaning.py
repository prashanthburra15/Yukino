import re

# Input files
dialogue_file = "/Users/prashanth/Documents/Yukino_AI/output/yukino_SE3_dialogues.txt"
context_file = "/Users/prashanth/Documents/Yukino_AI/output/yukino_SE3_context.txt"

# Output files
dialogue_clean = "/Users/prashanth/Documents/Yukino_AI/output/yukino_SE3_dialogues_clean.txt"
context_clean = "/Users/prashanth/Documents/Yukino_AI/output/yukino_SE3_context_clean.txt"

def clean_line(text):
    # Remove all styling tags like {\i1}, {\blur0.75}, etc.
    text = re.sub(r"\{[^}]+\}", "", text)

    # Replace \N (new line in .ass) with a period or space
    text = text.replace("\\N", ". ")

    # Remove leading/trailing whitespace
    text = text.strip()

    return text

def process_file(input_path, output_path):
    cleaned_lines = set()

    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        clean = clean_line(line)
        if clean:  # Skip empty lines
            cleaned_lines.add(clean)

    # Write to output
    with open(output_path, "w", encoding="utf-8") as f:
        for line in sorted(cleaned_lines):
            f.write(line + "\n")

    print(f"✅ Cleaned {len(cleaned_lines)} lines written to: {output_path}")


# Run for both dialogue and context files
process_file(dialogue_file, dialogue_clean)
process_file(context_file, context_clean)
