from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from django import forms
from django.contrib import admin

from app.users.models import Notification, NotificationShots

from django.urls import reverse
from django.utils.safestring import mark_safe

from app.users.forms import UserAdminChangeForm, UserAdminCreationForm
from app.users.models import TelegramUser

from .forms import CustomCKEditorWidget
from django.template.defaultfilters import striptags
from import_export.admin import ExportMixin
from import_export import resources, fields

User = get_user_model()


class TelegramUserResource(resources.ModelResource):
    user_phone = fields.Field(column_name='Телефон номер', attribute='phone')
    referral_count = fields.Field(column_name='Приглашено')

    class Meta:
        model = TelegramUser
        fields = ('fullname', 'user_phone', 'created_at', 'is_joined', 'is_active', 'referral_count')

    def dehydrate_user_phone(self, code):
        return code.phone

    def dehydrate_referral_count(self, user):
        return user.referrals.count()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]


@admin.register(TelegramUser)
class TelegramUserAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = TelegramUserResource
    list_filter = ['is_joined', 'is_active']
    list_display = ["phone", "fullname", "is_active", "is_joined", "language"]


class NotificationShotsInline(admin.TabularInline):
    extra = 1
    model = NotificationShots


class NotificationAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CustomCKEditorWidget())

    class Meta:
        model = Notification
        fields = '__all__'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["short_description", "display_image", "all_chats_count", "created_at", "tools_column"]
    inlines = [NotificationShotsInline]
    form = NotificationAdminForm

    def tools_column(self, obj):
        html_tag = "В процессе"
        if obj.status == 0:
            html_tag = '<a href="{0}" class="btn btn-success">Начать</a> '
        elif obj.status == 1:
            html_tag = 'Отправлено'
        return mark_safe(
            html_tag.format(
                reverse('send_notification', args=[obj.pk]), )
        )

    tools_column.short_description = 'Управление'
    tools_column.allow_tags = True

    def short_description(self, obj):
        descr = striptags(obj.description)
        return descr[:100] + "..."

    short_description.short_description = "Описание"

    def all_chats_count(self, obj):
        return obj.all_chats

    all_chats_count.short_description = "Отправлено"

    def display_image(self, obj):
        images = obj.notificationshots_set
        image = None
        if images.exists():
            image = images.first()
        img_html = f'<img src="{image.image.url}" width="50" height="50" />' if image else '<div>Без изображения</div>'
        return mark_safe(img_html)

    display_image.short_description = "Изображение"

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
