# from odoo import models, fields

# class BureauOrdreDocumentArrivee(models.Model):
#     # _name = 'bureau.ordre.document.arrivee'
#     _description = 'Gestion des Documents Arrivées au Bureau d\'Ordre'

#     num_arrivee=fields.Char(string='Numéro de Document arrive', required=True)
#     date_arr

#     date_reception = fields.Date(string='Date de Réception', default=fields.Date.today())
#     etat = fields.Selection([
#         ('recu', 'Reçu'),
#         ('en_cours', 'En cours de traitement'),
#         ('termine', 'Terminé'),
#     ], string='État', default='recu')
