#!/bin/bash

# Directory containing the files to be renamed
dir="/home/ubuntu/ContMigration/utils/data_extraction/extracted_data"

# Iterate through each file in the directory
for file in "$dir"/*; do
  # Extract the basename of the file
  basename=$(basename "$file")

  # Skip files that don't match the expected pattern
  if [[ ! $basename =~ data-checkpoint-.*T.*\.tar\.csv ]]; then
    continue
  fi

  # Construct the new filename
  new_basename=$(echo "$basename" | sed -e 's/:/-/g' -e 's/\.tar//g')

  # Full paths to the old and new filenames
  old_filepath="$dir/$basename"
  new_filepath="$dir/$new_basename"

  # Rename the file
  mv "$old_filepath" "$new_filepath"
done

echo "Renaming complete."
