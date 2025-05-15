from account.models import CustomUser
from mongoengine import Document, StringField, IntField, ReferenceField, DateTimeField, DictField
import datetime

class TesMinat(Document):
    siswa = ReferenceField(CustomUser, required=True)
    response = DictField()
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    similarity_scores = DictField()

    meta = {
        'collection': 'tesminat',
        'ordering': ['-created_at']
    }


class Quiz(Document):
    meta = {'collection': 'quiz'}  # nama koleksi MongoDB
    pertanyaan_id = StringField(required=True, primary_key=True)
    pertanyaan = StringField(required=True)

    def __str__(self):
        return self.pertanyaan[:50]


class Response(Document):
    user = ReferenceField(CustomUser, required=True)
    tesminat = ReferenceField(TesMinat, required=True)
    question = ReferenceField(Quiz, required=True)
    value = IntField(min_value=1, max_value=5)

    meta = {
        'collection': 'response',
        'indexes': [
            {'fields': ['tesminat', 'question'], 'unique': True}
        ]
    }
