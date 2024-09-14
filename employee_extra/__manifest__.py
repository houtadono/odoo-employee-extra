# -*- coding: utf-8 -*-
{
    'name': "Employee Extra",
    'summary': """Employee Extra""",
    'description': """Employee Extra""",
    'category': 'Uncategorized',
    'website': "https://123.com/",
    'author': 'Hz',
    'version': '0.0.1',
    'depends': [
        'base', 'hr'
    ],
    'data':[
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/batch_update.xml',
        'views/employee_extra.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}
