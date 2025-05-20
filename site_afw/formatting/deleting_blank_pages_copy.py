import os
import win32com.client

def process_deleting_blank_pages(file_path):
    # Константы Word
    wdStatisticPages = 2
    wdGoToPage = 1
    wdGoToAbsolute = 1
    wdPage = 1

    file_path = os.path.join(os.getcwd(), file_path)
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False

    doc = word.Documents.Open(file_path)
    total_pages = doc.ComputeStatistics(Statistic=wdStatisticPages)

    for page in range(total_pages, 0, -1):
        word.Selection.GoTo(What=wdGoToPage, Which=wdGoToAbsolute, Count=page)
        word.Selection.Expand(Unit=wdPage)
        selection = word.Selection

        text_on_page = selection.Text.strip()
        shapes_count = selection.InlineShapes.Count + selection.ShapeRange.Count

        # Проверяем: если нет текста и нет изображений — удаляем
        if not text_on_page and shapes_count == 0:
            print(f"Удаляется пустая страница {page}")
            selection.Delete()
            selection.Delete()
        else:
            print(f"Пропущена непустая страница {page} (Текст: {len(text_on_page)} символов, Объектов: {shapes_count})")

    doc.Save()
    doc.Close(SaveChanges=True)
    word.Quit()

    print("Удаление пустых страниц завершено.")


















