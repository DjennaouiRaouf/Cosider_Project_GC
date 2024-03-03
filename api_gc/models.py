from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from safedelete import SOFT_DELETE_CASCADE, DELETED_VISIBLE_BY_PK, SOFT_DELETE, HARD_DELETE
from safedelete.managers import SafeDeleteManager
from safedelete.models import SafeDeleteModel
from simple_history.models import HistoricalRecords


# Create your models here.

class DeletedModelManager(SafeDeleteManager):
    _safedelete_visibility = DELETED_VISIBLE_BY_PK

class Unite(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    id=models.CharField(max_length=500,primary_key=True,verbose_name='Code Unité',db_column='code_unite')
    libelle=models.CharField(max_length=500,null=False,verbose_name="Libelle")
    date_ouverture= models.DateField(null=False,verbose_name="Date d'ouverture")
    date_cloture = models.DateField(null=True,blank=True, verbose_name="Date de cloture")

    historique = HistoricalRecords()
    objects = DeletedModelManager()

    def __str__(self):
        return self.id
    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Unités'
        verbose_name_plural = 'Unités'

class Parametres(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    saisie_automatique=models.BooleanField(default=False, verbose_name="Saisie Automatique")
    port=models.CharField(max_length=500,default='COM1',null=False,verbose_name='Port')
    historique = HistoricalRecords()
    objects = DeletedModelManager()

    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Parametres'
        verbose_name_plural = 'Parametres'



class Clients(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    id = models.CharField(db_column='Code_Client', primary_key=True, max_length=500, verbose_name='Code du Client')
    type_client = models.PositiveSmallIntegerField(db_column='Type_Client', blank=True, null=True,
                                                   verbose_name='Type de Client')
    est_client_cosider = models.BooleanField(db_column='Est_Client_Cosider', blank=True, null=False
                                             , verbose_name='Est Client Cosider')
    libelle = models.CharField(db_column='Libelle_Client', max_length=300, blank=True, null=True,
                               verbose_name='Libelle')

    adresse = models.CharField(db_column='adresse', max_length=500, null=True,
                               verbose_name='Adresse')

    nif = models.CharField(db_column='NIF', unique=True, max_length=50, blank=True, null=True, verbose_name='NIF')
    raison_social = models.CharField(db_column='Raison_Social', max_length=50, blank=True, null=True,
                                     verbose_name='Raison Social')
    num_registre_commerce = models.CharField(db_column='Num_Registre_Commerce', max_length=20, blank=True, null=True,
                                             verbose_name='Numero du registre de commerce')

    sous_client = models.ForeignKey('Clients', on_delete=models.DO_NOTHING, db_column='sous_client',null=True, blank=True,verbose_name='Est client de')

    historique = HistoricalRecords()
    objects = DeletedModelManager()

    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Clients'
        verbose_name_plural = 'Clients'

class UniteMesure(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    libelle = models.CharField(db_column='libelle', max_length=10, blank=True, null=True)
    description = models.CharField(db_column='description', max_length=50, blank=True, null=True)
    historique = HistoricalRecords()
    objects = DeletedModelManager()

    def __str__(self):
        return self.libelle
    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Unités de mesure'
        verbose_name_plural = 'Unités de mesure'


class Produits(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    id=models.CharField(db_column='code_produits', max_length=500, primary_key=True)
    libelle = models.CharField(db_column='nom_produit', max_length=500, blank=True, null=False, verbose_name='Nom Produit')
    unite = models.ForeignKey(UniteMesure, on_delete=models.DO_NOTHING,null=False,verbose_name='Unite de Mesure')
    famille=models.CharField(db_column='famille', max_length=500,  null=True, verbose_name='Famille')
    historique = HistoricalRecords()
    objects = DeletedModelManager()

    def __str__(self):
        return self.id+' '+self.libelle
    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Produits'
        verbose_name_plural = 'Produits'


class PrixProduit(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    unite = models.ForeignKey(Unite, on_delete=models.DO_NOTHING, db_column='Unité', null=False, verbose_name='Unité')
    produit = models.ForeignKey(Produits, on_delete=models.DO_NOTHING,null=False,verbose_name='Produit')
    prix_unitaire = models.DecimalField(max_digits=38, decimal_places=3,validators=[MinValueValidator(0)],default=0, verbose_name = 'Prix unitaire')
    historique = HistoricalRecords()
    objects = DeletedModelManager()

    def __str__(self):
        return str(self.unite)+' '+str(self.produit)+' '+str(self.prix_unitaire)
    class Meta:
        unique_together = (('produit', 'prix_unitaire','unite'))
        app_label = 'api_gc'
        verbose_name = 'Prix des Produits'
        verbose_name_plural = 'Prix des Produits'


class Contrat(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    id=models.CharField(db_column='code_contrat', max_length=500, primary_key=True)
    libelle=models.CharField(db_column='libelle', max_length=500, blank=True, null=False, verbose_name='')
    tva=models.DecimalField(max_digits=38,decimal_places=3,validators=[MinValueValidator(0),MaxValueValidator(100)],default=0,verbose_name='TVA')
    transport=models.BooleanField(db_column='transport', default=False, verbose_name='Transport')
    rabais=models.DecimalField(max_digits=38,decimal_places=3,validators=[MinValueValidator(0),MaxValueValidator(100)],default=0,verbose_name='Rabais')
    rg = models.DecimalField(max_digits=38, decimal_places=3,
                                 validators=[MinValueValidator(0), MaxValueValidator(100)], default=0,
                                 verbose_name='Rabais')

    montant_ht=models.DecimalField(max_digits=38, decimal_places=3,validators=[MinValueValidator(0)],default=0, verbose_name = 'Montant en (HT)',editable=False)
    montant_ttc=models.DecimalField(max_digits=38, decimal_places=3,validators=[MinValueValidator(0)],default=0, verbose_name = 'Montant en (TTC)',editable=False)
    client=models.ForeignKey(Clients, on_delete=models.DO_NOTHING,null=False,verbose_name='Client')
    date_signature=models.DateField(db_column='date_signature', null=False, blank=False, verbose_name='Date de Signature')
    date_expiration=models.DateField(db_column='date_expiration', null=True, verbose_name='Date d\'expiration')
    validite=models.PositiveIntegerField(default=0, verbose_name='Durée de validité (en Mois)', null=False, blank=False,editable=False)
    historique = HistoricalRecords()
    objects = DeletedModelManager()

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Contrats'
        verbose_name_plural = 'Contrats'



class DQE(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    id=models.CharField(max_length=500,primary_key=True,verbose_name='id',editable=False)
    contrat=models.ForeignKey(Contrat, on_delete=models.DO_NOTHING,null=True,verbose_name='Contrat')
    prixPrduit=models.ForeignKey(PrixProduit, on_delete=models.DO_NOTHING,null=False,verbose_name='Produit')
    qte=models.DecimalField(max_digits=38, decimal_places=3,validators=[MinValueValidator(0)],default=0, verbose_name = 'Quantité')
    montant_qte=models.DecimalField(max_digits=38, decimal_places=3,validators=[MinValueValidator(0)],default=0, verbose_name = 'Montant de la quantité',editable=False)
    historique = HistoricalRecords()
    objects = DeletedModelManager()
    class Meta:
        app_label = 'api_gc'
        verbose_name = 'DQE'
        verbose_name_plural = 'DQE'

class ODS(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    Types=[
        ('Interruption','Interruption',),('Reprise','Reprise')
    ]
    contrat = models.ForeignKey(Contrat, on_delete=models.DO_NOTHING, null=False, verbose_name='Contrat')
    type=models.CharField(max_length=500, choices=Types, verbose_name='Type d\'Ordre de Service',null=False)
    date=models.DateField(null=False,verbose_name='Date d\'Ordre de Service')
    motif=models.TextField(null=True, verbose_name='Motif')
    historique = HistoricalRecords()
    objects = DeletedModelManager()

    class Meta:
        unique_together = (('contrat', 'type', 'date'),)
        app_label = 'api_gc'
        verbose_name = 'ODS'
        verbose_name_plural = 'ODS'


class Avances(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    contrat = models.ForeignKey(Contrat, on_delete=models.DO_NOTHING, null=False, verbose_name='Contrat')
    montant_avance = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)], default=0,
                                         verbose_name='Montant de l\'avance')
    remboursee = models.BooleanField(editable=False, default=False, null=False, verbose_name='Est remboursée')
    historique = HistoricalRecords()
    objects = DeletedModelManager()
    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Avances'
        verbose_name_plural = 'Avances'


class Planing(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    contrat = models.ForeignKey(Contrat, on_delete=models.DO_NOTHING, null=False, verbose_name='Contrat')
    dqe=models.ForeignKey(DQE, on_delete=models.DO_NOTHING, null=False, verbose_name='dqe')
    date=models.DateField(null=False, verbose_name='Date')
    qte_livre=models.DecimalField(max_digits=38, decimal_places=3,validators=[MinValueValidator(0)],default=0, verbose_name = 'Quantité à livré')
    qte_cumule = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)], default=0,editable=False,
                                    verbose_name='Quantité à livré cumulée')

    historique = HistoricalRecords()
    objects = DeletedModelManager()


    class Meta:
        unique_together = (('contrat', 'dqe', 'date'),)
        app_label = 'api_gc'
        verbose_name = 'Planing'
        verbose_name_plural = 'Planing'



class Camion(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    matricule=models.CharField(max_length=500, primary_key=True, verbose_name='Matricule')
    poids=models.DecimalField(max_digits=38, decimal_places=3,validators=[MinValueValidator(0)],default=0, verbose_name = 'Poids net du camion')
    historique = HistoricalRecords()
    objects = DeletedModelManager()
    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Camions'
        verbose_name_plural = 'Camions'

class Conducteur(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    nom=models.CharField(max_length=500,null=False, verbose_name='Nom')
    prenom = models.CharField(max_length=500, null=False, verbose_name='Prénom')
    num_id=models.CharField(max_length=500,null=False,verbose_name='Numero d\'identification')
    historique = HistoricalRecords()
    objects = DeletedModelManager()
    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Conducteur'
        verbose_name_plural = 'Conducteur'


class Conduire(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    conducteur=models.ForeignKey(Conducteur,null=False, on_delete=models.DO_NOTHING, verbose_name='Conducteur')
    camion=models.ForeignKey(Camion,null=False, on_delete=models.DO_NOTHING, verbose_name='Camion')
    date=models.DateField(null=False, verbose_name='Date')
    historique = HistoricalRecords()
    objects = DeletedModelManager()
    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Conduire'
        verbose_name_plural = 'Conduire'


# mode hors connexion
class BonLivraison(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    contrat = models.ForeignKey(Contrat, on_delete=models.DO_NOTHING, null=False, verbose_name='Contrat')
    dqe = models.ForeignKey(DQE, on_delete=models.DO_NOTHING, null=False, verbose_name='dqe')

    qte_precedent = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)], default=0,
                                     verbose_name='Quantité precedent',editable=False)

    qte_mois = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)], default=0,
                                    verbose_name='Quantité à livré')
    qte_cumule=models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)], default=0,
                                    verbose_name='Quantité cumulé',editable=False)

    montant_precedent = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)],
                                            default=0,
                                            editable=False, verbose_name='Montant précedent')
    montant_mois = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)], default=0,
                                       verbose_name='Montant du Mois', editable=False)
    montant_cumule = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)], default=0,
                                         editable=False, verbose_name='Montant cumulé')


    date=models.DateField(auto_now=True)
    historique = HistoricalRecords()
    objects = DeletedModelManager()

    # verifier ods
    class Meta:
        unique_together = (('contrat','dqe','date'))
        app_label = 'api_gc'
        verbose_name = 'Bon de livraison'
        verbose_name_plural = 'Bon de livraison'





