from django.contrib import admin
from django.urls import path
from system import views
from system.models import Announcement, CustomUser, Download, Question, Reviewer, Score, TopUpRecord
from django.contrib.auth.models import Group
from django_reverse_admin import ReverseModelAdmin
from admin_interface.models import Theme

class MyAdminSite(admin.AdminSite):
    site_header = "LTO Admin"
    site_title = "LTO Admin Portal"
    index_title = "Welcome to LTO Admin"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('users/', views.user_list, name='users'),
            path('get_users/', views.get_users, name='get_users'),
            path('delete_user/', views.delete_user, name='delete_user'),
        ]
        return custom_urls + urls
admin_site = MyAdminSite()


admin.site.unregister((Group, ))
exempted_models = (Group, )


# @admin.register(Reviewer)
class ReviewerAdmin(admin.ModelAdmin):
    exclude = ('updated_at',)
    list_display = ('key', 'category', 'order_position', 'updated_at')
    list_editable = ('order_position',)

#@admin.register(Question)
class Questiondmin(admin.ModelAdmin):
    list_display = ('text', 'category', 'correct_choice')

    

@admin.register(TopUpRecord)
class TopUpRecordAdmin(admin.ModelAdmin):
    list_display = ('email', 'amount', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('email',)


admin_site.register(TopUpRecord, TopUpRecordAdmin)
admin_site.register(Reviewer, ReviewerAdmin)
admin_site.register(Question, Questiondmin)


# admin.site.site_header = "LTO - Simulator"
# admin.site.site_title = "LTO - Simulator"
# admin.site.index_title = "LTO - Simulator's Admin Panel"
