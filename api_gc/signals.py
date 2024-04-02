from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q, F
from django.db.models.signals import *
from django.dispatch import *
from safedelete.signals import *
from api_gc.models import *

@receiver(pre_save, sender=Configurations)
def pre_save_params(sender, instance, **kwargs):
    if not instance.pk:
        count=Configurations.objects.all().count()
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
        instance.id = str(instance.unite) + "-" + str(instance.produit) + "-" + str(count + 1)





@receiver(pre_save, sender=Planing)
def pre_save_planing(sender, instance, **kwargs):
    if(instance.cumule > instance.dqe.qte):
        raise ValidationError("Vous avez dépassé la quantité contractuelle")




@receiver(pre_save, sender=BonLivraison)
def pre_save_bonlivraison(sender, instance, **kwargs):
    if not instance.pk:
        config=Configurations.objects.first()
        num=BonLivraison.objects.all_with_deleted().filter(date__date__year=datetime.now().year).count()
        instance.id=str(num+1)+"/"+str(datetime.now().year)+"/"+str(config.unite)

        instance.qte = instance.ptc - instance.camion.tare
        instance.montant = round(instance.qte * instance.dqe.prixProduit.prix_unitaire, 4)





@receiver(pre_save, sender=Factures)
def pre_save_facture(sender, instance, **kwargs):
    if not instance.pk:
        config=Configurations.objects.first()
        instance.id=str(Factures.objects.filter(date__year=datetime.now().year).count()+1)+'/'+str(datetime.now().year)+"/"+str(config.unite)

        if (instance.du > instance.au):
            raise ValidationError('Date de debut doit etre inferieur à la date de fin')
        else:
            debut = instance.du
            fin = instance.au
            try:
                details = BonLivraison.objects.filter(contrat=instance.contrat, date__date__lte=fin, date__date__gte=debut)
                sum=0
                for d in details:
                    DetailFacture.objects.create(facture=instance, detail=d)
                    sum+=d.montant
            except BonLivraison.DoesNotExist:
                raise ValidationError('Facturation impossible les bons de livraison ne sont pas disponible ')
        instance.montant=sum
        instance.montant_rb= round((instance.montant*instance.contrat.rabais/100),4)
        m = instance.montant - instance.montant_rb
        instance.montant_rg=round((m*instance.contrat.rg/100),4)
        instance.montant_facture_ht=round(instance.montant - instance.montant_rb - instance.montant_rg, 4)
        instance.montant_facture_ttc=round(instance.montant_facture_ht + (instance.montant_facture_ht * instance.contrat.tva / 100), 2)



@receiver(post_softdelete, sender=Factures)
def update_on_softdelete(sender, instance, **kwargs):
    DetailFacture.objects.filter(facture=instance.pk).delete()


@receiver(post_undelete, sender=Factures)
def update_on_undelete(sender, instance, **kwargs):
    deleted_objects = DetailFacture.deleted_objects.filter(facture=instance.pk)
    with transaction.atomic():
        for obj in deleted_objects:
            obj.undelete()