from odoo import models, fields, api
import datetime

class BureauOrdreDocumentDepart(models.Model):
    _name = 'bureau.ordre.document.depart'
    _description = 'Gestion des Documents de Départ au Bureau d\'Ordre'

    destinataire = fields.Many2one('bureau.ordre.service', string='Destinataire', required=True)
    expéditeur = fields.Many2one('bureau.ordre.service', string='Expéditeur', required=True)

    @api.model
    def _get_default_num_depart(self):
        # Obtenez l'année actuelle
        current_year = datetime.datetime.now().year

        # Obtenez l'ID du dernier enregistrement
        last_record = self.search([], order='id desc', limit=1)

        # Si un dernier enregistrement existe, obtenez son ID et incrémentez de 1
        if last_record:
            next_id = last_record.id + 1
        else:
            # Si aucun dernier enregistrement n'existe, définissez l'ID à 1
            next_id = 1

        # Combinez l'ID et l'année pour créer le format souhaité
        return f"{next_id:02}/{current_year}"

    num_depart = fields.Char(string='Numéro de départ', required=True, default=_get_default_num_depart, unique=True, readonly=True)
    date_depart = fields.Date(string='Date de départ', default=fields.Date.today())
    objet_de_correspondance = fields.Char(string='Objet de correspondance', required=True)
    piece_jointe = fields.Integer(string='Nombre de pièces jointes', required=True)
    reponse = fields.Boolean(string='Réponse', required=False)
    reference_destinataire= fields.Char(string='Référence du destinataire', required=True)

    name = fields.Char(string='Nom', compute='_compute_name', store=True)

    @api.depends('num_depart')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.num_depart}"
