from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from xml.etree import ElementTree as ET

def process_document_hyperlinks(doc_path):
    "функция для оработки гиперссылок"
    def get_paragraph_xml(paragraph):
        return paragraph._element.xml

    def is_hyperlink(paragraph_xml):
        root = ET.fromstring(paragraph_xml)
        return root.find('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}hyperlink') is not None

    def apply_hyperlink_styling(paragraph):
        for hyperlink in paragraph._element.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}hyperlink'):
            for run in hyperlink.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r'):
                rPr = run.find('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPr')
                if rPr is None:
                    rPr = OxmlElement('w:rPr')
                    run.insert(0, rPr)
                
                # Установка шрифта
                rFonts = OxmlElement('w:rFonts')
                rFonts.set(qn('w:ascii'), 'Times New Roman')
                rFonts.set(qn('w:eastAsia'), 'Times New Roman')
                rFonts.set(qn('w:hAnsi'), 'Times New Roman')
                rPr.append(rFonts)

                # Установка размера шрифта
                size = OxmlElement('w:sz')
                size.set(qn('w:val'), '28')  # 14 пунктов * 2
                rPr.append(size)

                # Установка цвета
                color = OxmlElement('w:color')
                color.set(qn('w:val'), "0000FF")
                rPr.append(color)

                # Установка подчеркивания
                underline = OxmlElement('w:u')
                underline.set(qn('w:val'), "single")
                rPr.append(underline)

    source_doc = doc_path
    source_document = Document(source_doc)

    for para in source_document.paragraphs:
        para_xml = get_paragraph_xml(para)
        if is_hyperlink(para_xml):
            apply_hyperlink_styling(para)

    source_document.save(source_doc)
    print("Готово")