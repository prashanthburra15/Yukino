from pathlib import Path

def extract_yukino_lines_by_season(input_folder: Path, output_folder: Path):
    yukino_only_path = output_folder / "yukino_only"
    yukino_context_path = output_folder / "yukino_context"
    yukino_only_path.mkdir(parents=True, exist_ok=True)
    yukino_context_path.mkdir(parents=True, exist_ok=True)

    all_yukino_lines = []
    all_context_lines = []

    for file_path in sorted(input_folder.rglob("*.txt")):  # use rglob for all subfolders
        lines = file_path.read_text(encoding="utf-8").splitlines()
        dialogue_lines = [line for line in lines if ":" in line and line.strip()]

        episode_yukino = []
        episode_context = []

        for i, line in enumerate(dialogue_lines):
            speaker = line.split(":")[0].strip().lower()
            if speaker in {"yukino", "yukinoshita", "yuki"}:
                episode_yukino.append(line)

                context_block = []

                # Find previous non-Yukino line
                for j in range(i - 1, -1, -1):
                    prev_speaker = dialogue_lines[j].split(":")[0].strip().lower()
                    if prev_speaker not in {"yukino", "yukinoshita", "yuki"}:
                        context_block.append(dialogue_lines[j])
                        break

                context_block.append(line)

                # Find next non-Yukino line
                for j in range(i + 1, len(dialogue_lines)):
                    next_speaker = dialogue_lines[j].split(":")[0].strip().lower()
                    if next_speaker not in {"yukino", "yukinoshita", "yuki"}:
                        context_block.append(dialogue_lines[j])
                        break

                context_block.append("")  # spacer
                episode_context.extend(context_block)

        # Save per episode
        (yukino_only_path / f"{file_path.stem}_yukino.txt").write_text(
            "\n".join(episode_yukino), encoding="utf-8"
        )
        (yukino_context_path / f"{file_path.stem}_context.txt").write_text(
            "\n".join(episode_context), encoding="utf-8"
        )

        # Add to full-season files
        all_yukino_lines.extend(episode_yukino + [""])
        all_context_lines.extend(episode_context + [""])

    # Save season-wide compiled files
    (output_folder / "Yukino_All_Lines.txt").write_text("\n".join(all_yukino_lines), encoding="utf-8")
    (output_folder / "Yukino_All_Context.txt").write_text("\n".join(all_context_lines), encoding="utf-8")


# ✅ Execute
extract_yukino_lines_by_season(
    Path("/Users/prashanth/Documents/Yukino_AI/data"),
    Path("/Users/prashanth/Documents/Yukino_AI/yukino_output")
)
