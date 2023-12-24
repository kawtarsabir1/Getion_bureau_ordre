from odoo import models, fields, api
import datetime

class BureauOrdreDocumentArrivee(models.Model):
    _name = 'bureau.ordre.document.arrivee'
    _description = 'Gestion des Documents Arrivées au Bureau d\'Ordre'

    destinataire = fields.Many2one('bureau.ordre.service', string='Destinataire', required=True)
    expediteur = fields.Many2one('bureau.ordre.service', string='Expéditeur', required=True)
    # pdf_file = fields.Many2one('bureau.ordre.document', string='PDF File')


    the_year = fields.Date(string='The Year', default=lambda self: datetime.datetime.now().strftime('%Y-%m-%d'))
    # active=fields.Boolean('Archived', default=True)

    sequences = fields.Integer('Sequence', default=1)

    # @api.model
    # def _get_default_num_arrivee(self):
    #     current_year = datetime.datetime.now().strftime('%y')

    #     # Obtenez la valeur du compteur
    #     next_id = self.sequences

    #     # Incrémentez le compteur
    #     self.sequences = self.sequences + 1

    #     # Combinez le compteur et l'année pour créer le format souhaité
    #     return f"{next_id}/{current_year}"

    # num_arrivee = fields.Char(string='Numéro de Document arrive', default=_get_default_num_arrivee, required=True ,readonly="1")
    num_arrivee = fields.Char(
        string='Num Arrivee',
        default='00/00',  # Initial default value
    )

    
    @api.model
    def create(self, vals):
        # if 'num_arrivee' not in vals or vals.get('num_arrivee') == '00/00':
         # Calculate the next number based on the current year
        # current_year = fields.Date.today().strftime('%y')
        current_year = "24"
        next_number = self.calculate_next_number(current_year)

                # Set the num_arrivee field with the calculated value
        vals['num_arrivee'] = f"{next_number:02}/{current_year}"
            # Create the record
        return super(BureauOrdreDocumentArrivee, self).create(vals)


    def calculate_next_number(self, current_year):
        # Search for the last record of the current year that is not archived
        last_record = self.search([
            ('num_arrivee', 'like', f"%/{current_year}"),
            # ('active', '=', True),  # Exclude archived records
        ], order='num_arrivee desc', limit=1)

        # If a last record exists and it's the same year, get its number and increment by 1
        if last_record and current_year == last_record.num_arrivee[-2:]:
            last_number = int(last_record.num_arrivee.split('/')[0])
            next_number = (last_number + 1) % 100
        else:
            # If no last record exists or it's a new year, start with 1
            next_number = 1

        return next_number

    date_arrivee = fields.Date(string='Date de départ', default=fields.Date.today())
    # destinataire = fields.Char(string='Destinataire', required=True)
    objet_de_correspondance = fields.Char(string='Objet de correspondance', required=True)
    piece_jointe = fields.Integer(string='Nombre de pièces jointes', required=True)
    # expediteur = fields.Char(string='Expéditeur', required=True)
    reference_expediteur= fields.Char(string='Référence de l\'expediteur', required=False)
    etat = fields.Selection([
        ('recu', 'Reçu'),
        ('en_cours', 'En cours de traitement'),
        ('termine', 'Terminé'),
        ('aarchived', 'Archived'),
    ], string='État', default='recu')

    # pdf_file = fields.Many2one('bureau.ordre.document', string='PDF File', readonly=lambda self: self.etat == 'aarchived')
    pdf_file = fields.Many2one(
    'bureau.ordre.document',
    string='PDF File',
    readonly=lambda self: hasattr(self, 'etat') and self.etat == 'aarchived'
)


    # pdf_file = fields.Binary(string='PDF File', attachment=True, help='Upload a PDF file')
    demande = fields.Boolean(string='Demande')
     

    def action_custom_archive(self):
        for rec in self:
            rec.write({'etat': 'aarchived'})
        # self.write({'active': False})
    


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
