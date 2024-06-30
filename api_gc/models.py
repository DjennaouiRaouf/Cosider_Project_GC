from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_currentuser.middleware import get_current_user
from django.db.models import Q, F, IntegerField, Sum
# Create your models here.


class GeneralManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(~Q(est_bloquer=True))
    def deleted(self):
        return super().get_queryset().filter(Q(est_bloquer=True))
    
    




class Unite(models.Model):
    
    id=models.CharField(max_length=500,primary_key=True,verbose_name='Code Unité',db_column='code_unite')
    libelle=models.CharField(max_length=500,null=False,verbose_name="Libelle")
    date_ouverture= models.DateField(null=False,verbose_name="Date d'ouverture")
    date_cloture = models.DateField(null=True,blank=True, verbose_name="Date de cloture")
    est_bloquer = models.BooleanField(default=False,editable=False)
    user_id = models.CharField(max_length=500, editable=False)

    date_modification = models.DateTimeField(editable=False, auto_now=True)
    objects = GeneralManager()
    def save(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        self.est_bloquer = True
        super().save(*args, **kwargs)


    def __str__(self):
        return self.id
    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Unités'
        verbose_name_plural = 'Unités'




class Configurations(models.Model):
    
    unite=models.ForeignKey(Unite,null=True,blank=True,verbose_name='Unite',db_column='unite',on_delete=models.DO_NOTHING)
    saisie_automatique=models.BooleanField(default=False, verbose_name="Saisie Automatique")
    port=models.CharField(max_length=500,default='COM1',null=False,verbose_name='Port')
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False, default=get_current_user)
    date_modification = models.DateTimeField(editable=False, auto_now=True)

    def save(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        self.est_bloquer = True
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Configurations'
        verbose_name_plural = 'Configurations'




class Images(models.Model):
    
    src= models.ImageField(upload_to="Images", null=False)
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False, default=get_current_user)
    date_modification = models.DateTimeField(editable=False, auto_now=True)

    objects = GeneralManager()

    def save(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        self.est_bloquer = True
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Images'
        verbose_name_plural = 'Images'



class Clients(models.Model):

    id = models.CharField(db_column='Code_Client', primary_key=True, max_length=500, verbose_name='Code du Client')
    type_client = models.PositiveSmallIntegerField(db_column='Type_Client', blank=True, null=True,
                                                   verbose_name='Type de Client')
    est_client_cosider = models.BooleanField(db_column='Est_Client_Cosider', blank=True, null=False
                                             , verbose_name='Est Client Cosider')
    libelle = models.CharField(db_column='Libelle_Client', max_length=300, null=False,
                               verbose_name='Libelle')

    adresse = models.CharField(db_column='adresse', max_length=500, null=False,
                               verbose_name='Adresse')

    nif = models.CharField(db_column='NIF', unique=True, max_length=50, blank=True, null=True, verbose_name='NIF')
    raison_social = models.CharField(db_column='Raison_Social', max_length=50, blank=True, null=True,
                                     verbose_name='Raison Social')
    num_registre_commerce = models.CharField(db_column='Num_Registre_Commerce', max_length=20, blank=True, null=True,
                                             verbose_name='Numero du registre de commerce')

    sous_client = models.ForeignKey('Clients', on_delete=models.DO_NOTHING, db_column='sous_client',null=True, blank=True,verbose_name='Est client de')

    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False, default=get_current_user)
    date_modification = models.DateTimeField(editable=False, auto_now=True)

    objects = GeneralManager()

    def save(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        self.est_bloquer = True
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Clients'
        verbose_name_plural = 'Clients'

class UniteMesure(models.Model):

    libelle = models.CharField(db_column='libelle', max_length=10, blank=True, null=True)
    description = models.CharField(db_column='description', max_length=50, blank=True, null=True)
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False, default=get_current_user)
    date_modification = models.DateTimeField(editable=False, auto_now=True)

    objects = GeneralManager()

    def save(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        self.est_bloquer = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.libelle
    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Unités de mesure'
        verbose_name_plural = 'Unités de mesure'


class Produits(models.Model):

    id=models.CharField(db_column='code_produits', max_length=500, primary_key=True)
    libelle = models.CharField(db_column='nom_produit', max_length=500, blank=True, null=False, verbose_name='Nom Produit')
    unite = models.ForeignKey(UniteMesure, on_delete=models.DO_NOTHING,null=False,verbose_name='Unite de Mesure')
    famille=models.CharField(db_column='famille', max_length=500,  null=True, verbose_name='Famille')
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False, default=get_current_user)
    date_modification = models.DateTimeField(editable=False, auto_now=True)

    objects = GeneralManager()

    def save(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        self.est_bloquer = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id+' '+self.libelle
    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Produits'
        verbose_name_plural = 'Produits'


class PrixProduit(models.Model):

    id = models.CharField(max_length=500, primary_key=True, verbose_name='ID', db_column='id',editable=False)
    unite = models.ForeignKey(Unite, on_delete=models.DO_NOTHING, db_column='Unité', null=False, verbose_name='Unité')
    produit = models.ForeignKey(Produits, on_delete=models.DO_NOTHING,null=False,verbose_name='Produit')
    prix_unitaire = models.DecimalField(max_digits=38, decimal_places=3,validators=[MinValueValidator(0)],default=0, verbose_name = 'Prix unitaire')
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False, default=get_current_user)
    date_modification = models.DateTimeField(editable=False, auto_now=True)

    objects = GeneralManager()

    def save(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        self.est_bloquer = True
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.unite)+' '+str(self.produit)+' '+str(self.prix_unitaire)
    class Meta:
        unique_together = (('produit', 'prix_unitaire','unite'))
        app_label = 'api_gc'
        verbose_name = 'Prix des Produits'
        verbose_name_plural = 'Prix des Produits'


