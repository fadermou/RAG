from django.db import models

# Create your models here.
import uuid
from django.conf import settings  # to reference the custom User model

class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="documents",
        null=True,
        blank=True
    )
    source = models.URLField(blank=True, null=True)  # optional if file uploaded via URL
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="documents/", blank=True, null=True)  # optional

    def __str__(self):
        return f"{self.title} ({self.uploaded_by.username})"


class DocumentChunk(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="chunks"
    )
    text = models.TextField()
    chunk_index = models.PositiveIntegerField()
    qdrant_id = models.CharField(max_length=255, blank=True, null=True)  # ID in vector DB

    def __str__(self):
        return f"Chunk {self.chunk_index} of {self.document.title}"

