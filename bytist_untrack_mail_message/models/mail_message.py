import re
from markupsafe import Markup
from odoo import models


class MailMessage(models.Model):
    _inherit = 'mail.message'

    def _message_format(self, fnames, format_reply=True, legacy=False):
        vals_list = super()._message_format(fnames=fnames, format_reply=format_reply, legacy=legacy)
        for msg in vals_list:
            msg['body'] = Markup(re.sub(r"\s+src\s*=\s*(.*)\s+", r" src='/bytist_untrack_mail_message/static/img/gallery-remove-svgrepo-com.svg' data-src=\1 ", str(msg['body'])))
        return vals_list
