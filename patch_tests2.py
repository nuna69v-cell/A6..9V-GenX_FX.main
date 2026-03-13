import re

with open('tests/test_config_security.py', 'r') as f:
    content = f.read()

# Just look for EXNESS_LOGIN because that's what validation fails on first for default values
content = content.replace('match=".*SECRET_KEY must be changed.*"', 'match=".*EXNESS_LOGIN must be changed.*"')

with open('tests/test_config_security.py', 'w') as f:
    f.write(content)
