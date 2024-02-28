from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.

class Parametres(models.Model):
    saisie_automatique=models.BooleanField(default=False, verbose_name="Saisie Automatique")

    class Meta:
        app_label = 'api_gc'



class Clients(models.Model):
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

    sous_client = models.ForeignKey('Clients', on_delete=models.DO_NOTHING, db_column='sous_client',null=True, blank=True)



    class Meta:
        app_label = 'api_gc'


class UniteMesure(models.Model):
    libelle = models.CharField(db_column='libelle', max_length=10, blank=True, null=True)
    description = models.CharField(db_column='description', max_length=50, blank=True, null=True)

    class Meta:
        app_label = 'api_gc'

class Produits(models.Model):
    id=models.CharField(db_column='code_produits', max_length=500, primary_key=True)
    libelle = models.CharField(db_column='nom_produit', max_length=500, blank=True, null=False, verbose_name='Nom Produit')
    unite = models.ForeignKey(UniteMesure, on_delete=models.DO_NOTHING,null=False,verbose_name='Unite de Mesure')
    famille=models.CharField(db_column='famille', max_length=500,  null=True, verbose_name='Famille')

    class Meta:
        app_label = 'api_gc'


class PrixProduit(models.Model):
    produit = models.ForeignKey(Produits, on_delete=models.DO_NOTHING,null=False,verbose_name='Produit')
    prix_unitaire = models.DecimalField(max_digits=38, decimal_places=2,validators=[MinValueValidator(0)],default=0, verbose_name = 'Montant')

    class Meta:
        unique_together = (('produit', 'prix_unitaire'))
        app_label = 'api_gc'


class Contrat(models.Model):
    id=models.CharField(db_column='code_contrat', max_length=500, primary_key=True)
    date_signature=models.DateField(db_column='date_signature', null=False, blank=False, verbose_name='Date de Signature')
    libelle=models.CharField(db_column='libelle', max_length=500, blank=True, null=False, verbose_name='')
    tva=models.DecimalField(max_digits=38,decimal_places=2,validators=[MinValueValidator(0),MaxValueValidator(100)],default=0,verbose_name='TVA')
    transport=models.BooleanField(db_column='transport', default=False, verbose_name='Transport')
    rabais=models.DecimalField(max_digits=38,decimal_places=2,validators=[MinValueValidator(0),MaxValueValidator(100)],default=0,verbose_name='Rabais')
    montant_ht=models.DecimalField(max_digits=38, decimal_places=2,validators=[MinValueValidator(0)],default=0, verbose_name = 'Montant en (HT)')
    montant_ttc=models.DecimalField(max_digits=38, decimal_places=2,validators=[MinValueValidator(0)],default=0, verbose_name = 'Montant en (TTC)')
    client=models.ForeignKey(Clients, on_delete=models.DO_NOTHING,null=False,verbose_name='Client')
    date_expiration=models.DateField(db_column='date_expiration', null=True, verbose_name='Date de Signature')

    class Meta:
        app_label = 'api_gc'



class DQE(models.Model):
    id=models.CharField(max_length=500,primary_key=True,verbose_name='id',editable=False)
    contrat=models.ForeignKey(Contrat, on_delete=models.DO_NOTHING,null=True,verbose_name='Contrat')
    prixPrduit=models.ForeignKey(PrixProduit, on_delete=models.DO_NOTHING,null=False,verbose_name='Produit')
    qte=models.DecimalField(max_digits=38, decimal_places=2,validators=[MinValueValidator(0)],default=0, verbose_name = 'Quantité')
    montant_qte=models.DecimalField(max_digits=38, decimal_places=2,validators=[MinValueValidator(0)],default=0, verbose_name = 'Montant de la quantité',editable=False)
    class Meta:
        app_label = 'api_gc'

class ODS(models.Model):
    Types=[
        ('Interruption','Interruption',),('Reprise','Reprise')
    ]
    contrat = models.ForeignKey(Contrat, on_delete=models.DO_NOTHING, null=False, verbose_name='Contrat')
    type=models.CharField(max_length=500, choices=Types, verbose_name='Type d\'Ordre de Service',null=False)
    date=models.DateField(null=False,verbose_name='Date d\'Ordre de Service')
    motif=models.TextField(null=True, verbose_name='Motif')


    class Meta:
        unique_together = (('contrat', 'type', 'date'),)
        app_label = 'api_gc'





class Planing(models.Model):
    contrat = models.ForeignKey(Contrat, on_delete=models.DO_NOTHING, null=False, verbose_name='Contrat')
    dqe=models.ForeignKey(DQE, on_delete=models.DO_NOTHING, null=False, verbose_name='dqe')
    date=models.DateField(null=False, verbose_name='Date')
    qte_livre=models.DecimalField(max_digits=38, decimal_places=2,validators=[MinValueValidator(0)],default=0, verbose_name = 'Quantité à livré')

    # ajuster selon l'ods
    class Meta:
        unique_together = (('contrat', 'dqe', 'date'),)
        app_label = 'api_gc'



