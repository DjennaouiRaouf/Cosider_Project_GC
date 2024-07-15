# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Activite(models.Model):
    id = models.CharField(primary_key=True, max_length=300)
    libelle = models.CharField(max_length=500)
    est_bloquer = models.BooleanField()
    user_id = models.CharField(max_length=500)
    date_modification = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'Activite'


class Avances(models.Model):
    id = models.BigAutoField(primary_key=True)
    num_avance = models.IntegerField()
    montant_avance = models.DecimalField(max_digits=38, decimal_places=3)
    est_bloquer = models.BooleanField()
    user_id = models.CharField(max_length=500)
    date_modification = models.DateTimeField()
    contrat_id = models.CharField(max_length=900)

    class Meta:
        managed = False
        db_table = 'Avances'
        unique_together = (('contrat_id', 'montant_avance'),)


class BonDeLivraison(models.Model):
    id = models.CharField(primary_key=True, max_length=500)
    conducteur = models.CharField(max_length=500)
    numero_permis_c = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateTimeField()
    ptc = models.DecimalField(max_digits=38, decimal_places=3)
    montant = models.DecimalField(max_digits=38, decimal_places=3)
    qte = models.DecimalField(max_digits=38, decimal_places=3)
    est_bloquer = models.BooleanField()
    user_id = models.CharField(max_length=500)
    date_modification = models.DateTimeField()
    camion = models.ForeignKey('Camions', models.DO_NOTHING)
    contrat = models.CharField(max_length=500)
    dqe_id = models.CharField(max_length=900)

    class Meta:
        managed = False
        db_table = 'Bon_De_Livraison'


