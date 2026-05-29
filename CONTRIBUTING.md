<<<<<<< HEAD
# Contributing to Vitalis-FSI

We welcome contributions to the Vitalis-FSI ecosystem. To ensure the framework remains lean, sovereign, and surgically precise:

1. **Keep it lean:** New modules must not introduce external dependencies. We prioritize pure NumPy implementations.
2. **Document everything:** Every new plugin or module must include clear docstrings.
3. **Benchmark impact:** If submitting a new cognitive layer, include a summary of the impact on reasoning benchmarks.
4. **Style:** Follow standard PEP-8 guidelines.
5. **PR Flow:** Create a feature branch, run the benchmark suite (`bash benchmark/run_all.sh`), and submit a Pull Request.

Happy hacking.
=======
# Contributing to Veritas_Core

We welcome professional contributions to Veritas_Core. To ensure the integrity of the architecture and the security of the framework, all contributions must adhere to the following guidelines.

## Development Standards
- **Security First**: All changes must undergo a security review. Any commit that introduces a potential vulnerability in the `kernel_interface` or `sovereign_shield` will be rejected.
- **Minimalism**: Veritas_Core is built on a "low-dependency" philosophy. Do not introduce new external libraries unless absolutely necessary for the core engine.
- **Code Style**: Code must be clean, modular, and documented. Ensure all new functions have clear docstrings and follow existing naming conventions.

## How to Contribute
1. **Fork the Repository**: Create your own fork of the main branch.
2. **Feature Branching**: Create a branch for your specific task (e.g., `feature/memory-optimization` or `fix/kernel-bridge`).
3. **Submit a Pull Request (PR)**: Clearly describe the change, the architectural impact, and the testing performed.
4. **Review Process**: The lead architect (Neuro_Nomad) will review the PR for security, efficiency, and structural alignment.

## Reporting Issues
If you identify a bug or a security vulnerability, please open an issue with:
- A clear description of the issue.
- Steps to reproduce the behavior.
- Expected vs. actual results.
- Any relevant logs or kernel telemetry.

*Veritas_Core is a sovereign framework. Contributions must uphold the integrity of this mission.*
>>>>>>> c3ceffd7c7253d3cb91ddea5998e5dc497615daa
