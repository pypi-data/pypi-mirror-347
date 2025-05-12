import zipfile
from io import BytesIO

from lxml import etree


def extract_document_xml(file_path: BytesIO | str) -> BytesIO:
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        with zip_ref.open("word/document.xml") as xml_file:
            document_xml_stream = BytesIO(xml_file.read())
            document_xml_stream.seek(0)
    return document_xml_stream


def replace_document_xml(docx_stream: BytesIO, document_xml_stream: BytesIO) -> BytesIO:
    output_zip_stream = BytesIO()
    with zipfile.ZipFile(docx_stream, "r") as docx_zip:
        with zipfile.ZipFile(output_zip_stream, "w", zipfile.ZIP_DEFLATED) as output_zip:
            for item in docx_zip.infolist():
                if item.filename != "word/document.xml":
                    output_zip.writestr(item, docx_zip.read(item.filename))
            output_zip.writestr("word/document.xml", document_xml_stream.getvalue())
    output_zip_stream.seek(0)
    return output_zip_stream


def get_xml_from_stream(file_stream: BytesIO):
    source_tree = etree.parse(file_stream)
    return source_tree.getroot()


def get_string_from_xml(xml_tree: etree._Element):
    # Convert the XML tree to a string
    return etree.tostring(xml_tree, encoding="UTF-8", xml_declaration=True, standalone=True)
