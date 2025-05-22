from django.db import models
import os
# Create your models here.

class Category(models.Model):
    name = models.CharField("カテゴリ名", max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField("タグ名", max_length=100)

    def __str__(self):
        return self.name
    

class Reference(models.Model):

    PROGRESS_CHOICES = [
        ("not_started", "未読"),
        ("in_progress", "途中まで読んだ"),
        ("done", "読了"),
    ]

    title      = models.CharField("タイトル", max_length=200)
    authors    = models.CharField("著者", max_length=200, help_text="姓 名, …")
    year       = models.PositiveIntegerField("出版年", blank=True, null=True)
    journal    = models.CharField("雑誌 / 会議名", max_length=200, blank=True)
    url        = models.URLField("URL", blank=True)
    pdf        = models.FileField("PDF", upload_to="pdfs/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    memo       = models.TextField("メモ（Markdown）", blank=True)

    category   = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags       = models.ManyToManyField(Tag, blank=True)
    progress = models.CharField(
        max_length=20,
        choices=PROGRESS_CHOICES,
        default="not_started",
        blank=False,
    )
    def delete(self, *args, **kwargs):
        # PDFファイルが存在すれば削除
        if self.pdf and os.path.isfile(self.pdf.path):
            os.remove(self.pdf.path)
        super().delete(*args, **kwargs)


    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.year})"
    

