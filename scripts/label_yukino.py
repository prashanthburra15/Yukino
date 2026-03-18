import os
import re

subtitle_dir = "/Users/prashanth/Documents/Yukino_AI/Sub_files"

# Comprehensive list of Yukino-style speech cues
yukino_keywords = [
    # Referring to others
    "Hikigaya-kun", "Yui-san", "Yuigahama-san", "Yukinoshita", "Service Club",
    "Hayama-kun", "sensei", "teacher", "Komachi",

    # Logical or harsh reasoning
    "That's wrong", "You're mistaken", "You're incompetent", "You're irrational",
    "You're hopeless", "That’s unnecessary", "You always misunderstand",
    "You’re illogical", "You lack awareness", "This is inefficient",
    "This is meaningless", "This is unnecessary", "Don’t waste time",
    "You don't understand", "That doesn't make sense", "You're being childish",

    # Common replies
    "I’ll do it myself", "I don't need help", "I can handle it", "No need",
    "Don’t involve me", "It has nothing to do with me", "Leave it to me",
    "I’m not asking for assistance", "Tch", "Hmph", "You can leave",
    "I’m fine by myself", "I don’t expect anything from you",

    # Self-reflections and beliefs
    "I prefer solitude", "I don’t need friends", "I’m used to being alone",
    "I’m not good with people", "I value logic", "I dislike hypocrisy",
    "Truth is harsh", "I don't like relying on others", "I'm not interested in friendships",
    "I’m used to being hated", "I accept the consequences", "I’m responsible for this",

    # Signature speech quirks
    "Tch", "Sigh", "It’s fine", "As expected", "It's not your concern",
    "There’s no point", "We’re wasting time", "This is meaningless",

    # Emotions through action
    "(sigh)", "..."  # often used to express awkward silences or pauses

    # Misc
    # Add variants if needed, like "I will", "I'll", "I’m", etc.
]

def is_yukino_line(text):
    """Check if dialogue contains Yukino-style patterns."""
    for keyword in yukino_keywords:
        if keyword.lower() in text.lower():
            return True
    return False

# Process all .ass files
for filename in os.listdir(subtitle_dir):
    if filename.endswith(".ass"):
        path = os.path.join(subtitle_dir, filename)

        with open(path, "r", encoding="latin-1") as f:
            lines = f.readlines()

        updated_lines = []
        changes = 0

        for line in lines:
            if line.startswith("Dialogue:"):
                parts = line.strip().split(",", 9)
                if len(parts) == 10:
                    text = parts[9]
                    current_name = parts[4].strip()

                    # If not already labeled and resembles Yukino
                    if current_name == "" and is_yukino_line(text):
                        parts[4] = "Yukino"
                        line = ",".join(parts)
                        changes += 1

            updated_lines.append(line)

        with open(path, "w", encoding="utf-8") as f:
            f.writelines(updated_lines)

        print(f"✅ Labeled {changes} lines in: {filename}")
