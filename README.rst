---------------
Config Settings
---------------

Document any optional config settings here. For example::

   drupal.site_url = {Drupal instance URL - ckan instance root by default}

   ckan.plugins = drupal_menu_sync

In Drupal site need to install and enabled custom module (can be found in drupal_custom_module_menu_export)::
	
   menu_export 

------------------------
Development Installation
------------------------

To install ckanext-drupal_menu_sync for development, activate your CKAN virtualenv and
do::

    git clone git@git.links.com.au:smotornyuk/ckanext-drupal_menu_sync.git
    cd ckanext-drupal_menu_sync
    python setup.py develop

-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.drupal_menu_sync --cover-inclusive --cover-erase --cover-tests

