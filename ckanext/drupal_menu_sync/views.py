# -*- coding: utf-8 -*-

from flask import Blueprint
import ckan.plugins.toolkit as tk

drupal_menu_sync = Blueprint("drupal_menu_sync", __name__)


def get_blueprints():
    return [drupal_menu_sync]


def manage_cache():
    from ckanext.drupal_menu_sync.plugin import cache, menu_links
    if not tk.request.params:
        return tk.render("admin/manage_cache.html")
    else:
        if "clear-main-menu-cache" in tk.request.params:
            cache.invalidate(menu_links, "main_menu", "main")

        return h.redirect_to("drupal_menu_sync.manage_cache")


drupal_menu_sync.add_url_rule(
    "/ckan-admin/drupal_menu_sync_admin", view_func=manage_cache, methods=('POST', 'GET')
)
