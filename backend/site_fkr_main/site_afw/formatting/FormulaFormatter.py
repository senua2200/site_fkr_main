import os
import win32com.client
import pythoncom  # Необходимо для инициализации COM

def process_formula_formatter(source_doc):
    """ Получаем путь к текущему скрипту
    current_dir = os.path.dirname(os.path.abspath(__file__))

    Указываем относительный путь к файлу
    source_doc = os.path.join(current_dir, 'КП_Чумаров_Черновик (10_12_2024)).docx') """
    
    # Проверяем, существует ли файл
    if not os.path.exists(source_doc):
        print("Файл не найден!")
    else:
        try:
            # Инициализация COM
            pythoncom.CoInitialize()

            # Открываем Microsoft Word через COM интерфейс
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = False  # Приложение Word будет скрытым (не отображается на экране)

            # Открываем документ
            doc = word.Documents.Open(source_doc)

            # Получаем ширину страницы и вычисляем центр
            page_width = doc.PageSetup.PageWidth  # Ширина страницы
            left_margin = doc.PageSetup.LeftMargin  # Левое поле
            right_margin = doc.PageSetup.RightMargin  # Правое поле
            
            # Устанавливаем значения по умолчанию для "нормальной" страницы
            default_page_width = 595.3  # Стандартная книжная страница в пунктах
            standard_center_position = 240.95  # Центр для стандартной страницы
            standard_right_tab_position = 481.9  # Правая метка для стандартной страницы

            # Проверка, если страница альбомная (ширина больше, чем стандартная)
            if page_width > default_page_width:
                print("Обнаружена альбомная страница, применяются стандартные значения для табуляций.")
                # Применяем стандартные значения для центральной и правой метки
                center_position = standard_center_position
                right_tab_position = standard_right_tab_position
            else:
                center_position = (page_width - left_margin - right_margin) / 2  # Центр страницы
                right_tab_position = page_width - left_margin - right_margin  # Положение второй метки

            # Выводим текущие параметры
            print(f"Ширина страницы: {page_width} pts")
            print(f"Левый отступ: {left_margin} pts")
            print(f"Правый отступ: {right_margin} pts")
            print(f"Центральная позиция табуляции: {center_position} pts")
            print(f"Правая позиция табуляции: {right_tab_position} pts")

            # Функция для проверки, является ли абзац формулой oMath
            def is_omath_formula(paragraph):
                try:
                    return paragraph.Range.OMaths.Count > 0
                except Exception:
                    return False

            # Функция для проверки, является ли абзац формулой OLE (Microsoft Equation 3.0)
            def is_ole_formula(paragraph):
                try:
                    # Проверяем, есть ли OLE-объект в диапазоне
                    for inline_shape in paragraph.Range.InlineShapes:
                        if inline_shape.OLEFormat and inline_shape.OLEFormat.ProgID == "Equation.3":
                            return True
                except Exception:
                    return False
                return False

            # Переменные для подсчета формул
            math_count = 0
            ole_count = 0

            # Переменная для нумерации формул
            math_form_count = 1 

            # Проходим по всем абзацам в документе
            for para in doc.Paragraphs:
                para_text = para.Range.Text.strip()
                
                # Проверяем, является ли абзац формулой oMath
                if is_omath_formula(para):
                    # Получаем первую формулу в абзаце
                    omath = para.Range.OMaths.Item(1)

                    # Удаляем запрещённые символы из текста перед добавлением
                    additional_text = "#" + str(math_form_count)
                    math_form_count+=1
                    cleaned_text = ''.join(ch for ch in additional_text if ch not in '\r\n')

                    # Проверяем, что текст не содержит запрещённых символов
                    if '\r' in cleaned_text or '\n' in cleaned_text:
                        raise ValueError("Запрещённые символы обнаружены в тексте!")

                    # Добавляем очищенный текст к формуле
                    omath.Range.InsertAfter(cleaned_text)

                    # Применяем метод BuildUp для "нажатия Enter" внутри формулы
                    omath.BuildUp()

                    # Увеличиваем счётчик формул
                    math_count += 1

                # Проверяем, является ли абзац формулой OLE
                elif is_ole_formula(para):
                    # Добавляем первую метку табуляции (центр)
                    para.Range.ParagraphFormat.TabStops.Add(Position=center_position, Alignment=1)  # 1 - по центру
                    # Добавляем вторую метку табуляции (по правому краю)
                    para.Range.ParagraphFormat.TabStops.Add(Position=right_tab_position, Alignment=2)  # 2 - по правому краю
                    # Вставляем табуляцию в начале текста
                    para.Range.InsertBefore("\t")

                    # Проходим по InlineShapes текущего абзаца
                    for inline_shape in para.Range.InlineShapes:
                        if inline_shape.OLEFormat and inline_shape.OLEFormat.ProgID == "Equation.3":
                            # Вставляем текст с табуляцией сразу после формулы
                            ole_range = inline_shape.Range
                            ole_range.InsertAfter("\t" + str(math_form_count))  # Добавляем табуляцию перед текстом
                            math_form_count+=1
                            break  # Предполагаем, что работаем только с первой формулой

                    # Увеличиваем счётчик OLE-формул
                    ole_count += 1

            # Сохраняем изменения в документе
            doc.Save()

            # Закрываем документ и Word
            doc.Close()
            word.Quit()

            print(f"Изменения сохранены в документе: {source_doc}")
            print(f"Количество найденных формул oMath: {math_count}")
            print(f"Количество найденных OLE-формул: {ole_count}")

        except Exception as e:
            print(f"Ошибка при обработке документа: {e}")
        
        finally:
            # Завершаем работу с COM
            pythoncom.CoUninitialize()

