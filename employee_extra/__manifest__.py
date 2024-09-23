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
        'data/hr_skills_type.xml',
        'data/hr.skills.level.csv',
        'data/hr.skills.csv',
        'data/hr_certifications.xml',
        'data/hr.certifications.skills.csv',
        'wizard/batch_update.xml',
        'views/employee_extra.xml',
        'views/certifications_view.xml',
        'views/skills_view.xml',
        'views/menu.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}
