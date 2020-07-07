import logging
import requests
from ckantoolkit import config

from beaker.cache import CacheManager
import ckan.lib.helpers as h


log = logging.getLogger(__name__)


cache = CacheManager()


def helpers():
    return {
        'menu_links': menu_links
    }


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
        menus = r.json()
    else:
        return None

    if menus:
        if section in menus:
            if section == 'main':
                return menus['main'][0]
            elif section == 'mobile':
                return menus['mobile'][0]
            else: 
                section_menu.extend(menus[section])
                return section_menu
        else:
            return None