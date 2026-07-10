#!/data/data/com.termux/files/usr/bin/bash
# NEXUS Quick Run for Termux
echo "ðŸš€ Starting NEXUS..."

# Install if not present
pip install -q -r requirements.txt 2>/dev/null

# Run
python3 nexus.py
