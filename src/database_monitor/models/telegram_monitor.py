# -*- coding: utf-8 -*-
import requests
import logging
import traceback
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime

_logger = logging.getLogger(__name__)


class TelegramConfig(models.Model):
    _name = 'telegram.config'
    _description = 'Telegram Configuration'
    _rec_name = 'name'

    name = fields.Char('Configuration Name', required=True, default='Telegram Bot')
    bot_token = fields.Char('Bot Token', required=True, help='Get from @BotFather')
    chat_id = fields.Char('Chat ID', required=True, help='Group chat ID (negative number)')
    active = fields.Boolean('Active', default=True)
    send_error_alerts = fields.Boolean('Send Error Alerts', default=True)
    send_warning_alerts = fields.Boolean('Send Warning Alerts', default=True)
    send_info_alerts = fields.Boolean('Send Info Alerts', default=False)
    send_client_errors = fields.Boolean('Send Client Errors', default=True)
    send_server_errors = fields.Boolean('Send Server Errors', default=True)
    include_traceback = fields.Boolean('Include Traceback', default=True)
    database_name = fields.Char('Database Name', compute='_compute_database_name', store=True)

    @api.depends('name')
    def _compute_database_name(self):
        for record in self:
            record.database_name = self.env.cr.dbname

    def send_telegram_message(self, message):
        """Send message to Telegram"""
        self.ensure_one()

        if not self.active:
            return False

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

        payload = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'HTML',
            'disable_web_page_preview': False
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()

            if result.get('ok'):
                _logger.info('Telegram message sent successfully')
                return True
            else:
                _logger.error(f'Telegram API error: {result.get("description")}')
                return False

        except Exception as e:
            _logger.error(f'Failed to send Telegram message: {str(e)}')
            return False

    def test_connection(self):
        """Test Telegram connection"""
        self.ensure_one()

        test_message = f"""✅ <b>Connection Test Successful!</b>

<b>Database:</b> {self.database_name}
<b>Configuration:</b> {self.name}

Your Telegram bot is working correctly!
You will receive error alerts here."""

        if self.send_telegram_message(test_message):
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Success'),
                    'message': _('Test message sent to Telegram!'),
                    'type': 'success',
                    'sticky': False,
                }
            }
        else:
            raise UserError(_('Failed to send test message. Please check your configuration.'))


class IrLogging(models.Model):
    _inherit = 'ir.logging'

    @api.model_create_multi
    def create(self, vals_list):
        records = super(IrLogging, self).create(vals_list)

        # Skip if context flag is set (prevents double alerts from controller)
        if self.env.context.get('skip_telegram_alert'):
            return records

        telegram_config = self.env['telegram.config'].search([('active', '=', True)], limit=1)
        if not telegram_config:
            return records

        for record in records:
            # 🛑 Prevent double alerts for frontend JavaScript client errors
            if record.type == 'client':
                continue

            # Server error handling continues normally
            should_alert = False

            # Server/backend error rules
            if record.type == 'server' and telegram_config.send_server_errors:
                if record.level == 'ERROR' and telegram_config.send_error_alerts:
                    should_alert = True
                elif record.level == 'WARNING' and telegram_config.send_warning_alerts:
                    should_alert = True
                elif record.level == 'INFO' and telegram_config.send_info_alerts:
                    should_alert = True
                elif record.level in ('CRITICAL', 'FATAL'):
                    should_alert = True

            # Fallback: Unknown types
            if record.type not in ('client', 'server') and record.level in ('ERROR', 'CRITICAL', 'FATAL'):
                should_alert = True

            if should_alert:
                self._send_error_alert(record, telegram_config)

        return records

    def _send_error_alert(self, record, telegram_config):
        """Send server error alert to Telegram"""
        try:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

            # Build error message
            alert_parts = [
                f"🔴 <b>Server Error - {record.level}</b>\n",
                f"<b>Database:</b> {self.env.cr.dbname}",
                f"<b>Name:</b> {record.name}",
            ]

            if record.func:
                alert_parts.append(f"<b>Function:</b> {record.func}")

            if record.path:
                alert_parts.append(f"<b>Path:</b> {record.path}")

            # Add error message
            alert_parts.append("\n<b>Message:</b>")
            error_msg = record.message[:500] if record.message else 'No message'
            alert_parts.append(f"<code>{error_msg}</code>")

            # Add line number if available
            if record.line:
                alert_parts.append(f"\n<b>Line:</b> {record.line}")

            # Add link to log record
            if base_url:
                log_link = f"{base_url}/web#id={record.id}&model=ir.logging&view_type=form"
                alert_parts.append(f"\n🔗 <b><a href='{log_link}'>View in Odoo</a></b>")

            # Add timestamp with timezone
            dt = fields.Datetime.context_timestamp(self.env.user, record.create_date)
            user_tz = self.env.user.tz or 'UTC'
            alert_parts.append(f"\n⏰ {dt.strftime('%Y-%m-%d %H:%M:%S')} ({user_tz})")

            alert_message = "\n".join(alert_parts)
            telegram_config.send_telegram_message(alert_message)

        except Exception as e:
            _logger.error(f'Failed to send error alert to Telegram: {str(e)}')


