import json
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
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from backend.services.document_service import process_document, search_similar_chunks
# from .rag_service import generate_answer  # the OpenAI/Claude call ##########



# ----- LOGIN VIEW -----from django.contrib.auth import authenticate

@csrf_exempt  # since frontend posts JSON, CSRF is not needed
def login_page(request):
    if request.method == "POST":
        print("Login POST request received\n")
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
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
                "error": "Invalid username or password"
            })

    return render(request, "login.html")


# ----- LOGOUT VIEW -----
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def logout_page(request):
    logout(request)
    return redirect("login-page")



# ----- UPLOAD VIEW -----
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
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

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        if not username or not password or not email:
            messages.error(request, "All fields are required.")
            return render(request, "register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "register.html")

        User.objects.create_user(username=username, password=password, email=email)
        messages.success(request, "Registration successful! Please log in.")
        return redirect("login-page")

    return render(request, "register.html")


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
