from odoo import models, fields, api
import datetime

class BureauOrdreDocumentArrivee(models.Model):
    _name = 'bureau.ordre.document.arrivee'
    _description = 'Gestion des Documents Arrivées au Bureau d\'Ordre'

    destinataire = fields.Many2one('bureau.ordre.service', string='Destinataire', required=True)
    expediteur = fields.Many2one('bureau.ordre.service', string='Expéditeur', required=True)

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

    # @api.model
    # def search_by_field(self, field_name, search_value):
    #     # Vérifiez si le champ est valide
    #     if field_name in self._fields:
    #         return self.search([(field_name, '=', search_value)])
    #     else:
    #         return self.search([])  # Retourne tous les enregistrements si le champ n'est pas valide

    # non modifiable??
    num_arrivee = fields.Char(string='Numéro de Document arrive', default=_get_default_num_arrivee, required=True ,readonly="1")
    date_arrivee = fields.Date(string='Date de départ', default=fields.Date.today())
    # destinataire = fields.Char(string='Destinataire', required=True)
    objet_de_correspondance = fields.Char(string='Objet de correspondance', required=True)
    piece_jointe = fields.Integer(string='Nombre de pièces jointes', required=True)
    # expediteur = fields.Char(string='Expéditeur', required=True)
    reference_expediteur= fields.Char(string='Référence du destinataire', required=False)
    etat = fields.Selection([
        ('recu', 'Reçu'),
        ('en_cours', 'En cours de traitement'),
        ('termine', 'Terminé'),
    ], string='État', default='recu')

    pdf_file = fields.Binary(string='PDF File', attachment=True, help='Upload a PDF file')
    demande = fields.Boolean(string='Demande')


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

    
    # cancell???

    # # champ de recherche
    # search_field = fields.Selection([
    #     ('num_arrivee', 'Numéro de Document arrive'),
    #     ('date_arrivee', 'date_arrivee'),
    #     ('destinataire', 'Destinataire'),
    #     ('objet_de_correspondance', 'objet de correspondance')], string='Champ de recherche')

    # search_value = fields.Char(string='Valeur de recherche')

    # def perform_search(self):
    #     model = self.env['bureau.ordre.document.arrivee']
    #     return model.search_by_field(self.search_field, self.search_value)
