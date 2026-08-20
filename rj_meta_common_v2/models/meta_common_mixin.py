# -*- coding: utf-8 -*-
"""Shared helpers for Meta suite modules that depend on rj_meta_common_v2."""
import json
import logging
import time

import requests

from odoo import fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)
DEFAULT_GRAPH = 'v21.0'


class MetaCommonApiMixin(models.AbstractModel):
    """Optional mixin for dependent Meta modules.

    Provides a standard Graph API call helper. Dependent modules may inherit
    this on their config models to share request patterns without duplicating
    low-level HTTP code.
    """
    _name = 'meta.common.api.mixin'
    _description = 'Meta Common API Mixin'

    def _meta_graph_base(self):
        return 'https://graph.facebook.com'

    def _meta_graph_version(self):
        return DEFAULT_GRAPH

    def _meta_access_token(self):
        """Override in concrete config models."""
        return False

    def meta_graph_request(self, method, path, params=None, json_body=None, timeout=30, log_model=None):
        """
        Perform a Meta Graph API request.
        :param log_model: optional model name with create() compatible log fields
        :return: dict {success, status_code, data, error, duration_ms}
        """
        self.ensure_one()
        token = self._meta_access_token()
        if not token:
            raise UserError(_('Meta access token is not configured.'))
        ver = self._meta_graph_version() or DEFAULT_GRAPH
        if not str(ver).startswith('v'):
            ver = f'v{ver}'
        url = f'{self._meta_graph_base().rstrip("/")}/{ver}/{path.lstrip("/")}'
        params = dict(params or {})
        params.setdefault('access_token', token)
        started = time.time()
        result = {
            'success': False,
            'status_code': 0,
            'data': None,
            'error': None,
            'duration_ms': 0,
            'url': url.split('?')[0],
            'method': (method or 'GET').upper(),
            'path': path,
        }
        try:
            response = requests.request(
                result['method'], url, params=params, json=json_body, timeout=timeout
            )
            result['status_code'] = response.status_code
            body = (response.text or '')[:4000]
            if response.status_code in (200, 201):
                result['success'] = True
                try:
                    result['data'] = response.json()
                except Exception:
                    result['data'] = {'raw': body}
            else:
                result['error'] = body[:500]
        except requests.RequestException as exc:
            result['error'] = str(exc)
            _logger.exception('Meta Graph request failed: %s %s', method, path)
        result['duration_ms'] = int((time.time() - started) * 1000)

        if log_model and log_model in self.env:
            try:
                self.env[log_model].sudo().create({
                    'name': f"{result['method']} {path}",
                    'method': result['method'],
                    'endpoint': path,
                    'url': result['url'],
                    'request_payload': json.dumps(json_body or params, default=str)[:4000],
                    'response_payload': json.dumps(result.get('data') or result.get('error'), default=str)[:4000],
                    'status_code': result['status_code'],
                    'state': 'success' if result['success'] else 'error',
                    'duration_ms': result['duration_ms'],
                    'error_message': result['error'] or False,
                    'user_id': self.env.user.id,
                })
            except Exception:
                _logger.debug('Could not write Meta API log on %s', log_model, exc_info=True)
        return result
