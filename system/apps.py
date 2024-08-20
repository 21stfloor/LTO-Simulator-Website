from django.apps import AppConfig

class SystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'system'



# class MyOwnConfig(AdminConfig):
#     default_site = 'system.admin.MyAdminSite'
#     label = 'admin'