# AIXtract

**AIXtract** is a modular library designed to support Retrieval-Augmented Generation (RAG) pipelines by providing flexible parsing tools for complex data sources. It enables users to ingest various types of input (e.g., PDFs, XML, raw text), transform them into a unified intermediate format, and evaluate the transformation quality using configurable metrics.

This toolkit is especially useful for building RAG pipelines where consistency and minimal information loss during document transformation are critical.
# ⚡ Quick Start
Follow the guild to quick run AIXtract. 
## 📑 Agenda

- [ 🏁 Install dependencies](#-install-dependencies)
- [ 🖥️ CLI Usage](#️-cli-usage)
- [ 🐳 Docker Usage](#-docker-usage)
- [ 🚀 UI Demo](#-ui-demo)
- [ 🧑‍💻 Join Development](#-for-developers)

## 🏁 Install dependencies
```bash
pip install -r requirements.txt
```
## 🖥️ CLI Usage
Download the source code.
```bash
git clone https://github.com/ChangLijie/AIXtract-dev__confidential.git && cd ./AIXtract-dev__confidential
```
Run the example:
```bash
python3 ./example/pdf2json/main.py

```
---

## 🐳 Docker Usage
Download & Run execute docker container.
```bash
docker run -it --rm --network host innodiskorg/aixtract:latest bash

```
Run the example:
```bash
python3 ./example/pdf2json/main.py

```

## 🚀 UI Demo

If you need to launch a simple Streamlit UI for demonstrating **AIXtract**, please refer to [DEMO.md](./DEMO.md) for detailed instructions.

---

## 🧑‍💻 For Developers
If you are ready to join develop, plz see the [Development README](./README_DEV.md).




