from odoo import fields, models

# Model Definition
class EstateProperty(models.Model):
   _name = "estate_property"
   


   # Fields
   model = fields.Char(string="Estate Property Model",
      required=True)
   estate_property_description = fields.Text()
   surface = fields.Float(required=True)

