# -*- coding: utf-8 -*-
{
    'name': "My Assembly",  # Module title
    'summary': "Montaje de muebles",  # Module subtitle phrase
    'description': """
Manage Assembly
==============
Description related to Assembly.
    """,  # Supports reStructuredText(RST) format
    'author': "Grupo2",
    'website': "http://www.grupo2.com",
    'category': 'Tools',
    'version': '1.0',
    'depends': ['base'],

    'data': [
        #'security/groups.xml',
        #'security/ir.model.access.csv',
        'views/montaje_mueble.xml',
        'views/montaje_mueble_categ.xml',
        #'views/partner.xml',
    ],
    # This demo data files will be loaded if db initialize with demo data (commented becaues file is not added in this example)
    # 'demo': [
    #     'demo.xml'
    # ],
}
