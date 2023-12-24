from odoo import models, fields, api
import datetime

class BureauOrdreDocumentDepart(models.Model):
    _name = 'bureau.ordre.document.depart'
    _description = 'Gestion des Documents de Départ au Bureau d\'Ordre'

    destinataire = fields.Many2one('bureau.ordre.service', string='Destinataire', required=True)
    expediteur = fields.Many2one('bureau.ordre.service', string='Expéditeur', required=True)
    
    # reference_destinataire = fields.Many2one('bureau.ordre.document.arrivee', string='Référence du destinataire', required=True)
    reference_destinataire = fields.Many2one('bureau.ordre.document.arrivee', string='Référence du destinataire')

    # Use a related field to display the value from the related model
    reference_expediteur = fields.Char(related='reference_destinataire.reference_expediteur', string='Référence de l\'expéditeur', readonly=True, store=True)

    # pdf_file = fields.Many2one('bureau.ordre.document', string='PDF File', required=True)
    pdf_file = fields.Many2one('bureau.ordre.document', string='PDF File')

    num_depart = fields.Char(
        string='Num Depart',
        default='00/00',  # Initial default value
    )

    @api.model
    def create(self, vals):
        # if 'num_depart' not in vals or vals.get('num_depart') == '00/00':
         # Calculate the next number based on the current year
        current_year = fields.Date.today().strftime('%y')
        # current_year = "24"
        next_number = self.calculate_next_number(current_year)

        vals['num_depart'] = f"{next_number:02}/{current_year}"
            # Create the record
        return super(BureauOrdreDocumentDepart, self).create(vals)


    def calculate_next_number(self, current_year):
        # Search for the last record of the current year that is not archived
        last_record = self.search([
            ('num_depart', 'like', f"%/{current_year}"),
            # ('active', '=', True),  # Exclude archived records
        ], order='num_depart desc', limit=1)

        # If a last record exists and it's the same year, get its number and increment by 1
        if last_record and current_year == last_record.num_depart[-2:]:
            last_number = int(last_record.num_depart.split('/')[0])
            next_number = (last_number + 1) % 100
        else:
            # If no last record exists or it's a new year, start with 1
            next_number = 1

        return next_number



    # @api.model
    # def create(self, values):
    #     # Your custom logic for creating a new record
    #     return super(BureauOrdreDocumentDepart, self).create(values)
        

    

    
    # @api.model
    # def _get_default_num_depart(self):
    #     # Obtenez l'année actuelle
    #     current_year = datetime.datetime.now().year

    #     # Obtenez l'ID du dernier enregistrement
    #     last_record = self.search([], order='id desc', limit=1)

    #     # Si un dernier enregistrement existe, obtenez son ID et incrémentez de 1
    #     if last_record:
    #         next_id = last_record.id + 1
    #     else:
    #         # Si aucun dernier enregistrement n'existe, définissez l'ID à 1
    #         next_id = 1

    #     # Combinez l'ID et l'année pour créer le format souhaité
    #     return f"{next_id:02}/{current_year}"

    # num_depart = fields.Char(string='Numéro de départ', required=True, default=_get_default_num_depart, unique=True, readonly=True)
    date_depart = fields.Date(string='Date de départ', default=fields.Date.today())
    objet_de_correspondance = fields.Char(string='Objet de correspondance', required=True)
    piece_jointe = fields.Integer(string='Nombre de pièces jointes', required=True)
    reponse = fields.Boolean(string='Réponse', required=False)
    # reference_destinataire= fields.Char(string='Référence du destinataire', required=True)

    name = fields.Char(string='Nom', compute='_compute_name', store=True)

    etat = fields.Selection([
        ('recu', 'Reçu'),
        ('en_cours', 'En cours de traitement'),
        ('termine', 'Terminé'),
         ('aarchived', 'Archived'),
    ], string='État', default='recu')

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
