import os
import re
import zipfile
import time
from googletrans import Translator
import time

# Configure folders
srt_folder = '/Users/prashanth/Documents/Yukino_AI/Sub_files/SE1'  # input SRT files
output_folder = '/Users/prashanth/Documents/Yukino_AI/data'       # output TXT files
zip_filename = '/Users/prashanth/Documents/Yukino_AI/data/SE1_Translated_Episodes.zip'

os.makedirs(output_folder, exist_ok=True)

# Regex patterns
speaker_re = re.compile(r"（(.+?)）")
effects_re = re.compile(r"<.*?>|♪|《.*?》|＜.*?＞|（.*?ＳＥ.*?）", re.DOTALL)
timestamp_re = re.compile(r"^\d{2}:\d{2}:\d{2},\d{3}")

# Japanese to English speaker names map
jp_to_en = {
    "比企谷": "Hikigaya",
    "雪ノ下": "Yukinoshita",
    "平塚": "Hiratsuka",
    "結衣": "Yuigahama",
    "材木座": "Zaimokuza",
    "一色": "Isshiki",
    "由比ヶ浜": "Yuigahama",
    "戸部": "Tobe",
    "大垣": "Ogaki",
    "葉山": "Hayama",
    "吉田": "Yoshida",
    "川崎": "Kawasaki",
    "戸村": "Tomura",
    "八幡": "Hikigaya",
    "雪乃": "Yukinoshita",
    "平塚先生": "Hiratsuka-sensei",
}

translator = Translator()

def clean_line(line):
    # Remove effects and extra spaces
    line = effects_re.sub("", line)
    return line.strip()

def detect_speaker(line):
    m = speaker_re.match(line)
    if m:
        jp_name = m.group(1)
        return jp_to_en.get(jp_name, jp_name)
    return None

def is_valid_line(text):
    # Skip lines that consist mostly of punctuation or brackets or are empty
    if not text:
        return False
    if re.match(r"^[\[\]\(\)「」『』]+$", text):
        return False
    return True



def translate_line(text, retries=7, delay=10, pause=1.0):
    global translator
    for attempt in range(retries):
        try:
            time.sleep(pause)
            result = translator.translate(text, src='ja', dest='en')
            return result.text
        except Exception as e:
            print(f"Translate error: '{text[:30]}...' => {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay}s (attempt {attempt + 1})...")
                time.sleep(delay)
            else:
                print(f"Giving up on line after {retries} attempts: {text}")
                return text




def process_srt(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    output_lines = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip blank lines, line numbers, timestamps
        if not line or line.isdigit() or timestamp_re.match(line):
            i += 1
            continue

        cleaned = clean_line(line)
        if not cleaned:
            i += 1
            continue

        speaker = detect_speaker(cleaned)
        # Remove speaker marker if it exists for clean text
        if speaker:
            text = speaker_re.sub("", cleaned, 1).strip()
        else:
            text = cleaned

        if not text:
            i += 1
            continue

        translated = translate_line(text)
        label = speaker if speaker else "Unknown"
        output_lines.append(f"{label}: {translated}")

        i += 1

    with open(output_path, 'w', encoding='utf-8') as out_f:
        out_f.write('\n\n'.join(output_lines))

def zip_outputs(output_folder, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w') as zf:
        for fname in sorted(os.listdir(output_folder)):
            if fname.endswith('.txt'):
                full_path = os.path.join(output_folder, fname)
                zf.write(full_path, arcname=fname)

def main():
    txt_exist = set(os.listdir(output_folder))
    for fname in sorted(os.listdir(srt_folder)):
        if not fname.lower().endswith('.srt'):
            continue
        out_name = fname.replace('.srt', '_EN.txt')
        if out_name in txt_exist:
            print(f"Skipping {fname} because {out_name} already exists.")
            continue

        input_path = os.path.join(srt_folder, fname)
        output_path = os.path.join(output_folder, out_name)
        print(f"Processing {fname}...")
        process_srt(input_path, output_path)

    print("Creating ZIP archive...")
    zip_outputs(output_folder, zip_filename)
    print(f"ZIP file created: {zip_filename}")

if __name__ == "__main__":
    main()
