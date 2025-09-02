from odoo import fields, models

# Model Definition
class EstatePropertyType(models.Model):
   _name = "estate_property_type"
   


   # Fields
   name = fields.Char(string="Estate Property Type Model", required=True)