class Factures(SafeDeleteModel):
    numero_facture=models.PositiveIntegerField(primary_key=True,null=False, verbose_name='Numero de facture')
    numero_situtation=models.PositiveIntegerField(null=False, verbose_name='Numero de situation',editable='')
    contrat=models.ForeignKey(Contrat, on_delete=models.DO_NOTHING, null=False, verbose_name='Contrat')
    du = models.DateField(null=False, verbose_name='Du')
    au = models.DateField(null=False, verbose_name='Au')
    paye = models.BooleanField(default=False, null=False, editable=False)
    montant_precedent = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)],
                                            default=0,
                                            verbose_name="Montant Precedent"
                                            , editable=False)
    montant_mois = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)], default=0,
                                       verbose_name="Montant du Mois"
                                       , editable=False)
    montant_cumule = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)], default=0,
                                         verbose_name="Montant Cumulé"
                                         , editable=False)

    montant_rb = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)], default=0,
                                     verbose_name="Montant du rabais"
                                     , editable=False)

    montant_rg = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)], default=0,
                                     verbose_name="Montant Retenue de garantie"
                                     , editable=False)

    montant_factureHT = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)],
                                            default=0,
                                            verbose_name="Montant de la facture en HT"
                                            , editable=False)

    montant_factureTTC = models.DecimalField(max_digits=38, decimal_places=3, validators=[MinValueValidator(0)],
                                             default=0,
                                             verbose_name="Montant de la facture en TTC"
                                             , editable=False)

    historique = HistoricalRecords()
    objects = DeletedModelManager()
    class Meta:
        app_label = 'api_gc'
        verbose_name = 'Factures'
        verbose_name_plural = 'Factures'