class IrMailServer(models.Model):
    _inherit = 'ir.mail_server'

    def send_email(self, message, mail_server_id=None, smtp_server=None, smtp_port=None,
                   smtp_user=None, smtp_password=None, smtp_encryption=None, smtp_debug=False,
                   smtp_session=None):
        """Override to catch email sending errors"""
        try:
            return super(IrMailServer, self).send_email(
                message, mail_server_id, smtp_server, smtp_port,
                smtp_user, smtp_password, smtp_encryption, smtp_debug, smtp_session
            )
        except Exception as e:
            # Send Telegram alert for email failures
            telegram_config = self.env['telegram.config'].search([('active', '=', True)], limit=1)

            if telegram_config and telegram_config.send_error_alerts:
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

                # Get user timezone
                user_tz = self.env.user.tz or 'UTC'
                dt = fields.Datetime.context_timestamp(self.env.user, fields.Datetime.now())
                formatted_time = f"{dt.strftime('%Y-%m-%d %H:%M:%S')} ({user_tz})"

                alert_message = f"""📧 <b>Email Sending Failed</b>

<b>Database:</b> {self.env.cr.dbname}
<b>User:</b> {self.env.user.name} ({self.env.user.login})
<b>Error:</b> <code>{str(e)[:400]}</code>

<b>Mail Server:</b> {smtp_server or 'Default'}
<b>Time:</b> {formatted_time}

⚠️ Email functionality is not working!"""

                telegram_config.send_telegram_message(alert_message)

            raise


class IrCron(models.Model):
    _inherit = 'ir.cron'

    def _callback(self, cron_name, server_action_id, job_id):
        """Override to catch scheduled action errors"""
        try:
            return super(IrCron, self)._callback(cron_name, server_action_id, job_id)
        except Exception as e:
            # Send Telegram alert for cron job failures
            telegram_config = self.env['telegram.config'].search([('active', '=', True)], limit=1)

            if telegram_config and telegram_config.send_error_alerts:
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

                # Try to get cron job details
                cron_job = self.browse(job_id) if job_id else None
                cron_link = None

                if cron_job and base_url:
                    cron_link = f"{base_url}/web#id={job_id}&model=ir.cron&view_type=form"

                alert_parts = [
                    "⏰ <b>Scheduled Action Failed</b>",
                    "",
                    f"<b>Database:</b> {self.env.cr.dbname}",
                    f"<b>Cron Job:</b> {cron_name}",
                    f"<b>Error:</b> <code>{str(e)[:400]}</code>",
                ]

                if telegram_config.include_traceback:
                    tb = traceback.format_exc()
                    if len(tb) > 500:
                        tb = tb[:500] + "..."
                    alert_parts.append("")
                    alert_parts.append(f"<b>Traceback:</b>")
                    alert_parts.append(f"<code>{tb}</code>")

                if cron_link:
                    alert_parts.append("")
                    alert_parts.append(f"🔗 <b><a href='{cron_link}'>VIEW CRON JOB</a></b>")

                alert_parts.append("")
                user_tz = self.env.user.tz or 'UTC'
                dt = fields.Datetime.context_timestamp(self.env.user, fields.Datetime.now())
                alert_parts.append(f"⏰ {dt.strftime('%Y-%m-%d %H:%M:%S')} ({user_tz})")

                alert_message = "\n".join(alert_parts)
                telegram_config.send_telegram_message(alert_message)

            raise