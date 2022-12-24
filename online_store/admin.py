from django.contrib import admin


class OnlineStoreAdminSite(admin.AdminSite):
    site_title = 'Online Store'
    site_header = 'Online Store Site Admin'
    index_title = 'Online Store admin interface'
