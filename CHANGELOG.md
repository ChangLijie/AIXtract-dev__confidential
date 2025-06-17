# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1] - 2025-06-17

### Added
- Initial v0.0.1 of AIXtract pipeline
- Modular structure:
  - readers/ : for parsing various formats (e.g., PDF/XML)
  - preprocessor/ : for document cleaning and segmentation
  - converter/ : for model-based transformation (e.g., LLM summarization)
  - metrics/ : for similarity scoring
  - evaluator/ : for calculating transformation loss
- End-to-end example script (example/py2pdf/main.py)
