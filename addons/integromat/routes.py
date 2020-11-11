# -*- coding: utf-8 -*-
"""Routes for the integromat addon.
"""

from framework.routing import Rule, json_renderer
from website.routes import OsfWebRenderer

from addons.integromat import views

TEMPLATE_DIR = './addons/integromat/templates/'

# HTML endpoints
page_routes = {

    'rules': [

        # Home (Base) | GET
        Rule(
            [
                '/<pid>/integromat',
                '/<pid>/node/<nid>/integromat',
            ],
            'get',
            views.project_integromat,
            OsfWebRenderer('page.mako', trust=False, template_dir=TEMPLATE_DIR)
        ),

    ]
}

# JSON endpoints
api_routes = {
    'rules': [

        Rule(
            '/settings/integromat/',
            'get',
            views.integromat_user_config_get,
            json_renderer,
        ),

        Rule(
            '/settings/integromat/accounts/',
            'post',
            views.integromat_add_user_account,
            json_renderer,
        ),

        Rule(
            [
                '/settings/integromat/accounts/',
            ],
            'get',
            views.integromat_account_list,
            json_renderer,
        ),

        Rule(
            [
                '/project/<pid>/settings/integromat/',
                '/project/<pid>/node/<nid>/settings/integromat/'
            ],
            'get',
            views.integromat_get_config,
            json_renderer,
        ),

        Rule(
            [
                '/project/<pid>/integromat/user_auth/',
                '/project/<pid>/node/<nid>/integromat/user_auth/'
            ],
            'put',
            views.integromat_import_auth,
            json_renderer,
        ),

        Rule(
            [
                '/project/<pid>/integromat/user_auth/',
                '/project/<pid>/node/<nid>/integromat/user_auth/'
            ],
            'delete',
            views.integromat_deauthorize_node,
            json_renderer,
        ),

        Rule(
            '/project/<pid>/integromat/register_meeting',
            'post',
            views.integromat_register_meeting,
            json_renderer,
        ),

    ],
    'prefix': '/api/v1'
}