import os
from rest_framework import status
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from documents.models import Document
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, logout
from backend.services.rag_service import generate_answer  
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from backend.services.document_service import process_document, search_similar_chunks



# ----- LOGIN VIEW -----
@csrf_exempt  # since frontend posts JSON, CSRF is not needed
def login_page(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)  # since fetch sends JSON
        username = data.get("username")
        password = data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                "success": True,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "redirect": "/user/upload/"
            })
        else:
            return JsonResponse({
                "success": False,
                "detail": "Invalid username or password"
            }, status=401)
    return render(request, "login.html")


# ----- LOGOUT VIEW -----
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def logout_page(request):
    logout(request)
    return redirect("login-page")


# ----- UPLOAD VIEW -----
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def upload_page(request):
    answer = None

    if request.method == "POST":
        action = request.POST.get("action")

        # --- Upload a document ---
        if action == "upload":
            title = request.POST.get("title")
            source = request.POST.get("source")
            file = request.FILES.get("file")

            if title or source or file:
                doc = Document.objects.create(
                    title=title or "Untitled",
                    uploaded_by=request.user,
                    source=source,
                    file=file
                )

                if file:
                    import PyPDF2
                    text = ""
                    reader = PyPDF2.PdfReader(file)
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    process_document(doc, text)

        # --- Ask a question ---
        elif action == "ask":
            query = request.POST.get("query")
            if query:
                results = search_similar_chunks(query, top_k=5)
                chunks_text = "\n".join([r.payload["text"] for r in results])
                answer = generate_answer(query, chunks_text)

    return render(request, "upload.html", {"answer": answer})



# ----- REGISTER VIEW -----
def register_page(request):
    return render(request, "register.html")  # Just render the page

# ----- REGISTER VIEW for JS + JWT-----
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(
                {"detail": "Username and password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.create_user(username=username, password=password)
        except IntegrityError:
            return Response(
                {"detail": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "username": user.username,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_201_CREATED)


# ----- CHAT VIEW -----
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # ensure upload folder exists

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def chat_view(request):
    try:
        message = request.data.get("message", "").strip()
        files = request.FILES.getlist("files")

        response_text = ""

        # Case 1: Files uploaded
        if files:
            for f in files:
                file_path = os.path.join(UPLOAD_DIR, f.name)
                with open(file_path, "wb+") as dest:
                    for chunk in f.chunks():
                        dest.write(chunk)
            response_text += f"✅ Uploaded {len(files)} file(s). "

        # Case 2: Message (query)
        if message:
            # Hook into your RAG pipeline here
            rag_answer = f"I received your question: '{message}'."
            response_text += rag_answer

        if not response_text:
            return Response(
                {"detail": "Please provide a message or file."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"answer": response_text}, status=status.HTTP_200_OK)

    except Exception as e:
        # Catch all errors and return JSON
        return Response(
            {"detail": f"Server error: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
