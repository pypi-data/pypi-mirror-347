from io import BytesIO
from pathlib import Path

# relative imports only! otherwise the module is not ofund in the published package
from .utils.merger import merge_xml
from .utils.xml import extract_document_xml, replace_document_xml


def read_file(file_path: str) -> BytesIO:
    with Path(file_path).open("rb") as file:
        stream = BytesIO(file.read())
        stream.seek(0)
    return stream


def merge_docx(
    source_path: str,
    content_path: str,
    output_path: str | None = None,
    pattern: str | None = None,
    insert_start: bool = False,
    insert_end: bool = False,
) -> BytesIO:
    if not source_path:
        raise ValueError("Source file path cannot be empty.")

    if not content_path:
        raise ValueError("Content file path cannot be empty.")

    if not isinstance(source_path, str) or not isinstance(content_path, str):
        raise TypeError("Source and content file paths must be strings.")

    if not isinstance(output_path, (str, type(None))):
        raise TypeError("Output file path must be a string or None.")

    if not isinstance(pattern, (str, type(None))):
        raise TypeError("Pattern must be a string or None.")

    if not isinstance(insert_start, bool):
        raise TypeError("insert_start must be a boolean.")

    if not isinstance(insert_end, bool):
        raise TypeError("insert_end must be a boolean.")

    if not source_path.endswith(".docx"):
        raise ValueError("Source file must be a DOCX file.")

    if not content_path.endswith(".docx"):
        raise ValueError("Content file must be a DOCX file.")

    if output_path and not output_path.endswith(".docx"):
        raise ValueError("Output file must be a DOCX file.")

    if not Path(source_path).is_file():
        raise FileNotFoundError(f"Source file {source_path} does not exist.")

    if not Path(content_path).is_file():
        raise FileNotFoundError(f"Content file {content_path} does not exist.")

    if output_path and Path(output_path).is_file():
        raise FileExistsError(f"Output file {output_path} already exists.")

    if pattern is None and not insert_start and not insert_end:
        raise ValueError("At least one of pattern, insert_start, or insert_end must be specified.")

    source_document_stream = extract_document_xml(source_path)
    content_document_stream = extract_document_xml(content_path)

    # Create the final document.xml stream
    output_document_xml_stream = merge_xml(
        source_xml_stream=source_document_stream,
        content_xml_stream=content_document_stream,
        pattern=pattern,
        insert_start=insert_start,
        insert_end=insert_end,
    )

    # Replace the document.xml in the template DOCX with the final document.xml
    template_stream = read_file(content_path)
    output_stream = replace_document_xml(template_stream, output_document_xml_stream)

    if output_path:
        # Save the modified DOCX to a new file
        with Path(output_path).open("wb") as output_file:
            output_file.write(output_stream.getvalue())

    return output_stream
