from odoo import fields, models

# Model Definition
class Vehicule(models.Model):
   _name = "Vehicule"
   


   # Fields
   model = fields.Char(string="Vehicule Model",
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
