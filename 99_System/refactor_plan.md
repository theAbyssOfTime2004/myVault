# Refactor Plan: Obsidian Vault Re-organization
**Target User:** Mai Phong Đăng (AI Engineer Intern, Final Year Student)
**Objective:** Transform a flat, cluttered vault into a "PARA-style" system optimized for Thesis work, Internship, and University Retakes.

---

## 1. Current State Analysis (Diagnosis)
* **Root Clutter:** High volume of loose assets (`Pasted image...png`, `Untitled.canvas`) polluting the root directory.
* **"Dumpster" Folders:**
    * `6 - Main Notes`: Contains mixed concerns (AI theory, Networking, Math, Thesis drafts, Homework reports). Hard to retrieve specific contexts.
    * `2 - Source Material`: Acts as a catch-all without categorization.
* **Project Isolation:** Active projects (`Seminar-Thesis`) and skill tracks (`dsa plan`, `oop`) are disconnected from the main knowledge base.
* **Missing Contexts:** No dedicated space for current high-priority goals (Internship at Tiger Tribe, 3 Retake Courses).

---

## 2. Target Directory Structure
The agent should create this folder tree. If a folder exists, merge into it.

```text
Root/
├── 00_Dashboard/                # High-level management (Home, Todo)
├── 10_Projects/                 # Active projects with deadlines
│   ├── 11_Thesis_WorldModel/    # Thesis & Research
│   ├── 12_TigerTribe_Intern/    # Work logs, Company projects
│   └── 13_Uni_Retake/           # The 3 retake courses (Math, Physics)
├── 20_Areas/                    # Ongoing responsibilities & Skills
│   ├── Coding_Skills/           # DSA, OOP, Leetcode
│   └── Personal_Growth/         # Reading, Health, Misc
├── 30_Knowledge_Base/           # The Core Library (Refactored from Main Notes)
│   ├── AI_DeepLearning/         # Models, Algorithms, Papers
│   ├── CS_Networking_OS/        # Networking, OS, Distributed Systems
│   ├── Math_Stats/              # Linear Algebra, Calculus, Prob
│   └── Dev_Tools/               # Docker, Git, Linux, LangChain
├── 40_Archives/                 # Inactive/Finished items
│   ├── Uni_Year1_3/             # Old homework, reports, slides
│   └── Old_Research/            # Old topics (Forest Fire, etc.)
└── 99_System/                   # Supporting files
    ├── Assets/
    │   ├── Images/              # All pasted images go here
    │   └── Files/               # PDFs, Docx attachments
    ├── Templates/               # Note templates
    └── Plugin_Data/             # Copilot, etc.