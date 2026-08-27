# Contributing to Vitalis-FSI

We welcome contributions to the Vitalis-FSI ecosystem. To ensure the framework remains lean, sovereign, and surgically precise:

1. **Keep it lean:** New modules must not introduce external dependencies. We prioritize pure NumPy implementations.
2. **Document everything:** Every new plugin or module must include clear docstrings.
3. **Benchmark impact:** If submitting a new cognitive layer, include a summary of the impact on reasoning benchmarks.
4. **Style:** Follow standard PEP-8 guidelines.
5. **PR Flow:** Create a feature branch, run the benchmark suite (`bash benchmark/run_all.sh`), and submit a Pull Request.

Happy hacking.
