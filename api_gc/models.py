import uuid
from dateutil.relativedelta import relativedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_currentuser.middleware import get_current_user
from django.db.models import Q, F, IntegerField, Sum
# Create your models here.
class GeneralManager(models.Manager):

    def get_queryset(self):
        if(self.model in  [Contrat,Clients,Camion,UniteMesure,DetailFacture,ModePaiement,Tva]):
            return super().get_queryset().filter(~Q(est_bloquer=True))
        else:
            unite = Config.objects.first().unite.id

            if( unite == 'F00'): # F00
                return super().get_queryset().filter(~Q(est_bloquer=True))
            else:
                return super().get_queryset().filter(~Q(est_bloquer=True) & Q(pk__contains=unite))

    def deleted(self):

        if (self.model in [Contrat,Clients,Camion,UniteMesure,DetailFacture,ModePaiement,Tva]):
            return super().get_queryset().filter(Q(est_bloquer=True))
        else:
            unite = Config.objects.first().unite.id

            if( unite == 'F00'): # F00
                return super().get_queryset().filter(Q(est_bloquer=True))
            else:
                return super().get_queryset().filter(Q(est_bloquer=True)& Q(pk__contains=unite))

    def all_with_deleted(self):
        unite = Config.objects.first().unite.id
        if (unite == 'F00'):  # F00
            return super().get_queryset().all()
        else:
            return super().get_queryset().filter(Q(pk__contains=unite))


class Tva(models.Model):
    id=models.DecimalField(primary_key=True,max_digits=38,decimal_places=3,validators=[MinValueValidator(0),MaxValueValidator(100)],default=0,verbose_name='TVA')
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False)
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

    def __str__(self):
        return str(self.id)+'%'
    class Meta:
        app_label = 'api_gc'
        verbose_name = 'TVA'
        verbose_name_plural = 'TVA'
        db_table = 'TVA'


class Unite(models.Model):
    
    id=models.CharField(max_length=500,primary_key=True,verbose_name='Code Unité',db_column='code_unite')
    libelle=models.CharField(max_length=500,null=False,verbose_name="Libelle")
    ai=models.CharField(max_length=500,null=True)
    adresse=models.CharField(max_length=500,null=True)
    contact=models.CharField(max_length=500, null=True)
    date_ouverture= models.DateField(null=False,verbose_name="Date d'ouverture")
    date_cloture = models.DateField(null=True,blank=True, verbose_name="Date de cloture")
    est_bloquer = models.BooleanField(default=False,editable=False)
    user_id = models.CharField(max_length=500, editable=False)
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


    def __str__(self):
        return self.id
    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Unités'
        verbose_name_plural = 'Unités'
        db_table = 'Unite'


class Config(models.Model):
    unite=models.ForeignKey(Unite,null=True,blank=True,verbose_name='Unite',db_column='unite',on_delete=models.DO_NOTHING)
    saisie_automatique=models.BooleanField(default=False, verbose_name="Saisie Automatique")
    port=models.CharField(max_length=500,default='COM1',null=False,verbose_name='Port')
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False)
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
        verbose_name = 'Config'
        verbose_name_plural = 'Config'
        db_table='Config'




class Images(models.Model):
    src= models.ImageField(upload_to="Images", null=False)
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False)
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
        verbose_name = 'Images'
        verbose_name_plural = 'Images'
        db_table = 'Images'


class TypeClient(models.Model):
    id=models.CharField(max_length=300,primary_key=True)
    libelle= models.CharField(max_length=500,null=False)
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False)
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


    def __str__(self):
        return self.libelle


    class Meta:
        app_label = 'api_gc'
        verbose_name = 'TypeClient'
        verbose_name_plural = 'TypeClient'
        db_table = 'Type_Client'


class Activite(models.Model):
    id=models.CharField(max_length=300,primary_key=True)
    libelle= models.CharField(max_length=500,null=False)
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False)
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

    def __str__(self):
        return self.libelle
    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Activite'
        verbose_name_plural = 'Activite'
        db_table = 'Activite'


