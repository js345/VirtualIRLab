from flask import send_file
from flask_login import login_required
from flask_restful import Resource

from schema.Document import Document


class DocumentAPI(Resource):
    @login_required
    def get(self, doc_id):
        doc = Document.objects(id=doc_id).first()
        return send_file(doc.path, as_attachment=True)
