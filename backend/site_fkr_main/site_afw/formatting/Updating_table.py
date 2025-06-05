import win32com.client
import os

def process_updating_table(file_path):
    def update_table_of_contents(file_path):
        # Укажите путь к вашему документу
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Указываем относительный путь к файлу
        file_path = os.path.join(current_dir, file_path)
        # Инициализация приложения Word
        word_app = win32com.client.Dispatch("Word.Application")
        word_app.Visible = False

        # Открытие документа
        doc = word_app.Documents.Open(file_path)

        # Обновление содержания
        for toc in doc.TablesOfContents:
            toc.Update()

            toc = doc.TablesOfContents(1)
            toc_range = toc.Range
            toc_range.Font.Size = 14  # Устанавливаем размер шрифта 16
            toc_range.Font.Bold = False
            toc_range.Font.Name = 'Times New Roman'

        # Сохранение документа
        doc.Save()
        doc.Close()
        word_app.Quit()
        print("Содержание успешно обновлено.")

    def remove_consecutive_empty_paragraphs(file_name):
        file_path = os.path.join(os.getcwd(), file_name)
        
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc = word.Documents.Open(file_path)

        # Получаем диапазоны всех TOC (оглавлений)
        toc_ranges = [(toc.Range.Start, toc.Range.End) for toc in doc.TablesOfContents]

        empty_sequence = []

        # Проходим абзацы с конца
        for i in range(doc.Paragraphs.Count, 0, -1):
            para = doc.Paragraphs(i)
            rng = para.Range
            text = rng.Text.strip()

            # Проверяем, входит ли абзац в один из TOC-диапазонов
            in_toc = any(start <= rng.Start <= end for start, end in toc_ranges)

            if not in_toc and text == "":
                empty_sequence.append(rng)
            else:
                # Если встретили непустой абзац, проверим длину последовательности
                if len(empty_sequence) >= 2:
                    for rng_to_delete in empty_sequence:
                        # Убедимся, что это не разрыв раздела
                        if not rng_to_delete.Find.Execute(FindText="^m"):
                            rng_to_delete.Delete()
                # Сбросим последовательность
                empty_sequence = []

        # Если документ заканчивается на пустую последовательность
        if len(empty_sequence) >= 2:
            for rng_to_delete in empty_sequence:
                if not rng_to_delete.Find.Execute(FindText="^m"):
                    rng_to_delete.Delete()

        doc.Save()
        doc.Close()
        word.Quit()
        print(f"Удалены последовательности из 2 и более пустых абзацев в файле '{file_name}'.")

    remove_consecutive_empty_paragraphs(file_path)

    update_table_of_contents(file_path)



