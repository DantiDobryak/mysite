from django.db import models


class Faction(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Knight(models.Model):
    name = models.CharField(max_length=100)
    race = models.CharField(max_length=50)       # Например: 'Elf', 'Demon', 'Orc'
    loyalty_level = models.IntegerField()        # Уровень лояльности от 0 до 100
    is_active = models.BooleanField(default=True) # На службе ли сейчас

    faction = models.ForeignKey(Faction, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Artifact(models.Model):
    title = models.CharField(max_length=100)
    power_level = models.IntegerField()
    is_sealed = models.BooleanField(default=False)

    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title