import os, sys, PyPDF2
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

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

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
                results = search_similar_chunks(query, request.user.id, top_k=5) ## Top-5 most relevant chunks retrieved
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
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def chat_page(request):
    try:
        message = request.data.get("message", "").strip()
        files = request.FILES.getlist("files")
        
        response_text = ""
        
        # Handle file uploads
        if files:
            for f in files:
                # Save file to disk
                file_path = os.path.join(UPLOAD_DIR, f.name)
                with open(file_path, "wb+") as dest:
                    for chunk in f.chunks():
                        dest.write(chunk)
                
                # Process PDF files
                if f.name.endswith('.pdf'):
                    try:
                        import PyPDF2
                        with open(file_path, 'rb') as pdf_file:
                            reader = PyPDF2.PdfReader(pdf_file)
                            text = ""
                            for page in reader.pages:
                                page_text = page.extract_text()
                                # Clean the text to remove NUL characters and other problematic chars
                                if page_text:
                                    clean_text = page_text.replace('\x00', '').replace('\0', '')
                                    # Remove other problematic characters
                                    clean_text = ''.join(char for char in clean_text if ord(char) >= 32 or char in '\n\r\t')
                                    text += clean_text + "\n"
                        
                        if not text.strip():
                            response_text += f"Could not extract readable text from {f.name}. The file may contain only images or be corrupted. "
                            continue
                            
                        print(f"Extracted text length: {len(text)}")  # Debug
                        
                        # Create document record
                        doc = Document.objects.create(
                            title=f.name,
                            uploaded_by=request.user,
                            file=f
                        )
                        
                        # Process with RAG
                        process_document(doc, text)
                        print(f"Document processed: {doc.id}")  # Debug
                        
                    except Exception as pdf_error:
                        print(f"PDF processing error: {pdf_error}")
                        response_text += f"Error processing {f.name}: The file may be password-protected or corrupted. Please try a different PDF. "
                        continue
            
            response_text += f"Uploaded and processed {len(files)} document(s). "
        
        # Handle questions
        if message:
            print(f"Searching for: {message}")  # Debug
            results = search_similar_chunks(message, request.user.id, top_k=5)
            print(f"Search results count: {len(results)}")  # Debug
            
            if results:
                context = "\n".join([result["text"] for result in results])
                answer = generate_answer(message, context)
                response_text += answer
            else:
                response_text += f"No relevant documents found for '{message}'. Try uploading some documents first."
        
        if not response_text:
            response_text = "Please provide a message or upload a file."
            
        return Response({"answer": response_text})
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return Response({"detail": str(e)}, status=500)