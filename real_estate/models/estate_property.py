from odoo import fields, models

# Model Definition
class EstateProperty(models.Model):
   _name = "estate_property"
   


   # Fields
   model = fields.Char(string="Estate Property Model",
      required=True)
   vehicule_description = fields.Text()
   mileage = fields.Float(required=True)
   is_available = fields.Boolean(default=True)
   last_service = fields.Date()
   transmission = fields.Selection(
      selection=[
         ("automatic", "Automatic Transmission"),
         ("standard", "Standard Transmission"),
      ],
   )