class Clients(models.Model):

    id = models.CharField(db_column='Code_Client', primary_key=True, max_length=500, verbose_name='Code du Client')

    libelle = models.CharField(db_column='Libelle_Client', max_length=300, null=False,
                               verbose_name='Libelle')

    adresse = models.CharField(db_column='adresse', max_length=500, null=False,
                               verbose_name='Adresse')
    ville= models.CharField(db_column='ville', max_length=500, null=False,default='',
                               verbose_name='Ville')

    nif = models.CharField(db_column='NIF', unique=True, max_length=50, blank=True, null=True, verbose_name='NIF')
    raison_social = models.CharField(db_column='Raison_Social', max_length=50, blank=True, null=True,
                                     verbose_name='Raison Sociale')
    num_registre_commerce = models.CharField(db_column='Num_Registre_Commerce', max_length=20, blank=True, null=True,
                                             verbose_name='Numero du registre de commerce')

    type= models.ForeignKey(TypeClient,on_delete=models.DO_NOTHING,null=True, verbose_name='Type')
    act=models.ForeignKey(Activite,on_delete=models.DO_NOTHING,null=True, verbose_name='Activite')

    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False)
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
        verbose_name = 'Clients'
        verbose_name_plural = 'Clients'
        db_table = 'Clients'

class UniteMesure(models.Model):
    id=models.CharField(max_length=10, primary_key=True)
    libelle = models.CharField(db_column='libelle', max_length=10, blank=True, null=True)
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False)
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

    def __str__(self):
        return self.libelle
    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Unités de mesure'
        verbose_name_plural = 'Unités de mesure'
        db_table = 'Unite_De_Mesure'

class Produits(models.Model):
    id=models.CharField(db_column='ref', max_length=500, primary_key=True)
    libelle = models.CharField(db_column='libelle', max_length=500, blank=True, null=False, verbose_name='Nom Produit')
    unite_m = models.ForeignKey(UniteMesure, on_delete=models.DO_NOTHING,null=False,verbose_name='Unite de Mesure')
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False)
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

    def __str__(self):
        return self.id
    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Produits'
        verbose_name_plural = 'Produits'
        db_table='Produit'

class TypePrix(models.Model):
    id=models.CharField(primary_key=True,max_length=10)
    libelle=models.CharField(max_length=500)
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False)
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

    def __str__(self):
        return self.id
    class Meta:
        app_label = 'api_gc'
        verbose_name = 'TypePrix'
        verbose_name_plural = 'TypePrix'
        db_table='Type_Prix'

class PrixProduit(models.Model):

    id = models.CharField(max_length=900,primary_key=True,  editable=False)
    u=models.ForeignKey(Unite, on_delete=models.DO_NOTHING,null=False,verbose_name='unite' )
    produit = models.ForeignKey(Produits, on_delete=models.DO_NOTHING,null=False,verbose_name='Produit')
    prix_unitaire = models.DecimalField(max_digits=38, decimal_places=3,validators=[MinValueValidator(0)],default=0, verbose_name = 'Prix unitaire')
    type_prix = models.ForeignKey(TypePrix, on_delete=models.DO_NOTHING, null=False, verbose_name='TypePrix')
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False)
    date_modification = models.DateTimeField(editable=False, auto_now=True)

    @property
    def unite(self):
        return self.id.split('|')[0]
    
    @property
    def index_prix(self):
        return self.id.split('|')[2]

    def save(self, *args, **kwargs):
        unite = Config.objects.first().unite
        count=PrixProduit.objects.filter(id__startswith=str(unite.id) + '|' + str(self.produit)).count()+1

        if(unite.id != 'F00'):
            self.u=unite
        self.id =f'{unite.id}|{self.produit}|{count}'




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
        unique_together = (('produit','u', 'prix_unitaire','type_prix','id'))
        app_label = 'api_gc'
        verbose_name = 'Prix des Produits'
        verbose_name_plural = 'Prix des Produits'
        db_table='Prix_Produit'

