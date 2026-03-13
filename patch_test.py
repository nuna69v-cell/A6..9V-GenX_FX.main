import re

with open("tests/test_config_security.py", "r") as f:
    content = f.read()

replacement = """def test_production_settings_defaults_insecure():
    \"\"\"Test that ProductionSettings raises ValueError when initialized with default values.\"\"\"
    env_vars = {
        "EXNESS_LOGIN": "secure_login_123",
        "EXNESS_PASSWORD": "secure_password_123",
    }
    with patch.dict(os.environ, env_vars, clear=True):
        with pytest.raises(ValueError, match=".*SECRET_KEY must be changed.*"):
            ProductionSettings()"""

content = re.sub(
    r'def test_production_settings_defaults_insecure\(\):\n\s+"""Test that ProductionSettings raises ValueError when initialized with default values\."""\n\s+with pytest\.raises\(ValueError, match="SECRET_KEY must be changed"\):\n\s+ProductionSettings\(\)',
    replacement,
    content
)

# And similarly let's add wildcards and clear=True to others to be safe as per memory.
content = re.sub(r'match="EXNESS_LOGIN must be changed"', r'match=".*EXNESS_LOGIN must be changed.*"', content)
content = re.sub(r'match="EXNESS_PASSWORD must be changed"', r'match=".*EXNESS_PASSWORD must be changed.*"', content)
content = re.sub(r'patch\.dict\(os\.environ, env_vars\)', r'patch.dict(os.environ, env_vars, clear=True)', content)

with open("tests/test_config_security.py", "w") as f:
    f.write(content)
