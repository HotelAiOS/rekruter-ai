from pathlib import Path

schemas_content = Path('schemas.py').read_text()

# Find JobCreate and add JobUpdate after it
jobupdate_class = """
class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[Dict] = None
    status: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
"""

# Find the line after JobCreate class definition
lines = schemas_content.split('\n')
new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)
    if line.strip().startswith('class JobCreate'):
        # Find the end of JobCreate class (next class or empty line)
        j = i + 1
        while j < len(lines) and (lines[j].strip() == '' or lines[j].startswith('    ')):
            new_lines.append(lines[j])
            j += 1
        # Insert JobUpdate
        new_lines.extend(jobupdate_class.split('\n'))
        # Skip lines we already added
        i = j - 1

Path('schemas.py').write_text('\n'.join(new_lines))
print("✅ JobUpdate added")
