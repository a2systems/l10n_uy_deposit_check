# -*- coding: utf-8 -*-
{
    'name': 'UY Deposit Check',
    'version': '14.0.1',
    'category': 'Accounting',
    'depends': [
        'account',
        'l10n_latam_check',
        ],
    'data':[
        'payment_view.xml',
        'wizard/wizard_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable' : True,
    'application' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
