# 📄 docx-merge-xml

A fast Python library for merging two Microsoft Word (`.docx`) documents into one. Easily insert content at specific positions or based on placeholder patterns.

---

## 📦 Installation

Install via pip:

```bash
pip install docx-merge-xml
```

## 📚 Dependencies

Only one dependency:

- `lxml` – for parsing and modifying the DOCX XML content

## 🛠️ API

```py
merge_docx(
	source_path: str,
	content_path: str,
	output_path: str | None = None,
	pattern: str | None = None,
	insert_start: bool = False,
	insert_end: bool = False,
) -> BytesIO
```

Parameters:

- `source_path` (_required_) – Path to the base `.docx` file
- `content_path` (_required_) – Path to the `.docx` file to insert into the base
- `output_path` – Path to save the merged document
- `pattern` – Placeholder string in the source file to be replaced with inserted content
- `insert_start` – Insert the content at the **beginning** of the source file
- `insert_end` – Insert the content at the **end** of the source file

🔔 Note: You can combine `pattern`, `insert_start`, and `insert_end` and at least one is required.

## 💡 Examples

### Replace a placeholder in the source DOCX

```py
from docx_merge import merge_docx

buffer = merge_docx(
	source_path="./source.docx",
	content_path="./table.docx",
	pattern="{{table}}"
)

# Use buffer (e.g., send as a response in a server)
```

### Save the output docx by providing an output_path

```py
from docx_merge import merge_docx

buffer = merge_docx(
	source_path="./source.docx",
	content_path="./table.docx",
	output_path="./output.docx",
	pattern="{{table}}"
)
```

### Insert at the start of the document

```py
from docx_merge import merge_docx

merge_docx(
	source_path="./source.docx",
	content_path="./table.docx",
	output_path="./output.docx",
  insert_start=True
)
```

### Insert at the end of the document

```py
from docx_merge import merge_docx

merge_docx(
	source_path="./source.docx",
	content_path="./table.docx",
	output_path="./output.docx",
  insert_end=True
)
```

## 🧪 Testing

This project uses Pytest for unit testing.

To run tests:

```bash
poetry run pytest
```

## 🔒 License

MIT

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome! Feel free to open an issue or submit a pull request.
