import os

from addons.base.apps import BaseAddonConfig

HERE = os.path.dirname(os.path.abspath(__file__))
NODE_SETTINGS_TEMPLATE = os.path.join(
    HERE,
    'templates',
    'forward_node_settings.mako',
)

class ForwardAddonConfig(BaseAddonConfig):

    name = 'addons.forward'
    label = 'addons_forward'
    full_name = 'External Link'
    short_name = 'forward'
    configs = ['node']
    views = ['widget']
    node_settings_template = NODE_SETTINGS_TEMPLATE
    user_settings_template = None

    URL_CHANGED = 'forward_url_changed'

    actions = (URL_CHANGED, )

    @property
    def node_settings(self):
        return self.get_model('NodeSettings')
