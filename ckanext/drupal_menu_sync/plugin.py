import routes
import requests
import urlparse
from pylons import config
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from pylons.decorators.cache import beaker_cache
import logging
import json
import re
from ckan.common import _, g
import ckan.lib.helpers as h

log = logging.getLogger(__name__)

@beaker_cache(expire=3600)
def menu_links(section=None):
    drupal_url = config.get('drupal.site_url')
    if drupal_url == None or drupal_url == h.full_current_url().split('?')[0][:-1]:
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
