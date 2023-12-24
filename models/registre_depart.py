from odoo import models, fields, api
import datetime

class BureauOrdreDocumentDepart(models.Model):
    _name = 'bureau.ordre.document.depart'
    _inherit= ["mail.thread", 'mail.activity.mixin']
    _description = 'Gestion des Documents de Départ au Bureau d\'Ordre'

    destinataire = fields.Many2one('bureau.ordre.service', string='Destinataire', tracking=True, required=True)
    expediteur = fields.Many2one('bureau.ordre.service', string='Expéditeur', tracking=True, required=True)
    num_depart = fields.Char(
        string='Num Depart',
        default='00/00',  # Initial default value
    )
    pdf_file = fields.Many2one('bureau.ordre.document', string='Attachment', tracking=True, required=True)


    
    @api.model
    def _get_default_num_depart(self):
        # Obtenez l'année actuelle
        current_year = datetime.datetime.now().year

        # Obtenez l'ID du dernier enregistrement
        last_record = self.search([], order='id desc', limit=1)

        # If a last record exists and it's the same year, get its number and increment by 1
        if last_record and current_year == last_record.num_depart[-2:]:
            last_number = int(last_record.num_depart.split('/')[0])
            next_number = (last_number + 1) % 100
        else:
            # If no last record exists or it's a new year, start with 1
            next_number = 1

        return next_number

    # num_depart = fields.Char(string='Numéro de départ', required=True, default=_get_default_num_depart, unique=True, readonly=True)
    date_depart = fields.Date(string='Date de départ', default=fields.Date.today(), tracking=True, required=True)
    objet_de_correspondance = fields.Char(string='Objet de correspondance', tracking=True, required=True)
    piece_jointe = fields.Integer(string='Nombre de pièces jointes', tracking=True, required=True)
    reponse = fields.Boolean(string='Réponse', tracking=True, required=False)
    reference_destinataire= fields.Char(string='Référence du destinataire', tracking=True, required=False)

    name = fields.Char(string='Nom', compute='_compute_name', store=True)

    etat = fields.Selection([
        ('recu', 'Reçu'),
        ('en_cours', 'En cours de traitement'),
        ('termine', 'Terminé'),
        ('aarchived', 'Archived'),
    ], string='État', tracking=True, default='recu')

    @api.depends('num_depart')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.num_depart}"


    def action_en_traitment(self):
        for rec in self:
            # rec.etat='en_cours'
            rec.write({'etat': 'en_cours'})
    
    def action_finish(self):
        for rec in self:
            rec.write({'etat': 'termine'})
    
    def action_modifier(self):
        for rec in self:
            rec.write({'etat': 'en_cours'})

    def action_custom_archive(self):
        for rec in self:
            rec.write({'etat': 'aarchived'})
        # self.write({'active': False})
