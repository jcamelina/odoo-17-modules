# -*- coding: utf-8 -*-
{
    "name": "update_hr_time_off_kkn",
    "summary": "Short (1 phrase/line) summary of the module's purpose",
    "description": """
Long description of module's purpose
    """,
    "author": "My Company",
    "website": "https://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Customizations",
    "version": "17.0.1.0.0",
    # any module necessary for this one to work correctly
    "depends": ["base", "hr_holidays"],
    # always loaded
    "data": [
        # 'security/ir.model.access.csv',
        "views/hr_leave_allocation_view.xml",
        "views/hr_leave_view.xml",
        "views/templates.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
}
