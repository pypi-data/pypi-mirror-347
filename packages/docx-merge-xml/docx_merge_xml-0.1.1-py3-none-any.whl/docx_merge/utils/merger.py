from copy import deepcopy
from io import BytesIO

# relative imports only! otherwise the module is not ofund in the published package
from .xml import get_string_from_xml, get_xml_from_stream


def merge_xml(
    source_xml_stream: BytesIO, content_xml_stream: BytesIO, pattern: str | None, insert_start: bool, insert_end: bool
) -> BytesIO:
    # Parse the content XML
    source_root = get_xml_from_stream(content_xml_stream)

    # Define the namespaces
    namespaces = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

    # Find the <w:body> tag in the source XML
    source_body = source_root.find(".//w:body", namespaces)
    if source_body is None:
        raise ValueError("No <body> tag found in the content XML")

    # Filter out <w:sectPr> tags from the source XML
    filtered_elements = []
    for elem in source_body:
        if elem.tag == "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}sectPr":
            continue
        filtered_elements.append(elem)

    # Parse the target template XML
    target_root = get_xml_from_stream(source_xml_stream)

    # Find the <w:body> tag in the target template XML
    target_body = target_root.find(".//w:body", namespaces)
    if target_body is None:
        raise ValueError("No <body> tag found in the target template XML")

    # Find the <w:sectPr> tag in the target XML
    sect_pr = target_body.find("w:sectPr", namespaces)
    if sect_pr is None:
        raise ValueError("No <sectPr> tag found in the target XML")

    index_offset = 0
    for index, elem in enumerate(target_body):
        text_elem = elem.find(".//w:t", namespaces)
        text_content = text_elem.text if text_elem is not None else ""
        if text_content == pattern:
            target_body.remove(elem)
            for content_elem_index, elem in enumerate(deepcopy(filtered_elements)):
                target_body.insert(index + index_offset + content_elem_index, elem)
            index_offset += len(filtered_elements)
        if elem.tag == "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}sectPr":
            if insert_end:
                # Insert the filtered elements at the end of the body
                for content_elem_index, elem in enumerate(deepcopy(filtered_elements)):
                    target_body.insert(index + index_offset + content_elem_index, elem)
            break

    if insert_start:
        # Insert the filtered elements at the start of the body
        for content_elem_index, elem in enumerate(deepcopy(filtered_elements)):
            target_body.insert(content_elem_index, elem)

    if index_offset == 0 and not insert_start and not insert_end:
        # No pattern found and no insert_start or insert_end specified
        raise ValueError("No pattern found in the target XML and no insert_start or insert_end specified.")

    output_stream = BytesIO()
    output_stream.write(get_string_from_xml(target_root))
    output_stream.seek(0)
    return output_stream