class Contrat(models.Model):
    id = models.CharField(max_length=900,primary_key=True,editable=False)
    numero=models.CharField(db_column='code_contrat', max_length=500,verbose_name = 'N° du contrat')
    avenant=models.PositiveIntegerField(default=0, verbose_name = 'Avenant N°')
    libelle=models.CharField(db_column='libelle', max_length=500, blank=True, null=False, verbose_name='libelle')
    tva=models.ForeignKey(Tva,null=True,on_delete=models.DO_NOTHING,verbose_name='TVA')
    transport=models.BooleanField(db_column='transport', default=False, verbose_name='Transport')
    rabais=models.DecimalField(max_digits=38,decimal_places=3,validators=[MinValueValidator(0)],default=0,verbose_name='Rabais Sur Tout')
    rg = models.DecimalField(max_digits=38, decimal_places=3,
                                 validators=[MinValueValidator(0)], default=0,
                                 verbose_name='Retenue de garantie')

    client=models.ForeignKey(Clients, on_delete=models.DO_NOTHING,null=False,verbose_name='Client')
    date_signature=models.DateField(db_column='date_signature', null=False, blank=False, verbose_name='Date de Signature')
    date_expiration=models.DateField(db_column='date_expiration', null=True, verbose_name='Date d\'expiration')
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False)
    date_modification = models.DateTimeField(editable=False, auto_now=True)

    

    def save(self, *args, **kwargs):
        self.id=self.numero+'('+str(self.avenant)+')'
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
        if(self.avenant > 0):
            return self.numero+'/'+str(self.avenant)
        else:
            return self.numero

    @property
    def validite(self):
        delta = relativedelta(self.date_expiration, self.date_signature)
        months = delta.months + (delta.years * 12)
        return months



    @property
    def montant_ht(self):
        if(self.avenant==0):
            try:
                dqes=DQE.objects.filter(contrat=self.id)
                sum=0
                for dqe in dqes:
                    sum=sum+dqe.montant_qte
                return sum
            except DQE.DoesNotExist:
                return 0
        else:
            try:
                dqes=DQE.objects.filter(contrat__avenant__lte=self.avenant)
                sum=0
                for dqe in dqes:
                    sum=sum+dqe.montant_qte
                return sum
            except DQE.DoesNotExist:
                return 0

    @property
    def montant_ttc(self):
        return round(self.montant_ht+(self.montant_ht*self.tva.id/100),4)
    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Contrats'
        verbose_name_plural = 'Contrats'
        db_table = 'Contrats'


class Contrat_Latest(models.Model):
    id = models.CharField(max_length=900, primary_key=True, editable=False)
    numero = models.CharField(db_column='code_contrat', max_length=500, verbose_name='N° du contrat')
    avenant = models.PositiveIntegerField(default=0, verbose_name='Avenant N°')
    libelle = models.CharField(db_column='libelle', max_length=500, blank=True, null=False, verbose_name='libelle')
    tva = models.ForeignKey(Tva,db_constraint=False, null=True, on_delete=models.DO_NOTHING, verbose_name='TVA')
    transport = models.BooleanField(db_column='transport', default=False, verbose_name='Transport')
    rabais = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)], default=0,
                                 verbose_name='Rabais Sur Tout')
    rg = models.DecimalField(max_digits=38, decimal_places=3,
                             validators=[MinValueValidator(0)], default=0,
                             verbose_name='Retenue de garantie')

    client = models.ForeignKey(Clients,db_constraint=False, on_delete=models.DO_NOTHING, null=False, verbose_name='Client')
    date_signature = models.DateField(db_column='date_signature', null=False, blank=False,
                                      verbose_name='Date de Signature')
    date_expiration = models.DateField(db_column='date_expiration', null=True, verbose_name='Date d\'expiration')
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False)
    date_modification = models.DateTimeField(editable=False, auto_now=True)

    

    def save(self, *args, **kwargs):
        self.id = self.numero + '(' + str(self.avenant) + ')'
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
        if (self.avenant > 0):
            return self.numero + '/' + str(self.avenant)
        else:
            return self.numero

    @property
    def validite(self):
        delta = relativedelta(self.date_expiration, self.date_signature)
        months = delta.months + (delta.years * 12)
        return months

    @property
    def montant_ht(self):
        try:
            dqes = DQECumule.objects.filter(code_contrat=self.numero)
            sum = 0
            for dqe in dqes:
                sum = sum + dqe.montant_qte
            return sum
        except DQE.DoesNotExist:
            return 0

    @property
    def montant_ttc(self):
        return round(self.montant_ht + (self.montant_ht * self.tva.id / 100), 4)

    class Meta:
        managed=False
        app_label = 'api_gc'
        verbose_name = 'Contrats'
        verbose_name_plural = 'Contrats'
        db_table = 'Contrats_View'




