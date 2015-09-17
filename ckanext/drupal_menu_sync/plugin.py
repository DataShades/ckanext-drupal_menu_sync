import routes
import requests
import urlparse
from pylons import config
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from pylons.decorators.cache import beaker_cache

sections = dict(
  main='main-menu',
  footer='menu-footer')


@beaker_cache(expire=3600)
def drupal_menu_get(section=None):
  drupal_url = config.get('drupal.site_url') or \
    routes.url_for('/', qualified=True).replace(':5000', '')
  menus_url = urlparse.urljoin(drupal_url, 'ckanext/menus/sync')

  try:
      menus = requests.get(menus_url).json()
  except Exception:
      menus = {}

  if section:
    return menus.get(sections[section])
  return menus


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
        'drupal_menu_get': drupal_menu_get,
        }
