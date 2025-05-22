from django import forms
from .models import Reference

class ReferenceForm(forms.ModelForm):
    new_category = forms.CharField(label="新規カテゴリ", required=False)
    new_tags = forms.CharField(label="新規タグ（カンマ区切り）", required=False)
    class Meta:
        model = Reference
        fields = ["title", "authors", "year", "journal", "url", "pdf", "category", "tags", "memo"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "mt-1 block w-full border-gray-300 rounded-md shadow-sm"}),
            "authors": forms.TextInput(attrs={"class": "mt-1 block w-full border-gray-300 rounded-md shadow-sm"}),
            "year": forms.NumberInput(attrs={"class": "mt-1 block w-full border-gray-300 rounded-md shadow-sm"}),
            "journal": forms.TextInput(attrs={"class": "mt-1 block w-full border-gray-300 rounded-md shadow-sm"}),
            "url": forms.URLInput(attrs={"class": "mt-1 block w-full border-gray-300 rounded-md shadow-sm"}),
            "pdf": forms.ClearableFileInput(attrs={"class": "mt-1 block w-full"}),
            "category": forms.Select(attrs={"class": "mt-1 block w-full border-gray-300 rounded-md shadow-sm"}),
            "tags": forms.CheckboxSelectMultiple(),  # 任意でカスタムCSSにする
            "memo": forms.Textarea(attrs={"rows": 5, "class": "mt-1 block w-full border-gray-300 rounded-md shadow-sm"}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 新規作成時は memo フィールドを除外または非表示にする
        if not self.instance.pk:
            self.fields['memo'].widget = forms.HiddenInput()
    def clean(self):
        cleaned_data = super().clean()
        new_category = cleaned_data.get("new_category")
        category = cleaned_data.get("category")

        # カテゴリのいずれも指定がない場合はエラー
        if not category and not new_category:
            raise forms.ValidationError("カテゴリを選択または新規入力してください。")

        return cleaned_data