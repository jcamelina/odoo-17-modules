# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Company(models.Model):
    _inherit = "res.company"
    company_short = fields.Char(string="Company Short", tracking=True)
