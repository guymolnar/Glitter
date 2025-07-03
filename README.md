# ✨ Glitter Pentesting Hub

**Glitter** is a Python-based pentesting tool developed as part of the **Magshimim Cyber Education Program**. It interacts with the Glitter platform to explore security vulnerabilities, bypass authentication, and test user-based logic flaws — all within an ethical, simulated environment.

---

## 🎯 Project Objectives

- Practice and demonstrate real-world penetration testing techniques
- Learn about client-server socket interaction, API exploitation, and logic-based vulnerabilities
- Develop reusable code for pentesting automation and educational demonstrations
- Provide a central menu-driven interface for testing multiple attack vectors

---

## ⚙️ Features

### 🔐 Authentication Bypass & Account Control
- Login with full credentials
- Login with username only (bypassing password via checksum)
- Account creation with invalid field lengths
- Username takeover via update

### 📡 Glit & User Interaction
- Like posts
- Reply to private glits
- Publish glits with custom colors
- View feeds (including private users)
- Comment on restricted posts
- Accept or reject friend requests programmatically

### 🔍 Data Extraction
- Fetch email addresses from usernames
- Extract account details (ID, avatar, email, etc.)
- View other users’ search histories
- Dump feeds even from private accounts

### 💣 Vulnerability Exploits
- **Password recovery abuse**: Reconstruct the recovery code to extract passwords
- **Session cookie leak**: Capture cookies via request spoofing
- **Stored XSS**: Craft malicious glits that spread when clicked

---

## 🛠️ Setup

### 🔗 Requirements

- Python 3.8+
- `requests` module

```bash
pip install requests
```
### 🚀 Running
```bash
python swissknife.py
```
### ⚠️ Disclaimer
This project is intended strictly for educational purposes within the Magshimim Cyber Program.
Do not use this against real systems, people, or organizations. Unauthorized use may be illegal.

### 👨‍💻 Author
Developed by Guy Molnar
Magshimim Cyber Education Program

