# AUTOMATED RESTORE-READINESS DRILL
## User Guide

### Requirements
- Python 3.9+

### Setup
1. Open a terminal in the `restore-readiness-drill` directory.
2. Create a virtual environment:
   `python -m venv .venv`
3. Activate it:
   - Mac/Linux: `source .venv/bin/activate`
   - Windows: `.venv\Scripts\activate`
4. Install dependencies:
   `pip install -r requirements.txt`

### Running the Demo Experiment
To generate the dataset, inject failures, and run the 10 restore drill attempts automatically:
```bash
python run_demo.py
```
This will populate the SQLite database and print a summary to the console.

### Viewing the Dashboard
To view the visual report:
```bash
uvicorn backend.main:app --reload --port 8000
```
Open a browser and navigate to `http://localhost:8000/`.

### Running Tests
To run the automated test suite:
```bash
pytest
```
