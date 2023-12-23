from odoo import models, fields

class BureauOrdreDocument(models.Model):
    _name = 'bureau.ordre.document'
    _description = 'Bureau d\'Ordre - Document'

    nom = fields.Char(string='Nom du document', required=True)
    pdf_file = fields.Binary(string='PDF File', attachment=True, help='Upload a PDF file', widget='binary')
    

    # Ajoutez cette méthode pour spécifier comment Odoo doit afficher les enregistrements
    def name_get(self):
        result = []
        for document in self:
            result.append((document.id, document.nom))
        return result
