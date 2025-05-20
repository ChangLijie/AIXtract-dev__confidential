# SmartDataTransform

**SmartDataTransform** is a modular library designed to support Retrieval-Augmented Generation (RAG) pipelines by providing flexible parsing tools for complex data sources. It enables users to ingest various types of input (e.g., PDFs, XML, raw text), transform them into a unified intermediate format, and evaluate the transformation quality using configurable metrics.

This toolkit is especially useful for building RAG pipelines where consistency and minimal information loss during document transformation are critical.

---

# 🧑‍💻 For Developers
## 🧩 Module Architecture Overview

This library is organized into modular components, each with a clearly defined role and interface. Below is a high-level summary of each core module for developers:

| Module          | Responsibility |
|-----------------|----------------|
| **`converter/`**     | **Unified entry point for data transformation.**<br>It receives raw or preprocessed data and transforms it, typically via LLM (e.g., summarization). All LLM integrations or custom transformation logic are handled here. |
| **`evaluator/`**     | **Entry point for evaluation.**<br>It accepts ground truth (`gt`) and generated data (`data`), along with a chosen metric, and calculates the similarity score. |
| **`metrics/`**       | **Implements similarity algorithms.**<br>Includes methods like string similarity, etc. Used by the evaluator for scoring. |
| **`preprocessor/`**  | **Handles text preprocessing.**<br>Cleans, segments, and formats the output from `readers` before it's sent to the converter. |
| **`readers/`**       | **Implements various data parsers.**<br>Extracts and structures data from sources such as PDF or XML using base readers like `XMLParser`. |
| **`example/`** | **Usage examples and integration demos** |
| **`tests/`** | **Unit tests** and regression coverage |
| **`utils/`** | Helper functions and shared tools |
---

### 📌 Developer Guidelines

- Each module contains a base abstract class (`BaseReader`, `BaseMetric`, etc.) which defines the required interface for that component.
- When extending functionality:
  - ✅ Inherit from the appropriate base class
  - ✅ Implement required methods (e.g., `.convert()`, `.calculate()`)
  - ✅ Place it in the corresponding module folder
  - ✅ Optionally register it in a factory or Enum dispatcher
- The system is designed to be **modular, extensible, and loosely coupled**, allowing plug-and-play for new models, formats, and metrics.

---
## 🚧 Development Workflow

To contribute or develop new features, please follow the branching and release policy below:

### 🔀 Branching Strategy

1. **Create a new feature branch from `main`**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feat/your-feature-name
2. **Develop and commit your changes locally** 
3. **Merge into `dev` first for integration testing.
    ```bash
    git checkout dev
    git merge feat/your-feature-name
    git push origin dev
    ```
4. **Once `dev` is stable, open a Pull Request to `main` for release**
    * Assign a reviewer
    * Ensure all tests pass
    * Describe the change clearly

## 📝 CHANGELOG Management
✅ Important: Before merging into main, update CHANGELOG.md
    This is required because our CI/CD pipeline uses it for versioning and deployment.
Each version update in CHANGELOG.md should follow this format:

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
```
## [x.x.x] - yyyy-mm-dd
### Added
- ...

### Fixed
- ...

### Changed
- ...

```