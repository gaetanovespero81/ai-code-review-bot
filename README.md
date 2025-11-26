# 🤖 AI Code Review Bot (GitHub Actions + GitHub Models)

![CI](https://github.com/gaetanovespero81/ai-code-review-bot/actions/workflows/ai-review.yml/badge.svg)
![Version](https://img.shields.io/github/v/tag/gaetanovespero81/ai-code-review-bot?label=version)

This repository contains an automated **AI-powered code review system** built using  
**GitHub Actions**, **GitHub Models**, and the **Azure AI Inference SDK**.

On every Pull Request, the workflow:

- extracts the PR diff
- sends the diff to an LLM (`openai/gpt-4o-mini`)
- generates a structured, professional review
- posts the review directly as a PR comment
- stores the full output as an artifact (`ai_review.md`)

This project demonstrates a realistic integration of **CI/CD automation** and **AI-driven code quality analysis**, suitable for enterprise environments and technical portfolios.

---

## 🚀 Features

### 🔍 Automated AI Code Review
Triggered on PR events (opened, updated, reopened):

1. Extract the pull request diff using `gh pr diff`
2. Build an LLM prompt dynamically
3. Call GitHub Models via Azure AI Inference
4. Generate a clear review in Markdown
5. Comment directly on the PR
6. Upload the review as an artifact

### 🧠 GitHub Models Integration
The system uses the GitHub Models inference endpoint with the Azure SDK:
- `@azure-rest/ai-inference`
- `@azure/core-auth`
- `@azure/core-sse`

### 🔐 Secure Authentication
The workflow uses a dedicated **Personal Access Token (PAT)** stored as:

GH_MODELS_TOKEN

This PAT includes `models:read` and is valid until:

- 📅 **25 November 2026**

### 💸 Free Model Usage
The workflow uses:
openai/gpt-4o-mini

which is **free** under GitHub Models usage limits and reliably available for API inference.

---

## 🧩 Architecture Overview


**flowchart TD**
- A[Pull Request Event] --> B[GitHub Actions Workflow]
- B --> C[Extract PR Diff<br>(gh pr diff)]
- C --> D[Azure AI Inference<br>via GitHub Models]
- D --> E[LLM Generates Code Review]
- E --> F[Comment on PR]
- E --> G[Upload ai_review.md Artifact]

---

## 📦 Repository Structure

This repository is intentionally kept clean and lightweight.
All AI-related JavaScript files (ai_review.js, package.json, dependencies) are not committed.

They are created dynamically by the workflow during execution.

├─ .github/

| └─ workflows/

| | └─ ai-review.yml

├─ bot/

| └─ review.py

The CI pipeline handles everything else automatically inside the GitHub Actions runner.

---

## 🐍 Optional Local Tool — `bot/review.py`

In addition to the CI-based Node.js workflow, this repository includes an optional
Python utility located at:
bot/review.py
This module provides a **standalone AI code review tool** that can be executed locally,
outside the GitHub Actions environment. It enables developers to request an AI-generated
review for any diff directly from the command line.

### 🔧 What It Does

- Reads a diff from a text file (e.g., output of `git diff`)
- Builds a professional review prompt
- Calls GitHub Models (`openai/gpt-4o-mini`) through the official Inference API
- Prints the full review to stdout

This is useful for:
- rapid offline testing
- experimenting with prompt design
- local pre-review before opening a Pull Request
- demonstration of Python-based LLM integration

### ▶️ How to Use

1. Set your GitHub Models PAT:


`export GITHUB_TOKEN=<your GH_MODELS_TOKEN>`

2.	Save any diff to a file:

`git diff > pr_diff.txt`

3.	Run the review script:

`python -m bot.review pr_diff.txt`

You will receive a full Markdown-formatted AI code review directly in the terminal.

**🧠 Notes**
- This local tool uses the same model and same PAT as the CI workflow.
- It does not require committing any additional files (package.json, Node dependencies).
- It demonstrates multi-language AI integration (Node.js in CI, Python locally).

---

## ⚙️ Setup Instructions

1️⃣ Generate the PAT (Personal Access Token)

The token was generated directly from the GPT-5 model page on GitHub Marketplace.
This ensures the token automatically includes the required:

`models:read`

The PAT used by this workflow expires on:

- 🗓️ 25.11.2026

2️⃣ Store the PAT in Repository Secrets

**Navigate to:**

Settings → Secrets and variables → Actions → New repository secret

**Create:**

Name: GH_MODELS_TOKEN

Value: `<your PAT>`

⚠️ Must be a secret, not a variable.

---

## 🛠 Workflow Execution Details

The workflow:
1.	Installs Node.js
2.	Dynamically creates a lightweight package.json
3.	Installs Azure AI dependencies
4.	Generates ai_review.js (the inference logic)
5.	Executes the script to produce AI feedback
6.	Comments on the PR
7.	Saves ai_review.md as an artifact

The repository stays clean — no JS files committed — while the workflow remains fully functional.

---

## 🧪 Testing the System

You can manually test the AI inference locally by exporting the PAT:

`export GITHUB_TOKEN=<your GH_MODELS_TOKEN>`

node ai_review.js

Or trigger the workflow by:
- opening a PR
- updating an existing PR

---

## 🩻 Troubleshooting

❌ Unavailable model: gpt-5

You have UI access to GPT-5, but API inference is not enabled for your account/region.

Use instead:
- openai/gpt-4o-mini   (recommended, free)

❌ key must be a non-empty string

The GH_MODELS_TOKEN secret is missing or empty.

Fix:
- Ensure it is stored under Secrets, not Variables
- No spaces, quotes, or trailing newlines

❌ The bot comments “null”

Means the model call failed silently → check token + model name.

---

## 💼 Why This Project Is Valuable for Companies

This repository demonstrates capabilities in:
- Advanced GitHub Actions automation
- Secure secret management
- Integration with cloud LLM inference APIs
- Dynamic CI scripting
- Code quality automation
- AI-assisted development workflows
- PR workflow enhancements

It presents practical skills for:
- DevOps / CI/CD Engineers
- Software Engineers
- AI Integration Engineers
- Automation Engineers

Perfect for modern engineering teams adopting AI in their pipelines.

---

## 📜 License

MIT License.

---

## 👤 Author

*Gaetano Vespero*

*DevOps & Automation Engineer* | *Specialist in CI/CD + AI Workflow Integration*