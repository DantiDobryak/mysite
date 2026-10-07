from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny

from .models import Knight, Faction, Location, Artifact

from rest_framework.views import APIView, status
from rest_framework.response import Response
from .serializers import ArtifactSerializer, KnightSerializer


def user_login(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')

        user = authenticate(request, username=u, password=p)

        if user:
            login(request, user)

            return redirect('main_menu')
        else:
            return render(request, 'login.html', {'error': 'Неверный логин или пароль'})

    return render(request, 'login.html')


def main_menu(request):
    return render(request, 'main_menu.html')


# работа с фракциями слуг
@login_required
def get_knights(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'delete':
            knight_id = int(request.POST.get('knight_id'))
            Knight.objects.filter(id=knight_id).delete()

            return redirect('knights_list')

        name = request.POST.get('name')
        race = request.POST.get('race')
        loyalty = request.POST.get('loyalty')
        faction_id = request.POST.get('faction_id')

        loyalty_int = int(loyalty) if loyalty else 0
        if loyalty_int < 0 or loyalty_int > 100:
            return HttpResponse('ОШИБКА: лояльность должна быть от 0 до 100!')
        elif not name or not race:
            return HttpResponse('ОШИБКА: поля не могут быть пустыми')

        selected_faction = None
        if faction_id:
            selected_faction = Faction.objects.get(id=faction_id)

        Knight.objects.create(name=name, race=race, loyalty_level=loyalty_int, faction=selected_faction)

        return redirect('knights_list')

    knights_queryset = Knight.objects.select_related('faction').all()

    f_race = request.GET.get('filter_race')
    f_loyalty = request.GET.get('filter_loyalty')
    f_active = request.GET.get('filter_active')

    if f_race:
        knights_queryset = knights_queryset.filter(race__icontains=f_race)

    if f_loyalty:
        knights_queryset = knights_queryset.filter(loyalty_level=int(f_loyalty))

    if f_active:
        is_active_bool = f_active == 'true'
        knights_queryset = knights_queryset.filter(is_active=is_active_bool)

    knights_queryset = knights_queryset.order_by('-loyalty_level')

    all_factions = Faction.objects.all()

    return render(
        request,
        'knights_list.html',
        {
            'knights': knights_queryset,
            'factions': all_factions,
            'current_race': f_race,
            'current_loyalty': f_loyalty,
            'current_active': f_active
        }
    )


def add_new_demon(request):
    Knight.objects.create(name='Malphas', race='demon', loyalty_level=95)

    return HttpResponse("Новый демон успешно нанят!")


def reward_demons(request):
    demons = Knight.objects.filter(is_active=True, race='demon').update(loyalty_level=100)

    return HttpResponse('Лояльность демонов успешно повышена!')


@login_required
def get_artifacts(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'delete':
            artifact_id = request.POST.get('artifact_id')
            Artifact.objects.filter(id=artifact_id).delete()

            return redirect('artifacts')

        title = request.POST.get('title')
        power_level = request.POST.get('power')
        location_id = request.POST.get('location_id')

        power_int = int(power_level) if power_level else 0
        if title == '':
            return HttpResponse('ОШИБКА: название артефакта не может быть пустым!')
        elif power_int < 0 or power_int > 100:
            return HttpResponse('ОШИБКА: мощность артефакта может быть только между 0 и 100')

        selected_location = None
        if location_id:
            selected_location = Location.objects.get(id=location_id)

        Artifact.objects.create(title=title, power_level=power_int, location=selected_location)

        return redirect('artifacts')

    artifact = Artifact.objects.select_related('location').filter(is_sealed=False).order_by('-power_level')
    location = Location.objects.all()

    return render(
        request,
        'artifact.html',
        {
            'artifacts': artifact,
            'locations': location
        })


class ArtifactListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        artifacts = Artifact.objects.select_related('location').all()
        serializer = ArtifactSerializer(artifacts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArtifactSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KnightListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        knights = Knight.objects.select_related('faction').filter(race='demon', is_active=True)
        serializer = KnightSerializer(knights, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = KnightSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
