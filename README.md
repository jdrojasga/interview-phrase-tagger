# Interview phrase tagger
It provides a set of functionalities to tagger interviews according to main topics provided. `iptag` is a toolkit and CLI for **tagging/underlining phrases in interviews** according to a **configurable set of topics** (10, 30, 50+), using **offline/local NLP models** to preserve privacy and meet data-governance constraints.

The main goals are:

- Receive **raw interview transcripts** (e.g. `.txt`, `.jsonl`).
- **Segment** them into phrases or spans.
- **Assign one or more topics** to each phrase (multi-label).
- Optionally **export underlined/annotated text** in different formats (plain text, JSON, etc.).
- Run **fully offline** with CPU-friendly models.

---

## Features

- 🔍 **Phrase-level tagging** of interview text (multi-label).
- 🏷️ **Configurable topic sets** through YAML/JSON schemas.
- 🔒 **Offline-first / local models** for privacy-sensitive data.
- 🧩 Clear **pipeline structure**: segmentation → encoding → classification → export.
- 🧪 Built-in **evaluation** utilities for multi-label settings.
- 💻 Simple **CLI**: `iptag`.

> **Status:** early prototype / WIP.

---

## Installation

The next steps being executed in the terminal, and you have to be in the source folder of this repo.
1. Install [uv](https://github.com/astral-sh/uv). 
```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```
2. Create a virtual environment in which you will install all the dependencies required in the project: 
```bash 
uv venv .venv
```
3. Activate the virtual environment 
```bash 
source .venv/bin/activate
```
4. Install the project to be able to execute the custom command line: 
```bash 
uv pip install -e .
```
5. Test that everything is working 
```bash 
uv run iptag
``` 
or 
```bash 
iptag
```
6. If you want to deactivate the environment just execute:
```bash 
deactivate
```

---

## Tests

### Markers
If you want to see all the available markers, just run:
```bash
uv run pytest --markers
```

#### Adding Markers to Tests
In your test functions, add markers using the `@pytest.mark.markername` decorator:

```python
@pytest.mark.unit
def test_fast_unit_test():
    """A fast unit test."""
    pass

@pytest.mark.integration
def test_component_integration():
    """Test integration between components."""
    pass

@pytest.mark.slow
def test_time_consuming_operation():
    """A test that takes a long time."""
    pass

@pytest.mark.slow
@pytest.mark.integration
def test_slow_integration():
    """A test with multiple markers."""
    pass
```

#### Basic Marker Usage
```bash
# Run only unit tests
uv run pytest -m unit

# Run only integration tests  
uv run pytest -m integration

# Run only slow tests
uv run pytest -m slow

# Skip slow tests
uv run pytest -m "not slow"

# Run unit OR integration tests
uv run pytest -m "unit or integration"

# Run integration AND slow tests
uv run pytest -m "integration and slow"

# Run unit tests but not slow ones
uv run pytest -m "unit and not slow"
```

---

## Project structure

Planned layout (subject to change):

```bash
interview-phrase-tagger/
├── README.md
├── pyproject.toml
├── .gitignore
├── configs/
│   ├── base.yaml           # common config (paths, logging, etc.)
│   ├── model_local.yaml    # config for offline local model
│   └── topics_example.yaml # example topic schema
├── data/
│   ├── raw/                # raw interviews (text, json, etc.)
│   ├── processed/          # cleaned+segmented phrases
│   └── annotations/        # human-labeled data
├── docs/
│   ├── cli_usage.md
│   ├── architecture.md
│   └── examples.md
├── models/
│   ├── checkpoints/        # saved model weights
│   └── artifacts/          # tokenizer, label encoders, etc.
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_training.ipynb
│   └── 03_evaluation.ipynb
├── scripts/
│   ├── preprocess_data.py
│   ├── train_model.py
│   ├── eval_model.py
│   └── export_cli_bundle.py
├── src/
│   └── iptag/
│       ├── __init__.py
│       ├── settings.py
│       ├── cli/
│       │   ├── __init__.py
│       │   ├── annotate/
│       │   ├── data/
│       │   └── models/
│       ├── config.py
│       ├── logging_utils.py
│       ├── phrase_segmentation/
│       │   ├── __init__.py
│       │   └── segmenter.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── classifier.py     # multi-label classifier wrapper
│       │   └── loaders.py        # load local/offline models
│       ├── topics/
│       │   ├── __init__.py
│       │   └── schema.py         # dynamic topic definitions
│       ├── pipeline/
│       │   ├── __init__.py
│       │   └── tagging.py        # end-to-end pipeline
│       └── utils/
│           ├── io.py
│           └── text_cleaning.py
└── tests/
