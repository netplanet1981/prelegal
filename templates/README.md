# Legal document templates

This directory is the seed dataset of legal document templates the
system will fill in on behalf of a user. Each template is a pair of
files sharing an id:

- `<id>.md` — the document text, with fillable spots marked as
  `{{snake_case_placeholder}}`.
- `<id>.json` — metadata describing every placeholder in the `.md` file
  as a field (`name`, `label`, `type`, `required`), plus a `title`,
  `description`, and `category` for the template as a whole.

`index.json` lists every template's `id`, `title`, and `category` for
discovery without reading each metadata file.

## Adding a template

1. Add `<id>.md` and `<id>.json` following the existing pairs.
2. Add an entry to `index.json`.
3. Ensure every `{{placeholder}}` used in the `.md` has a matching
   entry in the `.json` `fields` array, and vice versa — this is
   enforced by `tests/test_templates.py`.

## Field types

`string` (single line), `text` (multi-line/free text), `date`,
`currency`, `number`.
