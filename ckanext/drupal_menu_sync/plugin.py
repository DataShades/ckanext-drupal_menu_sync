import requests
import logging

from pylons import config
from beaker.cache import CacheManager

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h

log = logging.getLogger(__name__)
cache = CacheManager()


@cache.cache('main_menu', expire=3600)
def menu_links(section=None):
    drupal_url = config.get('drupal.site_url')
    if drupal_url is None or (
        drupal_url == h.full_current_url().split('?')[0][:-1]
    ):
        return None
    # request links from Drupal
    r = None
    section_menu = []
    try:
        r = requests.get(drupal_url + '/menu_export', verify=False, timeout=10)
    except requests.exceptions.Timeout:
        log.warning(drupal_url + '/menu_export connection timeout')
    except requests.exceptions.TooManyRedirects:
        log.warning(drupal_url + '/menu_export too many redirects')
    except requests.exceptions.RequestException as e:
        log.error(e.message)

    if r:
        links = r.json()
    else:
        return None

    if links:
        if section in links:
            if section == 'main':
                for item in links[section]:
                    if item['link'] == '<front>':
                        item['link'] = drupal_url
            section_menu.extend(links[section])
            return section_menu
        else:
            return None


class Drupal_Menu_SyncPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IRoutes, inherit=True)

    # IRoutes

    def before_map(self, map):
        map.connect(
            'manage_cache',
            '/ckan-admin/manage-cache',
            controller='ckanext.drupal_menu_sync.controller:MainController',
            action='manage_cache',
            ckan_icon='file-text'
        )
        map.connect(
            '/ckan-admin/clear-cache',
            controller='ckanext.drupal_menu_sync.controller:MainController',
            action='clear_cache'
        )
        return map

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'drupal_menu_sync')

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'menu_links': menu_links
        }
