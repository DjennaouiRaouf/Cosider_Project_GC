from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q, F
from django.db.models.signals import *
from django.dispatch import *

from api_gc.models import *

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
    pass

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









@receiver(pre_save, sender=Factures)
def pre_save_facture(sender, instance, **kwargs):

    if not instance.pk:
        if (instance.du > instance.au):
            raise ValidationError('Date de debut doit etre inferieur à la date de fin')
        else:
            debut = instance.du
            fin = instance.au

            if (not BonLivraison.objects.filter(contrat=instance.contrat.numero, date__date__lte=fin, date__date__gte=debut)):
                raise ValidationError('Facturation impossible les attachements ne sont pas disponible ')
            m = 0
            mrb=0
            bons = BonLivraison.objects.filter(contrat=instance.contrat.numero, date__date__lte=fin, date__date__gte=debut)
            for bon in bons:
                m += bon.montant
                mrb+=bon.dqe.rabais

            print(m)

        instance.montant=m
        instance.montant_rb= mrb
        m = instance.montant - instance.montant_rb
        instance.montant_rg=round((m*instance.contrat.rg/100),4)
        instance.montant_facture_ht=round(instance.montant - instance.montant_rb - instance.montant_rg, 4)
        instance.montant_facture_ttc=round(instance.montant_facture_ht + (instance.montant_facture_ht * instance.contrat.tva.id / 100), 2)



@receiver(post_save, sender=Factures)
def post_save_facture(sender, instance, created, **kwargs):
    if created:
        debut = instance.du
        fin = instance.au
        
        try:
            details =  BonLivraison.objects.filter(contrat=instance.contrat.numero, date__date__lte=fin, date__date__gte=debut)
            if(not details):
                raise ValueError('Pas de Bon de livraison')
            else:
                for d in details:
                    DetailFacture(
                        facture=instance,
                        detail=d
                    ).save()

        except BonLivraison.DoesNotExist:
            raise ValueError('Pas de Bon de livraison')