class Camions(models.Model):
    matricule = models.CharField(primary_key=True, max_length=500)
    tare = models.DecimalField(max_digits=38, decimal_places=3)
    est_bloquer = models.BooleanField()
    user_id = models.CharField(max_length=500)
    date_modification = models.DateTimeField()
    unite = models.ForeignKey('UniteDeMesure', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Camions'


class Clients(models.Model):
    code_client = models.CharField(db_column='Code_Client', primary_key=True, max_length=500)  # Field name made lowercase.
    libelle_client = models.CharField(db_column='Libelle_Client', max_length=300)  # Field name made lowercase.
    adresse = models.CharField(max_length=500)
    nif = models.CharField(db_column='NIF', unique=True, max_length=50, blank=True, null=True)  # Field name made lowercase.
    raison_social = models.CharField(db_column='Raison_Social', max_length=50, blank=True, null=True)  # Field name made lowercase.
    num_registre_commerce = models.CharField(db_column='Num_Registre_Commerce', max_length=20, blank=True, null=True)  # Field name made lowercase.
    est_bloquer = models.BooleanField()
    user_id = models.CharField(max_length=500)
    date_modification = models.DateTimeField()
    type = models.ForeignKey('TypeClient', models.DO_NOTHING, blank=True, null=True)
    act = models.ForeignKey(Activite, models.DO_NOTHING, blank=True, null=True)
    ville = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'Clients'


class Config(models.Model):
    id = models.BigAutoField(primary_key=True)
    saisie_automatique = models.BooleanField()
    port = models.CharField(max_length=500)
    est_bloquer = models.BooleanField()
    user_id = models.CharField(max_length=500)
    date_modification = models.DateTimeField()
    unite = models.ForeignKey('Unite', models.DO_NOTHING, db_column='unite', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Config'


class Contrats(models.Model):
    id = models.CharField(primary_key=True, max_length=900)
    code_contrat = models.CharField(max_length=500)
    avenant = models.IntegerField()
    libelle = models.CharField(max_length=500)
    transport = models.BooleanField()
    rabais = models.DecimalField(max_digits=38, decimal_places=3)
    rg = models.DecimalField(max_digits=38, decimal_places=3)
    date_signature = models.DateField()
    date_expiration = models.DateField(blank=True, null=True)
    est_bloquer = models.BooleanField()
    user_id = models.CharField(max_length=500)
    date_modification = models.DateTimeField()
    client = models.ForeignKey(Clients, models.DO_NOTHING)
    tva = models.ForeignKey('Tva', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Contrats'


class Dqe(models.Model):
    id = models.CharField(primary_key=True, max_length=900)
    qte = models.DecimalField(max_digits=38, decimal_places=3)
    rabais = models.DecimalField(max_digits=38, decimal_places=3)
    prix_transport = models.DecimalField(max_digits=38, decimal_places=3)
    est_bloquer = models.BooleanField()
    user_id = models.CharField(max_length=500)
    date_modification = models.DateTimeField()
    contrat = models.ForeignKey(Contrats, models.DO_NOTHING, blank=True, null=True)
    prixproduit = models.ForeignKey('PrixProduit', models.DO_NOTHING, db_column='prixProduit_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DQE'
        unique_together = (('contrat', 'prixproduit'),)


class Details(models.Model):
    id = models.BigAutoField(primary_key=True)
    est_bloquer = models.BooleanField()
    user_id = models.CharField(max_length=500)
    date_modification = models.DateTimeField()
    detail = models.ForeignKey(BonDeLivraison, models.DO_NOTHING)
    facture = models.ForeignKey('Factures', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Details'
        unique_together = (('facture', 'detail'),)


class Encaissements(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_encaissement = models.DateField()
    montant_encaisse = models.DecimalField(max_digits=38, decimal_places=3)
    numero_piece = models.CharField(max_length=300)
    est_bloquer = models.BooleanField()
    user_id = models.CharField(max_length=500)
    date_modification = models.DateTimeField()
    avance = models.ForeignKey(Avances, models.DO_NOTHING, blank=True, null=True)
    facture = models.ForeignKey('Factures', models.DO_NOTHING)
    mode_paiement = models.ForeignKey('ModeDePaiement', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Encaissements'
        unique_together = (('facture', 'date_encaissement'),)


class Factures(models.Model):
    id = models.CharField(primary_key=True, max_length=500)
    date = models.DateField()
    du = models.DateField()
    au = models.DateField()
    paye = models.BooleanField()
    montant = models.DecimalField(max_digits=38, decimal_places=3)
    montant_rb = models.DecimalField(max_digits=38, decimal_places=3)
    montant_rg = models.DecimalField(max_digits=38, decimal_places=3)
    montant_facture_ht = models.DecimalField(max_digits=38, decimal_places=3)
    montant_facture_ttc = models.DecimalField(max_digits=38, decimal_places=3)
    est_bloquer = models.BooleanField()
    user_id = models.CharField(max_length=500)
    date_modification = models.DateTimeField()
    contrat_id = models.CharField(max_length=900)

    class Meta:
        managed = False
        db_table = 'Factures'


class Images(models.Model):
    id = models.BigAutoField(primary_key=True)
    src = models.CharField(max_length=100)
    est_bloquer = models.BooleanField()
    user_id = models.CharField(max_length=500)
    date_modification = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'Images'


class ModeDePaiement(models.Model):
    id = models.CharField(primary_key=True, max_length=30)
    libelle = models.CharField(unique=True, max_length=500)
    est_bloquer = models.BooleanField()
    user_id = models.CharField(max_length=500)
    date_modification = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'Mode_De_Paiement'


class Newtable(models.Model):
    id = models.CharField(max_length=900, blank=True, null=True)
    produit_id = models.CharField(max_length=500)
    code_contrat = models.CharField(max_length=500)
    qte = models.DecimalField(db_column='Qte', max_digits=38, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    avenant = models.IntegerField(blank=True, null=True)
    contrat_id = models.CharField(max_length=514)
    prixproduit_id = models.CharField(db_column='prixProduit_id', max_length=900, blank=True, null=True)  # Field name made lowercase.
    rabais = models.DecimalField(max_digits=38, decimal_places=3, blank=True, null=True)
    prix_transport = models.DecimalField(max_digits=38, decimal_places=3, blank=True, null=True)
    est_bloquer = models.BooleanField(blank=True, null=True)
    user_id = models.CharField(max_length=500, blank=True, null=True)
    date_modification = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'NewTable'


class Planing(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    qte_livre = models.DecimalField(max_digits=38, decimal_places=3)
    est_bloquer = models.BooleanField()
    user_id = models.CharField(max_length=500)
    date_modification = models.DateTimeField()
    contrat = models.ForeignKey(Contrats, models.DO_NOTHING)
    dqe_id = models.CharField(max_length=900)

    class Meta:
        managed = False
        db_table = 'Planing'
        unique_together = (('contrat', 'dqe_id', 'date'),)


class PrixProduit(models.Model):
    id = models.CharField(primary_key=True, max_length=900)
    prix_unitaire = models.DecimalField(max_digits=38, decimal_places=3)
    est_bloquer = models.BooleanField()
    user_id = models.CharField(max_length=500)
    date_modification = models.DateTimeField()
    produit = models.ForeignKey('Produit', models.DO_NOTHING)
    type_prix = models.ForeignKey('TypePrix', models.DO_NOTHING)
    u = models.ForeignKey('Unite', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Prix_Produit'
        unique_together = (('produit', 'u', 'prix_unitaire', 'type_prix', 'id'),)


class Produit(models.Model):
    ref = models.CharField(primary_key=True, max_length=500)
    libelle = models.CharField(max_length=500)
    est_bloquer = models.BooleanField()
    user_id = models.CharField(max_length=500)
    date_modification = models.DateTimeField()
    unite_m = models.ForeignKey('UniteDeMesure', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Produit'


class Tva(models.Model):
    id = models.DecimalField(primary_key=True, max_digits=38, decimal_places=3)
    est_bloquer = models.BooleanField()
    user_id = models.CharField(max_length=500)
    date_modification = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'TVA'


class TypeClient(models.Model):
    id = models.CharField(primary_key=True, max_length=300)
    libelle = models.CharField(max_length=500)
    est_bloquer = models.BooleanField()
    user_id = models.CharField(max_length=500)
    date_modification = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'Type_Client'


class TypePrix(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    libelle = models.CharField(max_length=500)
    est_bloquer = models.BooleanField()
    user_id = models.CharField(max_length=500)
    date_modification = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'Type_Prix'


class Unite(models.Model):
    code_unite = models.CharField(primary_key=True, max_length=500)
    libelle = models.CharField(max_length=500)
    ai = models.CharField(max_length=500, blank=True, null=True)
    adresse = models.CharField(max_length=500, blank=True, null=True)
    contact = models.CharField(max_length=500, blank=True, null=True)
    date_ouverture = models.DateField()
    date_cloture = models.DateField(blank=True, null=True)
    est_bloquer = models.BooleanField()
    user_id = models.CharField(max_length=500)
    date_modification = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'Unite'


class UniteDeMesure(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    libelle = models.CharField(max_length=10, blank=True, null=True)
    est_bloquer = models.BooleanField()
    user_id = models.CharField(max_length=500)
    date_modification = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'Unite_De_Mesure'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
