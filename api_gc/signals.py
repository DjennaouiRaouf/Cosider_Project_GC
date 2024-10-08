from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q, F
from django.db.models.signals import *
from django.dispatch import *
from django.utils import timezone
from api_gc.models import *


@receiver(pre_save, sender=InfoEntr)
def pre_save_params(sender, instance, **kwargs):
    if not instance.pk:
        count=InfoEntr.objects.all().count()
        if( count > 0):
            raise ValidationError('Impossible d\'ajouter un parametre')




@receiver(pre_save, sender=Config)
def pre_save_params(sender, instance, **kwargs):
    if not instance.pk:
        count=Config.objects.all().count()
        if( count > 0):
            raise ValidationError('Impossible d\'ajouter un parametre')



@receiver(pre_save, sender=Avances)
def pre_save_avance(sender, instance, **kwargs):
    if not instance.pk:
        instance.num_avance = Avances.objects.filter(contrat=instance.contrat).count()
        instance.montant_restant=instance.montant_avance



@receiver(pre_save,  sender=Encaissement)
def pre_save_encaissement(sender, instance, **kwargs):
    if(instance.montant_encaisse > 0 ):
        cumule=Encaissement.objects.filter(facture=instance.facture, date_encaissement__lt=str(timezone.now().date().strftime('%Y-%m-%d'))).aggregate(models.Sum('montant_encaisse'))[
                "montant_encaisse__sum"] or 0    
        
        cumule+=instance.montant_encaisse 
        if(instance.facture.montant_facture_ttc-cumule < 0):
            raise ValidationError('Encaissement Terminer')
    else:
        raise ValidationError('Encaissement Impossible Pas de valeur Null')

@receiver(pre_save, sender=DQE)
def pre_save_dqe(sender, instance, **kwargs):
    if not instance.pk:
        instance.id = str(instance.contrat.id)+"-"+str(instance.prixProduit.id)


@receiver(pre_save, sender=PrixProduit)
def pre_save_prixProduit(sender, instance, **kwargs):
    if not instance.pk:
        count = PrixProduit.objects.filter(unite=instance.unite, produit=instance.produit).count()
        instance.id = str(instance.unite) + "-" + str(instance.produit) + "-" + str(count + 1)





@receiver(pre_save, sender=Planing)
def pre_save_planing(sender, instance, **kwargs):
    if(instance.cumule > instance.dqe.qte):
        raise ValidationError("Vous avez dépassé la quantité contractuelle")
