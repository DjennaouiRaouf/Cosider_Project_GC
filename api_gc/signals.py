import sys
from decimal import Decimal


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
        instance.montant_creance=instance.facture.montant_facture_ttc-sum
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
        instance.id = str(instance.contrat.id)+"-"+str(instance.prixProduit.id)



@receiver(pre_save, sender=PrixProduit)
def pre_save_prixProduit(sender, instance, **kwargs):
    if not instance.pk:
        count = PrixProduit.objects.filter(unite=instance.unite, produit=instance.produit).count()
        print(count)
        instance.id = str(instance.unite)+"-"+str(instance.produit.id)+"-"+str(count+1)





@receiver(pre_save, sender=Planing)
def pre_save_planing(sender, instance, **kwargs):
    if(instance.cumule > instance.dqe.qte):
        raise ValidationError("Vous avez dépassé la quantité contractuelle")




@receiver(pre_save, sender=BonLivraison)
def pre_save_bonlivraison(sender, instance, **kwargs):
    if (instance.qte_cumule > instance.dqe.qte):
        raise ValidationError("Vous avez dépassé la quantité contractuelle")


@receiver(pre_save, sender=Factures)
def pre_save_facture(sender, instance, **kwargs):
    if not instance.pk:
        instance.numero_facture=str(Factures.objects.all().count()+1)+'/'+str(datetime.now().year)
        if (instance.du > instance.au):
            raise ValidationError('Date de debut doit etre inferieur à la date de fin')
        else:
            debut = instance.du
            fin = instance.au
            try:
                details = BonLivraison.objects.filter(contrat=instance.contrat, date__lte=fin, date__gte=debut)
                for d in details:
                    DetailFacture.objects.create(facture=instance, detail=d)


            except BonLivraison.DoesNotExist:
                raise ValidationError('Facturation impossible les bons de livraison ne sont pas disponible ')