class Contrat(models.Model):


    id=models.CharField(db_column='code_contrat', max_length=500, primary_key=True,verbose_name = 'Code du contrat')
    libelle=models.CharField(db_column='libelle', max_length=500, blank=True, null=False, verbose_name='libelle')
    tva=models.DecimalField(max_digits=38,decimal_places=3,validators=[MinValueValidator(0),MaxValueValidator(100)],default=0,verbose_name='TVA')
    transport=models.BooleanField(db_column='transport', default=False, verbose_name='Transport')
    rabais=models.DecimalField(max_digits=38,decimal_places=3,validators=[MinValueValidator(0),MaxValueValidator(100)],default=0,verbose_name='Rabais')
    rg = models.DecimalField(max_digits=38, decimal_places=3,
                                 validators=[MinValueValidator(0), MaxValueValidator(100)], default=0,
                                 verbose_name='Retenue de garantie')

    client=models.ForeignKey(Clients, on_delete=models.DO_NOTHING,null=False,verbose_name='Client')
    date_signature=models.DateField(db_column='date_signature', null=False, blank=False, verbose_name='Date de Signature')
    date_expiration=models.DateField(db_column='date_expiration', null=True, verbose_name='Date d\'expiration')
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False, default=get_current_user)
    date_modification = models.DateTimeField(editable=False, auto_now=True)

    objects = GeneralManager()

    def save(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        self.est_bloquer = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id

    @property
    def validite(self):
        delta = relativedelta(self.date_expiration, self.date_signature)
        months = delta.months + (delta.years * 12)
        return months



    @property
    def montant_ht(self):
        try:
            dqes=DQE.objects.filter(contrat=self.id)
            sum=0
            for dqe in dqes:
                sum=sum+dqe.montant_qte
            return sum
        except DQE.DoesNotExist:
            return 0
    @property
    def montant_ttc(self):
        return round(self.montant_ht+(self.montant_ht*self.tva/100),4)
    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Contrats'
        verbose_name_plural = 'Contrats'

class DQE(models.Model):


    id=models.CharField(max_length=500,primary_key=True,verbose_name='id',editable=False)
    contrat=models.ForeignKey(Contrat, on_delete=models.DO_NOTHING,null=True,verbose_name='Contrat')
    prixProduit=models.ForeignKey(PrixProduit, on_delete=models.DO_NOTHING,null=False,verbose_name='Produit')
    qte=models.DecimalField(max_digits=38, decimal_places=3,validators=[MinValueValidator(0)],default=0, verbose_name = 'Quantité')
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False, default=get_current_user)
    date_modification = models.DateTimeField(editable=False, auto_now=True)

    objects = GeneralManager()

    def save(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        self.est_bloquer = True
        super().save(*args, **kwargs)

    @property
    def montant_qte(self):
        return round(self.qte*self.prixProduit.prix_unitaire,4)
    class Meta:
        app_label = 'api_gc'
        verbose_name = 'DQE'
        verbose_name_plural = 'DQE'




class Avances(models.Model):

    contrat = models.ForeignKey(Contrat, on_delete=models.DO_NOTHING, null=False, verbose_name='Contrat')
    num_avance=models.PositiveIntegerField(default=0, null=False, verbose_name='Num avance',editable=False)

    montant_avance = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)], default=0,
                                         verbose_name='Montant de l\'avance')
    montant_restant= models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)], default=0,
                                         verbose_name='Montant restant de l\'avance', editable=False)

    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False, default=get_current_user)
    date_modification = models.DateTimeField(editable=False, auto_now=True)

    objects = GeneralManager()

    def save(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        self.est_bloquer = True
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Avances'
        verbose_name_plural = 'Avances'
        unique_together=(('contrat', 'montant_avance'),)

class Planing(models.Model):

    contrat = models.ForeignKey(Contrat, on_delete=models.DO_NOTHING, null=False, verbose_name='Contrat')
    dqe=models.ForeignKey(DQE, on_delete=models.DO_NOTHING, null=False, verbose_name='dqe')
    date=models.DateField(null=False, verbose_name='Date')
    qte_livre=models.DecimalField(max_digits=38, decimal_places=3,validators=[MinValueValidator(0)],default=0, verbose_name = 'Quantité à livré')

    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False, default=get_current_user)
    date_modification = models.DateTimeField(editable=False, auto_now=True)

    objects = GeneralManager()

    def save(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        self.est_bloquer = True
        super().save(*args, **kwargs)

    @property
    def cumule(self):
        try:
            previous_cumule = Planing.objects.filter(dqe=self.dqe, contrat=self.contrat, date__lt=self.date).aggregate(models.Sum('qte_livre'))[
            "qte_livre__sum"]
            if(previous_cumule):
                return self.qte_livre+previous_cumule
            else:
                return self.qte_livre

        except Planing.DoesNotExist:
                return self.qte_livre

    class Meta:
        unique_together = (('contrat', 'dqe', 'date'),)
        app_label = 'api_gc'
        verbose_name = 'Planing'
        verbose_name_plural = 'Planing'



class Camion(models.Model):

    matricule=models.CharField(max_length=500, primary_key=True, verbose_name='Matricule')
    tare=models.DecimalField(max_digits=38, decimal_places=3,validators=[MinValueValidator(0)],default=0, verbose_name = 'Tare')
    unite = models.ForeignKey(UniteMesure, on_delete=models.DO_NOTHING,null=False,verbose_name='Unite de Mesure')

    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False, default=get_current_user)
    date_modification = models.DateTimeField(editable=False, auto_now=True)

    objects = GeneralManager()

    def save(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        self.est_bloquer = True
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Camions'
        verbose_name_plural = 'Camions'


# mode hors connexion 1 2 3 4 5
class BonLivraison(models.Model):

    id = models.CharField(max_length=500, primary_key=True, null=False, verbose_name='N° BL',
                          editable=False)
    conducteur=models.CharField(max_length=500, null=False, verbose_name='Conducteur')
    camion = models.ForeignKey(Camion, null=False, on_delete=models.DO_NOTHING, verbose_name='Camion')
    numero_permis_c=models.CharField(max_length=500,null=True,verbose_name='N° P.Conduire')
    contrat = models.ForeignKey(Contrat, on_delete=models.DO_NOTHING, null=False, verbose_name='Contrat')
    date=models.DateTimeField(auto_now=True)
    dqe = models.ForeignKey(DQE, on_delete=models.DO_NOTHING, null=False, verbose_name='dqe')
    ptc = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)], default=0,
                                   verbose_name='PTC')

    montant = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)], default=0,
                                  verbose_name='Montant', editable=False)


    qte = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)], default=0,
                                  verbose_name='QTE', editable=False)

    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False, default=get_current_user)
    date_modification = models.DateTimeField(editable=False, auto_now=True)

    objects = GeneralManager()

    def save(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        self.est_bloquer = True
        super().save(*args, **kwargs)

    @property
    def qte_cumule(self):
        previous_cumule = BonLivraison.objects.filter(dqe=self.dqe, contrat=self.contrat, date__lt=self.date)
        sum = self.qte
        if (previous_cumule):
            for pc in previous_cumule:
                sum +=pc.qte
            return sum
        else:
            return self.qte




    @property
    def montant_cumule(self):
        previous_cumule = BonLivraison.objects.filter(dqe=self.dqe, contrat=self.contrat, date__lt=self.date)
        sum = self.montant
        if (previous_cumule):
            for pc in previous_cumule:
                sum += pc.montant
            return sum
        else:
            return self.montant

    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Bon de livraison'
        verbose_name_plural = 'Bon de livraison'







class Factures(models.Model):

    id=models.CharField(max_length=500,primary_key=True,null=False, verbose_name='Numero de facture',editable=False)
    contrat=models.ForeignKey(Contrat, on_delete=models.DO_NOTHING, null=False, verbose_name='Contrat')
    date= models.DateField(auto_now=True, verbose_name='Date')
    du = models.DateField(null=False, verbose_name='Du')
    au = models.DateField(null=False, verbose_name='Au')
    paye = models.BooleanField(default=False, null=False, editable=False)
    montant=  models.DecimalField(max_digits=38, decimal_places=3,validators=[MinValueValidator(0)],default=0, verbose_name = 'Montant',editable=False)
    montant_rb=  models.DecimalField(max_digits=38, decimal_places=3,validators=[MinValueValidator(0)],default=0, verbose_name = 'Montant Rabais',editable=False)
    montant_rg=  models.DecimalField(max_digits=38, decimal_places=3,validators=[MinValueValidator(0)],default=0, verbose_name = 'Montant RG',editable=False)
    montant_facture_ht=models.DecimalField(max_digits=38, decimal_places=3,validators=[MinValueValidator(0)],default=0, verbose_name = 'Montant Facture (en HT)',editable=False)
    montant_facture_ttc=models.DecimalField(max_digits=38, decimal_places=3,validators=[MinValueValidator(0)],default=0, verbose_name = 'Montant Facture (en TTC)',editable=False)

    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False, default=get_current_user)
    date_modification = models.DateTimeField(editable=False, auto_now=True)

    objects = GeneralManager()

    def save(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        self.est_bloquer = True
        super().save(*args, **kwargs)

    @property
    def montant_cumule(self):
        try:
            details = DetailFacture.objects.filter(facture=self.id,facture__date__lte=self.date)
            montant_cumule = 0
            for detail in details:
                montant_cumule = montant_cumule + detail.detail.montant
            return montant_cumule
        except DetailFacture.DoesNotExist:
            return 0


    def __str__(self):
        return self.id

    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Factures'
        verbose_name_plural = 'Factures'




class DetailFacture(models.Model):

    facture = models.ForeignKey(Factures,null=True, on_delete=models.DO_NOTHING,to_field="id")
    detail = models.ForeignKey(BonLivraison, on_delete=models.DO_NOTHING)
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False, default=get_current_user)
    date_modification = models.DateTimeField(editable=False, auto_now=True)

    objects = GeneralManager()

    def save(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        self.est_bloquer = True
        super().save(*args, **kwargs)

    class Meta:
        unique_together = (('facture', 'detail',))
        app_label = 'api_gc'

        verbose_name = 'Details'
        verbose_name_plural = 'Details'

class ModePaiement(models.Model):
    libelle = models.CharField(max_length=500, null=False, unique=True)
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False, default=get_current_user)
    date_modification = models.DateTimeField(editable=False, auto_now=True)
    objects = GeneralManager()

    def save(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        self.est_bloquer = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.libelle
    class Meta:
        app_label = 'api_gc'

        verbose_name = 'Mode de Paiement'
        verbose_name_plural = 'Mode de Paiement'


class Encaissement(models.Model):

    facture = models.ForeignKey(Factures, on_delete=models.DO_NOTHING, null=False, verbose_name="Facture")
    date_encaissement = models.DateField(null=False, verbose_name="Date d'encaissement")
    avance= models.ForeignKey(Avances, on_delete=models.DO_NOTHING, null=True, verbose_name="Avance")
    mode_paiement = models.ForeignKey(ModePaiement, on_delete=models.DO_NOTHING, null=False,
                                      verbose_name="Mode de paiement")
    montant_encaisse = models.DecimalField(max_digits=38, decimal_places=3, blank=True, verbose_name="Montant encaissé",
                                           validators=[MinValueValidator(0)], default=0)
    numero_piece = models.CharField(max_length=300, null=False, verbose_name="Numero de piéce")

    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False, default=get_current_user)
    date_modification = models.DateTimeField(editable=False, auto_now=True)

    objects = GeneralManager()

    def save(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user and hasattr(current_user, 'username'):
                self.user_id = current_user.username
        self.est_bloquer = True
        super().save(*args, **kwargs)

    @property
    def montant_creance(self):
        try:
            enc = Encaissement.objects.filter(facture=self.facture, date_encaissement__lt=self.date_encaissement).aggregate(models.Sum('montant_encaisse'))[
            "montant_encaisse__sum"]

            if(enc==None):
                enc=self.montant_encaisse
            else:
                enc+=self.montant_encaisse

            return (self.facture.montant_facture_ttc-enc)
        except Encaissement.DoesNotExist:
            return 0
    class Meta:
        unique_together = (("facture", "date_encaissement"),)
        app_label = 'api_gc'
        verbose_name = 'Encaissements'
        verbose_name_plural = 'Encaissements'











