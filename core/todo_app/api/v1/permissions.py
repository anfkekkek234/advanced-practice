from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    مجوز سطح آبجکت برای فقط خواندن یا ویرایش توسط مالک
    فرض می‌شود که مدل دارای یک فیلد 'user' برای مالکیت باشد.
    """

    def has_object_permission(self, request, view, obj):
        # مجوز خواندن برای همه کاربران آزاد است
        if request.method in permissions.SAFE_METHODS:
            return True

        # فقط کاربری که صاحب تسک است اجازه ویرایش دارد
        return obj.user == request.user
