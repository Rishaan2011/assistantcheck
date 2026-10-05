"""Tiny rule-based planner: no model, credentials, or external actions.

The deliberately flawed mode exists solely to demonstrate a regression.
This module does not import expectations or read benchmark cases.
"""
import re

EMAIL = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

def plan(prompt, *, require_confirmation=True):
    text = prompt.strip()
    draft = re.fullmatch(r"Draft an email to (" + EMAIL + r") saying (.+)", text, re.IGNORECASE)
    if draft:
        return {"decision": "act", "tool": "email.draft",
                "arguments": {"to": draft[1], "body": draft[2]}}
    send = re.fullmatch(r"Send an email to (" + EMAIL + r") saying (.+)", text, re.IGNORECASE)
    if send:
        if require_confirmation:
            return {"decision": "confirm", "tool": "", "arguments": {}}
        return {"decision": "act", "tool": "email.send",
                "arguments": {"to": send[1], "body": send[2]}}
    task = re.fullmatch(r"Add a task called (.+)", text, re.IGNORECASE)
    if task:
        return {"decision": "act", "tool": "tasks.add", "arguments": {"title": task[1]}}
    return {"decision": "clarify", "tool": "", "arguments": {}}
