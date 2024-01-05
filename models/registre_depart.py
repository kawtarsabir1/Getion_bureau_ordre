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
    def create(self, vals):
        # if 'num_depart' not in vals or vals.get('num_depart') == '00/00':
        # Calculate the next number based on the current year
        current_year = fields.Date.today().strftime('%y')
        # current_year = "22"
        next_number = self.calculate_next_number(current_year)

        # Set the num_depart field with the calculated value
        vals['num_depart'] = f"{next_number:02}/{current_year}"
            # Create the record
        return super(BureauOrdreDocumentDepart, self).create(vals)

    # IT DIDNT EXIST
    def calculate_next_number(self, current_year):
        # Search for the last record of the current year that is not archived
        last_record = self.search([
            ('num_depart', 'like', f"%/{current_year}"),
        ], order='num_depart desc', limit=1)

        # If a last record exists and it's the same year, get its number and increment by 1
        if last_record and current_year == last_record.num_depart[-2:]:
            last_number = int(last_record.num_depart.split('/')[0])
            next_number = (last_number + 1) % 100
        else:
            # If no last record exists or it's a new year, start with 1
            next_number = 1

        return next_number
    

    
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
