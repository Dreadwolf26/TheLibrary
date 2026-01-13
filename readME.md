### Overview

This project implements a **local prompt evaluation and iteration system** designed to improve prompt quality through structured scoring and controlled evolution.

Prompts are treated as versioned artifacts. Each prompt execution is evaluated against a fixed rubric, scored, and stored for later review. Over time, prompt variants can be compared empirically rather than subjectively.

The system is intentionally minimal and deterministic to avoid uncontrolled prompt drift.

---

### Core Capabilities

* Versioned prompt storage with lineage tracking
* Automated prompt execution using **Ollama (local models)**
* Structured evaluation of prompt outputs using a fixed rubric
* Iterative prompt mutation based on evaluation results
* Persistent storage of prompts, outputs, and scores in **SQLite**
* Human-reviewable history of prompt performance over time

---

### Design Principles

* **Prompts are data**, not strings
* **Evaluation rules are fixed** and externalized (YAML)
* **Generation and evaluation are separated**
* **Iteration is controlled**, not autonomous
* **All results are persisted** for auditability

This project prioritizes reproducibility and observability over creative autonomy.

---

### Architecture (High-Level)

* **Configuration Layer**
  Task definition, constraints, and evaluation rubric stored in YAML

* **Prompt Engine**
  Executes prompts via Ollama and captures raw outputs

* **Evaluation Engine**
  Scores outputs against the rubric using a separate evaluator prompt

* **Persistence Layer**
  SQLite database storing prompt versions, executions, evaluations, and lineage

---

### Current Status

This project is under active development.

The current focus is establishing:

* A stable prompt execution loop
* A consistent evaluation rubric
* Reliable persistence and version tracking

Future enhancements may include additional mutation strategies, analytics, and workflow integration.

---

### Non-Goals

This project is **not**:

* A general autonomous agent
* A chatbot framework
* A self-modifying system without constraints
* A prompt marketplace or UI-driven tool

---

### Motivation

Prompt quality is often evaluated informally and inconsistently.
This project explores a structured, repeatable approach to prompt improvement that emphasizes measurement, traceability, and controlled iteration.
