<div align="center">
  
# ⚔️ CyberWarriorV2  
### AI-Powered Bug Bounty Scanner & Auto-Patching Agent

Find vulnerabilities. Fix code. Push secure patches — automatically.  
A hybrid local + cloud AI security platform built for real ethical hackers.

</div>

---

## 🚀 What is CyberWarriorV2?

CyberWarriorV2 is a next-generation AI bug bounty assistant that:

✔ Analyzes source code for vulnerabilities using **multiple ML models**  
✔ Scores risk using **CVSS** (industry standard)  
✔ Generates **security patches automatically** using cloud LLMs  
✔ Provides a **visual dashboard** with diffs, explanations, and severity  
✔ Works on **local folders**, private codebases, or GitHub repos  

It’s designed for:

- Bug bounty hunters  
- Red teams & security researchers  
- DevSecOps engineers  
- Students learning secure coding  

---

## 🔐 Key Features

| Capability | Status |
|----------|:------:|
| AI-based vulnerability detection (CodeBERT ensemble) | ✔ |
| Patch generation using Hugging Face Inference API | ✔ |
| FastAPI backend + React dashboard | ✔ |
| CVSS scoring & CWE context | ✔ |
| Local repo scanning (offline mode supported) | ✔ |
| GitHub URL scanning | Partial (depends on network) |
| GitHub PR auto-patching | 🔜 coming soon |
| ZIP uploads for scanning | 🔜 coming soon |
| Support for more languages | 🚧 in dev |

---

## 🧠 AI Models Used

| Purpose | Model | Location |
|--------|-------|---------|
| Vulnerability classification | CodeBERT + ensemble models | Local |
| Code repair & patching | Salesforce/codeT5-base | Cloud (HF Inference API) |

Hybrid AI gives the **best of both worlds**:

> Fast offline detection + Cloud intelligence for secure patches

---

## 🛠 Tech Stack

**Backend**
- Python 3.13
- FastAPI
- HuggingFace Inference API
- GitPython
- UVicorn
- CVSS scoring engine

**Frontend**
- React + Vite
- TailwindCSS
- Flexible dark cyber-theme UI
- Monaco Editor for code diffs (VS Code engine)

---

## 📦 Installation

```bash
git clone https://github.com/cybertarr-A/CyberWarriorV2.git
cd CyberWarriorV2
