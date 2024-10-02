"""
Project: Aplikace pro oziveni fotek
Author: Adrian Bobola
Email: xbobol00@stud.fit.vutbr.cz
University: FIT VUT Brno
Created on: 2024-05-09
"""

from django.db import models
from datetime import timedelta
from django.utils import timezone


class SystemState(models.Model):
    """
    Trieda SystemState sluzi na spravu stavu aktivity systemu ulozenej v databaze.
    Umoznuje sledovat, ci je system aktualne vyuzivany, akym uzivatelskym tokenom a kedy bola aplikacia
    spustena uzivatelovi.

    Attributes:
        is_active (bool): Hodnota urcujuce, ci je system aktualne pouzivany nejakym uzivatelom
        user_token (string): Token uzivatela, ktory ma prtisup do aplikacie a aktualne ju vyuziva
        last_activated (datetime): Casova znamka posledneho spustenia aplikacie uzivatelom
    """
    is_active = models.BooleanField(default=False)
    user_token = models.CharField(max_length=255, null=True, blank=True)
    last_activated = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = 'backend'

    @classmethod
    def set_active(cls, user_token):
        """
        Nastavi stav systemu ako aktivny a aktualne pouzivany
        """
        state, _ = cls.objects.get_or_create(pk=1)
        state.is_active = True
        state.user_token = user_token
        state.last_activated = timezone.now()
        state.save()

    @classmethod
    def set_inactive(cls):
        """
         Nastavi stav systemu ako neaktivny a aktualne nepouzivany
         """
        state, _ = cls.objects.get_or_create(pk=1)
        state.is_active = False
        state.user_token = None
        state.save()

    @classmethod
    def is_activated(cls):
        """
         Vrati aktualny stav vyuzitia systemu
         """
        state, _ = cls.objects.get_or_create(pk=1)
        return state.is_active

    @classmethod
    def get_current_user_token(cls):
        """
         Vrati token uzivatela, ktory aktualne vyuziva system
         """
        state, _ = cls.objects.get_or_create(pk=1)
        return state.user_token if state.is_active else None

    @classmethod
    def check_active_timer(cls):
        """
         Sluzi ku kontrole casovej znamky posledneho spustenia aplikacie.
         Ak uzivatel pouziva aplikaciu dlhsie nez 5 minut, dojde k odobratiu jeho pristupu a uvolneniu aplikacie
         pre dalsieho uzivatela cakajuceho vo fronte.
         """
        state, _ = cls.objects.get_or_create(pk=1)
        if state.is_active and state.last_activated:
            if timezone.now() - state.last_activated > timedelta(minutes=5):
                state.is_active = False
                state.user_token = None
                state.save()
                return True
        return False
