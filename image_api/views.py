from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from common.utils import create_hash, intTryParse, floatTryParse
from gallery.models import Image, Gallery, Tag
from gallery.models.image import upload_to
from image_api.serializers import ImageSerializer
from message_queue.models import create_message

import os
import PIL

MAX_FILE_SIZE = 15000000  # bytes

class ImageListView(viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = ImageSerializer

    def get_queryset(self):
        return Image.objects.filter(family_id = self.request.user.family_id).order_by('date_taken')[:20]

    def list(self, request):
        '''
        Lists images in users family.
        Use query parameters ?gallery_id=<id> to filter by gallery or
        ?person_id=<id> to filter by tagged people
        '''
        queryset = Image.objects.filter(family_id = self.request.user.family_id).order_by('date_taken')

        gallery_id = self.request.query_params.get('gallery_id', None)
        if gallery_id is not None:
            queryset = queryset.filter(gallery_id=gallery_id).order_by('date_taken')

        person_id = self.request.query_params.get('person_id', None)
        if person_id is not None:
            queryset= queryset.filter(tag__person_id = person_id).order_by('date_taken')

        page = self.paginate_queryset(queryset)
        serializer = ImageSerializer(page, many=True)

        # return Response(serializer.data)
        return self.get_paginated_response(serializer.data)



    def retrieve(self, request, pk=None):
        '''
        Gets a single image record
        '''
        queryset = Image.objects.filter(family_id = request.user.family_id)
        image = get_object_or_404(queryset, pk=pk)
        serializer = ImageSerializer(image)
        return Response(serializer.data)

    def create(self, request):
        '''
        Image upload
        '''
        queryset = Gallery.objects.filter(family_id = request.user.family_id)
        gallery_id, gallery_id_valid = intTryParse(request.data.get("gallery_id"))

        if not gallery_id_valid:
            return HttpResponse(status=400, content='Invalid gallery_id')

        # Check gallery is part of family
        gallery = get_object_or_404(queryset, pk=gallery_id)

        try:
            uploaded = request.FILES['picture']
            name, ext = os.path.splitext(uploaded.name)

            if uploaded.size > MAX_FILE_SIZE:
                return HttpResponse(status=400, content='File too big')

            filename =  create_hash(uploaded.name) +'.jpg'
            image = Image(gallery_id=gallery.id, family_id=gallery.family_id, title=name, uploaded_by=request.user)

            path = upload_to(image, filename)

            #Write the file to the destination
            destination = open(os.path.join(settings.MEDIA_ROOT, path), 'wb+')

            for chunk in uploaded.chunks():
                destination.write(chunk)
            destination.close()

            image.original_image = path
            PIL.Image.open(os.path.join(settings.MEDIA_ROOT, str(image.original_image))).verify()
            image.save()

            image.upload_files_to_s3()
            image.delete_local_image_files()

            create_message('image_face_detect', image.id)

            serializer = ImageSerializer(image)
            return Response(serializer.data)

        except Exception as e:


            if image:
                image.delete_local_image_files()
                image.delete()

            return HttpResponse(status=400, content=str(e))


    def destroy(self, request, pk=None):
        '''
        Gets a single image record
        '''
        queryset = Image.objects.filter(family_id = request.user.family_id)
        image = get_object_or_404(queryset, pk=pk)
        image.delete_local_image_files()
        image.delete_remote_image_files()
        image.delete()

        return Response('OK')


    def partial_update(self, request, pk=None):
        '''
        Editing image
        '''
        queryset = Image.objects.filter(family_id = request.user.family_id)
        image = get_object_or_404(queryset, pk=pk)

        title = self.request.data.get('title')
        if not title or len(title.strip()) == 0:
            return HttpResponse(status=400, content="Invalid title")


        anticlockwise_angle, rotation_valid = intTryParse(request.data.get("anticlockwise_angle"))
        if rotation_valid and anticlockwise_angle != 0:
            image.rotate(anticlockwise_angle)

            # Rotate any image tags
            for tag in list(Tag.objects.filter(image_id = image.id)):
                tag.rotate(anticlockwise_angle)
                tag.save()


        description = self.request.data.get('description')
        if not title or len(title.strip()) == 0:
            description = ""

        image.title = title
        image.description = description

        latitude, latitude_valid = floatTryParse(request.data.get("latitude"))
        longitude, longitude_valid = floatTryParse(request.data.get("longitude"))

        if latitude_valid and longitude_valid and latitude != 0 and longitude != 0:
            image.latitude = latitude
            image.longitude = longitude

        image.save()

        # if we have rotated image, run facial recognition again
        if rotation_valid and anticlockwise_angle != 0:
            create_message('image_face_detect', image.id)

        serializer = ImageSerializer(image)
        return Response(serializer.data)

