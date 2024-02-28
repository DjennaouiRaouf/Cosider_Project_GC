import sys

from django.core.exceptions import ValidationError
from django.db.models import Q, F
from django.db.models.signals import *
from django.dispatch import *
from safedelete.signals import *

from api_gc.models import *
@receiver(pre_save,  sender=Encaissement)
def pre_save_encaissement(sender, instance, **kwargs):
    if not instance.pk:
        try:

            sum = Encaissement.objects.filter(facture=instance.facture).aggregate(models.Sum('montant_encaisse'))[
                        "montant_encaisse__sum"]

        except Encaissement.DoesNotExist:
                pass

        if(not sum):
            sum=0
        sum=sum+instance.montant_encaisse
        instance.montant_creance=instance.facture.montant_factureTTC-sum
        if(instance.montant_creance == 0):
            instance.facture.paye=True
            instance.facture.save()
        if(instance.montant_creance < 0):
            raise ValidationError('Le paiement de la facture est terminer')

@receiver(post_softdelete, sender=Encaissement)
def update_on_softdelete(sender, instance, **kwargs):
    try:
        encaissements=Encaissement.objects.filter(Q(id__gt=instance.id))
        if(encaissements):
            encaissements.update(montant_creance=F('montant_creance') + instance.montant_encaisse)

    except Encaissement.DoesNotExist:
        pass


@receiver(pre_save, sender=DQE)
def pre_save_dqe(sender, instance, **kwargs):
    if not instance.pk:
        instance.id = str(instance.prixPrduit.produit.id) + "_" + str(instance.contrat.id)

    instance.montant_qte = round(instance.qte * instance.prixPrduit.prix_unitaire, 2)



@receiver(post_save, sender=DQE)
def post_save_dqe(sender, instance, created, **kwargs):
    if created:
        instance.id = str(instance.prixPrduit.produit.id) + "_" + str(instance.contrat.id)
    total = DQE.objects.filter(contrat=instance.contrat).aggregate(models.Sum('montant_qte'))[
            "montant_qte__sum"]
    if not total:
        total = 0
    instance.contrat.montant_ht = round(total, 2)
    instance.contrat.montant_ttc = round(total + (total * instance.marche.tva / 100), 2)
    instance.contrat.save()




@receiver(post_save, sender=Contrat)
def post_save_contrat(sender, instance, created, **kwargs):
    total = DQE.objects.filter(contrat=instance).aggregate(models.Sum('montant_qte'))[
        "montant_qte__sum"]
    if not total:
        total = 0

    Contrat.objects.filter(id=instance.pk).update(
        montant_ht=round(total, 2),
        montant_ttc=round(total + (total * instance.tva / 100), 2))
