# Glitter Pentesting Hub

This is a **personal project** I developed as part of the **Magshimim Cyber Education Program** to practice basic penetration testing techniques.

It simulates interaction with a mock social media platform ("Glitter") and includes scripts that experiment with things like authentication logic, data extraction, and simple client-server communication using sockets.



---

## What It Does

- Logs into the Glitter server using sockets
- Likes posts and comments
- Gets user info like ID or email
- Sends glits with custom colors
- Simulates vulnerabilities like:
- Logging in with just a username
- Viewing search history
- Getting password via recovery
- Triggering XSS with glit content

---

## Running the Project

### Requirements

- Python 3.8+
- `requests` library

### How to Run

```bash
pip install requests
python swissknife.py
