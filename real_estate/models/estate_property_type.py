from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Property Type"

    name = fields.Char(string="Property Type", required=True)

