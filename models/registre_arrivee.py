from odoo import models, fields, api
import datetime

class BureauOrdreDocumentArrivee(models.Model):
    _name = 'bureau.ordre.document.arrivee'
    _inherit= ["mail.thread", 'mail.activity.mixin']
    _description = 'Gestion des Documents Arrivées au Bureau d\'Ordre'

    destinataire = fields.Many2one('bureau.ordre.service', string='Destinataire', tracking=True, required=True)
    expediteur = fields.Many2one('bureau.ordre.service', string='Expéditeur', tracking=True, required=True)
    pdf_file = fields.Many2one('bureau.ordre.document', string='PDF File', tracking=True, required=True)

    @api.model
    def _get_default_num_arrivee(self):
        # Obtenez l'année actuelle!!!!!!!!!!!!!!change!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        current_year = datetime.datetime.now().strftime('%y')

        # Obtenez l'ID du dernier enregistrement!!! si supprimé!!!!!!!!!
        last_record = self.search([], order='id desc', limit=1)

        # Si un dernier enregistrement existe, obtenez son ID et incrémentez de 1
        if last_record:
            next_id = last_record.id + 1
        else:
            # Si aucun dernier enregistrement n'existe, définissez l'ID à 1
            next_id = 1

        # Combinez l'ID et l'année pour créer le format souhaité
        return f"{next_id:02}/{current_year}"

    num_arrivee = fields.Char(string='Numéro de Document arrive', default=_get_default_num_arrivee, tracking=True, required=True ,readonly="1")
    date_arrivee = fields.Date(string='Date de départ', tracking=True, default=fields.Date.today())
    # destinataire = fields.Char(string='Destinataire', required=True)
    objet_de_correspondance = fields.Char(string='Objet de correspondance', tracking=True, required=True)
    piece_jointe = fields.Integer(string='Nombre de pièces jointes', tracking=True, required=True)
    # expediteur = fields.Char(string='Expéditeur', required=True)
    reference_expediteur= fields.Char(string='Référence de l\'expediteur', tracking=True, required=False)
    etat = fields.Selection([
        ('recu', 'Reçu'),
        ('en_cours', 'En cours de traitement'),
        ('termine', 'Terminé'),
    ], string='État', tracking=True, default='recu')

    # pdf_file = fields.Binary(string='PDF File', attachment=True, help='Upload a PDF file')
    demande = fields.Boolean(string='Demande', tracking=True,)


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


    name = fields.Char(string='Nom', compute='_compute_name', store=True)

    @api.depends('num_arrivee')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.num_arrivee}"
