# cmfapi 
This package provides a simple, modular SDK for the Common Metadata Framework (CMF) REST API.

## Features

* Automatically handles authentication and renewal
* Graceful error management
* Logically organized modules
* Easily maintained

## Installation

**Install using `pip`:**

```bash
pip install cmfapi
```

**Install from source:**

```bash
git clone https://github.com/atripathy86/cmfapi.git
cd cmfapi
pip install -e .
```

**Build/Upload for pypi:**

```bash
pip install build
# Build the package
python -m build 
#Creates dist/ with tar.gz and .whl 
```

```bash 
pip install twine
twine upload dist/*
```

## Quick Start

### Initialize the Client

```python
from cmfapi import cmfClient
client = cmfClient("http://192.168.2.143:8080")
```

### Example Usage

#### Get CMF API Server Pipelines

```python
pipelines = client.get_pipelines()
print(pipelines)  
```
