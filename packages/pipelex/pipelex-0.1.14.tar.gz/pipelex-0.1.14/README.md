<div align="center">
  <img src=".github/assets/logo.png" alt="Pipelex Logo" width="400" style="max-width: 100%; height: auto;">

  <h3 align="center">The simpler way to build reliable LLM Pipelines</h3>
  <p align="center">Pipelex is an open‑source dev tool based on a simple declarative language<br/>that lets you define replicable, structured, composable LLM pipelines.</p>

  <div>
    <a href="https://github.com/Pipelex/pipelex/doc"><strong>Docs</strong></a> -
    <a href="https://github.com/Pipelex/pipelex/issues"><strong>Report Bug</strong></a> -
    <a href="https://github.com/Pipelex/pipelex/discussions"><strong>Feature Request</strong></a>
  </div>
  <br/>

  <p align="center">
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-ELv2-blue?style=flat-square" alt="ELv2 License"></a>
    <a href="https://github.com/Pipelex/pipelex/releases"><img src="https://img.shields.io/badge/release-v0.1.10-orange?style=flat-square" alt="Release v0.1.10"></a>
    <img src="https://img.shields.io/pypi/v/pipelex?logo=pypi&logoColor=white&color=blue&style=flat-square"
     alt="PyPI – latest release">
    <img src="https://img.shields.io/badge/npm-coming_soon-red?logo=npm&logoColor=white&style=flat-square" alt="npm (coming soon)">
    <br/>
    <br/>
    <a href="https://discord.gg/8UdjGyFh"><img src="https://img.shields.io/badge/Discord-5865F2?logo=discord&logoColor=white&style=flat" alt="Discord"></a>
    <a href="https://www.youtube.com/@PipelexAI"><img src="https://img.shields.io/badge/YouTube-FF0000?logo=youtube&logoColor=white" alt="YouTube"></a>
    <a href="https://twitter.com/pipelexai"><img src="https://img.shields.io/twitter/follow/pipelexai?logo=X&color=%20%23f5f5f5" alt="Follow on X"></a>
    <a href="https://www.linkedin.com/company/evotis"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?logo=linkedin&logoColor=white" alt="LinkedIn"></a>
    <a href="https://pipelex.com"><img src="https://img.shields.io/badge/Website-pipelex.com-0A66C2?logo=google-chrome&logoColor=white&style=flat" alt="Website"></a>
    <br/>
    <!-- <a href="https://github.com/Pipelex/pipelex/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed/Pipelex/pipelex?logo=github&color=purple" alt="Issues Closed"></a>
    <a href="https://github.com/Pipelex/pipelex/discussions"><img src="https://img.shields.io/github/discussions/Pipelex/pipelex?logo=github&color=blue" alt="Discussions"></a>
  </p> -->

  <h3 align="center">🎥 Watch Pipelex in Action</h3>
  <a href="https://vimeo.com/1075832879" style="max-width: 100%; height: auto; display: block; margin: 0 auto;">
    <img src="https://vumbnail.com/1075832879.jpg" alt="Watch the video" style="max-width: 100%; height: auto; display: block; margin: 0 auto;">
  </a>
</div>

## 📑 Table of Contents

- [Introduction](#-introduction)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Optional Features](#optional-features)
- [Contributing](#-contributing)
- [Support](#-support)
- [License](#-license)

## 🚀 Introduction

Pipelex™ is a developer tool designed to simplify building reliable AI applications. At its core is a clear, declarative pipeline language specifically crafted for knowledge-processing tasks.

**The Pipelex language uses pipelines,** or "pipes", each capable of integrating different language models (LLMs) or software to process knowledge. Pipes consistently deliver **structured, predictable outputs** at each stage.

Pipelex employs user-friendly TOML syntax, enabling developers to intuitively define workflows in a narrative-like manner. This approach facilitates collaboration between business professionals, developers, and language models (LLMs), ensuring clarity and ease of communication.

Pipes function like modular building blocks, **assembled by connecting other pipes sequentially, in parallel, or by calling sub-pipes.** This assembly resembles function calls in traditional programming but emphasizes a more intuitive, plug-and-play structure, focused explicitly on clear knowledge input and output.

Pipelex will be distributed as an **open-source Python library,** with a hosted API launching soon, enabling effortless integration into existing software systems and automation frameworks. Additionally, Pipelex will provide an MCP server that will enable AI Agents to run pipelines like any other tool.

## 🚀 Getting Started

### Prerequisites

- Python >=3.11,<3.12
- [pip](https://pip.pypa.io/en/stable/), [poetry](https://python-poetry.org/), or [uv](https://github.com/astral-sh/uv) package manager

### Installation

Choose your preferred installation method:

#### Using pip

```bash
pip install pipelex
```

#### Using Poetry

```bash
poetry add pipelex
```

#### Using uv (Recommended)

```bash
uv pip install pipelex
```

### Optional Features

The package supports additional features that can be installed separately:

```bash
# Using pip
pip install "pipelex[anthropic]"    # For Anthropic/Claude support
pip install "pipelex[google]"       # For Google API support
pip install "pipelex[mistralai]"    # For Mistral AI support
pip install "pipelex[bedrock]"      # For AWS Bedrock support
pip install "pipelex[fal]"          # For image generation with FAL

# Using poetry
poetry add "pipelex[anthropic,google,mistralai,bedrock,fal]"  # Install all features

# Using uv
uv pip install "pipelex[anthropic,google,mistralai,bedrock,fal]"
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to get started, including development setup and testing information.

## 💬 Support

- **GitHub Issues**: For bug reports and feature requests
- **Discussions**: For questions and community discussions
- [**Documentation**](doc/Documentation.md)

## ⭐ Star Us!

If you find Pipelex helpful, please consider giving us a star! It helps us reach more developers and continue improving the tool.

## 👥 Contributors

Contributions are welcome, check out our [Contributing to Pipelex](CONTRIBUTING.md) guide.

## 📝 License

This project is licensed under the **ELv2 license** - see [LICENSING.md](LICENSING.md) file for details.

---

"Pipelex" is a trademark of Evotis S.A.S.

© 2025 Evotis S.A.S.
