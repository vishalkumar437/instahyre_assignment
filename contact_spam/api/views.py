from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from contact_spam.serializers import ContactWithSpamSerialiazer
from contact_spam.service.service import get_contact_from_name, report_spam_by_phone, search_contact_by_phone
from rest_framework.views import APIView

class ContactSearchByName(APIView):
    """
    Search for a phone number in the contacts given 
    a name in request data.
    """
    
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs) -> Response:
        try:
            print("request", request.data)
            contact = ContactWithSpamSerialiazer(get_contact_from_name(request), many=True).data
            return Response(contact, status=status.HTTP_200_OK)
        except:
            return Response({"error":"Name cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
    
class ReportSpamByPhone(APIView):
    permission_classes = (IsAuthenticated,)
    """
    Mark Phone Number as spam
    """
    def post(self, request, *args, **kwargs) -> Response:
        print("request", request.data)
        error, spam_object = report_spam_by_phone(request)
        if spam_object is not None:
            return Response("Spam Reported Sucessfully", status=status.HTTP_200_OK)
        else:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        
class SearchByPhone(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, query_param):
        try:
            print(query_param)
            error, contacts = search_contact_by_phone(query_param)
            if error:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            return Response(list(contacts), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":e}, status=status.HTTP_400_BAD_REQUEST)
        