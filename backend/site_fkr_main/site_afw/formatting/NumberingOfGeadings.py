import os
import win32com.client as win32
from docx.enum.text import WD_LINE_SPACING
import pythoncom

def process_NumberingOfGeadings(file_path):
    # Получаем путь к текущей директории, в которой находится скрипт
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Формируем путь к файлу report.docx
    file_b = os.path.join(script_dir, file_path)

    # Запуск Word через COM
    pythoncom.CoInitialize()
    word = win32.Dispatch('Word.Application')
    word.Visible = False  # Скрыть приложение Word

    # Счетчики для нумерации заголовков
    counters = {
        1: 0,  # Уровень 1 (Желтый)
        2: 0,  # Уровень 2 (Ярко-зеленый)
        3: 0,  # Уровень 3 (Бирюзовый)
        4: 0,  # Уровень 4 (Лиловый)
        5: 0   # Уровень 5 (Синий)
    }

    # Соответствие цветов уровням
    highlight_to_level = {
        7: 1,  # Желтый
        4: 2,  # Ярко-зеленый
        3: 3,  # Бирюзовый
        5: 4,  # Лиловый
        2: 5   # Синий
    }

    # Соответствие уровней стилям
    level_to_style = {
        1: "Заголовок 1",
        2: "Заголовок 2",
        3: "Заголовок 3",
        4: "Заголовок 4",
        5: "Заголовок 5"
    }

    # Параметры для форматирования
    font_size_headlines = 16  # Размер заголовков
    font_name = 'Times New Roman'
    font_color_rgb = 0x000000  # Цвет шрифта — черный (OLE_COLOR)
    para_alignment_headlines = 1  # Выравнивание текста по центру
    line_spacing_rule_1_5 = WD_LINE_SPACING.ONE_POINT_FIVE  # Межстрочный интервал

    # Отступы
    left_margin = 0
    right_margin = 0
    interval_before_paragraph = 0
    interval_after_paragraph = 0

    # Слова, которые не должны нумероваться
    excluded_titles = {
        "введение", "заключение", "список литературы", "приложение", "список использованной литературы", 
        "список используемой литературы", "литература", "библиографический список", "перечень источников", 
        "источники и литература", "список источников и литературы", "рекомендуемая литература", 
        "привлеченные источники", "список использованных источников и материалов", 
        "список использованных источников и литературы", "список использованных источников", 
        "использованные источники", "используемые источники", "список использованных источников"
    }

    def reset_counters(level):
        """Сброс счетчиков ниже текущего уровня"""
        for lvl in range(level + 1, 6):
            counters[lvl] = 0

    def adjust_counters(current_level, previous_level):
        """Корректировка уровней для соблюдения вложенности"""
        if current_level > previous_level + 1:
            # Если текущий уровень больше допустимого, выравниваем его
            current_level = previous_level + 1
        elif current_level <= previous_level:
            # Сброс всех уровней ниже текущего
            reset_counters(current_level)
        return current_level

    # Основной цикл обработки документа
    try:
        doc_b = word.Documents.Open(file_b)

        previous_level = 0  # Уровень предыдущего обработанного слова

        for paragraph in doc_b.Paragraphs:
            # Пропускаем абзацы, которые находятся в таблицах
            if paragraph.Range.Information(win32.constants.wdWithInTable):
                continue  # Пропускаем текущий абзац, если он находится в таблице
            # Проверка, есть ли текст в абзаце
            if paragraph.Range.Text.strip():
                highlight = paragraph.Range.HighlightColorIndex
                text = paragraph.Range.Text.strip()
                if paragraph.Range.InlineShapes.Count > 0:
                    continue

                # Очистка текста от лишних пробелов и переводов строк
                cleaned_text = " ".join(text.split()).lower()

                # Отладочный вывод для проверки
                print(f"NumberingOfGeadings22NumberingOfGeadings22 Проверяемый текст: '{cleaned_text}'")

                # Проверка на исключенные заголовки
                if cleaned_text in (title.lower() for title in excluded_titles):
                    # Пропускаем нумерацию, но применяем форматирование
                    paragraph.Range.HighlightColorIndex = 0  # Убираем выделение цвета
                    paragraph.Range.Style = level_to_style.get(1, "")
                    paragraph.Range.Font.Size = font_size_headlines
                    paragraph.Range.Font.Name = font_name
                    paragraph.Range.Font.Color = font_color_rgb
                    paragraph.Range.Font.Bold = True  # Жирное выделение
                    paragraph.Alignment = para_alignment_headlines
                    paragraph.LineSpacingRule = line_spacing_rule_1_5
                    paragraph.SpaceBefore = interval_before_paragraph
                    paragraph.SpaceAfter = interval_after_paragraph
                    continue

                if highlight in highlight_to_level:
                    current_level = highlight_to_level[highlight]
                    current_level = adjust_counters(current_level, previous_level)

                    # Увеличиваем счетчик текущего уровня
                    counters[current_level] += 1
                    numbering = ".".join(str(counters[lvl]) for lvl in range(1, current_level + 1)) + "."

                    # Сбрасываем выделение текста абзаца
                    paragraph.Range.HighlightColorIndex = 0

                    # Применяем стиль заголовка ко всему абзацу
                    paragraph.Range.Style = level_to_style[current_level]

                    # Добавляем нумерацию с табуляцией и точкой к первому слову абзаца
                    words = list(paragraph.Range.Words)
                    if words:
                        first_word_range = words[0]
                        first_word_range.InsertBefore(f"{numbering} ")

                    # Форматирование всего текста заголовка
                    paragraph.Range.Font.Size = font_size_headlines
                    paragraph.Range.Font.Name = font_name
                    paragraph.Range.Font.Color = font_color_rgb  # Используем OLE_COLOR
                    paragraph.Range.Font.Bold = True  # Жирный шрифт
                    paragraph.Range.Font.Italic = False  # Убираем курсив
                    paragraph.Range.Font.Underline = False  # Убираем подчеркивание

                    # Форматирование текста абзаца
                    paragraph.Alignment = para_alignment_headlines
                    paragraph.LineSpacingRule = line_spacing_rule_1_5
                    paragraph.LeftIndent = left_margin
                    paragraph.RightIndent = right_margin
                    paragraph.SpaceBefore = interval_before_paragraph
                    paragraph.SpaceAfter = interval_after_paragraph

                    # Обновляем уровень предыдущего заголовка
                    previous_level = current_level

        # Сохраняем документ с изменениями
        new_file_path = os.path.join(script_dir, file_path)
        doc_b.SaveAs(new_file_path)
        print(f"Документ сохранен как: {new_file_path}")

    finally:
        # Закрываем документ и приложение Word
        doc_b.Close()
        word.Quit()
        pythoncom.CoUninitialize()


