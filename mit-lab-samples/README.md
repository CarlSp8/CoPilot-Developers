# MIT Lab Samples for Advanced LLMs

This directory contains cutting-edge samples and examples from MIT research labs focusing on advanced Large Language Models (LLMs) with new and unreleased models from 2025-2026.

## Overview

MIT has been at the forefront of LLM research, developing innovative techniques to address key challenges in artificial intelligence. This collection showcases the latest breakthroughs in:

- **Reinforcement Learning for LLMs**
- **Continuous Learning without Forgetting**
- **Self-Supervised Learning Techniques**
- **Adaptive Model Training**

## Available Samples

### 1. [FastRL](./fastrl/) - Efficient Reinforcement Learning Framework

MIT HAN Lab's open-source framework for efficient reinforcement learning in language models, particularly for complex reasoning tasks.

**Status**: Released (ASPLOS 2026)
**Key Features**:
- Adaptive speculative decoding
- Efficient RL-based training
- Optimized for long sequences and rare scenarios

### 2. [Self-Distillation Fine-Tuning (SDFT)](./sdft/) - Learning Without Forgetting

A novel fine-tuning technique developed by MIT and ETH Zurich that enables LLMs to learn new skills without catastrophic forgetting.

**Status**: Newly Released (2026)
**Key Features**:
- Prevents knowledge degradation
- Leverages in-context learning
- Continuous skill accumulation
- No retraining required

### 3. [Student-Note Learning](./student-note-learning/) - Self-Improving Models

An innovative approach where LLMs generate their own study notes and use trial-and-error to internalize updates permanently.

**Status**: Research Phase (2025-2026)
**Key Features**:
- Self-editing mechanism
- Adaptive knowledge integration
- Allows smaller models to outperform larger ones
- Improved pattern recognition

### 4. [Test-Time Training](./test-time-training/) - Dynamic Adaptation

A method to temporarily update deployed LLMs using just a few real-world examples for better adaptability on unfamiliar tasks.

**Status**: Research Phase (2025)
**Key Features**:
- On-the-fly model updates
- Improved complex reasoning
- Minimal example requirements
- Strategic planning optimization

### 5. [Models Catalog](./models-catalog/) - Comprehensive Model Information

A catalog of new, unreleased, and recently released LLM models with detailed specifications and capabilities.

## Getting Started

Each subdirectory contains:
- Detailed README with theory and implementation details
- Sample code and scripts
- Usage examples
- References to original papers and repositories

## Requirements

```bash
pip install torch transformers numpy
```

For specific samples, see individual README files for additional dependencies.

## Contributing

These samples are based on MIT research and are intended for educational and research purposes. For contributions or questions, please refer to the original MIT repositories.

## References

- MIT News: [https://news.mit.edu](https://news.mit.edu)
- MIT HAN Lab: [https://github.com/mit-han-lab](https://github.com/mit-han-lab)
- MIT CSAIL: [https://www.csail.mit.edu](https://www.csail.mit.edu)

## License

This educational material follows the MIT License. See individual samples for specific licensing information related to original research.
