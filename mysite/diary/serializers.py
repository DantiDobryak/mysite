from rest_framework import serializers
from .models import Artifact, Knight


class ArtifactSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.name', read_only=True)

    class Meta:
        model = Artifact

        fields = ['id', 'title', 'power_level', 'location_name']


class KnightSerializer(serializers.ModelSerializer):
    faction = serializers.CharField(source='faction.name', read_only=True)

    class Meta:
        model = Knight

        fields = ['id', 'name', 'race', 'loyalty_level',  'faction', 'is_active']