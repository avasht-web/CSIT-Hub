# CSIT Hub: Secure Task & Note Management

A lightweight, full-stack web application built with Python and Flask, designed to handle user authentication, task tracking, and note management. 

*Live Deployment:* []

## 🛠 Tech Stack
* **Backend:** Python, Flask, SQLite3
* **Frontend:** HTML5, CSS3, Jinja2
* **Security:** Werkzeug Cryptography

## 🔒 Security Audit & V1.0 Remediation
During the final development phase of Version 1.0, a self-led security audit was conducted to patch critical vulnerabilities:

1. **Authentication (Patched):** Transitioned from plaintext password storage to one-way cryptographic hashing using `werkzeug.security`. Passwords are mathematically scrambled before database insertion.
2. **Cross-Site Scripting / XSS (Patched):** Implemented strict backend input sanitization. All POST requests are intercepted, stripped of hidden whitespace, and enforced with hard character limits to prevent script injection and database overloading.
3. **Version Control Incident Response:** Executed an enterprise-level Git history rewrite (`git filter-repo`) to surgically remove an accidentally committed local `.db` file from the cryptographic timeline before force-pushing.

## 🚀 How to Run Locally
1. Clone the repository: `git clone https://github.com/avasht-web/CSIT-Hub.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the server: `flask run`
