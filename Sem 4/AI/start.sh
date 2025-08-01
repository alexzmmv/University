#!/bin/bash
# Script to launch Jupyter notebook
#matei vasile capilnas

# Run the Jupyter command
/opt/anaconda3/bin/jupyter_mac.command

# Check if command executed successfully
if [ $? -ne 0 ]; then
    echo "Error: Failed to start Jupyter notebook"
    exit 1
fi
