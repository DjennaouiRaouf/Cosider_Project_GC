import sys
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db.models import Q, F
from django.db.models.signals import *
from django.dispatch import *
from safedelete.signals import *

from api_gc.models import *

@receiver(pre_save, sender=Parametres)
def pre_save_params(sender, instance, **kwargs):
    if not instance.pk:
        count=Parametres.objects.all().count()
        if( count > 0):
            raise ValidationError('Impossible d\'ajouter un parametre')

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

    instance.montant_qte = round(instance.qte * instance.prixPrduit.prix_unitaire, 4)



@receiver(post_save, sender=DQE)
def post_save_dqe(sender, instance, created, **kwargs):
    total = DQE.objects.filter(contrat=instance.contrat).aggregate(models.Sum('montant_qte'))[
            "montant_qte__sum"]
    if not total:
        total = 0
    instance.contrat.montant_ht = round(total, 4)
    instance.contrat.montant_ttc = round(total + (total * instance.contrat.tva / 100), 4)
    instance.contrat.save()

    chunck=instance.contrat.validite
    if(chunck):
        date_debut = instance.contrat.date_signature
        cumule=0
        for i in range(chunck):
            date = date_debut + relativedelta(months=i)
            if(i<chunck-1):
                qte_chunck = Decimal(int(instance.qte / chunck))
            if(i==chunck-1):
                precedent=Planing.objects.filter(dqe=instance,contrat=instance.contrat,date__lt=date).latest('date')
                qte_chunck = Decimal(int(instance.qte - precedent.qte_cumule))

            cumule = cumule + qte_chunck


            product, created=Planing.objects.update_or_create(
                contrat=instance.contrat, dqe=instance,date=date,
                defaults={
                    "qte_livre":qte_chunck,
                    "qte_cumule":cumule,
                }
                )



    else:
        pass

@receiver(post_save, sender=Contrat)
def post_save_contrat(sender, instance, created, **kwargs):
    if(instance.date_signature < instance.date_expiration):
        delta=relativedelta(instance.date_expiration, instance.date_signature)
        months = delta.months + (delta.years * 12)
        Contrat.objects.filter(pk=instance.pk).update(validite=months)
    total = DQE.objects.filter(contrat=instance).aggregate(models.Sum('montant_qte'))[
        "montant_qte__sum"]
    if not total:
        total = 0

    Contrat.objects.filter(id=instance.pk).update(
        montant_ht=round(total, 4),
        montant_ttc=round(total + (total * instance.tva / 100), 4))

@receiver(post_save, sender=BonLivraison)
def post_save_bonlivraison(sender, instance, **kwargs):
    if not instance.pk:
        bonlivraison = BonLivraison.objects.filter(~Q(pk=instance.pk) & Q(dqe=instance.dqe))
        prix_u = instance.dqe.prixPrduit.prix_unitaire
        if (bonlivraison):  # courant
            previous = bonlivraison.latest('date')
            instance.qte_precedente = previous.qte_cumule
            instance.qte_cumule = instance.qte_precedente + instance.qte_mois
            instance.montant_precedent = round(previous.montant_cumule, 4)
            instance.montant_mois = round(instance.qte_mois * prix_u, 4)
            instance.montant_cumule = round(instance.montant_precedent + instance.montant_mois, 4)

        else:  # debut
            instance.qte_precedente = 0
            instance.qte_cumule = instance.qte_mois
            instance.montant_precedent = 0
            instance.montant_mois = instance.qte_mois * prix_u
            instance.montant_cumule = round(instance.montant_precedent + instance.montant_mois, 4)