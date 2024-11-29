from rest_framework import serializers
from ...models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'done', 'user']  # `user` را برای نمایش یا سایر اهداف نگه می‌داریم
        read_only_fields = ['user']  # فقط قابل خواندن است و توسط کاربر ارسال نمی‌شود

    def create(self, validated_data):
        # تنظیم خودکار فیلد user بر اساس کاربر احراز هویت‌شده
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
