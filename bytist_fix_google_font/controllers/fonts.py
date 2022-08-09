# -*- coding: utf-8 -*-
import requests
from odoo.addons.web.controllers.main import Binary
from odoo import http

class FixBinary(Binary):

    @http.route(['/web/content',
        '/web/content/<string:xmlid>',
        '/web/content/<string:xmlid>/<string:filename>',
        '/web/content/<int:id>',
        '/web/content/<int:id>/<string:filename>',
        '/web/content/<int:id>-<string:unique>',
        '/web/content/<int:id>-<string:unique>/<string:filename>',
        '/web/content/<int:id>-<string:unique>/<path:extra>/<string:filename>',
        '/web/content/<string:model>/<int:id>/<string:field>',
        '/web/content/<string:model>/<int:id>/<string:field>/<string:filename>'], type='http', auth="public")
    def content_common(self, xmlid=None, model='ir.attachment', id=None, field='datas',
                       filename=None, filename_field='name', unique=None, mimetype=None,
                       download=None, data=None, token=None, access_token=None, **kw):

        # Intercept response
        response = super(FixBinary,self).content_common(xmlid, model, id, field,
                       filename, filename_field, unique, mimetype,
                       download, data, token, access_token, **kw)

        # Fix google api calls
        if filename == 'web.assets_frontend.css':
            response.data = response.data.decode(response.charset).replace("https://fonts.googleapis.com/css", "/css/font/google").encode(response.charset)

        return response

    @http.route(['/css/font/google'], type='http', auth="public")
    def load_google_font(self, **kw):
        res = requests.get("https://fonts.googleapis.com/css", params=kw)
        text = res.text.replace("https://fonts.gstatic.com", "/css/font/gstatic")
        response = http.Response(text, res.status_code, mimetype='text/css')
        return response

    @http.route(['/css/font/gstatic/<string:pre>/<string:family>/<string:version>/<string:font>/'], type='http', auth="public")
    def load_gstatic(self, pre, family, version, font, **kw):
        res = requests.get("https://fonts.gstatic.com/%s/%s/%s/%s" % (pre, family, version, font), params=kw)
        return http.Response(res.content, res.status_code, headers=dict(res.headers))

