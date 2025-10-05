#!/usr/bin/env python3
"""
Script to remove PageSpeed Insights references from index.html
"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove psi from apiKeys state initialization
content = content.replace(
    "psi: localStorage.getItem('psi_key') || sessionStorage.getItem('psi_key') || ''",
    "// psi removed"
)

# 2. Remove psi_key from requestBody
content = content.replace(
    "requestBody.psi_key = apiKeys.psi;",
    "// psi_key removed"
)

# 3. Remove PSI API key input section (multiline - find and remove block)
# This is complex, so we'll use a marker-based approach
lines = content.split('\n')
new_lines = []
skip_until_line = -1
i = 0

while i < len(lines):
    line = lines[i]

    # Skip PSI API Key section
    if '{/* PSI API Key (Optional) */}' in line:
        # Find closing div - skip entire block
        skip_depth = 0
        found_start = False
        while i < len(lines):
            if '<div' in lines[i]:
                if not found_start:
                    found_start = True
                    skip_depth = 1
                else:
                    skip_depth += 1
            if '</div>' in lines[i]:
                skip_depth -= 1
                if skip_depth == 0:
                    i += 1  # Skip the closing </div>
                    break
            i += 1
        continue

    # Remove psi-related setTemp/storage calls
    if "tempKeys.psi" in line or "storage.setItem('psi_key'" in line:
        i += 1
        continue

    # Remove PageSpeed Google Console link
    if "console.cloud.google.com/apis/library/pagespeedonline" in line:
        # Skip this line and next 2
        i += 3
        continue

    new_lines.append(line)
    i += 1

content = '\n'.join(new_lines)

# 4. Remove Performance tab from navigation
# Find tab list and remove Performance
content = content.replace(
    '"Performance"',
    '// "Performance" removed'
)

# 5. Save
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] PageSpeed Insights references removed from index.html")
print("Changes:")
print("  - Removed psi from apiKeys state")
print("  - Removed psi_key from requestBody")
print("  - Removed PSI API Key input field")
print("  - Removed Google Cloud Console link")
print("  - Removed Performance tab from navigation")
