---
license: gpl-3.0
language:
  - en
tags:
  - code
  - autonomous
  - self-healing
  - agent
  - code-generation
  - software-engineering
  - agentic
  - devops
library_name: custom
pipeline_tag: text-generation
---

# Ferrell Synthetic Intelligence (FSI): Vitalis_Devcore

> **Vitalis is a self-evolving digital engineer that lives inside your computer — capable of writing, testing, and fixing its own code to build whatever software you can dream up, without you doing the manual heavy lifting.**

Built entirely by one developer. No team. No funding. Four years of self-taught work.

---

## What Is This?

Most AI coding tools are assistants — they wait for you to ask, then suggest. Vitalis is different.

Vitalis_Devcore is an **autonomous execution engine**. It receives an intent, writes the code, runs the tests, and if something breaks, it heals itself and tries again — all without human intervention. It is the "hands" of the FSI ecosystem, designed to operate alongside **[Vitalis_Core](https://huggingface.co/FerrellSyntheticIntelligence/Vitalis_Core)**, which provides the cognitive reasoning layer.

---

## Core Architecture

| Component | Role |
|---|---|
| `SovereignKernel` | Writes and scaffolds code to disk |
| `KernelDaemon` | Watches for tasks, executes them, validates results |
| `SelfHealingLoop` | Detects failures and autonomously attempts recovery |
| `KernelValidator` | Runs pytest against generated code |
| `ProjectLedger` | Immutable append-only audit log of every action |
| `InferenceEngine` | Confidence-gated response generation with RAG augmentation |
| `ConfidenceBridge` | Autonomously re-queries when confidence is in the hypothesis zone (0.45–0.65) |
| `Hippocampus` | Memory-mapped binary vector store for long-term recall |
| `ResonanceEngine` | Continual learning — adjusts kernel weights from interaction history |
| `ContextSerializer` | Serializes full project state for agent context windows |

---

## How It Works

```
You give Vitalis an intent
        ↓
CognitionEngine generates a plan
        ↓
KernelDaemon picks up the task
        ↓
SovereignKernel writes the code
        ↓
KernelValidator runs the tests
        ↓
    Pass → ProjectLedger logs success
    Fail → SelfHealingLoop attempts autonomous recovery
        ↓
    Pass → Recovered and logged
    Fail → Failure report generated for review
```

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://huggingface.co/FerrellSyntheticIntelligence/Vitalis_Devcore
cd Vitalis_Devcore
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the Kernel Daemon
```bash
python3 -m src.ide_kernel.daemon
```

### 4. Send your first task
```bash
python3 -m src.ide_kernel.client scaffold my_module
```

Vitalis will scaffold a full module structure under `app/modules/my_module/`, generate a test file, run it, and log the result — all automatically.

---

## REST Gateway (Optional)

Start the Flask gateway to send tasks over HTTP:

```bash
python3 src/ide_kernel/gateway.py
```

Then POST to it:

```bash
curl -X POST http://127.0.0.1:5001/execute \
  -H "Content-Type: application/json" \
  -d '{"intent": "scaffold", "module_name": "my_module"}'
```

---

## Self-Healing Demo

```bash
# Start the self-healing monitor in a separate terminal
python3 -m src.loop.self_healing

# Trigger a task that fails — Vitalis will detect the failure
# and autonomously attempt recovery without you touching anything
```

---

## Technical Highlights

- **Custom HDC Engine** — A compiled C extension (`hdc_engine.so`) for hyperdimensional computing operations including vector binding and bundling
- **Memory-Mapped Neural Store** — `Hippocampus` uses `numpy.memmap` for persistent binary vector storage across sessions
- **Confidence-Gated Inference** — The `InferenceEngine` uses a `ConfidenceBridge` to autonomously augment prompts when confidence falls in the hypothesis zone
- **Temporal Knowledge Retrieval** — `train_self.py` supports querying memory nodes that were alive at a specific Unix timestamp
- **Hot-Ingestion Daemon** — `watcher.py` monitors the knowledge directory and re-ingests new documents in real time

---

## Governance & Integrity

- **Quality Gates** — All autonomous actions require passing pytest before being committed to the ledger
- **Immutable Audit** — Every action is SHA-recorded in `project_ledger.json`
- **Failure Transparency** — All failures are written to `failure_report.json` before recovery is attempted

---

## Roadmap

- [ ] Connect Vitalis_Core LLM as the live reasoning backend
- [ ] HuggingFace Space interactive demo
- [ ] Natural language task input via CLI
- [ ] Multi-agent coordination between Devcore instances
- [ ] Web UI dashboard for ledger and task visualization

---

## About the Developer

FSI (Ferrell Synthetic Intelligence) is an independent AI research project built by a single self-taught developer over four years — no formal education, no team, no funding. Just a vision, a tablet, and a GPU.

If this project resonates with you, a ⭐ star goes a long way.

---

*License: GPL-3.0*
