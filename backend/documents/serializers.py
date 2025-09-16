# documents/serializers.py
from rest_framework import serializers
from .models import Document, DocumentChunk

# Serializer for document upload
class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'source']
        read_only_fields = ['id']

# Serializer for querying
class QuerySerializer(serializers.Serializer):
    query = serializers.CharField()

# Optional: Serializer for returning document info
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "title", "uploaded_by", "source", "file", "uploaded_at"]
        read_only_fields = ["id", "uploaded_by", "uploaded_at"]

# Optional: Serializer for returning chunk info
class DocumentChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentChunk
        fields = ["id", "document", "text", "chunk_index", "qdrant_id"]
        read_only_fields = ["id", "qdrant_id"]
