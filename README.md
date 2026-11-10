# 🛡️ AI-Driven DevSecOps CI/CD Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.103.1-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?logo=github-actions&logoColor=white)
![Google Gemini](https://img.shields.io/badge/AI_Engine-Gemini_3.8_Flash-8E75B2?logo=google&logoColor=white)

## 📖 Overview
This project demonstrates a modern **"Shift-Left" DevSecOps architecture** by integrating Generative AI directly into the CI/CD pipeline. 

It features an automated AI Security Gatekeeper that intercepts code changes (`git diff`), analyzes them for vulnerabilities (e.g., hardcoded secrets, insecure configurations, SQL injection) using the **Google Gemini API**, and makes automated Go/No-Go deployment decisions before the code ever reaches production.

## 🏗️ Architecture & Workflow

1. **Local Development:** A containerized target application (FastAPI + Docker).
2. **Commit Phase:** Code changes are staged.
3. **CI/CD Trigger:** Pushing to GitHub triggers a GitHub Actions workflow.
4. **AI Security Gatekeeper (`ai_sec_gate.py`):**
   - Extracts the latest `git diff`.
   - Sends the diff to the Gemini 3.8 Flash model with a strict DevSecOps system prompt.
   - Enforces a structured JSON output response.
5. **Deployment Decision:**
   - **Passed:** If the code is clean, the script exits with `0`, and the GitHub Actions pipeline turns green (Deployment allowed).
   - **Failed:** If vulnerabilities are found, the script prints the exact issue, exits with `1`, and halts the CI/CD pipeline (Deployment blocked).

## ✨ Key Features
* **Zero-Trust Code Scanning:** Automatically flags leaked AWS keys, database passwords, and insecure Git tracking (like compiled `.pyc` files).
* **Automated CI/CD:** Fully integrated with GitHub Actions (`pipeline.yml`).
* **Resilient API Logic:** Built-in exponential backoff and retry mechanisms to handle LLM rate limits and `503 Service Unavailable` API traffic spikes.
* **Deterministic AI Outputs:** Utilizes `response_mime_type="application/json"` to force the LLM to return strictly parseable JSON for pipeline automation.
* **Secure Secrets Management:** Utilizes `.env` for local testing and GitHub Secrets for secure cloud execution.

## 🛠️ Technology Stack
* **Core Language:** Python 3.11
* **AI Engine:** Google Gemini API (`google-genai` SDK, `gemini-3.8-flash`)
* **CI/CD:** GitHub Actions
* **Target Application:** FastAPI
* **Containerization:** Docker
* **Version Control:** Git & GitHub

## 🚀 Getting Started (Local Testing)

### 1. Prerequisites
* Python 3.11+
* Git installed
* A free [Google AI Studio API Key](https://aistudio.google.com/)

### 2. Installation
Clone the repository and install the required dependencies:
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/ai-devsecops-pipeline.git
cd ai-devsecops-pipeline
pip install google-genai python-dotenv
```

### 3. Environment Setup
Create a `.env` file in the root directory and add your Gemini API key:
```text
GEMINI_API_KEY="your_actual_api_key_here"
```

### 4. Run the Gatekeeper
Make a purposeful insecure change in `main.py` (e.g., type `AWS_KEY="AKIAIOSFODNN7EXAMPLE"`), save the file, and run:
```bash
python ai_sec_gate.py
```
**Expected Output:**
```json
SECURITY SCAN FAILED: Hardcoded AWS secret key detected in main.py. Remove this and use environment variables.
```

## ☁️ Cloud Pipeline (GitHub Actions)
The pipeline is defined in `.github/workflows/pipeline.yml`. It runs automatically on every push to the `main` branch. 
* To view the automated runs, click the **Actions** tab in this repository.
* The workflow securely accesses the AI engine via a repository secret named `GEMINI_API_KEY`.
