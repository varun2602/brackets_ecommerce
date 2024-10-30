# rm -rf /home/ubuntu/commerce

#!/bin/bash

# Define the directory to remove
DIR="/home/ubuntu/commerce"

# Log the action
echo "Checking if $DIR exists..."

# Only attempt to remove if the directory exists
if [ -d "$DIR" ]; then
    echo "Removing old files in $DIR..."
    rm -rf "$DIR"
    echo "Successfully removed $DIR."
else
    echo "$DIR does not exist; skipping removal."
fi

# Continue with other installation steps...
