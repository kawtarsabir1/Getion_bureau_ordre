# models.py
from odoo import models, fields

class BureauOrdreDocument(models.Model):
    _name = 'bureau.ordre.document'
    _description = 'Gestion des Documents au Bureau d\'Ordre'

    name = fields.Char(string='Numéro de Document', required=True)
    date_reception = fields.Date(string='Date de Réception', default=fields.Date.today())
    etat = fields.Selection([
        ('recu', 'Reçu'),
        ('en_cours', 'En cours de traitement'),
        ('termine', 'Terminé'),
    ], string='État', default='recu')
