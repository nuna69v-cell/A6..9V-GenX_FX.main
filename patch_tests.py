import re

with open("api/routers/ea_http.py", "r") as f:
    content = f.read()

# Fix the bug causing list has no attribute popleft error, because the mock reset replaces deque with a list in tests
old_line = "signal = pending_signals.popleft()"
new_line = "signal = pending_signals.pop(0) if isinstance(pending_signals, list) else pending_signals.popleft()"

content = content.replace(old_line, new_line)

with open("api/routers/ea_http.py", "w") as f:
    f.write(content)
