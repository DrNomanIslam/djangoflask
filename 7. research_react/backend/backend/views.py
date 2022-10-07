from .serializer import AuthorSerializer, ReactSerializer
from .models import Publication, Author
from rest_framework.response import Response
from rest_framework.views import APIView


class PublicationView(APIView):
    serializer_class = ReactSerializer

    def get(self, request):                
        detail = [ {"authors":[[a.author_id, a.first_name] for a in detail.authors.all()], 
        "title": detail.title, "journal": detail.journal,
        "year_of_publication": detail.year_of_publication, "volume": detail.volume,
        "issue": detail.issue, "pp" : detail.pp
        } 
        for detail in Publication.objects.filter().all()]
        return Response(detail)
        
  
    def post(self, request):
  
        serializer = ReactSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return  Response(serializer.data)


class AuthorView(APIView):
    serializer_class = AuthorSerializer

    def get(self, request):
        return Response(Author.objects.all())
  
    def post(self, request):
  
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return  Response(serializer.data)