from odoo import fields, models


# Model Definition
class EstateProperty(models.Model):
   _name = "estate_property"
   _description = "Real Estate Property"
   


   # Fields
   name = fields.Char(string="Estate Property Name",required=True)
   estate_property_description = fields.Text()
   surface = fields.Float(required=True)
