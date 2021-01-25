from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from .authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Post
from .serializers import BlogPostSerializer

from .producer import publish

@api_view(['GET'])
def api_blog_post_detail(request,pk):
    # user=request.user
    # print(user)
    try:
        post=Post.objects.get(pk=pk)
    except post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method=='GET':
        serializer=BlogPostSerializer(post)
        return Response(serializer.data)

@api_view(['PUT'])
def api_blog_post_update(request,pk):
    try:
        post=Post.objects.get(pk=pk)
    except post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # user=request.user
    # if post.author != user:
    #     return Response("You don't have permission to edit it.")

    if request.method=='PUT':
        serializer=BlogPostSerializer(post,data=request.data)
        if serializer.is_valid():
            serializer.save()
            publish("post_updated", serializer.data)
            data={'success':'update succes'}
            return Response(data=data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def api_blog_post_delete(request,pk):
    try:
        post=Post.objects.get(pk=pk)
    except post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user=request.user
    if post.author!=user:
        return Response("You don't have permission to delete it.")

    if request.method=='DELETE':
        operation=post.delete()
        if operation:
            data={'success':'delete success'}
        else:
            data={'failure':'delete failed'}
        return Response(data=data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def api_blog_post_create(request):
    user=request.user
    print(user)

    if request.method=='POST':
        serializer=BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['author'] = request.user
            serializer.save()
            publish("post_created", serializer.data)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)