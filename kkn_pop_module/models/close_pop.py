# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessDenied

# AVAILABLE_PRIORITIES = [
#     ('0', 'Low'),
#     ('1', 'Medium'),
#     ('2', 'High'),
#     ('3', 'Very High'),
# ]

STATES = [
    ("draft", "Draft"),
    ("admin_approval", "Admin Approval"),
    ("approved", "Approved"),
    ("coo_approval", "COO Approval"),
    ("ceo_approval", "CEO Approval"),
    ("rejected", "Rejected"),
    ("cancel", "Cancel"),
]


class kknClosePopModel(models.Model):
    _name = 'close.pop.model'
    _description = 'Close POP'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    state = fields.Selection(
        STATES,
        string="State",
        required=True,
        default="draft",
        tracking=True,
        group_expand="_expand_states",
    )

    # color = fields.Integer("Color Index")
    # priority = fields.Selection(
    #     AVAILABLE_PRIORITIES,
    #     string="Priority",
    #     index=True,
    #     default=AVAILABLE_PRIORITIES[0][0],
    # )

    kanban_state = fields.Selection(
        [
            ("draft", "Grey"),
            ("admin_approval", "Yellow"),
            ("approved", "Green"),
            ("ceo_approval", "Red"),
            ("coo_approval", "Blue"),
            ("rejected", "Red"),
            ("cancel", "Red"),
        ],
        string="Kanban State",
        copy=False,
        default="draft",
        required=True,
    )
    kanban_state_label = fields.Char(
        compute="_compute_kanban_state_label", string="Kanban State Label", store=True
    )

    @api.depends("state", "kanban_state")
    def _compute_kanban_state_label(self):
        for task in self:
            task.kanban_state = task.state
            task.kanban_state_label = task.state

    existing_location_id = fields.Many2one('stock.location', 'Existing Location', domain="['|', ('usage', '=', 'pop'),"
                                                                                         " ('customer_is_pop', '=', "
                                                                                         "True)]", required=1,
                                           tracking=True)

    @api.onchange('existing_location_id')
    def _onchange_existing_location(self):
        self.unique_id = False
        self.city_code = False
        self.usage = False
        self.street = False
        self.name = False
        self.location_id = False
        self.city_id = False
        self.state_id = False
        self.country_id = False
        self.company_id = False
        self.zip_id = False
        self.partner_latitude = 0.000
        self.partner_longitude = 0.000
        if self.existing_location_id:
            self.unique_id = self.existing_location_id.unique_id
            self.city_id = self.existing_location_id.city_id
            self.unique_id = self.existing_location_id.unique_id
            self.city_code = self.existing_location_id.city_code
            self.unique_id = self.existing_location_id.unique_id
            self.usage = self.existing_location_id.usage
            self.street = self.existing_location_id.street
            self.name = self.existing_location_id.name
            self.location_id = self.existing_location_id.location_id
            self.state_id = self.existing_location_id.state_id
            self.country_id = self.existing_location_id.country_id
            self.company_id = self.existing_location_id.company_id
            self.zip_id = self.existing_location_id.zip_id
            self.partner_latitude = self.existing_location_id.partner_latitude
            self.partner_longitude = self.existing_location_id.partner_longitude
            self.unique_id = self.existing_location_id.unique_id

    name = fields.Char('Location Name', tracking=True)
    complete_name = fields.Char("Full Location Name", compute='_compute_complete_name', store=True, tracking=True)
    location_id = fields.Many2one(
        'stock.location', 'Parent Location', index=True, ondelete='cascade', check_company=True,
        help="The parent location that includes this location. Example : The 'Dispatch Zone' is the 'Gate 1' parent "
             "location.", tracking=True, default=lambda self: self.env['stock.location'].search(
            [('name', '=', 'KKN')]).id)
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env.company, index=True,
        help='Let this field empty if this location is shared between companies', tracking=True)
    city_code = fields.Char(related='city_id.code', tracking=True)
    # Unique ID for location form
    unique_id = fields.Char(string='Unique ID', tracking=True)

    file_upload = fields.Binary(string='Documents', tracking=True)
    file_name = fields.Char(tracking=True, string='Rental Agreement', required=False)

    # New Type in usage Pop
    usage = fields.Selection(related='location_id.usage', string='Location Type', tracking=True)
    partner_latitude = fields.Float('Geo Latitude', digits=(16, 6), tracking=True)
    partner_longitude = fields.Float('Geo Longitude', digits=(16, 6), tracking=True)
    date_localization = fields.Date(string='Geolocation Date', tracking=True)
    comment = fields.Text('Additional Information')

    street = fields.Char(tracking=True, required=True)
    street2 = fields.Char(tracking=True)
    city_id = fields.Many2one('res.district', tracking=True,
                              default=lambda self: self.env['res.district'].search([('code', '=', 'LHR')]).id,
                              required=True)
    state_id = fields.Many2one("res.country.state", tracking=True,
                               default=lambda self: self.env['res.country.state'].search([('code', '=', 'PK-PJ')]).id,
                               required=True)
    zip_id = fields.Char(tracking=True, default='54000')
    country_id = fields.Many2one('res.country', domain="[('name','=','PAKISTAN')]", tracking=True,
                                 default=lambda self: self.env['res.country'].search(
                                     [('name', '=', 'PAKISTAN')]).id, required=True)
    picking_id = fields.Many2one('stock.picking', 'Return Transfer')

    def draft_state_method(self):
        # code for draft state method
        self.set_state_draft()

    def admin_approval_state_method(self):
        # code for admin_approval state method
        self.set_state_admin_approval()

    def approved_state_method(self):
        # code for assigned state method
        self.set_state_approved()

    def coo_approval_state_method(self):
        # code for unassign_request state method
        self.set_state_coo_approval()

    def ceo_approval_state_method(self):
        # code for unassigned state method
        self.set_state_ceo_approval()

    def rejected_state_method(self):
        # code for rejected state method
        self.set_state_rejected()

    def cancel_state_method(self):
        # code for cancel state method
        self.set_state_cancel()

    # state setter methods
    def set_state_draft(self):
        self.state = "draft"

    def set_state_admin_approval(self):
        self.state = "admin_approval"

    def set_state_approved(self):
        self.state = "approved"

    def set_state_coo_approval(self):
        self.state = "coo_approval"

    def set_state_ceo_approval(self):
        self.state = "ceo_approval"

    def set_state_rejected(self):
        self.state = "rejected"

    def set_state_cancel(self):
        self.state = "cancel"

    @api.model
    def _geo_localize(self, street='', zip='', city='', state='', country=''):
        geo_obj = self.env['base.geocoder']
        search = geo_obj.geo_query_address(street=street, zip=zip, city=city, state=state, country=country)
        result = geo_obj.geo_find(search, force_country=country)
        if result is None:
            search = geo_obj.geo_query_address(city=city, state=state, country=country)
            result = geo_obj.geo_find(search, force_country=country)
        return result

    # Get address along city, state adn country and write latitude, longitude
    def geo_localize_location(self):
        # We need country names in English below
        for partner in self.with_context(lang='en_US'):
            result = self._geo_localize(partner.street,
                                        partner.zip_id,
                                        partner.city_id.name,
                                        partner.state_id.name,
                                        partner.country_id.name)

            if result:
                partner.write({
                    'partner_latitude': result[0],
                    'partner_longitude': result[1],
                    'date_localization': fields.Date.context_today(partner)
                })
        return True
