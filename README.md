# prelegal
A platform for draftng common legal agreements

## Status
🚧 This project is currently in progress. Expected completion: within 1 week.

## Legal document templates

Seed dataset of legal document templates lives in [`templates/`](templates/README.md).
Each template pairs a Markdown document with `{{placeholder}}` fields and a
JSON metadata file describing those fields, for the system to fill in later.
Run `pip install -r requirements-dev.txt && pytest` to validate the dataset.
