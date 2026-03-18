#!/bin/bash

SOURCE_DIR="/Users/prashanth/Documents/Yukino_AI/Oregairu/Oregairu_S3"
DEST_DIR="/Users/prashanth/Documents/Yukino_AI/Sub_files"
TARGET_LABEL="Full Subs(MTBB without honorifics)"

for filepath in "$SOURCE_DIR"/*.mkv; do
    filename=$(basename "$filepath")
    if [[ $filename =~ _([0-9]+)_ ]]; then
        ep_num="${BASH_REMATCH[1]}"
        output_file="$DEST_DIR/S3_EP${ep_num}.ass"

        echo "🔍 Scanning subtitle tracks for Episode ${ep_num}..."

        # Get the correct track ID using mkvmerge + jq
        track_id=$(mkvmerge -J "$filepath" | jq -r --arg label "$TARGET_LABEL" '
            .tracks[] | select(.type == "subtitles" and .properties.track_name == $label) | .id' | head -n 1)

        if [[ -n "$track_id" ]]; then
            mkvextract tracks "$filepath" "${track_id}:${output_file}"
            if [[ $? -eq 0 ]]; then
                echo "✅ Successfully extracted Episode ${ep_num} to $output_file"
            else
                echo "❌ Failed to extract Episode ${ep_num}"
            fi
        else
            echo "❌ Could not find subtitle track with label: $TARGET_LABEL for Episode ${ep_num}"
        fi
    else
        echo "⚠️ Could not determine episode number from $filename"
    fi
done
