from django.contrib import admin
from system.models import Announcement, CustomUser, Download, Reviewer, Score
from django.contrib.auth.models import Group
from django_reverse_admin import ReverseModelAdmin
from admin_interface.models import Theme

admin.site.unregister((Group, ))
exempted_models = (Group, )


@admin.register(Reviewer)
class ReviewerAdmin(admin.ModelAdmin):
    exclude = ('updated_at',)
    list_display = ('key', 'category', 'order_position', 'updated_at')
    list_editable = ('order_position',)


admin.site.site_header = "LTO - Simulator"
admin.site.site_title = "LTO - Simulator"
admin.site.index_title = "LTO - Simulator's Admin Panel"