class DQECumule(models.Model):

    id = models.CharField(max_length=900, null=False,primary_key=True)
    produit_id = models.ForeignKey(Produits,db_column='produit_id',on_delete=models.DO_NOTHING,db_constraint=False,null=False)
    code_contrat = models.CharField(max_length=500)
    qte = models.DecimalField(db_column='Qte', max_digits=38, decimal_places=3, blank=True,
                                  null=True)  
    avenant = models.IntegerField(blank=True, null=True)
    contrat_id = models.CharField(max_length=900, blank=True, null=True)
    prixproduit_id = models.ForeignKey(PrixProduit,db_column='prixProduit_id',on_delete=models.DO_NOTHING,db_constraint=False,null=False)
    rabais = models.DecimalField(max_digits=38, decimal_places=3, blank=True, null=True)
    prix_transport = models.DecimalField(max_digits=38, decimal_places=3, blank=True, null=True)
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False)
    date_modification = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        managed = False
        db_table = 'DQE_View_Cumule'

    @property
    def montant_qte(self):
        return round(self.qte*self.prixproduit_id.prix_unitaire,4)






class DQE(models.Model):

    id=models.CharField(max_length=900,primary_key=True,  editable=False)
    contrat=models.ForeignKey(Contrat_Latest,db_constraint=False,on_delete=models.DO_NOTHING,null=True,verbose_name='Contrat')
    prixProduit=models.ForeignKey(PrixProduit, on_delete=models.DO_NOTHING,null=False,verbose_name='Produit')
    qte = models.DecimalField(max_digits=38, decimal_places=3,default=0,verbose_name='Quantité')

    rabais = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)], default=0,
                                 verbose_name='Rabais Par Produit')
    prix_transport = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)], default=0,
                              verbose_name='Tarif de Transport')
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False)
    date_modification = models.DateTimeField(editable=False, auto_now=True)

    objects = GeneralManager()

    def save(self, *args, **kwargs):
        config = Config.objects.first()
        count= DQE.objects.all_with_deleted().all().count()
        if not self.pk:
            self.id=config.unite.id+f'({count})'
        
        if(self.contrat.transport != True):
            self.prix_transport = 0
        
        if(self.contrat.rabais):
            self.rabais =self.contrat.rabais

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

    @property
    def montant_qte_t(self): # prop prix_prod * qte + transport
        return round(self.montant_qte+self.prix_transport, 4)




    class Meta:
        unique_together=(('contrat','prixProduit'))
        app_label = 'api_gc'
        verbose_name = 'DQE'
        verbose_name_plural = 'DQE'
        db_table = 'DQE'



class Avances(models.Model):

    contrat = models.ForeignKey(Contrat_Latest,db_constraint=False ,on_delete=models.DO_NOTHING, null=False, verbose_name='Contrat')
    num_avance=models.PositiveIntegerField(default=0, null=False, verbose_name='Num avance',editable=False)

    montant_avance = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)], default=0,
                                         verbose_name='Montant de l\'avance')

    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False)
    date_modification = models.DateTimeField(editable=False, auto_now=True)

    @property
    def montant_cumule(self):
        previous_cumule = Avances.objects.filter(contrat=self.contrat,date_modification__lt=self.date_modification)
        sum = self.montant_avance
        if (previous_cumule):
            for pc in previous_cumule:
                sum += pc.montant_avance
            return sum
        else:
            return self.montant_avance

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
        db_table='Avances'
class Planing(models.Model):
    contrat = models.ForeignKey(Contrat_Latest,db_constraint=False, on_delete=models.DO_NOTHING, null=False, verbose_name='Contrat')
    dqe=models.ForeignKey('DQECumule',db_constraint=False, on_delete=models.DO_NOTHING, null=False, verbose_name='dqe')
    date=models.DateField(null=False, verbose_name='Date')
    qte_livre=models.DecimalField(max_digits=38, decimal_places=3,validators=[MinValueValidator(0)],default=0, verbose_name = 'Quantité à livré')

    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False)
    date_modification = models.DateTimeField(editable=False, auto_now=True)
    
    @property
    def qte_realise(self):
        qr = BonLivraison.objects.filter(dqe=self.dqe, contrat=self.contrat, date__month=self.date.month , date__year=self.date.year
                                         ).aggregate(models.Sum('qte'))[
            "qte__sum"] or 0
        return qr
            


        return(f'{mm}-{aa}')    

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
        db_table = 'Planing'


