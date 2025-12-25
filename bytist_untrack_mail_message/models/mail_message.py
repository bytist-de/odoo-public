import re
from markupsafe import Markup
from odoo import models
from odoo.addons.mail.tools.discuss import Store

class MailMessage(models.Model):
    _inherit = 'mail.message'

    def _to_store(self, store: Store, **kwargs):
        """Extends the channel header by adding the livechat operator and the 'anonymous' profile"""
        super()._to_store(store, **kwargs)
        for msg in store.data['mail.message'].values():
            msg['body'] = Markup(re.sub(r"\s+src\s*=\s*(.*)\s+", r" src='/bytist_untrack_mail_message/static/img/gallery-remove-svgrepo-com.svg' data-src=\1 ", str(msg['body'])))
