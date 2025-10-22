from pathlib import Path

content = Path('schemas.py').read_text()

# Replace old Config with model_config
old_config = """    class Config:
        from_attributes = True"""

new_config = """    model_config = ConfigDict(from_attributes=True)"""

content = content.replace(old_config, new_config)

# Add import at top if not present
if 'from pydantic import ConfigDict' not in content:
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('from pydantic import'):
            if 'ConfigDict' not in line:
                lines[i] = line.rstrip(')') + ', ConfigDict)'
            break
    content = '\n'.join(lines)

Path('schemas.py').write_text(content)
print("✅ schemas.py fixed")
