from odoo import fields, models


# Model Definition
class EstateProperty(models.Model):
   _name = "estate.property"
   _description = "Real Estate Property"
   


   # Fields
   name = fields.Char(string="Estate Property Name",required=True)
   estate_property_description = fields.Text()
   surface = fields.Float(required=True)
    # ... tus campos existentes ...
   property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type"
    )
