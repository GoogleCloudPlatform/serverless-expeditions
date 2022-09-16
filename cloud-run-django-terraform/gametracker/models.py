from django.db import models
from django.contrib import admin


class Player(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


admin.site.register(Player)


class Game(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=5)
    description = models.TextField()

    def __str__(self):
        return self.name


admin.site.register(Game)


class Match(models.Model):
    players = models.ManyToManyField(
        Player, related_name="matches", verbose_name="List of players"
    )
    game = models.ForeignKey(Game, on_delete=models.RESTRICT)
    winner = models.ForeignKey(
        Player, default=None, related_name="winning_matches", on_delete=models.RESTRICT
    )
    datetime = models.DateTimeField()
    notes = models.TextField(default=None)

    # Oxford comma implementation
    def __str__(self):
        players = [p.name for p in self.players.all()]

        if (len(players)) < 3:
            nice_list = " and ".join(players)

        *ps, an = players
        nice_list = f"{', '.join(ps)} and {an}"

        return f"{self.game.name} match between {nice_list}"

    class Meta:
        verbose_name_plural = "matches"


admin.site.register(Match)
