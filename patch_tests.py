import re

with open("tests/test_config_security.py", "r") as f:
    content = f.read()

content = content.replace(
    'match="SECRET_KEY must be changed"', 'match=".*SECRET_KEY must be changed.*"'
)
content = content.replace(
    'match="EXNESS_LOGIN must be changed"', 'match=".*EXNESS_LOGIN must be changed.*"'
)
content = content.replace(
    'match="EXNESS_PASSWORD must be changed"',
    'match=".*EXNESS_PASSWORD must be changed.*"',
)
content = content.replace(
    "with patch.dict(os.environ, env_vars):",
    "with patch.dict(os.environ, env_vars, clear=True):",
)
content = content.replace(
    'with patch.dict(os.environ, {"ENVIRONMENT": "development"}):',
    'with patch.dict(os.environ, {"ENVIRONMENT": "development"}, clear=True):',
)

with open("tests/test_config_security.py", "w") as f:
    f.write(content)
