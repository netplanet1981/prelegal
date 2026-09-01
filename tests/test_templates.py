"""Validates the legal document template dataset in /templates.

Each template is a pair of files: <id>.md (the document text with
{{snake_case}} placeholders) and <id>.json (metadata describing those
placeholders as fillable fields). These tests guarantee the two stay in
sync and that templates/index.json accurately lists the dataset, since a
mismatch would silently break the future template-filling feature.
"""
import json
import re
from pathlib import Path

import pytest

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
PLACEHOLDER_RE = re.compile(r"\{\{\s*([a-z][a-z0-9_]*)\s*\}\}")

REQUIRED_METADATA_KEYS = {"id", "title", "description", "category", "fields"}
REQUIRED_FIELD_KEYS = {"name", "label", "type", "required"}


def load_index():
    index_path = TEMPLATES_DIR / "index.json"
    with index_path.open(encoding="utf-8") as f:
        return json.load(f)


def template_ids():
    return [entry["id"] for entry in load_index()]


def test_index_lists_at_least_five_templates():
    assert len(template_ids()) >= 5


def test_index_entries_have_matching_files_on_disk():
    for template_id in template_ids():
        assert (TEMPLATES_DIR / f"{template_id}.md").is_file(), (
            f"missing markdown file for {template_id}"
        )
        assert (TEMPLATES_DIR / f"{template_id}.json").is_file(), (
            f"missing metadata file for {template_id}"
        )


@pytest.mark.parametrize("template_id", template_ids())
def test_metadata_has_required_keys(template_id):
    metadata = json.loads((TEMPLATES_DIR / f"{template_id}.json").read_text(encoding="utf-8"))
    missing = REQUIRED_METADATA_KEYS - metadata.keys()
    assert not missing, f"{template_id}.json missing keys: {missing}"
    assert metadata["id"] == template_id


@pytest.mark.parametrize("template_id", template_ids())
def test_metadata_fields_have_required_keys(template_id):
    metadata = json.loads((TEMPLATES_DIR / f"{template_id}.json").read_text(encoding="utf-8"))
    assert metadata["fields"], f"{template_id}.json has no fields"
    for field in metadata["fields"]:
        missing = REQUIRED_FIELD_KEYS - field.keys()
        assert not missing, f"{template_id}.json field {field} missing keys: {missing}"


@pytest.mark.parametrize("template_id", template_ids())
def test_placeholders_match_metadata_fields_exactly(template_id):
    markdown = (TEMPLATES_DIR / f"{template_id}.md").read_text(encoding="utf-8")
    placeholders = set(PLACEHOLDER_RE.findall(markdown))

    metadata = json.loads((TEMPLATES_DIR / f"{template_id}.json").read_text(encoding="utf-8"))
    field_names = {field["name"] for field in metadata["fields"]}

    missing_fields = placeholders - field_names
    unused_fields = field_names - placeholders
    assert not missing_fields, f"{template_id}.md has placeholders with no metadata field: {missing_fields}"
    assert not unused_fields, f"{template_id}.json declares fields never used in the template: {unused_fields}"
