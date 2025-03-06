from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse


class TaskListView(ListView):
    model = Task
    template_name = "task_list.html"
    context_object_name = "tasks"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "todo_app/task_form.html"
    fields = ["title", "done"]

    def form_valid(self, form):
        # افزودن کاربر وارد شده به فیلد user
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy("task_list")


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = "todo_app/task_form.html"
    fields = ["title", "done"]
    success_url = reverse_lazy("task_list")


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "todo_app/task_confirm_delete.html"
    success_url = reverse_lazy("task_list")


class MarkDoneView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        task.done = True
        task.save()

        # پس از تکمیل تسک، به صفحه لیست تسک‌ها برمی‌گردیم
        next_url = request.GET.get("next", reverse("task_list"))
        return redirect(next_url)
