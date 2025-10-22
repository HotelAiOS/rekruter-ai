import os
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Skip if already using logger
    if 'import logging' not in content:
        content = 'import logging\n\nlogger = logging.getLogger(__name__)\n\n' + content
    
    # Replace print with logger.info
    content = re.sub(r'\bprint\((.*?)\)', r'logger.info(\1)', content)
    
    with open(filepath, 'w') as f:
        f.write(content)

for root, dirs, files in os.walk('.'):
    if 'venv' in root or '__pycache__' in root:
        continue
    for file in files:
        if file.endswith('.py') and not file.startswith('test_'):
            filepath = os.path.join(root, file)
            try:
                fix_file(filepath)
                logger.info(f"Fixed: {filepath}")
            except Exception as e:
                logger.info(f"Error: {filepath} - {e}")
