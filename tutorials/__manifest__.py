{
    'name' : 'QWEB Tutorial',
    'version' : '17.0',
    'summary': 'QWEB Tutorial',
    'sequence': -1,
    'description': """QWEB Tutorial""",
    'category': 'Website',
    'depends' : ['base'],
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'menu/actions.xml',
        'menu/menu.xml',
        'views/devices.xml',
        'views/sequence.xml',
        'views/plan.xml',
    ]
}