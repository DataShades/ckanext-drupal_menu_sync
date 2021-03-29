from flask import Blueprint

import ckan.lib.helpers as h
from ckan.lib.base import request, render

from ckanext.drupal_menu_sync.helpers import cache, get_header_menu, get_footer_menu


drupal_menu_sync = Blueprint('drupal_menu_sync', __name__)


def get_blueprints():
    return [drupal_menu_sync]


def manage_cache():
    if not request.form:
        return render('admin/manage_cache.html')
    else:
        if 'clear-main-menu-cache' in request.form:
            cache.invalidate(get_header_menu, 'header_menu')
            cache.invalidate(get_footer_menu, 'footer_menu')
        return h.redirect_to('drupal_menu_sync.manage_cache')


drupal_menu_sync.add_url_rule(
    "/ckan-admin/drupal_menu_sync_admin",
    view_func=manage_cache, methods=(u'GET', u'POST')
)
