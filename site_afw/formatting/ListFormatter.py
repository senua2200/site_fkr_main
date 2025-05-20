from lxml import etree
from zipfile import ZipFile, ZIP_DEFLATED
import shutil
import os

def process_list_formatter(docx_path):
    def extract_and_modify_xml_in_docx(docx_path):
        """Извлекает XML контент, модифицирует его и сохраняет обратно в тот же файл .docx."""
        temp_dir = "temp_docx"
        
        # Распаковываем файл .docx во временную директорию
        with ZipFile(docx_path, 'r') as docx:
            docx.extractall(temp_dir)
        
        # Читаем и модифицируем XML
        xml_path = os.path.join(temp_dir, 'word/document.xml')
        with open(xml_path, 'rb') as xml_file:
            xml_content = xml_file.read()
        
        modified_xml_content = parse_and_modify_paragraphs(xml_content)
        
        # Сохраняем изменения
        with open(xml_path, 'wb') as xml_file:
            xml_file.write(modified_xml_content)
        
        # Пересобираем файл .docx
        temp_docx_path = f"{docx_path}.temp"
        with ZipFile(temp_docx_path, 'w', ZIP_DEFLATED) as modified_docx:
            for folder_name, subfolders, filenames in os.walk(temp_dir):
                for filename in filenames:
                    file_path = os.path.join(folder_name, filename)
                    arcname = os.path.relpath(file_path, temp_dir)
                    modified_docx.write(file_path, arcname)
        
        # Заменяем исходный файл
        shutil.move(temp_docx_path, docx_path)
        
        # Удаляем временные файлы
        shutil.rmtree(temp_dir)


    def parse_and_modify_paragraphs(xml_content):
        """Извлекает абзацы, модифицирует текст списков в определенном диапазоне."""
        namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        tree = etree.XML(xml_content)

        # Список исключенных заголовков
        excluded_titles = {
            "введение", "Список литературы", "Приложение", "список использованной литературы", "Список используемой литературы", "Литература", 
            "Библиографический список", "Перечень источников", "Источники и литература", "Список источников и литературы", "Рекомендуемая литература", 
            "Привлеченные источники", "Список использованных источников и материалов", "Список использованных источников и литературы", "Список использованных источников",  
            "Использованные источники", "Используемые источники"
        }

        # Константы для расчёта отступов
        base_indent_cm = 1.88  # Базовый отступ, см
        additional_indent_cm = 1.25  # Дополнительный отступ на уровень, см
        hanging_indent = 357  # Выступ (0,63 см)
        cm_to_word_units = 567  # 1 см = 567 единиц Word
        base_indent = int(base_indent_cm * cm_to_word_units)
        additional_indent = int(additional_indent_cm * cm_to_word_units)

        paragraphs = tree.xpath('//w:p', namespaces=namespaces)

        processing = False
        start_processing_count = 0

        for i, para in enumerate(paragraphs, start=1):
            # Проверяем текст абзаца
            text_elements = para.xpath('.//w:t', namespaces=namespaces)
            text = ''.join(el.text for el in text_elements if el.text).strip()

            # Проверяем, выделен ли текст желтым цветом
            highlighted = para.xpath('.//w:highlight[@w:val="yellow"]', namespaces=namespaces)
            if highlighted and text.lower() in (title.lower() for title in excluded_titles):
                start_processing_count += 1
                if start_processing_count == 1:
                    print(f"Обнаружен первый выделенный заголовок: {text}. Начинаем обработку списков.")
                    processing = True
                    continue
                elif start_processing_count == 2:
                    print(f"Обнаружен второй выделенный заголовок: {text}. Завершаем обработку списков.")
                    processing = False
                    break

            if processing:
                # Проверяем, является ли абзац элементом списка
                ilvl = para.xpath('.//w:numPr/w:ilvl/@w:val', namespaces=namespaces)
                ilvl = int(ilvl[0]) if ilvl else None  # Уровень списка

                # Игнорируем элементы списка, выделенные желтым цветом
                if highlighted and ilvl is not None:
                    print(f"Абзац {i}: Элемент списка, выделенный желтым цветом, игнорируется.")
                    continue

                if ilvl is not None:  # Это пункт списка
                    # Добавляем или модифицируем тег отступов
                    para_properties = para.find('./w:pPr', namespaces=namespaces)
                    if para_properties is None:
                        para_properties = etree.SubElement(para, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pPr')

                    ind_tag = para_properties.find('./w:ind', namespaces=namespaces)
                    if ind_tag is None:
                        ind_tag = etree.SubElement(para_properties, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ind')

                    # Рассчитываем отступ слева для текущего уровня
                    left_indent = base_indent + additional_indent * ilvl
                    ind_tag.set('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}left', str(left_indent))
                    ind_tag.set('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}hanging', str(hanging_indent))
                    print(f"Абзац {i}: Уровень списка = {ilvl}, отступ слева = {left_indent}, выступ = {hanging_indent}")
                else:
                    print(f"Абзац {i}: не является элементом списка, изменения не применяются.")

        # Возвращаем изменённое дерево в виде строки
        return etree.tostring(tree, encoding='utf-8', xml_declaration=True)


    # Путь к вашему файлу .docx
    # docx_path = 'C:/test_python/КП_Чумаров_Черновик (10_12_2024)).docx'

    # Обрабатываем файл: изменяем XML внутри документа
    extract_and_modify_xml_in_docx(docx_path)

    print(f"Изменения сохранены в исходный файл {docx_path}.")
