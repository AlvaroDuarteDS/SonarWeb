"""
#!/bin/bash
echo "Cleaning up Voice Web Assistant..."

# Stop any running services
pkill -f "uvicorn api"
pkill -f "python main_app.py"

# Clean temporary files
rm -rf temp/
rm -rf /tmp/web_assistant_*

# Clean logs (optional)
read -p "Clean log files? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf logs/*.log
    echo "Logs cleaned."
fi

# Clean cache
rm -rf __pycache__/
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete

echo "Cleanup complete!"
"""
