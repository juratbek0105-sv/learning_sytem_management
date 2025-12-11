{
    'name': 'Telegram Error Logger',
    'version': '17.0.1.0.0',
    'category': 'Tools',
    'summary': 'Send Odoo errors to Telegram',
    'description': """
        Telegram Error Logger
        =====================
        * Send server errors to Telegram
        * Send JavaScript/frontend errors to Telegram
        * Track cron job failures
        * Monitor email sending failures
    """,
    'author': 'Your Name',
    'website': 'https://www.yourwebsite.com',
    'depends': ['base', 'web', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/telegram_config_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'telegram_error_logger/static/src/js/error_tracker.js',
        ],
        'web.assets_frontend': [
            'telegram_error_logger/static/src/js/error_tracker.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}