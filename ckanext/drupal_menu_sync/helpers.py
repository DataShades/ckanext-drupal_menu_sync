import logging
from urllib.parse import urljoin

import requests
from ckantoolkit import config
from bs4 import BeautifulSoup as BS4, element
from beaker.cache import CacheManager

import ckan.lib.helpers as h


log = logging.getLogger(__name__)
cache = CacheManager()

HEADER_ENDPOINT: str = 'layout/resource/menu_export'
FOOTER_ENDPOINT: str = 'layout/resource/footer_export'


def get_helpers():
    return {
        'get_footer_menu': get_footer_menu,
        'get_header_menu': get_header_menu
    }


@cache.cache('header_menu', expire=3600)
def get_header_menu(style: str = "desktop") -> str:
    """
    Returns drupal header html structure
    Depends on style arg returns desktop or mobile menu

    style type: str
    return type: str
    """
    html_markup: str = _get_html_markup(HEADER_ENDPOINT)
    if not html_markup:
        return

    soup: BS4 = BS4(html_markup)

    if style == "desktop":
        return str(soup.find('nav', {'id': 'block-mainmenu'}))
    return str(soup.find('div', {'id': 'mobile-menu'}))


@cache.cache('footer_menu', expire=3600)
def get_footer_menu() -> str:
    """
    Returns drupal footer html structure
    return type: str
    """
    html_markup: str = _get_html_markup(FOOTER_ENDPOINT)
    if not html_markup:
        return

    soup: BS4 = BS4(html_markup)

    nav_section: element.Tag = soup.new_tag(
        'nav', attrs={'class': 'container'})
    soup.find('ul').wrap(nav_section)

    return str(soup)


def _get_html_markup(endpoint: str) -> str:
    """
    Returns html markup from response json
    return type: str
    """
    drupal_url = _get_drupal_site_url()
    if not drupal_url:
        return

    url: str = urljoin(drupal_url, endpoint)
    resp: dict = _make_request(url)

    return resp['main'][0] if resp else None


def _get_drupal_site_url() -> str:
    """
    Drupal site url should be setted up in CKAN config
    """
    drupal_url: str = config.get('drupal.site_url')

    if drupal_url is None or (
        drupal_url == h.full_current_url().split('?')[0][:-1]
    ):
        return
    return drupal_url


def _make_request(url: str) -> dict:
    resp = None

    try:
        resp = requests.get(url, verify=False, timeout=10)
    except requests.exceptions.Timeout:
        log.warning('{} connection timeout'.format(url))
    except requests.exceptions.TooManyRedirects:
        log.warning('{} too many redirects'.format(url))
    except requests.exceptions.RequestException as e:
        log.error(str(e))

    return resp.json() if resp else None
