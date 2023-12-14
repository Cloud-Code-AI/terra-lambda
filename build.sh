#!/bin/bash

# Define the name of the zip file
ZIP_FILE="terra_lambda.zip"

# Check if the zip file already exists
if [ -f "$ZIP_FILE" ]; then
    echo "Zip file $ZIP_FILE exists. Deleting it."
    rm -f "$ZIP_FILE"
else
    echo "Zip file $ZIP_FILE does not exist."
fi

# Create a new zip file excluding the script itself
echo "Creating new zip file $ZIP_FILE."
zip -r "$ZIP_FILE" . -x "$(basename "$0")"

echo "Zip file created successfully."