class Camion(models.Model):
    matricule=models.CharField(max_length=500, primary_key=True, verbose_name='Matricule')
    tare=models.DecimalField(max_digits=38, decimal_places=3,validators=[MinValueValidator(0)],default=0, verbose_name = 'Tare')
    unite = models.ForeignKey(UniteMesure, on_delete=models.DO_NOTHING,null=False,verbose_name='Unite de Mesure')
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False)
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
        verbose_name = 'Camions'
        verbose_name_plural = 'Camions'
        db_table = 'Camions'

# mode hors connexion
class BonLivraison(models.Model):
    id = models.CharField(max_length=500, primary_key=True, null=False, verbose_name='N° BL',
                          editable=False)
    conducteur=models.CharField(max_length=500, null=False, verbose_name='Conducteur')
    camion = models.ForeignKey(Camion, null=False, on_delete=models.DO_NOTHING, verbose_name='Camion')
    numero_permis_c=models.CharField(max_length=500,null=True,verbose_name='N° P.Conduire')
    contrat = models.ForeignKey(Contrat_Latest,db_constraint=False, on_delete=models.DO_NOTHING, null=False, verbose_name='Contrat')
    date=models.DateTimeField(auto_now=True)
    dqe = models.ForeignKey('DQECumule', on_delete=models.DO_NOTHING,db_constraint=False, null=False, verbose_name='dqe')
    ptc = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)], default=0,
                                   verbose_name='PTC')

    montant = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)], default=0,
                                  verbose_name='Montant', editable=False)


    qte = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)], default=0,
                                  verbose_name='QTE', editable=False)

    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False)
    date_modification = models.DateTimeField(editable=False, auto_now=True)

    objects = GeneralManager()

    def save(self, *args,num_bl=2, **kwargs):
        config = Config.objects.first()

        self.id = str(config.unite) + '_' + str(num_bl)

        self.qte = self.ptc - self.camion.tare
        self.montant = round((self.qte * self.dqe.prixproduit_id.prix_unitaire)-self.dqe.rabais, 4)
        # verifier si on ajoute le cout du transport  lors de la creation du bon de livraison
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
        db_table = 'Bon_De_Livraison'






class Factures(models.Model):

    id=models.CharField(max_length=500,primary_key=True,null=False, verbose_name='Numero de facture',editable=False)
    contrat=models.ForeignKey(Contrat_Latest,db_constraint=False, on_delete=models.DO_NOTHING, null=False, verbose_name='Contrat')
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
    user_id = models.CharField(max_length=500, editable=False)
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
        DetailFacture.objects.filter(facture=self).delete()
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
        db_table = 'Factures'



class DetailFacture(models.Model):

    facture = models.ForeignKey(Factures,null=True, on_delete=models.DO_NOTHING,to_field="id")
    detail = models.ForeignKey(BonLivraison, on_delete=models.DO_NOTHING)
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False)
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
        unique_together = (('facture', 'detail',))
        app_label = 'api_gc'
        verbose_name = 'Details'
        verbose_name_plural = 'Details'
        db_table = 'Details'

class ModePaiement(models.Model):
    id=models.CharField(max_length=30, primary_key=True)
    libelle = models.CharField(max_length=500, null=False, unique=True)
    est_bloquer = models.BooleanField(default=False, editable=False)
    user_id = models.CharField(max_length=500, editable=False)
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

    def __str__(self):
        return self.libelle
    class Meta:
        app_label = 'api_gc'

        verbose_name = 'Mode de Paiement'
        verbose_name_plural = 'Mode de Paiement'
        db_table = 'Mode_De_Paiement'

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
    user_id = models.CharField(max_length=500, editable=False)
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
        db_table = 'Encaissements'


