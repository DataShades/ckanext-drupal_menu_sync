# -*- coding: utf-8 -*-

import logging

import ckan.lib.helpers as h
import ckan.plugins as p
import ckan.plugins.toolkit as tk
import requests
from beaker.cache import CacheManager

import ckanext.drupal_menu_sync.views as views

log = logging.getLogger(__name__)
cache = CacheManager()


@cache.cache("main_menu", expire=3600)
def menu_links(section=None):
    drupal_url = tk.config.get("drupal.site_url")
    if drupal_url is None or (drupal_url == h.full_current_url().split("?")[0][:-1]):
        return None
    # request links from Drupal
    r = None
    section_menu = []
    try:
        r = requests.get(drupal_url + "/menu_export", verify=False, timeout=10)
    except requests.exceptions.Timeout:
        log.warning(drupal_url + "/menu_export connection timeout")
    except requests.exceptions.TooManyRedirects:
        log.warning(drupal_url + "/menu_export too many redirects")
    except requests.exceptions.RequestException as e:
        log.error(e.message)

    if r:
        links = r.json()
    else:
        return None

    if links:
        if section in links:
            if section == "main":
                for item in links[section]:
                    if item["link"] == "<front>":
                        item["link"] = drupal_url
            section_menu.extend(links[section])
            return section_menu
        else:
            return None


class Drupal_Menu_SyncPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IBlueprint)

    # IBlueprint

    def get_blueprint(self):
        return views.get_blueprints()

    # IConfigurer
    def update_config(self, config_):
        tk.add_template_directory(config_, "templates")
        tk.add_ckan_admin_tab(
            config_,
            "drupal_menu_sync.manage_cache",
            "Manage Menu sync",
            icon="file-text",
        )

    # ITemplateHelpers
    def get_helpers(self):
        return {"menu_links": menu_links}
