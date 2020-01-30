from flask import Blueprint

import ckan.lib.base as base
import ckan.lib.helpers as h
from ckanext.drupal_menu_sync.helpers import cache, menu_links

request = base.request

drupal_menu_sync = Blueprint('drupal_menu_sync', __name__)


def manage_cache():
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

drupal_menu_sync.add_url_rule(
    "/ckan-admin/drupal_menu_sync_admin", view_func=manage_cache, methods=(u'GET', u'POST')
)

blueprints = [drupal_menu_sync]