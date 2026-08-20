# -*- coding: utf-8 -*-
from odoo import api, models, _


# Feature modules of the Meta suite (all independent except depend on rj_meta_common_v2).
# Used to build customer-facing dashboard cards dynamically if installed.
META_SUITE_CATALOG = [
    {
        'tech': 'rj_meta_common_v2',
        'name': 'Meta Common Panel',
        'subtitle': 'Website floating panel & snippet',
        'icon': 'fa-th-large',
        'color': '#1877F2',
        'kind': 'common',
    },
    {
        'tech': 'rj_website_facebook_pixel',
        'name': 'Facebook Pixel + CAPI',
        'subtitle': 'Browser & server conversion tracking',
        'icon': 'fa-crosshairs',
        'color': '#0d8a3e',
        'kind': 'feature',
    },
    {
        'tech': 'rj_meta_business_connector',
        'name': 'Business Connector',
        'subtitle': 'Tokens, pages & ad accounts',
        'icon': 'fa-plug',
        'color': '#1877F2',
        'config_model': 'meta.business.connector.config',
        'log_model': 'meta.business.connector.api.log',
        'biz_model': 'meta.business.asset',
    },
    {
        'tech': 'rj_meta_capi_crm',
        'name': 'CRM Conversions',
        'subtitle': 'Lead & opportunity events',
        'icon': 'fa-handshake-o',
        'color': '#714B67',
        'config_model': 'meta.capi.crm.config',
        'log_model': 'meta.capi.crm.api.log',
        'biz_model': 'meta.crm.conversion',
    },
    {
        'tech': 'rj_meta_capi_sale',
        'name': 'Sales Conversions',
        'subtitle': 'Orders & invoice purchases',
        'icon': 'fa-shopping-cart',
        'color': '#017e84',
        'config_model': 'meta.capi.sale.config',
        'log_model': 'meta.capi.sale.api.log',
        'biz_model': 'meta.sale.conversion',
    },
    {
        'tech': 'rj_meta_product_catalog',
        'name': 'Product Catalog',
        'subtitle': 'Sync products to Meta Catalog',
        'icon': 'fa-cubes',
        'color': '#d5653e',
        'config_model': 'meta.product.catalog.config',
        'log_model': 'meta.product.catalog.api.log',
        'biz_model': 'meta.catalog.item',
    },
    {
        'tech': 'rj_meta_lead_ads_v2',
        'name': 'Lead Ads',
        'subtitle': 'Import lead forms to CRM',
        'icon': 'fa-bullhorn',
        'color': '#875a7b',
        'config_model': 'meta.lead.ads.config',
        'log_model': 'meta.lead.ads.api.log',
        'biz_model': 'meta.lead.ads.form',
    },
    {
        'tech': 'rj_meta_ads_campaigns',
        'name': 'Ads Campaigns',
        'subtitle': 'Campaigns, ad sets & ads',
        'icon': 'fa-flag',
        'color': '#f39c12',
        'config_model': 'meta.ads.campaigns.config',
        'log_model': 'meta.ads.campaigns.api.log',
        'biz_model': 'meta.ads.campaign',
    },
    {
        'tech': 'rj_meta_ads_insights',
        'name': 'Ads Insights & ROI',
        'subtitle': 'Spend, clicks & performance',
        'icon': 'fa-line-chart',
        'color': '#e67e22',
        'config_model': 'meta.ads.insights.config',
        'log_model': 'meta.ads.insights.api.log',
        'biz_model': 'meta.ads.insight',
    },
    {
        'tech': 'rj_meta_whatsapp_business',
        'name': 'WhatsApp Business',
        'subtitle': 'Templates & customer messages',
        'icon': 'fa-whatsapp',
        'color': '#25d366',
        'config_model': 'meta.whatsapp.business.config',
        'log_model': 'meta.whatsapp.business.api.log',
        'biz_model': 'meta.whatsapp.message',
    },
    {
        'tech': 'rj_meta_custom_audiences',
        'name': 'Custom Audiences',
        'subtitle': 'Upload customer lists',
        'icon': 'fa-users',
        'color': '#3498db',
        'config_model': 'meta.custom.audiences.config',
        'log_model': 'meta.custom.audiences.api.log',
        'biz_model': 'meta.custom.audience',
    },
    {
        'tech': 'rj_meta_page_publisher',
        'name': 'Page Publisher',
        'subtitle': 'Facebook & Instagram posts',
        'icon': 'fa-newspaper-o',
        'color': '#9b59b6',
        'config_model': 'meta.page.publisher.config',
        'log_model': 'meta.page.publisher.api.log',
        'biz_model': 'meta.page.post',
    },
    {
        'tech': 'rj_meta_dynamic_ads',
        'name': 'Dynamic Ads',
        'subtitle': 'Product sets for retargeting',
        'icon': 'fa-retweet',
        'color': '#1abc9c',
        'config_model': 'meta.dynamic.ads.config',
        'log_model': 'meta.dynamic.ads.api.log',
        'biz_model': 'meta.product.set',
    },
    {
        'tech': 'rj_meta_delivery_tracking',
        'name': 'Delivery Journey',
        'subtitle': 'Shipment events to Meta',
        'icon': 'fa-truck',
        'color': '#16a085',
        'config_model': 'meta.delivery.tracking.config',
        'log_model': 'meta.delivery.tracking.api.log',
        'biz_model': 'meta.delivery.event',
    },
    {
        'tech': 'rj_meta_messenger_inbox',
        'name': 'Messenger Bridge',
        'subtitle': 'Page conversations in Odoo',
        'icon': 'fa-comments',
        'color': '#0084ff',
        'config_model': 'meta.messenger.inbox.config',
        'log_model': 'meta.messenger.inbox.api.log',
        'biz_model': 'meta.messenger.thread',
    },
    {
        'tech': 'rj_meta_instagram_engagement',
        'name': 'Instagram Engagement',
        'subtitle': 'Comments & lead capture',
        'icon': 'fa-instagram',
        'color': '#e1306c',
        'config_model': 'meta.instagram.engagement.config',
        'log_model': 'meta.instagram.engagement.api.log',
        'biz_model': 'meta.instagram.comment',
    },
    {
        'tech': 'rj_meta_lookalike_audiences',
        'name': 'Lookalike Audiences',
        'subtitle': 'Grow similar audiences',
        'icon': 'fa-expand',
        'color': '#8e44ad',
        'config_model': 'meta.lookalike.audiences.config',
        'log_model': 'meta.lookalike.audiences.api.log',
        'biz_model': 'meta.lookalike.audience',
    },
    {
        'tech': 'rj_meta_event_promotion',
        'name': 'Event Promotion',
        'subtitle': 'Odoo events & conversions',
        'icon': 'fa-calendar',
        'color': '#c0392b',
        'config_model': 'meta.event.promotion.config',
        'log_model': 'meta.event.promotion.api.log',
        'biz_model': 'meta.event.promotion',
    },
    {
        'tech': 'rj_meta_pos_conversions',
        'name': 'POS Offline Conversions',
        'subtitle': 'Store purchases to Meta',
        'icon': 'fa-desktop',
        'color': '#2c3e50',
        'config_model': 'meta.pos.conversions.config',
        'log_model': 'meta.pos.conversions.api.log',
        'biz_model': 'meta.pos.conversion.batch',
    },
    {
        'tech': 'rj_meta_seo_social_preview',
        'name': 'SEO & Social Preview',
        'subtitle': 'Open Graph share cards',
        'icon': 'fa-share-alt',
        'color': '#27ae60',
        'config_model': 'meta.seo.social.preview.config',
        'log_model': 'meta.seo.social.preview.api.log',
        'biz_model': 'meta.seo.page.meta',
    },
    {
        'tech': 'rj_meta_ads_cost_accounting',
        'name': 'Ads Cost Accounting',
        'subtitle': 'Import ad spend to accounting',
        'icon': 'fa-money',
        'color': '#f1c40f',
        'config_model': 'meta.ads.cost.accounting.config',
        'log_model': 'meta.ads.cost.accounting.api.log',
        'biz_model': 'meta.ads.cost.line',
    },
    {
        'tech': 'rj_meta_lead_scoring',
        'name': 'Lead Scoring',
        'subtitle': 'Score leads from ad signals',
        'icon': 'fa-star',
        'color': '#e74c3c',
        'config_model': 'meta.lead.scoring.config',
        'log_model': 'meta.lead.scoring.api.log',
        'biz_model': 'meta.lead.score.rule',
    },
]


