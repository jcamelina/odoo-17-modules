# -*- coding: utf-8 -*-


from odoo import models, fields, api


class Employee(models.Model):
    _inherit = "hr.employee"

    station_id = fields.Many2one("res.station", string="Station", required=True)

    def _inverse_work_contact_details(self):
        for employee in self:
            if not employee.work_contact_id:
                employee.work_contact_id = (
                    self.env["res.partner"]
                    .sudo()
                    .create(
                        {
                            "email": employee.work_email,
                            "mobile": employee.mobile_phone,
                            "name": employee.name,
                            "image_1920": employee.image_1920,
                            "company_id": employee.company_id.id,
                            "contact_type": "employee",
                            "company_type": "person",
                            "station_id": employee.station_id.id,
                            "phone": employee.work_phone,
                        }
                    )
                )
            else:
                employee.work_contact_id.sudo().write(
                    {
                        "email": employee.work_email,
                        "mobile": employee.mobile_phone,
                        "phone": employee.work_phone,
                    }
                )
