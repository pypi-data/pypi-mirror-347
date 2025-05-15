# gcp_toolkit

This library provides simple utility functions for Google Cloud Storage and Cloud Scheduler.

## Installation

```bash
pip install gcp_toolkit
```

## Usage

```python
from gcp_toolkit import upload_file, create_scheduler_job

upload_file("my-bucket", "local.txt", "remote.txt")
create_scheduler_job("my-project", "us-central1", "my-job", "my-topic")
```

## directory structure

gcp_toolkit/
├── gcp_toolkit/
│   ├── __init__.py
│   ├── storage.py
│   └── scheduler.py
├── tests/
│   ├── __init__.py
│   ├── test_storage.py
│   └── test_scheduler.py
├── README.md
├── pyproject.toml
├── LICENSE
└── .gitignore
