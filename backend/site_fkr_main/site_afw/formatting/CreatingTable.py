import win32com.client
import os

def process_CreatingTable(file_path):
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False  # Word работает в фоне
    
    file_name = file_path
    file_path = os.path.join(os.getcwd(), file_name)  # Путь к документу
    
    doc = word.Documents.Open(file_path)
    paragraphs = doc.Paragraphs
    intro_index = None
    
    # Ищем заголовок "Введение"
    for i in range(1, paragraphs.Count + 1):
        para = paragraphs(i)
        if para.Range.Text.strip().lower() == "введение" and para.OutlineLevel <= 3:  # Проверяем, что это заголовок
            intro_index = i
            break
    
    # Проверяем, есть ли уже оглавление в документе
    toc_exists = False
    if doc.TablesOfContents.Count > 0:
        toc_exists = True  # Если хотя бы одно оглавление есть, считаем, что оно уже существует
    
    if toc_exists:
        print("Оглавление уже существует.")
        doc.Close()
        word.Quit()
        return  # Оглавление не будем создавать, если оно уже есть
    
    if intro_index:
        toc_range = paragraphs(intro_index).Range
        toc_range.Collapse(1)  # Устанавливаем курсор перед "Введение"
    else:
        toc_range = doc.Range(0, 0)  # Вставляем в начало документа

    # Вставляем разрыв страницы перед "ОГЛАВЛЕНИЕ"
    toc_range.InsertBreak(7)  # Разрыв страницы (7 = wdPageBreak)
    
    # Вставляем заголовок "ОГЛАВЛЕНИЕ"
    toc_heading = toc_range.Duplicate
    toc_heading.InsertBefore("ОГЛАВЛЕНИЕ\n")
    # Убираем стиль заголовка, чтобы не применялись дополнительные стили
    toc_heading.Style = "Обычный"  # Устанавливаем обычный стиль (без стиля заголовка)

    toc_heading.Font.Name = "Times New Roman"
    toc_heading.Font.Size =  14
    toc_heading.Font.Bold = True  # Делаем заголовок жирным
    toc_heading.ParagraphFormat.Alignment = 1  # Выравнивание по центру (1 = wdAlignParagraphCenter)

    # Убираем интервалы перед и после абзаца для "ОГЛАВЛЕНИЕ"
    toc_heading.ParagraphFormat.SpaceBefore = 0  # Интервал перед абзацем = 0
    toc_heading.ParagraphFormat.SpaceAfter = 0   # Интервал после абзаца = 0
    
    # Перемещаем курсор после "ОГЛАВЛЕНИЕ"
    toc_range = toc_heading.Duplicate
    toc_range.Collapse(0)  

    # Вставляем оглавление
    doc.TablesOfContents.Add(
        Range=toc_range,
        UseHeadingStyles=True,
        UpperHeadingLevel=1,
        LowerHeadingLevel=3,
        UseFields=True,
        TableID="",
        RightAlignPageNumbers=True,
        IncludePageNumbers=True
    )

    # Обновляем оглавление
    doc.TablesOfContents(1).Update()

    # Вставляем разрыв страницы после оглавления
    toc_range = doc.TablesOfContents(1).Range
    toc_range.Collapse(0)  # Перемещаем курсор в конец оглавления
    toc_range.InsertBreak(7)  # Разрыв страницы (7 = wdPageBreak)

    # Сохраняем и закрываем документ
    doc.Save()
    doc.Close()
    word.Quit()

