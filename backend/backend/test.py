from django.core.management.base import BaseCommand
from documents.models import Document
from backend.services.document_service import process_document

class Command(BaseCommand):
    help = "Test RAG workflow with a sample document"

    def handle(self, *args, **kwargs):
        doc = Document.objects.create(
            title="Test Doc",
            uploaded_by_id=1,
            file=None,
            source="https://example.com/test.txt"
        )
        sample_text = "This is a test document. " * 100
        process_document(doc, sample_text)
        self.stdout.write(self.style.SUCCESS("Test document processed successfully."))
