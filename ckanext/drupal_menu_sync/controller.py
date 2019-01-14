import ckan.plugins.toolkit as tk
from ckan.controllers.package import PackageController

from ckanext.drupal_menu_sync.plugin import cache, menu_links


class MainController(PackageController):

    def manage_cache(self):
        extra_vars = {}
        return tk.render('admin/manage_cache.html', extra_vars)

    def clear_cache(self):
        cache.invalidate(menu_links, 'main_menu', 'main')
        return tk.redirect_to('manage_cache')
