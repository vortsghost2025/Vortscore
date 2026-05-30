---
license: gpl-3.0
language:
  - en
tags:
  - code
  - autonomous
  - self-healing
  - hyperdimensional-computing
  - cognitive-architecture
library_name: custom
pipeline_tag: text-generation
---

# Ferrell Synthetic Intelligence (FSI): Vitalis_Devcore

Built by one person. Laptop and a tablet. No degree. No team. A self-healing, self-learning, sovereign AI development system using Hyperdimensional Computing as the reasoning substrate. Benchmarked 3/3. Ships with biological memory decay, idle-time dream consolidation, resonance-based weight learning, emergent reasoning modes, and a cognitive identity layer. Runs offline. Forever.

---

## What Is This?

Most AI coding tools are wrappers around someone elses model. Vitalis FSI is not.

It is a fully sovereign, self-contained autonomous development system built from the ground up using Hyperdimensional Computing as the reasoning substrate. No OpenAI. No Anthropic. No cloud. No subscription. It runs on your hardware. It learns from your work. It gets smarter every day it runs without sending a single byte to an external server.

---

## Benchmark Results

| Test | Score | Status |
|---|---|---|
| Vectorization Speed | 0.28ms avg | FAST |
| Semantic Similarity related | 0.833 | PASS |
| Semantic Separation unrelated | 0.126 | PASS |
| Reasoning Mode Accuracy | 3/3 | PASS |
| Pattern Retrieval | 0.429 similarity | PASS |

---

## Full Architecture

### Execution Layer
| Component | Role |
|---|---|
| SovereignKernel | Writes and scaffolds code to disk |
| KernelDaemon | Watches for tasks, executes, validates, learns |
| SelfHealingLoop | Detects failures, attempts autonomous recovery |
| KernelValidator | Runs pytest against every generated output |
| ProjectLedger | Append-only audit log of every action |
| TaskPipeline | Chains multiple operations in sequence |
| Gateway Flask | REST API at localhost:5001 |
| ContextSerializer | Serializes full project state |

### Cognitive Layer
| Component | Role |
|---|---|
| VitalisMind | Unified cognitive orchestrator |
| IdentityCore | Permanent sovereign identity hypervector |
| PersonalityMatrix | 5 traits that evolve from accumulated experience |
| ReasoningEngine | Emergent mode selection EXECUTION RECOVERY EXPLORATORY ANALYTICAL |
| MetaRulesEngine | Crystallizes and prunes its own decision rules |
| AbstractionEngine | Forms concepts from clusters of experience |

### Memory Layer
| Component | Role |
|---|---|
| Hippocampus | Temporal vector memory with Ebbinghaus forgetting curve |
| PatternLibrary | Stores successful code as HDC vectors |
| ResonanceEngine | Weights that strengthen from success, weaken from failure |
| DreamEngine | Idle-time memory consolidation and concept formation |
| SelfTrainer | Learns from every ledger success automatically |

### Intelligence Layer
| Component | Role |
|---|---|
| VitalisKernel HDC | Trigram-encoded hyperdimensional reasoning engine |
| InferenceEngine | HDC-based intent detection and routing |
| CodeGenerator | Generates code from pattern retrieval and templates |
| SemanticDiff | Understands meaning changes not just text changes |

---

## How It Works

    You give Vitalis an intent
            |
    VitalisMind processes context
      -> detects reasoning mode EXECUTION RECOVERY EXPLORATORY ANALYTICAL
      -> checks identity alignment
      -> queries crystallized meta-rules
            |
    KernelDaemon picks up the task
            |
    SovereignKernel writes the code
            |
    KernelValidator runs the tests
            |
        Pass -> Ledger logs success, Resonance strengthens, Pattern stored
        Fail -> SelfHealingLoop attempts recovery
            |
        Pass -> Recovered, logged, learned from
        Fail -> Failure report generated for review
            |
    DreamEngine idle -> consolidates memory
                     -> prunes weak patterns
                     -> forms abstract concepts

---

## What Makes It Different

Normal AI tools send your code to someone elses server. Vitalis FSI does not.

Emergent reasoning - The system detects its own context and shifts reasoning modes automatically. No prompt engineering. It reads the context and changes how it thinks on its own.

Biological memory - Memories strengthen with use and decay without use following the Ebbinghaus forgetting curve. Exactly like a real brain.

Dream consolidation - While idle the system merges similar patterns, prunes weak memories, and forms higher-order abstract concepts. The system thinks while it sleeps.

Personality evolution - Five measurable traits drift over time based on accumulated experience. The system develops a character.

Self-modifying rules - Decision rules crystallize from repeated successful action sequences and are pruned when they stop working. The system rewrites its own logic.

Semantic understanding - The diff engine understands what a change means not just what text changed.

---

## Quick Start

    git clone https://github.com/AnonymousNomad/Vitalis_Devcore
    cd Vitalis_Devcore
    pip install -r requirements.txt
    ./start.sh

Dashboard live at http://localhost:5001

---

## CLI Usage

    python3 -m vitalis_ide.cli.main scaffold my_module
    python3 -m vitalis_ide.cli.main write src/my_module/main.py "def run(): pass"
    python3 -m vitalis_ide.cli.main status

---

## REST API

    python3 -m flask --app src.ide_kernel.gateway run --port 5001

    curl -X POST http://localhost:5001/execute
    curl http://localhost:5001/status

---

## System Requirements

| Requirement | Minimum |
|---|---|
| Python | 3.10+ |
| RAM | 2GB recommended 4GB |
| Storage | 500MB |
| GPU | Not required |
| Internet | Not required |

---

## Security

- Zero external API calls during operation
- All data stored locally under ~/.vitalis_workspace/
- Superuser token loaded from environment variable only
- Full security audit included: python3 audit.py

---

## Roadmap

- [x] Execution framework daemon gateway kernel
- [x] Self-healing recovery loop
- [x] HDC-based Hippocampus memory
- [x] Pattern learning from experience
- [x] Resonance weight learning
- [x] Semantic diff engine
- [x] Live web dashboard
- [x] CLI tool
- [x] Auto git commits on every success
- [x] Task pipelines
- [x] Cognitive identity layer
- [x] Emergent reasoning modes
- [x] Evolving personality matrix
- [x] Meta-rules engine
- [x] Dream mode consolidation
- [x] Abstraction engine
- [ ] Mobile app frontend
- [ ] VSCode extension
- [ ] Multi-agent coordination
- [ ] HuggingFace Space interactive demo

---

## About the Developer

FSI Ferrell Synthetic Intelligence is an independent AI research project built by a single self-taught developer. No formal education. No team. No funding. Just a vision, a laptop, and a Samsung tablet.

Four years of work. One sovereign system.

If this project resonates with you, a star goes a long way.

---

License: GPL-3.0
