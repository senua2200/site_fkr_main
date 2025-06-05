from formatting import process_document_hyperlinks, process_document_tables, process_image_diagram_formatter, process_list_formatter, process_formula_formatter, process_table_formatter, process_deleting_blank_pages, process_GeneralFormating, process_NumberingOfGeadings, process_CreatingTable, process_updating_table, process_page_numbering

class FormattingPipeline:
    def __init__(self):
        # self.process_document_hyperlinks = process_document_hyperlinks
        # self.process_document_tables = process_document_tables
        self.process_image_diagram_formatter = process_image_diagram_formatter
        self.process_list_formatter = process_list_formatter
        self.process_formula_formatter = process_formula_formatter
        self.process_table_formatter = process_table_formatter
        self.process_GeneralFormating = process_GeneralFormating
        self.process_NumberingOfGeadings = process_NumberingOfGeadings
        self.process_CreatingTable = process_CreatingTable
        self.process_deleting_blank_pages = process_deleting_blank_pages
        self.process_page_numbering = process_page_numbering
        self.process_updating_table = process_updating_table

    def process(self, url):
        "Последовательная обработка документа."
        self.process_GeneralFormating(url)
        self.process_image_diagram_formatter(url)
        self.process_list_formatter(url)
        self.process_formula_formatter(url)
        self.process_table_formatter(url)
        self.process_NumberingOfGeadings(url)
        self.process_CreatingTable(url)
        self.process_deleting_blank_pages(url)
        self.process_updating_table(url)
        self.process_page_numbering(url, 1)
        
    print("Все готово!")