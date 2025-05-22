import markdown

from django.shortcuts import render,get_object_or_404, redirect
from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .models import Reference, Category, Tag

from .forms import ReferenceForm

from sentence_transformers import SentenceTransformer, util

from pdfminer.high_level import extract_text


model = SentenceTransformer("all-MiniLM-L6-v2")  # ローカルで保持していれば高速

class RefList(ListView):
    model = Reference
    template_name = "main/reference_list.html"
    context_object_name = "references"

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q", "")
        category = self.request.GET.get("category")
        tag = self.request.GET.get("tag")

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(authors__icontains=q)
            )
        if category:
            queryset = queryset.filter(category__id=category)
        if tag:
            queryset = queryset.filter(tags__id=tag)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["tags"] = Tag.objects.all()
        context["q"] = self.request.GET.get("q", "")
        context["selected_category"] = self.request.GET.get("category", "")
        context["selected_tag"] = self.request.GET.get("tag", "")
        return context


class RefCreate(CreateView):
    model = Reference
    form_class = ReferenceForm
    success_url = reverse_lazy("main:list")

    def form_valid(self, form):
        # カテゴリの動的作成
        new_category_name = form.cleaned_data.get("new_category")
        if new_category_name:
            category, _ = Category.objects.get_or_create(name=new_category_name.strip())
            form.instance.category = category

        # 保存（ここで一旦Referenceが保存される）
        response = super().form_valid(form)

        # タグの動的作成
        new_tags_raw = form.cleaned_data.get("new_tags", "")
        tag_names = [name.strip() for name in new_tags_raw.split(",") if name.strip()]
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            form.instance.tags.add(tag)

        return response

class RefUpdate(UpdateView):
    model = Reference

    form_class = ReferenceForm
    success_url = reverse_lazy("main:list")
    def form_valid(self, form):
    # カテゴリの動的作成
        new_category_name = form.cleaned_data.get("new_category")
        if new_category_name:
            category, _ = Category.objects.get_or_create(name=new_category_name.strip())
            form.instance.category = category

        # 保存（ここで一旦Referenceが保存される）
        response = super().form_valid(form)

        # タグの動的作成
        new_tags_raw = form.cleaned_data.get("new_tags", "")
        tag_names = [name.strip() for name in new_tags_raw.split(",") if name.strip()]
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            form.instance.tags.add(tag)

        return response

class RefDelete(DeleteView):
    model = Reference
    success_url = reverse_lazy("main:list")





def ref_detail(request, pk):
    ref = get_object_or_404(Reference, pk=pk)
    memo_html = mark_safe(markdown.markdown(ref.memo))  # Markdown → HTML
    return render(request, "main/reference_detail.html", {"ref": ref, "memo_html": memo_html})

@require_POST
def update_progress(request, pk):
    ref = get_object_or_404(Reference, pk=pk)
    progress = request.POST.get("progress")
    if progress in dict(Reference.PROGRESS_CHOICES):
        ref.progress = progress
        ref.save()
    return redirect("main:list")


def extract_text_from_pdf(path):
    try:
        return extract_text(path)
    except Exception as e:
        print("PDFテキスト抽出エラー:", e)
        return ""

def pdf_view(request, pk):
    ref = get_object_or_404(Reference, pk=pk)

    # 🔁 メモを保存
    if request.method == "POST":
        ref.memo = request.POST.get("memo", "")
        ref.save()
        return redirect("main:reference_pdf", pk=ref.pk)  # 保存後リロード

    # 🧾 表示用メモをHTML化
    memo_html = mark_safe(markdown.markdown(ref.memo or ""))

    return render(request, "main/pdf_view.html", {
        "ref": ref,
        "memo_html": memo_html,
    })

def similar_references_api(request, pk):
    ref = Reference.objects.get(pk=pk)

    try:
        query_text = extract_text_from_pdf(ref.pdf.path)
        model = SentenceTransformer("all-MiniLM-L6-v2")
        query_embedding = model.encode(query_text, convert_to_tensor=True)

        results = []
        for other in Reference.objects.exclude(pk=ref.pk).filter(pdf__isnull=False):
            try:
                other_text = extract_text_from_pdf(other.pdf.path)
                other_embedding = model.encode(other_text, convert_to_tensor=True)
                score = util.cos_sim(query_embedding, other_embedding).item()
                results.append({
                    "id": other.pk,
                    "title": other.title,
                    "score": round(score, 3),
                })
            except:
                continue

        results = sorted(results, key=lambda x: x["score"], reverse=True)[:5]
        return JsonResponse({"results": results})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)