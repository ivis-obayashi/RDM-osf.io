# -*- coding: utf-8 -*-

import traceback
import uuid
from collections import defaultdict
from requests.compat import urljoin
from django.views.generic import View, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.urls import reverse
import flask

import osf
import addons
from admin.rdm.utils import RdmPermissionMixin
from admin.rdm_addons.utils import get_rdm_addon_option
from admin.rdm_addons.api_v1.views import disconnect
from website.oauth.utils import get_service
from website.routes import make_url_map
from website import settings as website_settings
from framework.exceptions import PermissionsError
from framework.sessions import get_session

class RdmAddonRequestContextMixin(object):
    app = flask.Flask(__name__)
    make_url_map(app)
    app.config['SECRET_KEY'] = str(uuid.uuid4())
    ctx_dict = defaultdict(app.test_request_context)

    def get_request_context(self, session_id, institution_id, addon_name):
        return self.ctx_dict[(session_id, institution_id, addon_name)]

    def get_session(self, addon_name):
        if addon_name == 'dropbox':
            return addons.dropbox.models.session
        return osf.models.external.session

    def get_callback_url_func(self, addon_name):
        """Get a function that returns the OAuth Callback Admin'sURL """
        def web_url_for(view_name, _absolute=False, _internal=False, _guid=False, *args, **kwargs):
            path = 'oauth/callback/{}/'.format(addon_name)
            return urljoin(website_settings.ADMIN_URL, path)
        return web_url_for


class ConnectView(RdmPermissionMixin, RdmAddonRequestContextMixin, UserPassesTestMixin, View):
    """View OAUTH Connect"""
    raise_exception = True

    def test_func(self):
        """check user permissions"""
        institution_id = int(self.kwargs.get('institution_id'))
        return self.has_auth(institution_id)

    def get(self, request, *args, **kwargs):
        addon_name = kwargs['addon_name']
        institution_id = int(kwargs['institution_id'])
        is_custom = kwargs.get('is_custom', False)

        provider = get_service(addon_name)

        if request.session.get('oauth_states') is None:
            request.session['oauth_states'] = {}

        request.session['oauth_states'][addon_name] = {
            'institution_id': institution_id,
            'is_custom': is_custom
        }
        auth_url = None

        with self.app.test_request_context(request.get_full_path()):
            from framework.sessions import session
            auth_url = provider.auth_url
            state = session.data['oauth_states'][addon_name]['state']
            request.session['oauth_states'][addon_name]['state'] = state

        print('Django Session:')
        print(request.session['oauth_states'])

        return redirect(auth_url)

class CallbackView(RdmPermissionMixin, RdmAddonRequestContextMixin, UserPassesTestMixin, View):
    """View OAUTH callback"""
    raise_exception = True

    def test_func(self):
        """check user permissions"""
        institution_id = None
        addon_name = self.kwargs.get('addon_name')

        print('Django Session:')
        print(self.request.session['oauth_states'])

        session_data = {}
        try:
            session = get_session()
            session_data = session.data
        except RuntimeError:
            print('Unable to access session data')
            traceback.print_exc()

        if 'oauth_states' in session_data:
            institution_id = int(session_data['oauth_states'][addon_name]['institution_id'])
        elif 'institution_id' in self.kwargs:
            institution_id = int(self.kwargs.get('institution_id'))
        return self.has_auth(institution_id)

    def get(self, request, *args, **kwargs):
        addon_name = kwargs['addon_name']

        try:
            session = self.get_session(addon_name)
            state = session.data['oauth_states'][addon_name]['state']
            institution_id = session.data['oauth_states'][addon_name]['institution_id']

            provider = get_service(addon_name)

            # The following code uses flask context, so we temporarily create a context
            # similar to the one we have here in Django
            with self.app.test_request_context(request.get_full_path()):
                session.data['oauth_states'] = {addon_name: {'state': state}}

                rdm_addon_option = get_rdm_addon_option(institution_id, addon_name)
                # Retrieve permanent credentials from provider
                auth_callback_result = provider.auth_callback(user=rdm_addon_option)
                if auth_callback_result and provider.account and \
                        not rdm_addon_option.external_accounts.filter(id=provider.account.id).exists():

                    rdm_addon_option.external_accounts.add(provider.account)
                    rdm_addon_option.save()
        except Exception:
            traceback.print_exc()
            raise

        return redirect(reverse('addons:oauth:complete', kwargs={'addon_name': addon_name}))


class CompleteView(RdmPermissionMixin, UserPassesTestMixin, TemplateView):
    """View OAUTH callback completed"""
    template_name = 'rdm_addons/oauth_complete.html'
    raise_exception = True

    def test_func(self):
        """user login check"""
        return self.is_authenticated

    def get_context_data(self, **kwargs):
        ctx = super(CompleteView, self).get_context_data(**kwargs)
        return ctx

class AccountsView(RdmPermissionMixin, UserPassesTestMixin, View):
    """View OAUTH disconnect"""
    raise_exception = True

    def test_func(self):
        """check user permissions"""
        institution_id = int(self.kwargs.get('institution_id'))
        return self.has_auth(institution_id)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """imvalidate CSRF"""
        return super(AccountsView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """disconnect OAuth"""
        external_account_id = kwargs['external_account_id']
        institution_id = int(kwargs['institution_id'])
        user = self.request.user
        return disconnect(external_account_id, institution_id, user)
