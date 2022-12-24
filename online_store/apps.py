from django.contrib.admin.apps import AdminConfig


class OnlineStoreAdminConfig(AdminConfig):
    default_site = 'online_store.admin.OnlineStoreAdminSite'
