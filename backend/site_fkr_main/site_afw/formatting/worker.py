from docx import Document
from docx.oxml.ns import qn

def process_document_tables(doc_path):
    """
    Обрабатывает документ, добавляя к параграфам перед таблицами номера таблиц.
    """
    source_document = Document(doc_path)

    def is_next_element_table(paragraph):
        """
        Проверяет, является ли следующий элемент после параграфа таблицей.
        """
        xml_element = paragraph._element
        next_element = xml_element.getnext()
        if next_element is not None and len(next_element.tag) > 0 and next_element.tag == qn('w:tbl'):
            return True
        return False

    table_number = 1
    # Обработка каждого параграфа
    for para in source_document.paragraphs:
        if is_next_element_table(para):  # Если следующий элемент — таблица
            print("ТАБЛИЦА НАЙДЕНА")
            if para.text.strip():
                para.text = f"Таблица – {table_number} {para.text[0].upper() + para.text[1:]}"  # Форматируем текст параграфа
                table_number += 1

    # Сохранение документа
    source_document.save(doc_path)
    print(f"Документ '{doc_path}' успешно обработан!")
