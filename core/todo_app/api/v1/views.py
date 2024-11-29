from rest_framework import viewsets
from ...models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای مدیریت مدل Task
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]  # فقط کاربران احراز هویت‌شده اجازه دسترسی دارند
    
    # فیلترها و جستجو
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['done', 'user']  # فیلتر بر اساس وضعیت (done) و کاربر
    search_fields = ['title']  # جستجو بر اساس عنوان
    ordering_fields = ['id', 'title']  # مرتب‌سازی بر اساس id یا عنوان
