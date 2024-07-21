import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from contact_spam.serializers import ContactWithSpamSerialiazer
from contact_spam.service.service import get_contact_from_name, report_spam_by_phone, search_contact_by_phone
from rest_framework.views import APIView

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContactSearchByName(APIView):
    """
    Search for a phone number in the contacts given 
    a name in request data.
    """
    
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs) -> Response:
        logger.info("Received request to search contact by name")
        try:
            logger.debug("Request data: %s", request.data)
            contact = ContactWithSpamSerialiazer(get_contact_from_name(request), many=True).data
            logger.info("Successfully retrieved contact information")
            return Response(contact, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Error occurred: %s", e)
            return Response({"error": "Name cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
    
class ReportSpamByPhone(APIView):
    """
    Mark Phone Number as spam
    """
    
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs) -> Response:
        logger.info("Received request to report spam by phone")
        logger.debug("Request data: %s", request.data)
        error, spam_object = report_spam_by_phone(request)
        if spam_object is not None:
            logger.info("Spam reported successfully")
            return Response("Spam Reported Successfully", status=status.HTTP_200_OK)
        else:
            logger.warning("Failed to report spam: %s", error)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        
class SearchByPhone(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, query_param):
        logger.info("Received request to search contact by phone")
        logger.debug("Query parameter: %s", query_param)
        try:
            error, contacts = search_contact_by_phone(query_param)
            if error:
                logger.warning("Failed to search contact: %s", error)
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            logger.info("Successfully retrieved contacts")
            return Response(list(contacts), status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Error occurred: %s", e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
