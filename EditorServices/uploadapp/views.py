
from rest_framework.parsers import FileUploadParser
#from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import json
import os
import logging
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from uploadapp.serializers import BgFileSerializer
from uploadapp.models  import BgFileToolModel
from rest_framework import generics, status
from rest_framework import permissions
from run import background_removal
from dotenv import load_dotenv

envPath = os.path.join('D:/backgroundTool','.env')

load_dotenv(envPath)

class BgFileUploadView(APIView):

    def post(self, request, *args, **kwargs):
        file_serializer = BgFileSerializer(data=request.data, context={'request': request})
        if file_serializer.is_valid():
            file_serializer.save()
            processId = file_serializer.data.get("id","Unknown Error")
            processUrl = file_serializer.data.get("url","Unknown Error")
            imageInputBaseUrl = os.getenv("IMAGEBASEINPUTPATH","error in config file")
            basePath = os.getenv("BASEPATH","config file error")
            imageOutputPath = os.getenv("IMAGEOUTPUTPATH")
            postFilePath = processUrl.split("media")
            if len(postFilePath) ==2:
                print ("recieved fine")

            else:
                raise ValueError("error in generating the url")
            fileName = postFilePath[1].split("/layers")
            finalInput = str(imageInputBaseUrl) + str(postFilePath[1])

            finalOutput = str(imageOutputPath) + str(fileName[1])
            print ("final input and output request {}".format(finalInput,finalOutput))
            scriptPath =os.getenv("SCRIPTPATH","error in SCRIPTPATH")
            commandToRun = "python {}\main.py -i '{}' -o '{}'".format(scriptPath,finalInput,finalOutput)
            print (commandToRun)
            removalProcess = background_removal(commandToRun)
            removalProcessreturnData =False
            if removalProcess is True:
                print ("O/p has been saved successfully")
                removalProcessreturnData =True

            if removalProcessreturnData is False:
                print ("Error occurred while calling main.py")
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)

            # else:
            #     postUrl= os.getenv("APIURL")
            #     files = {'media': open(finalOutput, 'rb')}
            #     responsePost = requests.post(url, files=files)
            #      if responsePost.status_code!=200:
            #          raise FileNotFoundError("Output file does not exists")
            #TO DO In case of multipart
            #data = MultipartEncoder(
            #                fields={
            #                      'filename': (os.path.basename(finalOutput), open(finalOutput, 'rb'), 'text/plain')
            #                                 }
            #                             )
            #                     response = requests.post(PREVIEW_URL,
            #                                          data=data,
            #                                          headers={
            #                                              'Content-Type': data.content_type
            #
            #                                              }
            #                                          )
            #json_response = json.loads(response.text)
            #print json_response

        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BgFileListView(generics.ListAPIView):
    queryset = BgFileToolModel.objects.all()  #.filter(status='active')
    serializer_class = BgFileSerializer
    # permission_classes = [
    #     permissions.IsAuthenticated
    # ]


