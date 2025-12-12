# -*- coding: utf-8 -*-
{
    'name': 'Telegram Error Logger',
    'version': '17.0.1.0.0',
    'category': 'Tools',
    'summary': 'Automatically send Odoo backend and frontend errors to Telegram',

    'depends': [
        'base',
        'web',
        'mail',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/telegram_config_views.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'database_monitor/static/src/js/error_logger.js',
        ],
        'web.assets_frontend': [
            'database_monitor/static/src/js/error_logger.js',
        ],
    },

    'installable': True,
    'application': False,
    'auto_install': False,
}
