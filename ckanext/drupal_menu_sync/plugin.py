from ckantoolkit import config

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.drupal_menu_sync.views import get_blueprints
from ckanext.drupal_menu_sync.helpers import get_helpers


class Drupal_Menu_SyncPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IBlueprint)


    # IBlueprint
    def get_blueprint(self):
        return get_blueprints()

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'drupal_menu_sync')
        toolkit.add_ckan_admin_tab(
            config_, 'drupal_menu_sync.manage_cache', 'Manage Menu sync'
        )

    # ITemplateHelpers
    def get_helpers(self):
        return get_helpers()
