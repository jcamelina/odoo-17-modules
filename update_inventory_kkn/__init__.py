# -*- coding: utf-8 -*-


def _auto_post_init(env):
    companies = env["res.company"].search([])
    for company in companies:
        station = env.ref("update_contact_kkn.lahore_station_id")
        name = company.company_short or company.name.strip().split()[0]
        kkn_parent_location_values = {
            "name": name,
            "usage": "view",
            "station_id": station.id,
            "company_id": company.id,
            "location_id": env.ref("stock.stock_location_locations").id,
            "street": company.street or "KK House 1566/124 Walton Road",
        }
        parent_location = env["stock.location"].create(kkn_parent_location_values)
        kkn_employee_location_values = {
            "name": "Employee",
            "usage": "employee",
            "station_id": station.id,
            "company_id": company.id,
            "location_id": parent_location.id,
            "street": company.street or "KK House 1566/124 Walton Road",
        }
        env["stock.location"].create(kkn_employee_location_values)
        kkn_customer_location_values = {
            "name": "Customer",
            "usage": "customer",
            "station_id": station.id,
            "company_id": company.id,
            "location_id": parent_location.id,
            "street": company.street or "KK House 1566/124 Walton Road",
        }
        env["stock.location"].create(kkn_customer_location_values)


from . import controllers
from . import models