class MetaDashboard(models.AbstractModel):
    _name = 'meta.common.dashboard'
    _description = 'Meta Suite Customer Dashboard'

    def _module_installed(self, tech):
        Mod = self.env['ir.module.module'].sudo()
        return bool(Mod.search_count([('name', '=', tech), ('state', '=', 'installed')]))

    def _count_safe(self, model_name, domain=None):
        if not model_name or model_name not in self.env:
            return 0
        try:
            return self.env[model_name].sudo().search_count(domain or [])
        except Exception:
            return 0

    def _action_window(self, name, res_model, view_mode='list,form', domain=None, context=None):
        return {
            'type': 'ir.actions.act_window',
            'name': name,
            'res_model': res_model,
            'view_mode': view_mode,
            'domain': domain or [],
            'context': context or {},
            'target': 'current',
        }

    def _recent_logs(self, log_model, limit=8):
        """Return recent API log rows for the dashboard details panel."""
        if not log_model or log_model not in self.env:
            return []
        try:
            Model = self.env[log_model].sudo()
            fields_get = Model.fields_get()
            rows = Model.search([], limit=limit)
            result = []
            for rec in rows:
                name = rec.display_name or getattr(rec, 'name', False) or str(rec.id)
                state = getattr(rec, 'state', False) or ''
                endpoint = getattr(rec, 'endpoint', False) or getattr(rec, 'method', False) or ''
                err = getattr(rec, 'error_message', False) or ''
                status_code = getattr(rec, 'status_code', False) or ''
                create_date = fields_get.get('create_date') and rec.create_date
                result.append({
                    'id': rec.id,
                    'name': name,
                    'state': state,
                    'endpoint': endpoint or '',
                    'error': (err[:120] + '…') if err and len(err) > 120 else (err or ''),
                    'status_code': status_code,
                    'date': create_date.strftime('%Y-%m-%d %H:%M') if create_date else '',
                    'model': log_model,
                })
            return result
        except Exception:
            return []

    def _suite_recent_logs(self, limit=12):
        """Aggregate recent logs across installed feature modules."""
        collected = []
        for entry in META_SUITE_CATALOG:
            log = entry.get('log_model')
            if not log or log not in self.env:
                continue
            if not self._module_installed(entry['tech']):
                continue
            for row in self._recent_logs(log, limit=4):
                row = dict(row)
                row['app'] = entry.get('name') or entry['tech']
                row['color'] = entry.get('color') or '#1877F2'
                collected.append(row)
        # Sort by date string desc (ISO-like) then id
        collected.sort(key=lambda r: (r.get('date') or '', r.get('id') or 0), reverse=True)
        return collected[:limit]

    def _build_module_actions(self, entry, *, include_open_app=True, primary_open=True):
        """All customer-visible actions for a suite module card."""
        tech = entry['tech']
        cfg = entry.get('config_model')
        log = entry.get('log_model')
        biz = entry.get('biz_model')
        actions = []

        if tech == 'rj_website_facebook_pixel':
            return [
                {
                    'label': _('Pixel Settings'),
                    'icon': 'fa-cog',
                    'type': 'object',
                    'method': 'action_open_pixel_settings',
                    'params': {},
                    'primary': True,
                },
            ]

        if include_open_app:
            actions.append({
                'label': _('Open App'),
                'icon': 'fa-th-large',
                'type': 'object',
                'method': 'action_open_module_dashboard',
                'params': {'module_tech': tech},
                'primary': bool(primary_open),
            })
        if cfg and cfg in self.env:
            actions.append({
                'label': _('Configuration'),
                'icon': 'fa-cog',
                'type': 'object',
                'method': 'action_open_model',
                'params': {'model': cfg, 'name': _('Configuration'), 'view_mode': 'list,form'},
                'primary': not include_open_app,
            })
        if log and log in self.env:
            actions.append({
                'label': _('API Logs'),
                'icon': 'fa-list-alt',
                'type': 'object',
                'method': 'action_open_model',
                'params': {
                    'model': log,
                    'name': _('API Logs'),
                    'view_mode': 'graph,pivot,list,form',
                },
            })
            actions.append({
                'label': _('Errors'),
                'icon': 'fa-exclamation-triangle',
                'type': 'object',
                'method': 'action_open_model',
                'params': {
                    'model': log,
                    'name': _('Error Logs'),
                    'view_mode': 'list,form',
                    'domain': [('state', '=', 'error')],
                },
            })
        if biz and biz in self.env:
            actions.append({
                'label': _('Records'),
                'icon': 'fa-database',
                'type': 'object',
                'method': 'action_open_model',
                'params': {'model': biz, 'name': _('Records'), 'view_mode': 'list,form'},
            })
        # Import / Export always listed when wizards exist (or show toast)
        actions.append({
            'label': _('Import'),
            'icon': 'fa-download',
            'type': 'object',
            'method': 'action_open_import_export',
            'params': {'tech': tech, 'kind': 'import'},
        })
        actions.append({
            'label': _('Export / Sync'),
            'icon': 'fa-upload',
            'type': 'object',
            'method': 'action_open_import_export',
            'params': {'tech': tech, 'kind': 'export'},
        })
        return actions

    @api.model
    def get_dashboard_data(self, mode='suite', module_tech=None):
        """
        Return card dashboard payload for the OWL client action.
        mode: 'suite' | 'module'
        """
        company = self.env.company

        if mode == 'module' and module_tech:
            entry = next((e for e in META_SUITE_CATALOG if e['tech'] == module_tech), None)
            if not entry:
                return {
                    'title': _('Meta Dashboard'),
                    'subtitle': '',
                    'kpis': [],
                    'cards': [],
                    'recent_logs': [],
                    'mode': 'module',
                }
            return self._module_dashboard(entry)

        # ---- Suite overview ----
        cards = []
        installed = []
        total_logs = total_errors = total_records = 0

        for entry in META_SUITE_CATALOG:
            tech = entry['tech']
            if tech == 'rj_meta_common_v2':
                installed.append({**entry, 'installed': True})
                continue
            if not self._module_installed(tech):
                continue
            cfg = entry.get('config_model')
            log = entry.get('log_model')
            biz = entry.get('biz_model')
            conf_count = self._count_safe(cfg)
            log_ok = self._count_safe(log, [('state', '=', 'success')]) if log else 0
            log_err = self._count_safe(log, [('state', '=', 'error')]) if log else 0
            rec_count = self._count_safe(biz)
            total_logs += log_ok + log_err
            total_errors += log_err
            total_records += rec_count
            installed.append({
                **entry,
                'installed': True,
                'stats': {
                    'configs': conf_count,
                    'logs_ok': log_ok,
                    'logs_error': log_err,
                    'records': rec_count,
                },
                'actions': self._build_module_actions(entry, include_open_app=True, primary_open=True),
            })

        # Common panel card always first
        cards.append({
            'id': 'panel_settings',
            'title': _('Meta Website Panel'),
            'subtitle': _('Floating button & console links on every page'),
            'icon': 'fa-window-maximize',
            'color': '#1877F2',
            'badge': _('Core'),
            'stats': [],
            'details': [
                _('Panel settings for each website'),
                _('Console shortcuts: Ads, Events, Commerce, WhatsApp'),
            ],
            'actions': [
                {
                    'label': _('Panel Settings'),
                    'icon': 'fa-sliders',
                    'type': 'object',
                    'method': 'action_open_panel_settings',
                    'params': {},
                    'primary': True,
                },
                {
                    'label': _('Websites'),
                    'icon': 'fa-globe',
                    'type': 'object',
                    'method': 'action_open_websites',
                    'params': {},
                },
            ],
        })

        for mod in installed:
            if mod['tech'] == 'rj_meta_common_v2':
                continue
            stats = mod.get('stats') or {}
            cards.append({
                'id': mod['tech'],
                'title': mod['name'],
                'subtitle': mod.get('subtitle') or '',
                'icon': mod.get('icon') or 'fa-cube',
                'color': mod.get('color') or '#1877F2',
                'tech': mod['tech'],
                'badge': _('Installed'),
                'stats': [
                    {'label': _('Configs'), 'value': stats.get('configs', 0)},
                    {'label': _('OK Logs'), 'value': stats.get('logs_ok', 0), 'tone': 'success'},
                    {'label': _('Errors'), 'value': stats.get('logs_error', 0), 'tone': 'danger'},
                    {'label': _('Records'), 'value': stats.get('records', 0)},
                ],
                'details': [
                    _('Open App for full module dashboard'),
                    _('Configuration · API Logs · Errors · Records'),
                    _('Import & Export / Sync wizards'),
                ],
                'actions': mod.get('actions') or [],
            })

        kpis = [
            {'label': _('Active Meta Apps'), 'value': max(0, len(installed) - 1), 'icon': 'fa-th', 'color': '#1877F2'},
            {'label': _('Total Log Lines'), 'value': total_logs, 'icon': 'fa-list', 'color': '#0d8a3e'},
            {'label': _('Errors'), 'value': total_errors, 'icon': 'fa-exclamation-triangle', 'color': '#e74c3c'},
            {'label': _('Synced Records'), 'value': total_records, 'icon': 'fa-database', 'color': '#8e44ad'},
            {'label': _('Company'), 'value': company.name, 'icon': 'fa-building', 'color': '#34495e', 'is_text': True},
        ]

        return {
            'title': _('Meta Marketing Suite'),
            'subtitle': _('Customer dashboard — every card shows actions for configuration, logs, records and tools'),
            'kpis': kpis,
            'cards': cards,
            'recent_logs': self._suite_recent_logs(12),
            'mode': 'suite',
        }

    def _module_dashboard(self, entry):
        tech = entry['tech']
        if tech == 'rj_meta_business_connector':
            return self._business_connector_dashboard(entry)
            
        cfg = entry.get('config_model')
        log = entry.get('log_model')
        biz = entry.get('biz_model')
        conf_count = self._count_safe(cfg)
        log_ok = self._count_safe(log, [('state', '=', 'success')]) if log else 0
        log_err = self._count_safe(log, [('state', '=', 'error')]) if log else 0
        log_all = self._count_safe(log) if log else 0
        rec_count = self._count_safe(biz)

        kpis = [
            {'label': _('Configurations'), 'value': conf_count, 'icon': 'fa-cog', 'color': '#1877F2'},
            {'label': _('Successful Logs'), 'value': log_ok, 'icon': 'fa-check', 'color': '#27ae60'},
            {'label': _('Error Logs'), 'value': log_err, 'icon': 'fa-exclamation-triangle', 'color': '#e74c3c'},
            {'label': _('Business Records'), 'value': rec_count, 'icon': 'fa-database', 'color': '#8e44ad'},
            {'label': _('All Logs'), 'value': log_all, 'icon': 'fa-list-alt', 'color': '#3498db'},
        ]

        cards = []

        # Overview card with ALL actions visible in one place
        cards.append({
            'id': 'overview',
            'title': _('All Actions'),
            'subtitle': _('Everything you can open for this app'),
            'icon': 'fa-bolt',
            'color': entry.get('color') or '#1877F2',
            'badge': _('Quick access'),
            'stats': [
                {'label': _('Configs'), 'value': conf_count},
                {'label': _('OK'), 'value': log_ok, 'tone': 'success'},
                {'label': _('Errors'), 'value': log_err, 'tone': 'danger'},
                {'label': _('Records'), 'value': rec_count},
            ],
            'details': [
                _('Configuration — tokens, accounts, connection'),
                _('API Logs — every request with status & payload'),
                _('Records — synced business data'),
                _('Import / Export — wizards for sync helpers'),
            ],
            'actions': self._build_module_actions(entry, include_open_app=False, primary_open=False),
        })

        if cfg and cfg in self.env:
            cards.append({
                'id': 'config',
                'title': _('Configuration'),
                'subtitle': _('Tokens, accounts and connection settings'),
                'icon': 'fa-cog',
                'color': '#1877F2',
                'stats': [{'label': _('Records'), 'value': conf_count}],
                'details': [
                    _('Create or edit app configuration'),
                    _('Store access tokens and Meta IDs'),
                ],
                'actions': [
                    {
                        'label': _('Open Configuration'),
                        'icon': 'fa-arrow-right',
                        'type': 'object',
                        'method': 'action_open_model',
                        'params': {'model': cfg, 'name': _('Configuration'), 'view_mode': 'list,form'},
                        'primary': True,
                    },
                    {
                        'label': _('New Configuration'),
                        'icon': 'fa-plus',
                        'type': 'object',
                        'method': 'action_open_model',
                        'params': {
                            'model': cfg,
                            'name': _('Configuration'),
                            'view_mode': 'form',
                            'context': {'form_view_initial_mode': 'edit'},
                        },
                    },
                ],
            })
        if log and log in self.env:
            cards.append({
                'id': 'logs',
                'title': _('API Logs'),
                'subtitle': _('Every Meta API request with status and details'),
                'icon': 'fa-list-alt',
                'color': '#0d8a3e',
                'stats': [
                    {'label': _('All'), 'value': log_all},
                    {'label': _('OK'), 'value': log_ok, 'tone': 'success'},
                    {'label': _('Errors'), 'value': log_err, 'tone': 'danger'},
                ],
                'details': [
                    _('Graph and pivot analytics on logs'),
                    _('Filter errors only for troubleshooting'),
                    _('Request / response payload on each line'),
                ],
                'actions': [
                    {
                        'label': _('All Logs'),
                        'icon': 'fa-list',
                        'type': 'object',
                        'method': 'action_open_model',
                        'params': {'model': log, 'name': _('API Logs'), 'view_mode': 'graph,pivot,list,form'},
                        'primary': True,
                    },
                    {
                        'label': _('Only Errors'),
                        'icon': 'fa-exclamation-triangle',
                        'type': 'object',
                        'method': 'action_open_model',
                        'params': {
                            'model': log,
                            'name': _('Error Logs'),
                            'view_mode': 'list,form',
                            'domain': [('state', '=', 'error')],
                        },
                    },
                    {
                        'label': _('Success Only'),
                        'icon': 'fa-check',
                        'type': 'object',
                        'method': 'action_open_model',
                        'params': {
                            'model': log,
                            'name': _('Success Logs'),
                            'view_mode': 'list,form',
                            'domain': [('state', '=', 'success')],
                        },
                    },
                ],
            })
        if biz and biz in self.env:
            cards.append({
                'id': 'records',
                'title': _('Business Records'),
                'subtitle': _('Synced items, campaigns, messages or events'),
                'icon': 'fa-database',
                'color': '#8e44ad',
                'stats': [{'label': _('Total'), 'value': rec_count}],
                'details': [
                    _('Browse and open business objects'),
                    _('Linked to configuration and company'),
                ],
                'actions': [
                    {
                        'label': _('Open Records'),
                        'icon': 'fa-table',
                        'type': 'object',
                        'method': 'action_open_model',
                        'params': {'model': biz, 'name': _('Records'), 'view_mode': 'list,form'},
                        'primary': True,
                    },
                ],
            })
        cards.append({
            'id': 'tools',
            'title': _('Tools'),
            'subtitle': _('Import, export and suite navigation'),
            'icon': 'fa-wrench',
            'color': '#e67e22',
            'stats': [],
            'details': [
                _('Import wizard for pulling Meta data'),
                _('Export / Sync wizard for pushing data'),
            ],
            'actions': [
                {
                    'label': _('Import Wizard'),
                    'icon': 'fa-download',
                    'type': 'object',
                    'method': 'action_open_import_export',
                    'params': {'tech': tech, 'kind': 'import'},
                    'primary': True,
                },
                {
                    'label': _('Export Wizard'),
                    'icon': 'fa-upload',
                    'type': 'object',
                    'method': 'action_open_import_export',
                    'params': {'tech': tech, 'kind': 'export'},
                },
                {
                    'label': _('Suite Dashboard'),
                    'icon': 'fa-th-large',
                    'type': 'object',
                    'method': 'action_open_suite_dashboard',
                    'params': {},
                },
            ],
        })

        return {
            'title': entry.get('name') or tech,
            'subtitle': entry.get('subtitle') or _('Module dashboard — actions, logs and configuration'),
            'kpis': kpis,
            'cards': cards,
            'recent_logs': self._recent_logs(log, limit=10) if log else [],
            'mode': 'module',
            'module_tech': tech,
        }

    def _business_connector_dashboard(self, entry):
        tech = entry['tech']
        cfg = entry.get('config_model')
        log = entry.get('log_model')
        biz = entry.get('biz_model')
        
        conf_count = self._count_safe(cfg)
        log_ok = self._count_safe(log, [('state', '=', 'success')]) if log else 0
        log_err = self._count_safe(log, [('state', '=', 'error')]) if log else 0
        log_all = self._count_safe(log) if log else 0
        rec_count = self._count_safe(biz)

        kpis = [
            {'label': _('Active Connections'), 'value': conf_count, 'icon': 'fa-plug', 'color': '#1877F2'},
            {'label': _('API Calls Success'), 'value': log_ok, 'icon': 'fa-check-circle', 'color': '#0d8a3e'},
            {'label': _('API Errors'), 'value': log_err, 'icon': 'fa-exclamation-triangle', 'color': '#e74c3c'},
            {'label': _('Meta Assets Synced'), 'value': rec_count, 'icon': 'fa-building', 'color': '#8e44ad'},
        ]

        cards = []

        cards.append({
            'id': 'config',
            'title': _('Connection & Tokens'),
            'subtitle': _('Manage your Meta API access and credentials'),
            'icon': 'fa-key',
            'color': '#1877F2',
            'badge': _('Required'),
            'stats': [{'label': _('Credentials'), 'value': conf_count}],
            'details': [
                _('Set up System User Access Tokens'),
                _('Configure Meta App ID & Secret'),
                _('Test API connection securely'),
            ],
            'actions': [
                {
                    'label': _('Manage Credentials'),
                    'icon': 'fa-arrow-right',
                    'type': 'object',
                    'method': 'action_open_model',
                    'params': {'model': cfg, 'name': _('Configuration'), 'view_mode': 'list,form'},
                    'primary': True,
                },
                {
                    'label': _('New Connection'),
                    'icon': 'fa-plus',
                    'type': 'object',
                    'method': 'action_open_model',
                    'params': {
                        'model': cfg,
                        'name': _('Configuration'),
                        'view_mode': 'form',
                        'context': {'form_view_initial_mode': 'edit'},
                    },
                },
            ],
        })

        cards.append({
            'id': 'records',
            'title': _('Meta Business Assets'),
            'subtitle': _('Ad Accounts, Pages, Pixels & Catalogs'),
            'icon': 'fa-briefcase',
            'color': '#8e44ad',
            'stats': [{'label': _('Total Assets'), 'value': rec_count}],
            'details': [
                _('View imported Ad Accounts and Facebook Pages'),
                _('Manage Instagram Accounts and WABA IDs'),
                _('Link assets to specific Odoo Companies'),
            ],
            'actions': [
                {
                    'label': _('Browse Assets'),
                    'icon': 'fa-table',
                    'type': 'object',
                    'method': 'action_open_model',
                    'params': {'model': biz, 'name': _('Meta Assets'), 'view_mode': 'list,form'},
                    'primary': True,
                },
            ],
        })

        cards.append({
            'id': 'tools',
            'title': _('Sync & Import'),
            'subtitle': _('Fetch data directly from Meta Graph API'),
            'icon': 'fa-refresh',
            'color': '#e67e22',
            'stats': [],
            'details': [
                _('Run the Import Wizard to sync your accounts'),
                _('Refresh asset tokens and permissions'),
                _('Verify Webhook endpoints'),
            ],
            'actions': [
                {
                    'label': _('Run Import Wizard'),
                    'icon': 'fa-download',
                    'type': 'object',
                    'method': 'action_open_import_export',
                    'params': {'tech': tech, 'kind': 'import'},
                    'primary': True,
                },
                {
                    'label': _('Sync Outbound'),
                    'icon': 'fa-upload',
                    'type': 'object',
                    'method': 'action_open_import_export',
                    'params': {'tech': tech, 'kind': 'export'},
                },
            ],
        })

        cards.append({
            'id': 'logs',
            'title': _('API Request Logs'),
            'subtitle': _('Monitor Graph API traffic and rate limits'),
            'icon': 'fa-server',
            'color': '#0d8a3e',
            'stats': [
                {'label': _('Total'), 'value': log_all},
                {'label': _('OK'), 'value': log_ok, 'tone': 'success'},
                {'label': _('Failed'), 'value': log_err, 'tone': 'danger'},
            ],
            'details': [
                _('Inspect JSON payloads for debugging'),
                _('Filter 4xx / 5xx HTTP errors'),
                _('Identify rate limiting bottlenecks'),
            ],
            'actions': [
                {
                    'label': _('View All Logs'),
                    'icon': 'fa-list',
                    'type': 'object',
                    'method': 'action_open_model',
                    'params': {'model': log, 'name': _('API Logs'), 'view_mode': 'graph,pivot,list,form'},
                    'primary': True,
                },
                {
                    'label': _('Review Errors'),
                    'icon': 'fa-exclamation-triangle',
                    'type': 'object',
                    'method': 'action_open_model',
                    'params': {
                        'model': log,
                        'name': _('Error Logs'),
                        'view_mode': 'list,form',
                        'domain': [('state', '=', 'error')],
                    },
                },
            ],
        })

        return {
            'title': _('Meta Business Connector'),
            'subtitle': _('Central hub for managing Meta Business Manager credentials, assets, and API sync.'),
            'kpis': kpis,
            'cards': cards,
            'recent_logs': self._recent_logs(log, limit=10) if log else [],
            'mode': 'module',
            'module_tech': tech,
        }

    @api.model
    def action_open_model(self, model=None, name=None, view_mode='list,form', domain=None, context=None):
        if not model or model not in self.env:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Unavailable'),
                    'message': _('This feature is not available.'),
                    'type': 'warning',
                },
            }
        return self._action_window(name or model, model, view_mode=view_mode, domain=domain, context=context)

    @api.model
    def action_open_log_record(self, model=None, res_id=None):
        if not model or model not in self.env or not res_id:
            return False
        return {
            'type': 'ir.actions.act_window',
            'name': _('API Log'),
            'res_model': model,
            'res_id': int(res_id),
            'view_mode': 'form',
            'target': 'current',
        }

    @api.model
    def action_open_panel_settings(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Meta Panel Settings'),
            'res_model': 'res.config.settings',
            'view_mode': 'form',
            'target': 'current',
            'context': {'module': 'website'},
        }

    @api.model
    def action_open_websites(self):
        return self._action_window(_('Websites'), 'website', view_mode='list,form')

    @api.model
    def action_open_pixel_settings(self):
        return self.action_open_panel_settings()

    @api.model
    def action_open_import_export(self, tech=None, kind='import'):
        """Open module import/export wizard when models exist."""
        if not tech:
            return False
        short = tech[3:] if tech.startswith('rj_') else tech
        # e.g. meta_ads_campaigns -> meta.ads.campaigns.import.wizard
        wiz = short.replace('_', '.') + f'.{kind}.wizard'
        if wiz not in self.env:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Wizard'),
                    'message': _('Open Configuration and use Import / Export buttons there.'),
                    'type': 'info',
                },
            }
        return {
            'type': 'ir.actions.act_window',
            'name': _('Import') if kind == 'import' else _('Export / Sync'),
            'res_model': wiz,
            'view_mode': 'form',
            'target': 'new',
        }

    @api.model
    def action_open_suite_dashboard(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'rj_meta_common_v2_dashboard',
            'name': _('Meta Marketing Suite'),
            'params': {'mode': 'suite'},
        }

    @api.model
    def action_open_module_dashboard(self, module_tech=None):
        if not module_tech:
            return self.action_open_suite_dashboard()
        entry = next((e for e in META_SUITE_CATALOG if e['tech'] == module_tech), None)
        name = (entry or {}).get('name') or _('Dashboard')
        return {
            'type': 'ir.actions.client',
            'tag': 'rj_meta_common_v2_dashboard',
            'name': name,
            'params': {'mode': 'module', 'module_tech': module_tech},
            'context': {'module_tech': module_tech, 'meta_dash_mode': 'module'},
        }

    @api.model
    def get_module_dashboard_action(self, module_tech):
        return self.action_open_module_dashboard(module_tech)
