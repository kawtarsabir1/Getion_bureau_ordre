from odoo import models, fields

class BureauOrdreService(models.Model):
    _name = 'bureau.ordre.service'
    _description = 'Bureau d\'Ordre - Service'

    nom = fields.Char(string='Nom du service', required=True)
    image = fields.Binary(string='Image')
    date_release = fields.Date(default=fields.Date.today(), required=True)

    # Ajoutez cette méthode pour spécifier comment Odoo doit afficher les enregistrements
    def name_get(self):
        result = []
        for service in self:
            result.append((service.id, service.nom))
        return result
