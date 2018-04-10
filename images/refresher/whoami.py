import json
import os
from urllib.parse import urlencode, urlparse

import requests

import yaml

from tornado.log import app_log
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.web import HTTPError, RequestHandler, Application, authenticated
import tornado.options

from jupyterhub.services.auth import HubAuthenticated
from jupyterhub.utils import url_path_join


def get_config(key, default=None):
    """
    Find a config item of a given name & return it
    Parses everything as YAML, so lists and dicts are available too
    """
    path = os.path.join('/etc/jupyterhub/config', key)
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
            return data
    except FileNotFoundError:
        return default


async def fetch_new_token(token_url, client_id, client_secret, refresh_token):
    params = {"grant_type": "refresh_token",
              "client_id": client_id,
              "client_secret": client_secret,
              "refresh_token": refresh_token,
              }
    body = urlencode(params)
    req = HTTPRequest(token_url, 'POST', body=body)
    app_log.error("URL: %s body: %s", token_url, body)

    client = AsyncHTTPClient()
    resp = await client.fetch(req)

    resp_json = json.loads(resp.body.decode('utf8', 'replace'))
    return resp_json


class TokenHandler(HubAuthenticated, RequestHandler):
    def api_request(self, method, url, **kwargs):
        """Make an API request"""
        url = url_path_join(self.hub_auth.api_url, url)
        allow_404 = kwargs.pop('allow_404', False)
        headers = kwargs.setdefault('headers', {})
        headers.setdefault('Authorization', 'token %s' % self.hub_auth.api_token)
        try:
            r = requests.request(method, url, **kwargs)
        except requests.ConnectionError as e:
            app_log.error("Error connecting to %s: %s", url, e)
            msg = "Failed to connect to Hub API at %r." % url
            msg += "  Is the Hub accessible at this URL (from host: %s)?" % socket.gethostname()
            if '127.0.0.1' in url:
                msg += "  Make sure to set c.JupyterHub.hub_ip to an IP accessible to" + \
                       " single-user servers if the servers are not on the same host as the Hub."
            raise HTTPError(500, msg)

        data = None
        if r.status_code == 404 and allow_404:
            pass
        elif r.status_code == 403:
            app_log.error("I don't have permission to check authorization with JupyterHub, my auth token may have expired: [%i] %s", r.status_code, r.reason)
            app_log.error(r.text)
            raise HTTPError(500, "Permission failure checking authorization, I may need a new token")
        elif r.status_code >= 500:
            app_log.error("Upstream failure verifying auth token: [%i] %s", r.status_code, r.reason)
            app_log.error(r.text)
            raise HTTPError(502, "Failed to check authorization (upstream problem)")
        elif r.status_code >= 400:
            app_log.warning("Failed to check authorization: [%i] %s", r.status_code, r.reason)
            app_log.warning(r.text)
            raise HTTPError(500, "Failed to check authorization")
        else:
            data = r.json()

        return data

    @authenticated
    async def get(self):
        oauth_config = get_config('auth.custom.config')

        client_id = oauth_config['client_id']
        client_secret = oauth_config['client_secret']
        token_url = oauth_config['token_url']
        user_model = self.get_current_user()

        # Fetch current auth state
        u = self.api_request('GET', url_path_join('users', user_model['name']))
        app_log.error("User: %s", u)
        auth_state = u['auth_state']

        new_tokens = await fetch_new_token(token_url,
                                           client_id,
                                           client_secret,
                                           auth_state.get('refresh_token')
                                           )

        # update auth state in the hub
        auth_state['access_token'] = new_tokens['access_token']
        auth_state['refresh_token'] = new_tokens['refresh_token']
        self.api_request('PATCH',
                         url_path_join('users', user_model['name']),
                         data=json.dumps({'auth_state': auth_state})
                         )

        # send new token to the user
        tokens = {'access_token': auth_state.get('access_token')}
        self.set_header('content-type', 'application/json')
        self.write(json.dumps(tokens, indent=1, sort_keys=True))


class PingHandler(RequestHandler):
    def get(self):
        self.set_header('content-type', 'application/json')
        self.write(json.dumps({'ping': 1}))


def main():
    tornado.options.parse_command_line()
    app = Application([
        (os.environ['JUPYTERHUB_SERVICE_PREFIX'] + 'tokens', TokenHandler),
        (os.environ['JUPYTERHUB_SERVICE_PREFIX'] + '/?', PingHandler),
    ])

    http_server = HTTPServer(app)
    url = urlparse(os.environ['JUPYTERHUB_SERVICE_URL'])

    http_server.listen(url.port)

    IOLoop.current().start()


if __name__ == '__main__':
    main()
