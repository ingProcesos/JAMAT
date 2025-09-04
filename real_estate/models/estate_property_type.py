from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(string="Property Type", required=True)


    _sql_constraints = [
        ('estate_property_type_name_unique',
         'UNIQUE(name)',
         'Property Type name must be unique.'),
    ]