import ckan.lib.base as base
import ckan.lib.helpers as h
from ckan.controllers.admin import AdminController

from ckanext.drupal_menu_sync.plugin import cache, menu_links

request = base.request


class SyncAdmController(AdminController):

    def manage_cache(self):
        extra_vars = {}
        if not request.params:
            return base.render('admin/manage_cache.html', extra_vars)
        else:
            if 'clear-main-menu-cache' in request.params:
                cache.invalidate(menu_links, 'main_menu', 'main')

            ctrl = 'ckanext.drupal_menu_sync.controller:SyncAdmController'
            h.redirect_to(
                controller=ctrl,
                action='manage_cache'
            )