class DetailFacture(SafeDeleteModel):
    facture = models.ForeignKey(Factures, on_delete=models.DO_NOTHING,to_field="numero_facture")
    detail = models.ForeignKey(BonLivraison, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = (('facture', 'detail',))
        app_label = 'api_gc'

        verbose_name = 'Details'
        verbose_name_plural = 'Details'

class ModePaiement(SafeDeleteModel):
    libelle = models.CharField(max_length=500, null=False, unique=True)
    historique = HistoricalRecords()
    objects = DeletedModelManager()
    class Meta:
        app_label = 'api_gc'

        verbose_name = 'Mode de Paiement'
        verbose_name_plural = 'Mode de Paiement'


class Encaissement(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    facture = models.ForeignKey(Factures, on_delete=models.DO_NOTHING, null=False, verbose_name="Facture")
    date_encaissement = models.DateField(null=False, verbose_name="Date d'encaissement")
    mode_paiement = models.ForeignKey(ModePaiement, on_delete=models.DO_NOTHING, null=False,
                                      verbose_name="Mode de paiement")
    montant_encaisse = models.DecimalField(max_digits=38, decimal_places=3, blank=True, verbose_name="Montant encaissé",
                                           validators=[MinValueValidator(0)], default=0)
    montant_creance = models.DecimalField(max_digits=38, decimal_places=3, blank=True,
                                          verbose_name="Montant en créance",
                                          validators=[MinValueValidator(0)], default=0, editable=False)
    # banque ou agence  soit charfield soit FK
    numero_piece = models.CharField(max_length=300, null=False, verbose_name="Numero de piéce")
    historique = HistoricalRecords()
    objects = DeletedModelManager()
    class Meta:
        unique_together = (("facture", "date_encaissement"),)
        app_label = 'api_gc'
        verbose_name = 'Encaissements'
        verbose_name_plural = 'Encaissements'










