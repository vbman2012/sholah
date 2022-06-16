from django.http import Http404
from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from sholah_api.models import Guest, Movie, Reservation
from sholah_api.serializers import GuestSerializer, MovieSerializer, ReservationSerializer
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, generics, viewsets
# Create your views here.


def no_rest_no_model(request):
    guests = [
        {
            'id': '1',
            'name': 'Mahmoud',
            'mobile': '11125555555'
        },
        {
            'id': '2',
            'name': 'Lojain',
            'mobile': '885749995'
        }
    ]

    return JsonResponse(guests, safe=False)


def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {
        'guests': list(data.values('name', 'mobile'))
    }
    return JsonResponse(response)


@api_view(['GET', 'POST'])
def FBV_list(request):
    # GET request
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    # POST request
    elif request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def FBV_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoseNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # GET request
    if request.method == 'GET':
        serializer = GuestSerializer(guest, many=False)
        return Response(serializer.data)
    # PUT request
    elif request.method == 'PUT':
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE request
    if request.method == 'DELETE':
        if guest.is_valid():
            guest.delete()
            return Response("data is deleted", status=status.HTTP_200_OK)
        return Response("data is un valid", status=status.HTTP_400_BAD_REQUEST)


class CbvList(APIView):
    """
    _summary_list = filters.SearchFilter(

    Args:
        APIView (_type_): _description_
    """

    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CbvDetail(APIView):
    """
    _summary_list = filters.SearchFilter(

    Args:
        APIView (_type_): _description_
    """

    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, many=False)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        guest = self.get_object(pk)
        guest.delete()
        return Response("data is deleted", status=status.HTTP_204_NO_CONTENT)


# mixins
class mixins_list(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)


# Generics request
class grnrrics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class generaics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


# viewsets
class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    filter_backends = [filters.SearchFilter]
    search_backends = [filters.SearchFilter]


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filter_backends = [filters.SearchFilter]


@api_view(['GET'])
def get_movie(request):
    movies = Movie.objects.filter(
        hall=request.data['hall'],
        movie=request.data['movie']
    )
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def new_reservation(request):
    movie = Movie.objects.get(
        hall=request.data['hall'],
        movie=request.data['movie']
    )
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()

    reservation = Reservation()
    reservation.movie = movie
    reservation.guest = guest
    reservation.save()

    return Response(status=status.HTTP_201_CREATED)
