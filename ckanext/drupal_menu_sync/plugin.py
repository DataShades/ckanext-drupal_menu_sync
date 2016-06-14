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

log = logging.getLogger(__name__)

def menu_links(section=None):
    # Drupal URL is the root of the domain without the slash
    drupal_url = config.get('drupal.site_url')
    # fallback links
    json_str = '[{"title":"Home","link":"'+drupal_url+'"},' \
               '{"title":"Datasets","link":"'+drupal_url+'/data/dataset"},' \
               '{"title":"Organisations","link":"'+drupal_url+'/data/organization"},' \
               '{"title":"Groups","link":"'+drupal_url+'/data/group"},' \
               '{"title":"Strategies","link":"'+drupal_url+'/strategies"},' \
               '{"title":"Toolkit","link":"'+drupal_url+'/toolkit"},' \
               '{"title":"Apps & Ideas","link":"'+drupal_url+'/data/showcase"}]'
    links = json.loads(json_str)
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
    if section:
      for item in links[section]:
        section_menu.append(item)
      return section_menu  
    return links

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
