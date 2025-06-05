from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'


class FormattingProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_template = models.BooleanField(default=False)
    cloned_from_profile = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'formatting_profiles'


class UserProfileChoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chosen_profile = models.ForeignKey(FormattingProfile, related_name='chosen_by_users', on_delete=models.CASCADE)
    custom_profile = models.ForeignKey(FormattingProfile, related_name='custom_by_users', on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_profile_choices'


class UploadedDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=512)
    formatting_profile = models.ForeignKey(FormattingProfile, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'uploaded_documents'


class FormattingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_document = models.ForeignKey(UploadedDocument, on_delete=models.CASCADE)
    formatting_profile = models.ForeignKey(FormattingProfile, on_delete=models.CASCADE)
    total_pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    download_link = models.CharField(max_length=512)
    formatted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'formatting_history'


class ContentsFormatting(models.Model):
    formatting_profile = models.ForeignKey(FormattingProfile, on_delete=models.CASCADE)
    font_size = models.IntegerField()
    font_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'contents_formatting'


class BlankPagesFormatting(models.Model):
    formatting_profile = models.ForeignKey(FormattingProfile, on_delete=models.CASCADE)
    style_name = models.CharField(max_length=100)
    file_name = models.CharField(max_length=255)
    paras = models.TextField()

    class Meta:
        db_table = 'blank_pages_formatting'


class BlankParagraphFormatting(models.Model):
    formatting_profile = models.ForeignKey(FormattingProfile, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    start_index = models.IntegerField()
    para = models.TextField()

    class Meta:
        db_table = 'blank_paragraph_formatting'


class FormulaFormatting(models.Model):
    formatting_profile = models.ForeignKey(FormattingProfile, on_delete=models.CASCADE)
    ole_count = models.IntegerField()
    math_count = models.IntegerField()
    default_page_width = models.FloatField()

    class Meta:
        db_table = 'formula_formatting'


class GeneralFormatting(models.Model):
    formatting_profile = models.ForeignKey(FormattingProfile, on_delete=models.CASCADE)
    line_spacing = models.FloatField()
    font_name = models.CharField(max_length=100)
    font_size = models.IntegerField()

    class Meta:
        db_table = 'general_formatting'


class ImageDiagramFormatting(models.Model):
    formatting_profile = models.ForeignKey(FormattingProfile, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=512)
    images = models.TextField()
    num_chart = models.IntegerField()

    class Meta:
        db_table = 'image_diagram_formatting'


class ListFormatting(models.Model):
    formatting_profile = models.ForeignKey(FormattingProfile, on_delete=models.CASCADE)
    base_indent_cm = models.FloatField()
    additional_indent_cm = models.FloatField()
    hanging_indent = models.FloatField()

    class Meta:
        db_table = 'list_formatting'


class NumberingHeadingsFormatting(models.Model):
    formatting_profile = models.ForeignKey(FormattingProfile, on_delete=models.CASCADE)
    font_name = models.CharField(max_length=100)
    font_size_headlines = models.IntegerField()
    font_color_rgb = models.CharField(max_length=20)

    class Meta:
        db_table = 'numbering_headings_formatting'


class PageNumberingFormatting(models.Model):
    formatting_profile = models.ForeignKey(FormattingProfile, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=512)
    run = models.CharField(max_length=255)
    name_doc_os = models.CharField(max_length=255)

    class Meta:
        db_table = 'page_numbering_formatting'


class TableFormatting(models.Model):
    formatting_profile = models.ForeignKey(FormattingProfile, on_delete=models.CASCADE)
    para_alignment_headlines = models.CharField(max_length=100)
    interval_after_paragraph = models.FloatField()
    interval_before_paragraph = models.FloatField()

    class Meta:
        db_table = 'table_formatting'


class UpdatingContentsFormatting(models.Model):
    formatting_profile = models.ForeignKey(FormattingProfile, on_delete=models.CASCADE)
    font_name = models.CharField(max_length=100)
    font_bold = models.BooleanField(default=False)
    font_size = models.IntegerField()

    class Meta:
        db_table = 'updating_contents_formatting'


class UserQuestions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    question = models.TextField()
    answer = models.TextField()
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_questions'
