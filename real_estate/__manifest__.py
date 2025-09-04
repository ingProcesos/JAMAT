# __manifest__
{
    "name": "Real Estate",
    "version": "18.0.1.0.0",
    "depends": ["base"],
    "author": "Author Name",
    "category": "Custom/Training",
    "description": """
        Description text
    """,
    "data": [
            'security/ir.model.access.csv',
            'views/estate_property_views.xml',        # action estate.property
            'views/estate_property_type_views.xml',   # list+form+action del tipo
            'views/estate_property_form.xml',         # form estate.property
            'views/estate_property_list.xml',         # list estate.property
            'views/estate_property_search.xml',
            'views/estate_property_offer_views.xml',   # views de las ofertas
            'views/estate_property_menu.xml',         # menús al final
    ],
}