class Camion(models.Model):
    matricule=models.CharField(max_length=500, primary_key=True, verbose_name='Matricule')
    poids=models.DecimalField(max_digits=38, decimal_places=2,validators=[MinValueValidator(0)],default=0, verbose_name = 'Poids net du camion')
    class Meta:
        app_label = 'api_gc'

class Conducteur(models.Model):
    nom=models.CharField(max_length=500,null=False, verbose_name='Nom')
    prenom = models.CharField(max_length=500, null=False, verbose_name='Prénom')
    num_id=models.CharField(max_length=500,null=False,verbose_name='Numero d\'identification')
    class Meta:
        app_label = 'api_gc'


class Conduire(models.Model):
    conducteur=models.ForeignKey(Conducteur,null=False, on_delete=models.DO_NOTHING, verbose_name='Conducteur')
    camion=models.ForeignKey(Camion,null=False, on_delete=models.DO_NOTHING, verbose_name='Camion')
    date=models.DateField(null=False, verbose_name='Date')
    class Meta:
        app_label = 'api_gc'




# mode hors connexion
class BonLivraison(models.Model):
    contrat = models.ForeignKey(Contrat, on_delete=models.DO_NOTHING, null=False, verbose_name='Contrat')
    dqe = models.ForeignKey(DQE, on_delete=models.DO_NOTHING, null=False, verbose_name='dqe')

    qte_precedent = models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,
                                     verbose_name='Quantité precedent')

    qte_livre = models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,
                                    verbose_name='Quantité à livré')
    qte_cumule=models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,
                                    verbose_name='Quantité cumulé')

    date=models.DateField(auto_now=True)

    # verifier ods
    class Meta:
        app_label = 'api_gc'





class Factures(models.Model):
    numero_facture=models.PositiveIntegerField(primary_key=True,null=False, verbose_name='Numero de facture')
    numero_situtation=models.PositiveIntegerField(null=False, verbose_name='Numero de situation',editable='')
    contrat=models.ForeignKey(Contrat, on_delete=models.DO_NOTHING, null=False, verbose_name='Contrat')
    du = models.DateField(null=False, verbose_name='Du')
    au = models.DateField(null=False, verbose_name='Au')
    paye = models.BooleanField(default=False, null=False, editable=False)
    montant_precedent = models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)],
                                            default=0,
                                            verbose_name="Montant Precedent"
                                            , editable=False)
    montant_mois = models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,
                                       verbose_name="Montant du Mois"
                                       , editable=False)
    montant_cumule = models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,
                                         verbose_name="Montant Cumulé"
                                         , editable=False)

    montant_rb = models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,
                                     verbose_name="Montant du rabais"
                                     , editable=False)

    montant_rg = models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)], default=0,
                                     verbose_name="Montant Retenue de garantie"
                                     , editable=False)

    montant_factureHT = models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)],
                                            default=0,
                                            verbose_name="Montant de la facture en HT"
                                            , editable=False)

    montant_factureTTC = models.DecimalField(max_digits=38, decimal_places=2, validators=[MinValueValidator(0)],
                                             default=0,
                                             verbose_name="Montant de la facture en TTC"
                                             , editable=False)

    class Meta:
        app_label = 'api_gc'



class DetailFacture(models.Model):
    facture = models.ForeignKey(Factures, on_delete=models.DO_NOTHING,to_field="numero_facture")
    detail = models.ForeignKey(BonLivraison, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = (('facture', 'detail',))
        app_label = 'api_gc'

class ModePaiement(models.Model):
    libelle = models.CharField(max_length=500, null=False, unique=True)
    class Meta:
        app_label = 'api_gc'


class Encaissements(models.Model):
    facture = models.ForeignKey(Factures, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="Facture")
    date_encaissement = models.DateField(null=False, verbose_name="Date d'encaissement")
    mode_paiement = models.ForeignKey(ModePaiement, on_delete=models.DO_NOTHING, null=False,
                                      verbose_name="Mode de paiement")
    montant_encaisse = models.DecimalField(max_digits=38, decimal_places=2, blank=True, verbose_name="Montant encaissé",
                                           validators=[MinValueValidator(0)], default=0)
    montant_creance = models.DecimalField(max_digits=38, decimal_places=2, blank=True,
                                          verbose_name="Montant en créance",
                                          validators=[MinValueValidator(0)], default=0, editable=False)
    # banque ou agence  soit charfield soit FK
    numero_piece = models.CharField(max_length=300, null=False, verbose_name="Numero de piéce")

    class Meta:
        app_label = 'api_gc'









