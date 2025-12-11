# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime
from odoo import http, fields
from odoo.http import request

_logger = logging.getLogger(__name__)


class TelegramErrorController(http.Controller):

    @http.route('/telegram/log_js_error', type='json', auth='user', methods=['POST'], csrf=False, cors='*')
    def log_js_error(self, error_data):
        try:
            telegram_config = request.env['telegram.config'].search([('active', '=', True)], limit=1)
            if not telegram_config or not telegram_config.send_client_errors:
                return {'success': False, 'message': 'Telegram alerts disabled'}

            # Extract data
            error_message = error_data.get('message', 'Unknown error')
            error_type = error_data.get('type', 'JavaScript Error')
            stack_trace = error_data.get('stack', '')
            url = error_data.get('url', '')
            timestamp = error_data.get('timestamp')

            # Get user and database info
            user_name = request.env.user.name
            user_login = request.env.user.login
            db_name = request.env.cr.dbname

            # Prepare base URL for links
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')

            # Build Telegram message
            message_parts = [
                "🔴 <b>Frontend JavaScript Error</b>\n",
                f"<b>Database:</b> {db_name}",
                f"<b>User:</b> {user_name} ({user_login})",
                f"<b>Error Type:</b> {error_type}\n",
                "<b>Message:</b>",
                f"<code>{error_message[:500]}</code>",
            ]

            if url:
                display_url = url if len(url) <= 80 else url[:77] + "..."
                message_parts.append(f"\n<b>Page:</b> {display_url}")

            if stack_trace and telegram_config.include_traceback:
                trace = stack_trace[:600] + ("...\n[Truncated]" if len(stack_trace) > 600 else "")
                message_parts.append("\n<b>Stack Trace:</b>")
                message_parts.append(f"<code>{trace}</code>")

            # Handle timestamp - convert to user's timezone
            if timestamp:
                try:
                    # Parse ISO format timestamp (JavaScript sends UTC)
                    if isinstance(timestamp, str):
                        # Parse as UTC datetime
                        if timestamp.endswith('Z'):
                            timestamp = timestamp[:-1] + '+00:00'
                        dt_utc = datetime.fromisoformat(timestamp)

                        # Convert UTC to Odoo datetime object (naive datetime in UTC)
                        if dt_utc.tzinfo is not None:
                            dt_utc = dt_utc.replace(tzinfo=None)

                        # Convert to user's timezone using Odoo's context_timestamp
                        dt = fields.Datetime.context_timestamp(request.env.user, dt_utc)
                    else:
                        # Fallback to current time in user's timezone
                        dt = fields.Datetime.context_timestamp(request.env.user, fields.Datetime.now())
                except Exception as e:
                    _logger.warning(f"Error parsing timestamp: {e}, using current time")
                    dt = fields.Datetime.context_timestamp(request.env.user, fields.Datetime.now())
            else:
                # No timestamp provided, use current time in user's timezone
                dt = fields.Datetime.context_timestamp(request.env.user, fields.Datetime.now())

            formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
            message_parts.append(f"\n⏰ {formatted_time}")

            # Create ir.logging record AFTER sending Telegram message
            # This prevents double alerts since IrLogging.create() is overridden
            log_record = request.env['ir.logging'].sudo().with_context(
                skip_telegram_alert=True  # Flag to prevent double alert
            ).create({
                'name': 'odoo.addons.web.frontend',
                'type': 'client',
                'level': 'ERROR',
                'message': f"{error_type}: {error_message}\nURL: {url}\nStack: {stack_trace[:500]}",
                'func': error_type,
                'path': url,
                'line': error_data.get('line', 0),
            })

            # Add link to Odoo log record
            if base_url and log_record:
                share_link = f"{base_url}/web#id={log_record.id}&model=ir.logging&view_type=form"
                message_parts.append(f"\n🔗 <b><a href='{share_link}'>View full error in Odoo</a></b>")

            # Send Telegram message
            telegram_config.send_telegram_message("\n".join(message_parts))

            return {'success': True, 'log_id': log_record.id}

        except Exception as e:
            _logger.error(f'Failed to log JS error to Telegram: {e}')
            return {'success': False, 'message': str(e)}