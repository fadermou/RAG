from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Document, DocumentChunk
from .serializers import DocumentSerializer
import PyPDF2

class DocumentUploadAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = DocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document = serializer.save(uploaded_by=request.user)

        if document.file:
            text = extract_text_from_pdf(document.file.path)
            chunks = split_text_into_chunks(text)
            save_chunks(document, chunks)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DocumentListAPIView(generics.ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]


# Utility functions
def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
            text += "\n"
    return text


def split_text_into_chunks(text, chunk_size=1000, overlap=150):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def save_chunks(document, chunks):
    for idx, chunk_text in enumerate(chunks):
        DocumentChunk.objects.create(
            document=document,
            text=chunk_text,
            chunk_index=idx
        )
