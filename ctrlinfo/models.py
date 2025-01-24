# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Ansiedad(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    consejeroan = models.SmallIntegerField(blank=True, null=True)
    fechaansiedad = models.DateField(blank=True, null=True)
    pan1 = models.SmallIntegerField(blank=True, null=True)
    pan2 = models.SmallIntegerField(blank=True, null=True)
    pan3 = models.SmallIntegerField(blank=True, null=True)
    pan4 = models.SmallIntegerField(blank=True, null=True)
    pan5 = models.SmallIntegerField(blank=True, null=True)
    pan6 = models.SmallIntegerField(blank=True, null=True)
    pan7 = models.SmallIntegerField(blank=True, null=True)
    pan8 = models.SmallIntegerField(blank=True, null=True)
    pan9 = models.SmallIntegerField(blank=True, null=True)
    pan10 = models.SmallIntegerField(blank=True, null=True)
    pan11 = models.SmallIntegerField(blank=True, null=True)
    pan12 = models.SmallIntegerField(blank=True, null=True)
    pan13 = models.SmallIntegerField(blank=True, null=True)
    pan14 = models.SmallIntegerField(blank=True, null=True)
    pan15 = models.SmallIntegerField(blank=True, null=True)
    pan16 = models.SmallIntegerField(blank=True, null=True)
    pan17 = models.SmallIntegerField(blank=True, null=True)
    pan18 = models.SmallIntegerField(blank=True, null=True)
    pan19 = models.SmallIntegerField(blank=True, null=True)
    pan20 = models.SmallIntegerField(blank=True, null=True)
    pan21 = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ansiedad'


class Assist(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    p1s1 = models.SmallIntegerField(blank=True, null=True)
    p1s2 = models.SmallIntegerField(blank=True, null=True)
    p1s3 = models.SmallIntegerField(blank=True, null=True)
    p1s4 = models.SmallIntegerField(blank=True, null=True)
    p1s5 = models.SmallIntegerField(blank=True, null=True)
    p1s6 = models.SmallIntegerField(blank=True, null=True)
    p1s7 = models.SmallIntegerField(blank=True, null=True)
    p1s8 = models.SmallIntegerField(blank=True, null=True)
    p1s9 = models.SmallIntegerField(blank=True, null=True)
    p1s10 = models.SmallIntegerField(blank=True, null=True)
    asistotras1 = models.CharField(max_length=20, blank=True, null=True)
    p2s1 = models.SmallIntegerField(blank=True, null=True)
    p2s3 = models.SmallIntegerField(blank=True, null=True)
    p2s4 = models.SmallIntegerField(blank=True, null=True)
    p2s5 = models.SmallIntegerField(blank=True, null=True)
    p2s6 = models.SmallIntegerField(blank=True, null=True)
    p2s7 = models.SmallIntegerField(blank=True, null=True)
    p2s8 = models.SmallIntegerField(blank=True, null=True)
    p2s9 = models.SmallIntegerField(blank=True, null=True)
    p2s10 = models.SmallIntegerField(blank=True, null=True)
    asistotras2 = models.CharField(max_length=20, blank=True, null=True)
    p3s1 = models.SmallIntegerField(blank=True, null=True)
    p3s2 = models.SmallIntegerField(blank=True, null=True)
    p3s3 = models.SmallIntegerField(blank=True, null=True)
    p3s4 = models.SmallIntegerField(blank=True, null=True)
    p3s5 = models.SmallIntegerField(blank=True, null=True)
    p3s6 = models.SmallIntegerField(blank=True, null=True)
    p3s7 = models.SmallIntegerField(blank=True, null=True)
    p3s8 = models.SmallIntegerField(blank=True, null=True)
    p3s9 = models.SmallIntegerField(blank=True, null=True)
    p3s10 = models.SmallIntegerField(blank=True, null=True)
    asistotras3 = models.CharField(max_length=20, blank=True, null=True)
    p4s1 = models.SmallIntegerField(blank=True, null=True)
    p4s2 = models.SmallIntegerField(blank=True, null=True)
    p4s3 = models.SmallIntegerField(blank=True, null=True)
    p4s4 = models.SmallIntegerField(blank=True, null=True)
    p4s5 = models.SmallIntegerField(blank=True, null=True)
    p4s6 = models.SmallIntegerField(blank=True, null=True)
    p4s7 = models.SmallIntegerField(blank=True, null=True)
    p4s8 = models.SmallIntegerField(blank=True, null=True)
    p4s9 = models.SmallIntegerField(blank=True, null=True)
    p4s10 = models.SmallIntegerField(blank=True, null=True)
    asistotras4 = models.CharField(max_length=20, blank=True, null=True)
    p5s1 = models.SmallIntegerField(blank=True, null=True)
    p5s2 = models.SmallIntegerField(blank=True, null=True)
    p5s3 = models.SmallIntegerField(blank=True, null=True)
    p5s4 = models.SmallIntegerField(blank=True, null=True)
    p5s5 = models.SmallIntegerField(blank=True, null=True)
    p5s6 = models.SmallIntegerField(blank=True, null=True)
    p5s7 = models.SmallIntegerField(blank=True, null=True)
    p5s8 = models.SmallIntegerField(blank=True, null=True)
    p5s9 = models.SmallIntegerField(blank=True, null=True)
    p5s10 = models.SmallIntegerField(blank=True, null=True)
    asistotras5 = models.CharField(max_length=20, blank=True, null=True)
    p7s1 = models.SmallIntegerField(blank=True, null=True)
    p7s2 = models.SmallIntegerField(blank=True, null=True)
    p7s3 = models.SmallIntegerField(blank=True, null=True)
    p7s4 = models.SmallIntegerField(blank=True, null=True)
    p7s5 = models.SmallIntegerField(blank=True, null=True)
    p7s6 = models.SmallIntegerField(blank=True, null=True)
    p7s7 = models.SmallIntegerField(blank=True, null=True)
    p7s8 = models.SmallIntegerField(blank=True, null=True)
    p7s9 = models.SmallIntegerField(blank=True, null=True)
    p7s10 = models.SmallIntegerField(blank=True, null=True)
    asistotras7 = models.CharField(max_length=20, blank=True, null=True)
    p8s1 = models.SmallIntegerField(blank=True, null=True)
    p6s1 = models.SmallIntegerField(blank=True, null=True)
    p6s2 = models.SmallIntegerField(blank=True, null=True)
    p6s3 = models.SmallIntegerField(blank=True, null=True)
    p6s4 = models.SmallIntegerField(blank=True, null=True)
    p6s5 = models.SmallIntegerField(blank=True, null=True)
    p6s6 = models.SmallIntegerField(blank=True, null=True)
    p6s7 = models.SmallIntegerField(blank=True, null=True)
    p6s8 = models.SmallIntegerField(blank=True, null=True)
    p6s9 = models.SmallIntegerField(blank=True, null=True)
    p6s10 = models.SmallIntegerField(blank=True, null=True)
    asistotras6 = models.CharField(max_length=20, blank=True, null=True)
    habitosinyectarse = models.SmallIntegerField(blank=True, null=True)
    puntos1 = models.SmallIntegerField(blank=True, null=True)
    puntos2 = models.SmallIntegerField(blank=True, null=True)
    puntos3 = models.SmallIntegerField(blank=True, null=True)
    puntos4 = models.SmallIntegerField(blank=True, null=True)
    puntos5 = models.SmallIntegerField(blank=True, null=True)
    puntos6 = models.SmallIntegerField(blank=True, null=True)
    puntos7 = models.SmallIntegerField(blank=True, null=True)
    puntos8 = models.SmallIntegerField(blank=True, null=True)
    puntos9 = models.SmallIntegerField(blank=True, null=True)
    puntos10 = models.SmallIntegerField(blank=True, null=True)
    consejeroassist = models.SmallIntegerField(blank=True, null=True)
    riesgo1 = models.SmallIntegerField(blank=True, null=True)
    riesgo2 = models.SmallIntegerField(blank=True, null=True)
    riesgo3 = models.SmallIntegerField(blank=True, null=True)
    riesgo4 = models.SmallIntegerField(blank=True, null=True)
    riesgo5 = models.SmallIntegerField(blank=True, null=True)
    riesgo6 = models.SmallIntegerField(blank=True, null=True)
    riesgo7 = models.SmallIntegerField(blank=True, null=True)
    riesgo8 = models.SmallIntegerField(blank=True, null=True)
    riesgo9 = models.SmallIntegerField(blank=True, null=True)
    riesgo10 = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assist'


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


class Autorizacion(models.Model):
    campo = models.CharField(max_length=40, blank=True, null=True)
    campo1 = models.CharField(max_length=20, blank=True, null=True)
    campo2 = models.CharField(max_length=10, blank=True, null=True)
    campo3 = models.CharField(max_length=10, blank=True, null=True)
    campo4 = models.CharField(max_length=10, blank=True, null=True)
    campo5 = models.CharField(max_length=20, blank=True, null=True)
    campo6 = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'autorizacion'


class Cfamiliar(models.Model):
    expediente = models.CharField(max_length=20, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    hora = models.TimeField(blank=True, null=True)
    sesion = models.SmallIntegerField(blank=True, null=True)
    diasestancia = models.SmallIntegerField(blank=True, null=True)
    objetivo = models.TextField(blank=True, null=True)
    aspectos = models.TextField(blank=True, null=True)
    resultados = models.TextField(blank=True, null=True)
    seesperan = models.TextField(blank=True, null=True)
    tareas = models.TextField(blank=True, null=True)
    quesetrabajo = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    proximasesion = models.DateField(blank=True, null=True)
    cerrada = models.SmallIntegerField(blank=True, null=True)
    familiares = models.TextField(blank=True, null=True)
    consejero = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cfamiliar'


class Cfisicas(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    p1 = models.SmallIntegerField(blank=True, null=True)
    p1a = models.SmallIntegerField(blank=True, null=True)
    p2 = models.SmallIntegerField(blank=True, null=True)
    p2a = models.SmallIntegerField(blank=True, null=True)
    p3 = models.SmallIntegerField(blank=True, null=True)
    p3a = models.SmallIntegerField(blank=True, null=True)
    p4 = models.SmallIntegerField(blank=True, null=True)
    p4a = models.SmallIntegerField(blank=True, null=True)
    p5 = models.SmallIntegerField(blank=True, null=True)
    p5a = models.SmallIntegerField(blank=True, null=True)
    p6 = models.SmallIntegerField(blank=True, null=True)
    p6a = models.SmallIntegerField(blank=True, null=True)
    p7 = models.SmallIntegerField(blank=True, null=True)
    p7a = models.SmallIntegerField(blank=True, null=True)
    p8 = models.SmallIntegerField(blank=True, null=True)
    p8a = models.SmallIntegerField(blank=True, null=True)
    p9 = models.SmallIntegerField(blank=True, null=True)
    p9a = models.SmallIntegerField(blank=True, null=True)
    p10 = models.SmallIntegerField(blank=True, null=True)
    p10a = models.SmallIntegerField(blank=True, null=True)
    p11 = models.SmallIntegerField(blank=True, null=True)
    p11a = models.SmallIntegerField(blank=True, null=True)
    p12 = models.SmallIntegerField(blank=True, null=True)
    p12a = models.SmallIntegerField(blank=True, null=True)
    p13 = models.SmallIntegerField(blank=True, null=True)
    p13a = models.SmallIntegerField(blank=True, null=True)
    p14 = models.SmallIntegerField(blank=True, null=True)
    p14a = models.SmallIntegerField(blank=True, null=True)
    p15 = models.SmallIntegerField(blank=True, null=True)
    p15a = models.SmallIntegerField(blank=True, null=True)
    p16 = models.SmallIntegerField(blank=True, null=True)
    p16a = models.SmallIntegerField(blank=True, null=True)
    p17 = models.SmallIntegerField(blank=True, null=True)
    p17a = models.SmallIntegerField(blank=True, null=True)
    p18 = models.SmallIntegerField(blank=True, null=True)
    p18a = models.SmallIntegerField(blank=True, null=True)
    p19 = models.SmallIntegerField(blank=True, null=True)
    p19a = models.SmallIntegerField(blank=True, null=True)
    p20 = models.SmallIntegerField(blank=True, null=True)
    p20a = models.SmallIntegerField(blank=True, null=True)
    p21 = models.SmallIntegerField(blank=True, null=True)
    p21a = models.SmallIntegerField(blank=True, null=True)
    p22 = models.SmallIntegerField(blank=True, null=True)
    p22a = models.SmallIntegerField(blank=True, null=True)
    p23 = models.SmallIntegerField(blank=True, null=True)
    p23a = models.SmallIntegerField(blank=True, null=True)
    p24 = models.SmallIntegerField(blank=True, null=True)
    p24a = models.SmallIntegerField(blank=True, null=True)
    p25 = models.SmallIntegerField(blank=True, null=True)
    p25a = models.SmallIntegerField(blank=True, null=True)
    p26 = models.SmallIntegerField(blank=True, null=True)
    p26a = models.SmallIntegerField(blank=True, null=True)
    otro = models.CharField(max_length=15, blank=True, null=True)
    otro1 = models.CharField(max_length=15, blank=True, null=True)
    otro2 = models.CharField(max_length=15, blank=True, null=True)
    otro3 = models.CharField(max_length=15, blank=True, null=True)
    papa = models.SmallIntegerField(blank=True, null=True)
    pedad = models.SmallIntegerField(blank=True, null=True)
    pescolaridad = models.CharField(max_length=20, blank=True, null=True)
    psededica = models.CharField(max_length=20, blank=True, null=True)
    mama = models.SmallIntegerField(blank=True, null=True)
    medad = models.SmallIntegerField(blank=True, null=True)
    mescolaridad = models.CharField(max_length=20, blank=True, null=True)
    msededica = models.CharField(max_length=20, blank=True, null=True)
    comoesrelacion = models.SmallIntegerField(blank=True, null=True)
    cuantoshermanos = models.SmallIntegerField(blank=True, null=True)
    lugar = models.SmallIntegerField(blank=True, null=True)
    relacionhermanos = models.SmallIntegerField(blank=True, null=True)
    comovemama = models.SmallIntegerField(blank=True, null=True)
    comovepapa = models.SmallIntegerField(blank=True, null=True)
    comovemaestros = models.SmallIntegerField(blank=True, null=True)
    comoveamigos = models.SmallIntegerField(blank=True, null=True)
    comovepareja = models.SmallIntegerField(blank=True, null=True)
    comovehermanos = models.SmallIntegerField(blank=True, null=True)
    pr1 = models.SmallIntegerField(blank=True, null=True)
    pr2 = models.SmallIntegerField(blank=True, null=True)
    pr3 = models.SmallIntegerField(blank=True, null=True)
    pr4 = models.SmallIntegerField(blank=True, null=True)
    pn1 = models.SmallIntegerField(blank=True, null=True)
    pn2 = models.SmallIntegerField(blank=True, null=True)
    pn3 = models.SmallIntegerField(blank=True, null=True)
    rsexuales = models.SmallIntegerField(blank=True, null=True)
    involucrado = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cfisicas'


class Cgrupal(models.Model):
    sesion = models.SmallIntegerField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    hora = models.TimeField(blank=True, null=True)
    internos = models.TextField(blank=True, null=True)
    objetivo = models.TextField(blank=True, null=True)
    aspectos = models.TextField(blank=True, null=True)
    resultados = models.TextField(blank=True, null=True)
    seesperan = models.TextField(blank=True, null=True)
    tareas = models.TextField(blank=True, null=True)
    aspectostrabajados = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    proximasesion = models.DateField(blank=True, null=True)
    cerrada = models.SmallIntegerField(blank=True, null=True)
    consejero = models.SmallIntegerField(blank=True, null=True)
    conrecursosinout = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cgrupal'


class Cindividual(models.Model):
    expediente = models.CharField(max_length=20, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    hora = models.TimeField(blank=True, null=True)
    sesion = models.SmallIntegerField(blank=True, null=True)
    diasestancia = models.SmallIntegerField(blank=True, null=True)
    objetivo = models.TextField(blank=True, null=True)
    aspectos = models.TextField(blank=True, null=True)
    resultados = models.TextField(blank=True, null=True)
    seesperan = models.TextField(blank=True, null=True)
    tareas = models.TextField(blank=True, null=True)
    quesetrabajo = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    consejero = models.SmallIntegerField(blank=True, null=True)
    proximasesion = models.DateField(blank=True, null=True)
    cerrada = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cindividual'


class Cmentales(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    p1 = models.SmallIntegerField(blank=True, null=True)
    p1a = models.SmallIntegerField(blank=True, null=True)
    p2 = models.SmallIntegerField(blank=True, null=True)
    p2a = models.SmallIntegerField(blank=True, null=True)
    p3 = models.SmallIntegerField(blank=True, null=True)
    p3a = models.SmallIntegerField(blank=True, null=True)
    p4 = models.SmallIntegerField(blank=True, null=True)
    p4a = models.SmallIntegerField(blank=True, null=True)
    p5 = models.SmallIntegerField(blank=True, null=True)
    p5a = models.SmallIntegerField(blank=True, null=True)
    p6 = models.SmallIntegerField(blank=True, null=True)
    p6a = models.SmallIntegerField(blank=True, null=True)
    p7 = models.SmallIntegerField(blank=True, null=True)
    p7a = models.SmallIntegerField(blank=True, null=True)
    p8 = models.SmallIntegerField(blank=True, null=True)
    p8a = models.SmallIntegerField(blank=True, null=True)
    p9 = models.SmallIntegerField(blank=True, null=True)
    p9a = models.SmallIntegerField(blank=True, null=True)
    p10 = models.SmallIntegerField(blank=True, null=True)
    p10a = models.SmallIntegerField(blank=True, null=True)
    p11 = models.SmallIntegerField(blank=True, null=True)
    p11a = models.SmallIntegerField(blank=True, null=True)
    p12 = models.SmallIntegerField(blank=True, null=True)
    p12a = models.SmallIntegerField(blank=True, null=True)
    p13 = models.SmallIntegerField(blank=True, null=True)
    p13a = models.SmallIntegerField(blank=True, null=True)
    p14 = models.SmallIntegerField(blank=True, null=True)
    p14a = models.SmallIntegerField(blank=True, null=True)
    p15 = models.SmallIntegerField(blank=True, null=True)
    p15a = models.SmallIntegerField(blank=True, null=True)
    p16 = models.SmallIntegerField(blank=True, null=True)
    p16a = models.SmallIntegerField(blank=True, null=True)
    p17 = models.SmallIntegerField(blank=True, null=True)
    p17a = models.SmallIntegerField(blank=True, null=True)
    p18 = models.SmallIntegerField(blank=True, null=True)
    p18a = models.SmallIntegerField(blank=True, null=True)
    p19 = models.SmallIntegerField(blank=True, null=True)
    p19a = models.SmallIntegerField(blank=True, null=True)
    p20 = models.SmallIntegerField(blank=True, null=True)
    p20a = models.SmallIntegerField(blank=True, null=True)
    p21 = models.SmallIntegerField(blank=True, null=True)
    p21a = models.SmallIntegerField(blank=True, null=True)
    p22 = models.SmallIntegerField(blank=True, null=True)
    p22a = models.SmallIntegerField(blank=True, null=True)
    p23 = models.SmallIntegerField(blank=True, null=True)
    p23a = models.SmallIntegerField(blank=True, null=True)
    p24 = models.SmallIntegerField(blank=True, null=True)
    p24a = models.SmallIntegerField(blank=True, null=True)
    p25 = models.SmallIntegerField(blank=True, null=True)
    p25a = models.SmallIntegerField(blank=True, null=True)
    p26 = models.SmallIntegerField(blank=True, null=True)
    p26a = models.SmallIntegerField(blank=True, null=True)
    p27 = models.SmallIntegerField(blank=True, null=True)
    p27a = models.SmallIntegerField(blank=True, null=True)
    p28 = models.SmallIntegerField(blank=True, null=True)
    p28a = models.SmallIntegerField(blank=True, null=True)
    p29 = models.SmallIntegerField(blank=True, null=True)
    p29a = models.SmallIntegerField(blank=True, null=True)
    p30 = models.SmallIntegerField(blank=True, null=True)
    p30a = models.SmallIntegerField(blank=True, null=True)
    p31 = models.SmallIntegerField(blank=True, null=True)
    p31a = models.SmallIntegerField(blank=True, null=True)
    p32 = models.SmallIntegerField(blank=True, null=True)
    p32a = models.SmallIntegerField(blank=True, null=True)
    p33 = models.SmallIntegerField(blank=True, null=True)
    p33a = models.SmallIntegerField(blank=True, null=True)
    p34 = models.SmallIntegerField(blank=True, null=True)
    p34a = models.SmallIntegerField(blank=True, null=True)
    otro = models.CharField(max_length=15, blank=True, null=True)
    otro1 = models.CharField(max_length=15, blank=True, null=True)
    otro2 = models.CharField(max_length=15, blank=True, null=True)
    otro3 = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cmentales'


class Conceptos(models.Model):
    codigo = models.CharField(max_length=2, blank=True, null=True)
    descripcion = models.CharField(max_length=30, blank=True, null=True)
    tipo = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conceptos'


class Crelaciones(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    p1 = models.SmallIntegerField(blank=True, null=True)
    p1a = models.SmallIntegerField(blank=True, null=True)
    p2 = models.SmallIntegerField(blank=True, null=True)
    p2a = models.SmallIntegerField(blank=True, null=True)
    p3 = models.SmallIntegerField(blank=True, null=True)
    p3a = models.SmallIntegerField(blank=True, null=True)
    p4 = models.SmallIntegerField(blank=True, null=True)
    p4a = models.SmallIntegerField(blank=True, null=True)
    p5 = models.SmallIntegerField(blank=True, null=True)
    p5a = models.SmallIntegerField(blank=True, null=True)
    p6 = models.SmallIntegerField(blank=True, null=True)
    p6a = models.SmallIntegerField(blank=True, null=True)
    p7 = models.SmallIntegerField(blank=True, null=True)
    p7a = models.SmallIntegerField(blank=True, null=True)
    p8 = models.SmallIntegerField(blank=True, null=True)
    p8a = models.SmallIntegerField(blank=True, null=True)
    p9 = models.SmallIntegerField(blank=True, null=True)
    p9a = models.SmallIntegerField(blank=True, null=True)
    p10 = models.SmallIntegerField(blank=True, null=True)
    p10a = models.SmallIntegerField(blank=True, null=True)
    p11 = models.SmallIntegerField(blank=True, null=True)
    p11a = models.SmallIntegerField(blank=True, null=True)
    p12 = models.SmallIntegerField(blank=True, null=True)
    p12a = models.SmallIntegerField(blank=True, null=True)
    p13 = models.SmallIntegerField(blank=True, null=True)
    p13a = models.SmallIntegerField(blank=True, null=True)
    p14 = models.SmallIntegerField(blank=True, null=True)
    p14a = models.SmallIntegerField(blank=True, null=True)
    p15 = models.SmallIntegerField(blank=True, null=True)
    p15a = models.SmallIntegerField(blank=True, null=True)
    p16 = models.SmallIntegerField(blank=True, null=True)
    p16a = models.SmallIntegerField(blank=True, null=True)
    p17 = models.SmallIntegerField(blank=True, null=True)
    p17a = models.SmallIntegerField(blank=True, null=True)
    p18 = models.SmallIntegerField(blank=True, null=True)
    p18a = models.SmallIntegerField(blank=True, null=True)
    p19 = models.SmallIntegerField(blank=True, null=True)
    p19a = models.SmallIntegerField(blank=True, null=True)
    p20 = models.SmallIntegerField(blank=True, null=True)
    p20a = models.SmallIntegerField(blank=True, null=True)
    p21 = models.SmallIntegerField(blank=True, null=True)
    p21a = models.SmallIntegerField(blank=True, null=True)
    p22 = models.SmallIntegerField(blank=True, null=True)
    p22a = models.SmallIntegerField(blank=True, null=True)
    p23 = models.SmallIntegerField(blank=True, null=True)
    p23a = models.SmallIntegerField(blank=True, null=True)
    p24 = models.SmallIntegerField(blank=True, null=True)
    p24a = models.SmallIntegerField(blank=True, null=True)
    p25 = models.SmallIntegerField(blank=True, null=True)
    p25a = models.SmallIntegerField(blank=True, null=True)
    p26 = models.SmallIntegerField(blank=True, null=True)
    p26a = models.SmallIntegerField(blank=True, null=True)
    p27 = models.SmallIntegerField(blank=True, null=True)
    p27a = models.SmallIntegerField(blank=True, null=True)
    p28 = models.SmallIntegerField(blank=True, null=True)
    p28a = models.SmallIntegerField(blank=True, null=True)
    p29 = models.SmallIntegerField(blank=True, null=True)
    p29a = models.SmallIntegerField(blank=True, null=True)
    p30 = models.SmallIntegerField(blank=True, null=True)
    p30a = models.SmallIntegerField(blank=True, null=True)
    p31 = models.SmallIntegerField(blank=True, null=True)
    p31a = models.SmallIntegerField(blank=True, null=True)
    p32 = models.SmallIntegerField(blank=True, null=True)
    p32a = models.SmallIntegerField(blank=True, null=True)
    p33 = models.SmallIntegerField(blank=True, null=True)
    p33a = models.SmallIntegerField(blank=True, null=True)
    p34 = models.SmallIntegerField(blank=True, null=True)
    p34a = models.SmallIntegerField(blank=True, null=True)
    p35 = models.SmallIntegerField(blank=True, null=True)
    p35a = models.SmallIntegerField(blank=True, null=True)
    p36 = models.SmallIntegerField(blank=True, null=True)
    p36a = models.SmallIntegerField(blank=True, null=True)
    p37 = models.SmallIntegerField(blank=True, null=True)
    p37a = models.SmallIntegerField(blank=True, null=True)
    p38 = models.SmallIntegerField(blank=True, null=True)
    p38a = models.SmallIntegerField(blank=True, null=True)
    p39 = models.SmallIntegerField(blank=True, null=True)
    p39a = models.SmallIntegerField(blank=True, null=True)
    p40 = models.SmallIntegerField(blank=True, null=True)
    p40a = models.SmallIntegerField(blank=True, null=True)
    p41 = models.SmallIntegerField(blank=True, null=True)
    p41a = models.SmallIntegerField(blank=True, null=True)
    p42 = models.SmallIntegerField(blank=True, null=True)
    p42a = models.SmallIntegerField(blank=True, null=True)
    p43 = models.SmallIntegerField(blank=True, null=True)
    p43a = models.SmallIntegerField(blank=True, null=True)
    p44 = models.SmallIntegerField(blank=True, null=True)
    p44a = models.SmallIntegerField(blank=True, null=True)
    p45 = models.SmallIntegerField(blank=True, null=True)
    p45a = models.SmallIntegerField(blank=True, null=True)
    p46 = models.SmallIntegerField(blank=True, null=True)
    p46a = models.SmallIntegerField(blank=True, null=True)
    p47 = models.SmallIntegerField(blank=True, null=True)
    p47a = models.SmallIntegerField(blank=True, null=True)
    p48 = models.SmallIntegerField(blank=True, null=True)
    p48a = models.SmallIntegerField(blank=True, null=True)
    p49 = models.SmallIntegerField(blank=True, null=True)
    p49a = models.SmallIntegerField(blank=True, null=True)
    p50 = models.SmallIntegerField(blank=True, null=True)
    p50a = models.SmallIntegerField(blank=True, null=True)
    p51 = models.SmallIntegerField(blank=True, null=True)
    p51a = models.SmallIntegerField(blank=True, null=True)
    fdc = models.CharField(max_length=30, blank=True, null=True)
    otro = models.CharField(max_length=15, blank=True, null=True)
    otro2 = models.CharField(max_length=15, blank=True, null=True)
    otro1 = models.CharField(max_length=15, blank=True, null=True)
    otro3 = models.CharField(max_length=15, blank=True, null=True)
    otro4 = models.CharField(max_length=15, blank=True, null=True)
    otro5 = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crelaciones'


class Datosgrales(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    calleynumero = models.CharField(max_length=50, blank=True, null=True)
    colonia = models.CharField(max_length=50, blank=True, null=True)
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    sitioweb = models.CharField(max_length=50, blank=True, null=True)
    correelectronico = models.CharField(max_length=50, blank=True, null=True)
    rfc = models.CharField(max_length=13, blank=True, null=True)
    cp = models.CharField(max_length=6, blank=True, null=True)
    expediente = models.SmallIntegerField(blank=True, null=True)
    recibo = models.SmallIntegerField(blank=True, null=True)
    receta = models.SmallIntegerField(blank=True, null=True)
    sesiong = models.SmallIntegerField(blank=True, null=True)
    recibootros = models.SmallIntegerField(blank=True, null=True)
    responsable = models.CharField(max_length=30, blank=True, null=True)
    cedula = models.CharField(max_length=20, blank=True, null=True)
    cargo = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datosgrales'


class Depresion(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    fechadepresion = models.DateField(blank=True, null=True)
    consejerodepresion = models.SmallIntegerField(blank=True, null=True)
    pde1 = models.SmallIntegerField(blank=True, null=True)
    pde2 = models.SmallIntegerField(blank=True, null=True)
    pde3 = models.SmallIntegerField(blank=True, null=True)
    pde4 = models.SmallIntegerField(blank=True, null=True)
    pde5 = models.SmallIntegerField(blank=True, null=True)
    pde6 = models.SmallIntegerField(blank=True, null=True)
    pde7 = models.SmallIntegerField(blank=True, null=True)
    pde8 = models.SmallIntegerField(blank=True, null=True)
    pde9 = models.SmallIntegerField(blank=True, null=True)
    pde10 = models.SmallIntegerField(blank=True, null=True)
    pde11 = models.SmallIntegerField(blank=True, null=True)
    pde12 = models.SmallIntegerField(blank=True, null=True)
    pde13 = models.SmallIntegerField(blank=True, null=True)
    pde14 = models.SmallIntegerField(blank=True, null=True)
    pde15 = models.SmallIntegerField(blank=True, null=True)
    pde16 = models.SmallIntegerField(blank=True, null=True)
    pde17 = models.SmallIntegerField(blank=True, null=True)
    pde18 = models.SmallIntegerField(blank=True, null=True)
    pde19 = models.SmallIntegerField(blank=True, null=True)
    pde20 = models.SmallIntegerField(blank=True, null=True)
    pde21 = models.SmallIntegerField(blank=True, null=True)
    puntajedepresion = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'depresion'


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


class Einicial(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    consumo1 = models.SmallIntegerField(blank=True, null=True)
    forma1 = models.SmallIntegerField(blank=True, null=True)
    frecuencia1 = models.CharField(max_length=10, blank=True, null=True)
    cantidad1 = models.CharField(max_length=10, blank=True, null=True)
    edad1 = models.SmallIntegerField(blank=True, null=True)
    consumo2 = models.SmallIntegerField(blank=True, null=True)
    forma2 = models.SmallIntegerField(blank=True, null=True)
    frecuencia2 = models.CharField(max_length=10, blank=True, null=True)
    cantidad2 = models.CharField(max_length=10, blank=True, null=True)
    edad2 = models.SmallIntegerField(blank=True, null=True)
    consumo3 = models.SmallIntegerField(blank=True, null=True)
    forma3 = models.SmallIntegerField(blank=True, null=True)
    frecuencia3 = models.CharField(max_length=10, blank=True, null=True)
    cantidad3 = models.CharField(max_length=10, blank=True, null=True)
    edad3 = models.SmallIntegerField(blank=True, null=True)
    consumo4 = models.SmallIntegerField(blank=True, null=True)
    forma4 = models.SmallIntegerField(blank=True, null=True)
    frecuencia4 = models.CharField(max_length=10, blank=True, null=True)
    cantidad4 = models.CharField(max_length=10, blank=True, null=True)
    edad4 = models.SmallIntegerField(blank=True, null=True)
    consumo5 = models.SmallIntegerField(blank=True, null=True)
    forma5 = models.SmallIntegerField(blank=True, null=True)
    frecuencia5 = models.CharField(max_length=10, blank=True, null=True)
    cantidad5 = models.CharField(max_length=10, blank=True, null=True)
    edad5 = models.SmallIntegerField(blank=True, null=True)
    consumo6 = models.SmallIntegerField(blank=True, null=True)
    forma6 = models.SmallIntegerField(blank=True, null=True)
    frecuencia6 = models.CharField(max_length=10, blank=True, null=True)
    cantidad6 = models.CharField(max_length=10, blank=True, null=True)
    edad6 = models.SmallIntegerField(blank=True, null=True)
    consumo7 = models.SmallIntegerField(blank=True, null=True)
    forma7 = models.SmallIntegerField(blank=True, null=True)
    frecuencia7 = models.CharField(max_length=10, blank=True, null=True)
    cantidad7 = models.CharField(max_length=10, blank=True, null=True)
    edad7 = models.SmallIntegerField(blank=True, null=True)
    consumo8 = models.SmallIntegerField(blank=True, null=True)
    forma8 = models.SmallIntegerField(blank=True, null=True)
    frecuencia8 = models.CharField(max_length=10, blank=True, null=True)
    cantidad8 = models.CharField(max_length=10, blank=True, null=True)
    edad8 = models.SmallIntegerField(blank=True, null=True)
    consumo9 = models.SmallIntegerField(blank=True, null=True)
    forma9 = models.SmallIntegerField(blank=True, null=True)
    frecuencia9 = models.CharField(max_length=10, blank=True, null=True)
    cantidad9 = models.CharField(max_length=10, blank=True, null=True)
    edad9 = models.SmallIntegerField(blank=True, null=True)
    consumo10 = models.SmallIntegerField(blank=True, null=True)
    forma10 = models.SmallIntegerField(blank=True, null=True)
    frecuencia10 = models.CharField(max_length=10, blank=True, null=True)
    cantidad10 = models.CharField(max_length=10, blank=True, null=True)
    edad10 = models.SmallIntegerField(blank=True, null=True)
    consumo11 = models.SmallIntegerField(blank=True, null=True)
    forma11 = models.SmallIntegerField(blank=True, null=True)
    frecuencia11 = models.CharField(max_length=10, blank=True, null=True)
    cantidad11 = models.CharField(max_length=10, blank=True, null=True)
    edad11 = models.SmallIntegerField(blank=True, null=True)
    otrassustancias = models.CharField(max_length=50, blank=True, null=True)
    pricipalsustancia = models.SmallIntegerField(blank=True, null=True)
    cualalcohol = models.SmallIntegerField(blank=True, null=True)
    cualdestilado = models.CharField(max_length=10, blank=True, null=True)
    hacecuanto = models.CharField(max_length=10, blank=True, null=True)
    normalmentecomo = models.SmallIntegerField(blank=True, null=True)
    normalmentedonde = models.SmallIntegerField(blank=True, null=True)
    quelugares = models.CharField(max_length=30, blank=True, null=True)
    detenervoluntariamente = models.SmallIntegerField(blank=True, null=True)
    gastomalcohol = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    gastomtabaco = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    gastomdrogas = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    desagradables = models.SmallIntegerField(blank=True, null=True)
    enfermedad = models.SmallIntegerField(blank=True, null=True)
    agradables = models.SmallIntegerField(blank=True, null=True)
    necesidad = models.SmallIntegerField(blank=True, null=True)
    probando = models.SmallIntegerField(blank=True, null=True)
    conflictos = models.SmallIntegerField(blank=True, null=True)
    agradablesotros = models.SmallIntegerField(blank=True, null=True)
    presionsocial = models.SmallIntegerField(blank=True, null=True)
    tamanoproblema = models.CharField(max_length=10, blank=True, null=True)
    tamanoproblemad = models.CharField(max_length=10, blank=True, null=True)
    tipo = models.CharField(max_length=15, blank=True, null=True)
    mayortiempo = models.SmallIntegerField(blank=True, null=True)
    cuandomes = models.CharField(max_length=3, blank=True, null=True)
    porquelohizo = models.CharField(max_length=20, blank=True, null=True)
    mayortiempo6 = models.SmallIntegerField(blank=True, null=True)
    cuandomes6 = models.CharField(max_length=3, blank=True, null=True)
    porquelohizo6 = models.CharField(max_length=20, blank=True, null=True)
    quetanimportante = models.SmallIntegerField(blank=True, null=True)
    cuandoyear = models.CharField(max_length=4, blank=True, null=True)
    cuandoyear6 = models.CharField(max_length=4, blank=True, null=True)
    quetanseguro = models.SmallIntegerField(blank=True, null=True)
    piensaque = models.SmallIntegerField(blank=True, null=True)
    quetandispuesto = models.SmallIntegerField(blank=True, null=True)
    razon1 = models.CharField(max_length=20, blank=True, null=True)
    razon2 = models.CharField(max_length=20, blank=True, null=True)
    razon3 = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'einicial'


class Estadocuenta(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    costototal = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    aportacioninicial = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    aportaciones = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    saldo = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    ultimopago = models.DateField(blank=True, null=True)
    siguientepago = models.DateField(blank=True, null=True)
    periodicidad = models.SmallIntegerField(blank=True, null=True)
    aportacion = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    primerpago = models.DateField(blank=True, null=True)
    otro = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estadocuenta'


class Estados(models.Model):
    edo = models.CharField(max_length=3, blank=True, null=True)
    nombre = models.CharField(max_length=20, blank=True, null=True)
    pais = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estados'


class Hclinica(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    hora = models.TimeField(blank=True, null=True)
    padcronicos = models.CharField(max_length=1, blank=True, null=True)
    padinfecto = models.CharField(max_length=1, blank=True, null=True)
    padalergicos = models.CharField(max_length=1, blank=True, null=True)
    padtraumaticos = models.CharField(max_length=1, blank=True, null=True)
    padconsumo = models.CharField(max_length=1, blank=True, null=True)
    padmentales = models.CharField(max_length=1, blank=True, null=True)
    padotras = models.CharField(max_length=1, blank=True, null=True)
    hercronicos = models.CharField(max_length=1, blank=True, null=True)
    herinfecto = models.CharField(max_length=1, blank=True, null=True)
    heralergicos = models.CharField(max_length=1, blank=True, null=True)
    hertraumaticos = models.CharField(max_length=1, blank=True, null=True)
    herconsumo = models.CharField(max_length=1, blank=True, null=True)
    hermentales = models.CharField(max_length=1, blank=True, null=True)
    herotras = models.CharField(max_length=1, blank=True, null=True)
    concronicos = models.CharField(max_length=1, blank=True, null=True)
    coninfecto = models.CharField(max_length=1, blank=True, null=True)
    conalergicos = models.CharField(max_length=1, blank=True, null=True)
    contraumaticos = models.CharField(max_length=1, blank=True, null=True)
    conconsumo = models.CharField(max_length=1, blank=True, null=True)
    conmentales = models.CharField(max_length=1, blank=True, null=True)
    conotras = models.CharField(max_length=1, blank=True, null=True)
    hijcronicos = models.CharField(max_length=1, blank=True, null=True)
    hijinfecto = models.CharField(max_length=1, blank=True, null=True)
    hijalergicos = models.CharField(max_length=1, blank=True, null=True)
    hijtraumaticos = models.CharField(max_length=1, blank=True, null=True)
    hijconsumo = models.CharField(max_length=1, blank=True, null=True)
    hijmentales = models.CharField(max_length=1, blank=True, null=True)
    hijotras = models.CharField(max_length=1, blank=True, null=True)
    colcronicos = models.CharField(max_length=1, blank=True, null=True)
    colinfecto = models.CharField(max_length=1, blank=True, null=True)
    colalergicos = models.CharField(max_length=1, blank=True, null=True)
    coltraumaticos = models.CharField(max_length=1, blank=True, null=True)
    colconsumo = models.CharField(max_length=1, blank=True, null=True)
    colmentales = models.CharField(max_length=1, blank=True, null=True)
    colotras = models.CharField(max_length=1, blank=True, null=True)
    cncronicos = models.CharField(max_length=1, blank=True, null=True)
    cninfecto = models.CharField(max_length=1, blank=True, null=True)
    cnalergicos = models.CharField(max_length=1, blank=True, null=True)
    cntraumaticos = models.CharField(max_length=1, blank=True, null=True)
    cnconsumo = models.CharField(max_length=1, blank=True, null=True)
    cnmehtales = models.CharField(max_length=1, blank=True, null=True)
    cnotras = models.CharField(max_length=1, blank=True, null=True)
    bano = models.SmallIntegerField(blank=True, null=True)
    urbana = models.CharField(max_length=1, blank=True, null=True)
    rural = models.CharField(max_length=1, blank=True, null=True)
    servicios = models.CharField(max_length=1, blank=True, null=True)
    contexto = models.CharField(max_length=1, blank=True, null=True)
    inmunizacion = models.SmallIntegerField(blank=True, null=True)
    alimentacion = models.CharField(max_length=1, blank=True, null=True)
    actividad = models.CharField(max_length=1, blank=True, null=True)
    enfactual = models.CharField(max_length=30, blank=True, null=True)
    alergias = models.CharField(max_length=30, blank=True, null=True)
    traumaticos = models.CharField(max_length=30, blank=True, null=True)
    quirurgico = models.CharField(max_length=1, blank=True, null=True)
    hospitalizacion = models.CharField(max_length=1, blank=True, null=True)
    transfuciones = models.CharField(max_length=1, blank=True, null=True)
    adicciones = models.CharField(max_length=1, blank=True, null=True)
    notasadiccion = models.CharField(max_length=40, blank=True, null=True)
    internamientos = models.CharField(max_length=1, blank=True, null=True)
    notasinternamientos = models.CharField(max_length=40, blank=True, null=True)
    padecimiento = models.CharField(max_length=100, blank=True, null=True)
    digestivo = models.CharField(max_length=100, blank=True, null=True)
    nodigestivo = models.CharField(max_length=1, blank=True, null=True)
    cardio = models.CharField(max_length=100, blank=True, null=True)
    nocardio = models.CharField(max_length=1, blank=True, null=True)
    respiratorio = models.CharField(max_length=100, blank=True, null=True)
    norespiratorio = models.CharField(max_length=1, blank=True, null=True)
    urinario = models.CharField(max_length=100, blank=True, null=True)
    nourinario = models.CharField(max_length=1, blank=True, null=True)
    genital = models.CharField(max_length=100, blank=True, null=True)
    nogenital = models.CharField(max_length=1, blank=True, null=True)
    hematologico = models.CharField(max_length=100, blank=True, null=True)
    nohematologico = models.CharField(max_length=1, blank=True, null=True)
    endocrino = models.CharField(max_length=100, blank=True, null=True)
    noendocrino = models.CharField(max_length=1, blank=True, null=True)
    osteomuscular = models.CharField(max_length=100, blank=True, null=True)
    noosteomuscular = models.CharField(max_length=1, blank=True, null=True)
    nervioso = models.CharField(max_length=100, blank=True, null=True)
    nonervioso = models.CharField(max_length=1, blank=True, null=True)
    sensorial = models.CharField(max_length=100, blank=True, null=True)
    nosensorial = models.CharField(max_length=1, blank=True, null=True)
    psicomatico = models.CharField(max_length=100, blank=True, null=True)
    nopsicomatico = models.CharField(max_length=1, blank=True, null=True)
    ta = models.CharField(max_length=10, blank=True, null=True)
    fc = models.CharField(max_length=10, blank=True, null=True)
    fr = models.CharField(max_length=10, blank=True, null=True)
    t = models.CharField(max_length=10, blank=True, null=True)
    pco2 = models.CharField(max_length=10, blank=True, null=True)
    glucosa = models.CharField(max_length=10, blank=True, null=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    imc = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    talla = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    cabeza = models.CharField(max_length=1, blank=True, null=True)
    cabello = models.CharField(max_length=1, blank=True, null=True)
    cicatriz = models.CharField(max_length=30, blank=True, null=True)
    pupilas = models.CharField(max_length=1, blank=True, null=True)
    faringe = models.CharField(max_length=1, blank=True, null=True)
    amigdalas = models.CharField(max_length=1, blank=True, null=True)
    nariz = models.CharField(max_length=1, blank=True, null=True)
    adenomegalias = models.CharField(max_length=1, blank=True, null=True)
    cabezaobs = models.CharField(max_length=100, blank=True, null=True)
    cuello = models.CharField(max_length=1, blank=True, null=True)
    traquea = models.CharField(max_length=1, blank=True, null=True)
    tiroides = models.CharField(max_length=1, blank=True, null=True)
    cueadeno = models.CharField(max_length=1, blank=True, null=True)
    pulsos = models.CharField(max_length=1, blank=True, null=True)
    cuelloobs = models.CharField(max_length=100, blank=True, null=True)
    torax = models.CharField(max_length=1, blank=True, null=True)
    respiratorios = models.CharField(max_length=1, blank=True, null=True)
    campos = models.CharField(max_length=1, blank=True, null=True)
    ruidos = models.CharField(max_length=1, blank=True, null=True)
    adenoaxilar = models.CharField(max_length=1, blank=True, null=True)
    toraxobs = models.CharField(max_length=100, blank=True, null=True)
    abdomen = models.CharField(max_length=1, blank=True, null=True)
    dolor = models.CharField(max_length=1, blank=True, null=True)
    viceromegalias = models.CharField(max_length=1, blank=True, null=True)
    peristalsis = models.CharField(max_length=1, blank=True, null=True)
    abdomenobs = models.CharField(max_length=100, blank=True, null=True)
    superiores = models.CharField(max_length=1, blank=True, null=True)
    inferiores = models.CharField(max_length=1, blank=True, null=True)
    miembrosobs = models.CharField(max_length=100, blank=True, null=True)
    genitales = models.CharField(max_length=1, blank=True, null=True)
    genitalesobs = models.CharField(max_length=50, blank=True, null=True)
    examenes = models.TextField(blank=True, null=True)
    edad = models.CharField(max_length=1, blank=True, null=True)
    posicion = models.CharField(max_length=1, blank=True, null=True)
    actitud = models.CharField(max_length=1, blank=True, null=True)
    inspeccionobs = models.CharField(max_length=100, blank=True, null=True)
    fluidez = models.CharField(max_length=1, blank=True, null=True)
    lenguaje = models.CharField(max_length=1, blank=True, null=True)
    lenguajeobs = models.CharField(max_length=100, blank=True, null=True)
    orientado = models.CharField(max_length=1, blank=True, null=True)
    memoria = models.CharField(max_length=1, blank=True, null=True)
    funcionesobs = models.CharField(max_length=100, blank=True, null=True)
    afectividad = models.CharField(max_length=1, blank=True, null=True)
    afectividadobs = models.CharField(max_length=100, blank=True, null=True)
    sensopercepcion = models.CharField(max_length=1, blank=True, null=True)
    sensopercepcionobs = models.CharField(max_length=100, blank=True, null=True)
    ideacion = models.CharField(max_length=1, blank=True, null=True)
    ideacionobs = models.CharField(max_length=100, blank=True, null=True)
    dependencia = models.TextField(blank=True, null=True)
    otros = models.CharField(max_length=30, blank=True, null=True)
    pronostico = models.CharField(max_length=100, blank=True, null=True)
    residencia = models.CharField(max_length=1, blank=True, null=True)
    dieta = models.CharField(max_length=1, blank=True, null=True)
    otro = models.CharField(max_length=100, blank=True, null=True)
    justificacion = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    atendio = models.CharField(max_length=60, blank=True, null=True)
    cedula = models.CharField(max_length=30, blank=True, null=True)
    expedidapor = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hclinica'


class Hojaatencionps(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    lateralidad = models.CharField(max_length=1, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    motivo = models.CharField(max_length=20, blank=True, null=True)
    antecedentes = models.TextField(blank=True, null=True)
    instrumentos = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    resultados = models.TextField(blank=True, null=True)
    diagnosticos = models.TextField(blank=True, null=True)
    psicologo = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hojaatencionps'


class Internos(models.Model):
    numeroexpediente = models.CharField(max_length=10, blank=True, null=True)
    fechaingreso = models.DateField(blank=True, null=True)
    fsalidareal = models.DateField(blank=True, null=True)
    apaterno = models.CharField(max_length=20, blank=True, null=True)
    amaterno = models.CharField(max_length=20, blank=True, null=True)
    nombre = models.CharField(max_length=20, blank=True, null=True)
    nombrecompleto = models.CharField(max_length=60, blank=True, null=True)
    edad = models.SmallIntegerField(blank=True, null=True)
    sexo = models.CharField(max_length=1, blank=True, null=True)
    estadocivil = models.CharField(max_length=1, blank=True, null=True)
    calleynumero = models.CharField(max_length=40, blank=True, null=True)
    colonia = models.CharField(max_length=30, blank=True, null=True)
    ciudad = models.CharField(max_length=10, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    pais = models.CharField(max_length=3, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    escolaridad = models.CharField(max_length=20, blank=True, null=True)
    ocupacion = models.CharField(max_length=20, blank=True, null=True)
    tiempodesempleado = models.CharField(max_length=10, blank=True, null=True)
    conquienvive = models.CharField(max_length=1, blank=True, null=True)
    responsable = models.CharField(max_length=40, blank=True, null=True)
    rcalle = models.CharField(max_length=40, blank=True, null=True)
    rcolonia = models.CharField(max_length=30, blank=True, null=True)
    rciudad = models.CharField(max_length=10, blank=True, null=True)
    restado = models.CharField(max_length=2, blank=True, null=True)
    rpais = models.CharField(max_length=3, blank=True, null=True)
    rtelefono = models.CharField(max_length=20, blank=True, null=True)
    dpadres = models.SmallIntegerField(blank=True, null=True)
    dhijos = models.SmallIntegerField(blank=True, null=True)
    dconyugue = models.SmallIntegerField(blank=True, null=True)
    dotros = models.SmallIntegerField(blank=True, null=True)
    comentarios = models.TextField(blank=True, null=True)
    serviciosmedicos = models.CharField(max_length=20, blank=True, null=True)
    afiliasion = models.CharField(max_length=10, blank=True, null=True)
    codigopostal = models.CharField(max_length=6, blank=True, null=True)
    telefonotrabajo = models.CharField(max_length=15, blank=True, null=True)
    tipoingreso = models.CharField(max_length=1, blank=True, null=True)
    proviene = models.CharField(max_length=2, blank=True, null=True)
    provieneotro = models.CharField(max_length=20, blank=True, null=True)
    acudecon = models.CharField(max_length=1, blank=True, null=True)
    acudeotro = models.CharField(max_length=20, blank=True, null=True)
    enfermedadesotro = models.CharField(max_length=20, blank=True, null=True)
    tomamedicinas = models.CharField(max_length=1, blank=True, null=True)
    especifique = models.CharField(max_length=20, blank=True, null=True)
    porcualingresa = models.CharField(max_length=20, blank=True, null=True)
    embarazo = models.SmallIntegerField(blank=True, null=True)
    psiquiatricas = models.SmallIntegerField(blank=True, null=True)
    fisicas = models.SmallIntegerField(blank=True, null=True)
    contagiosas = models.SmallIntegerField(blank=True, null=True)
    padecimientos = models.SmallIntegerField(blank=True, null=True)
    basiloscopia = models.SmallIntegerField(blank=True, null=True)
    alcohol = models.SmallIntegerField(blank=True, null=True)
    anfetaminas = models.SmallIntegerField(blank=True, null=True)
    secantes = models.SmallIntegerField(blank=True, null=True)
    marihuana = models.SmallIntegerField(blank=True, null=True)
    rohypnol = models.SmallIntegerField(blank=True, null=True)
    analgesicos = models.SmallIntegerField(blank=True, null=True)
    disolventes = models.SmallIntegerField(blank=True, null=True)
    cocaina = models.SmallIntegerField(blank=True, null=True)
    opio = models.SmallIntegerField(blank=True, null=True)
    cristal = models.SmallIntegerField(blank=True, null=True)
    numeroreuniones = models.SmallIntegerField(blank=True, null=True)
    diversasactividades = models.CharField(max_length=30, blank=True, null=True)
    duracion = models.CharField(max_length=15, blank=True, null=True)
    quieninformo = models.CharField(max_length=30, blank=True, null=True)
    aportacioninicial = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    aportaciontotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    lugarnac = models.CharField(max_length=20, blank=True, null=True)
    estadonac = models.CharField(max_length=3, blank=True, null=True)
    paisnac = models.CharField(max_length=3, blank=True, null=True)
    motivoegreso = models.TextField(blank=True, null=True)
    resumenanexo = models.TextField(blank=True, null=True)
    estadodesalud = models.TextField(blank=True, null=True)
    prevencionrecaidas = models.TextField(blank=True, null=True)
    proxsesconind = models.DateField(blank=True, null=True)
    proxsesconfam = models.DateField(blank=True, null=True)
    proxsescongru = models.DateField(blank=True, null=True)
    periodopago = models.SmallIntegerField(blank=True, null=True)
    proximasesionps = models.DateField(blank=True, null=True)
    proximasesiong = models.DateField(blank=True, null=True)
    reciboinicial = models.SmallIntegerField(blank=True, null=True)
    proxseseg = models.DateField(blank=True, null=True)
    fechariesgo = models.DateField(blank=True, null=True)
    nacionalidad = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'internos'


class MappDatosgrales(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True)
    calleynumero = models.CharField(max_length=50, blank=True, null=True)
    colonia = models.CharField(max_length=50, blank=True, null=True)
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    sitioweb = models.CharField(max_length=50, blank=True, null=True)
    correoelectronico = models.CharField(max_length=50, blank=True, null=True)
    rfc = models.CharField(max_length=13, blank=True, null=True)
    cp = models.CharField(max_length=6, blank=True, null=True)
    expediente = models.SmallIntegerField(blank=True, null=True)
    receta = models.SmallIntegerField(blank=True, null=True)
    recibootros = models.SmallIntegerField(blank=True, null=True)
    sesiong = models.SmallIntegerField(blank=True, null=True)
    recibo = models.SmallIntegerField(blank=True, null=True)
    responsable = models.CharField(max_length=30, blank=True, null=True)
    cedula = models.CharField(max_length=20, blank=True, null=True)
    cargo = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mapp_datosgrales'


class MappUsuarios(models.Model):
    id = models.BigAutoField(primary_key=True)
    usuario = models.BigIntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=30, blank=True, null=True)
    cargo = models.CharField(max_length=20, blank=True, null=True)
    permisos = models.CharField(max_length=5, blank=True, null=True)
    password = models.CharField(max_length=10, blank=True, null=True)
    cedula = models.CharField(max_length=20, blank=True, null=True)
    expedidapor = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mapp_usuarios'


class Marcadores(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    usadroga = models.SmallIntegerField(blank=True, null=True)
    masdecincoveces = models.SmallIntegerField(blank=True, null=True)
    marcador1 = models.SmallIntegerField(blank=True, null=True)
    marcador2 = models.SmallIntegerField(blank=True, null=True)
    marcador3 = models.SmallIntegerField(blank=True, null=True)
    marcador4 = models.SmallIntegerField(blank=True, null=True)
    marcador5 = models.SmallIntegerField(blank=True, null=True)
    marcador6 = models.SmallIntegerField(blank=True, null=True)
    marcador7 = models.SmallIntegerField(blank=True, null=True)
    marcador8 = models.SmallIntegerField(blank=True, null=True)
    marcador9 = models.SmallIntegerField(blank=True, null=True)
    marcador10 = models.SmallIntegerField(blank=True, null=True)
    marcador11 = models.SmallIntegerField(blank=True, null=True)
    marcador12 = models.SmallIntegerField(blank=True, null=True)
    marcador13 = models.SmallIntegerField(blank=True, null=True)
    marcador14 = models.SmallIntegerField(blank=True, null=True)
    marcador15 = models.SmallIntegerField(blank=True, null=True)
    marcador16 = models.SmallIntegerField(blank=True, null=True)
    marcador17 = models.SmallIntegerField(blank=True, null=True)
    marcadorfecha = models.DateField(blank=True, null=True)
    marcadoruser = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'marcadores'


class Medico(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    motivo = models.CharField(max_length=50, blank=True, null=True)
    padecimiento = models.TextField(blank=True, null=True)
    sintomas = models.TextField(blank=True, null=True)
    tratamientos = models.TextField(blank=True, null=True)
    ta = models.CharField(max_length=10, blank=True, null=True)
    fc = models.CharField(max_length=10, blank=True, null=True)
    fr = models.CharField(max_length=10, blank=True, null=True)
    temp = models.CharField(max_length=5, blank=True, null=True)
    peso = models.CharField(max_length=10, blank=True, null=True)
    talla = models.CharField(max_length=10, blank=True, null=True)
    exploracion = models.TextField(blank=True, null=True)
    examenmental = models.TextField(blank=True, null=True)
    diagnostico = models.CharField(max_length=50, blank=True, null=True)
    pronostico = models.CharField(max_length=50, blank=True, null=True)
    tratamientosugerido = models.TextField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    medico = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medico'


class Movimientos(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    concepto = models.CharField(max_length=2, blank=True, null=True)
    referencia = models.CharField(max_length=25, blank=True, null=True)
    tipo = models.CharField(max_length=2, blank=True, null=True)
    cargo = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    abono = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    saldo = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    recibo = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movimientos'


class Notasevolucionps(models.Model):
    expediente = models.CharField(max_length=20, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    sesion = models.SmallIntegerField(blank=True, null=True)
    objetivo = models.TextField(blank=True, null=True)
    resumen = models.TextField(blank=True, null=True)
    resultado = models.TextField(blank=True, null=True)
    objetivoyplan = models.TextField(blank=True, null=True)
    actividades = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    psicologo = models.SmallIntegerField(blank=True, null=True)
    fechaproxima = models.DateField(blank=True, null=True)
    cerrada = models.SmallIntegerField(blank=True, null=True)
    individualogrupal = models.SmallIntegerField(blank=True, null=True)
    selograron = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notasevolucionps'


class Otros(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    concepto = models.CharField(max_length=2, blank=True, null=True)
    referencia = models.CharField(max_length=30, blank=True, null=True)
    tipo = models.CharField(max_length=2, blank=True, null=True)
    cargo = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    abono = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    recibo = models.SmallIntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'otros'


class Paises(models.Model):
    pais = models.CharField(max_length=3, blank=True, null=True)
    nombre = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'paises'


class Participantes(models.Model):
    sesion = models.SmallIntegerField(blank=True, null=True)
    expediente = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'participantes'


class Paso(models.Model):
    numeroexpediente = models.CharField(max_length=10, blank=True, null=True)
    fechaingreso = models.DateField(blank=True, null=True)
    fsalidareal = models.DateField(blank=True, null=True)
    apaterno = models.CharField(max_length=20, blank=True, null=True)
    amaterno = models.CharField(max_length=20, blank=True, null=True)
    nombre = models.CharField(max_length=20, blank=True, null=True)
    nombrecompleto = models.CharField(max_length=60, blank=True, null=True)
    edad = models.SmallIntegerField(blank=True, null=True)
    sexo = models.CharField(max_length=1, blank=True, null=True)
    estadocivil = models.CharField(max_length=1, blank=True, null=True)
    calleynumero = models.CharField(max_length=40, blank=True, null=True)
    colonia = models.CharField(max_length=20, blank=True, null=True)
    ciudad = models.CharField(max_length=10, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    pais = models.CharField(max_length=3, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    escolaridad = models.CharField(max_length=20, blank=True, null=True)
    ocupacion = models.CharField(max_length=20, blank=True, null=True)
    tiempodesempleado = models.CharField(max_length=10, blank=True, null=True)
    conquienvive = models.CharField(max_length=1, blank=True, null=True)
    responsable = models.CharField(max_length=40, blank=True, null=True)
    rcalle = models.CharField(max_length=40, blank=True, null=True)
    rcolonia = models.CharField(max_length=20, blank=True, null=True)
    rciudad = models.CharField(max_length=10, blank=True, null=True)
    restado = models.CharField(max_length=2, blank=True, null=True)
    rpais = models.CharField(max_length=3, blank=True, null=True)
    rtelefono = models.CharField(max_length=20, blank=True, null=True)
    dpadres = models.SmallIntegerField(blank=True, null=True)
    dhijos = models.SmallIntegerField(blank=True, null=True)
    dconyugue = models.SmallIntegerField(blank=True, null=True)
    dotros = models.SmallIntegerField(blank=True, null=True)
    comentarios = models.TextField(blank=True, null=True)
    serviciosmedicos = models.CharField(max_length=20, blank=True, null=True)
    afiliasion = models.CharField(max_length=10, blank=True, null=True)
    codigopostal = models.CharField(max_length=6, blank=True, null=True)
    telefonotrabajo = models.CharField(max_length=15, blank=True, null=True)
    tipoingreso = models.CharField(max_length=1, blank=True, null=True)
    proviene = models.CharField(max_length=2, blank=True, null=True)
    provieneotro = models.CharField(max_length=20, blank=True, null=True)
    acudecon = models.CharField(max_length=1, blank=True, null=True)
    acudeotro = models.CharField(max_length=20, blank=True, null=True)
    enfermedadesotro = models.CharField(max_length=20, blank=True, null=True)
    tomamedicinas = models.CharField(max_length=1, blank=True, null=True)
    especifique = models.CharField(max_length=20, blank=True, null=True)
    porcualingresa = models.CharField(max_length=20, blank=True, null=True)
    psiquiatricas = models.SmallIntegerField(blank=True, null=True)
    fisicas = models.SmallIntegerField(blank=True, null=True)
    contagiosas = models.SmallIntegerField(blank=True, null=True)
    padecimientos = models.SmallIntegerField(blank=True, null=True)
    basiloscopia = models.SmallIntegerField(blank=True, null=True)
    alcohol = models.SmallIntegerField(blank=True, null=True)
    anfetaminas = models.SmallIntegerField(blank=True, null=True)
    secantes = models.SmallIntegerField(blank=True, null=True)
    marihuana = models.SmallIntegerField(blank=True, null=True)
    rohypnol = models.SmallIntegerField(blank=True, null=True)
    analgesicos = models.SmallIntegerField(blank=True, null=True)
    disolventes = models.SmallIntegerField(blank=True, null=True)
    cocaina = models.SmallIntegerField(blank=True, null=True)
    opio = models.SmallIntegerField(blank=True, null=True)
    cristal = models.SmallIntegerField(blank=True, null=True)
    numeroreuniones = models.SmallIntegerField(blank=True, null=True)
    diversasactividades = models.CharField(max_length=30, blank=True, null=True)
    duracion = models.CharField(max_length=15, blank=True, null=True)
    quieninformo = models.CharField(max_length=30, blank=True, null=True)
    aportacioninicial = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    aportaciontotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    lugarnac = models.CharField(max_length=20, blank=True, null=True)
    estadonac = models.CharField(max_length=3, blank=True, null=True)
    paisnac = models.CharField(max_length=3, blank=True, null=True)
    motivoegreso = models.TextField(blank=True, null=True)
    resumenanexo = models.TextField(blank=True, null=True)
    estadodesalud = models.TextField(blank=True, null=True)
    prevencionrecaidas = models.TextField(blank=True, null=True)
    proxsesconind = models.DateField(blank=True, null=True)
    proxsesconfam = models.DateField(blank=True, null=True)
    proxsescongru = models.DateField(blank=True, null=True)
    periodopago = models.SmallIntegerField(blank=True, null=True)
    proximasesionps = models.DateField(blank=True, null=True)
    proximasesiong = models.DateField(blank=True, null=True)
    reciboinicial = models.SmallIntegerField(blank=True, null=True)
    proxseseg = models.DateField(blank=True, null=True)
    fechariesgo = models.DateField(blank=True, null=True)
    embarazo = models.SmallIntegerField(blank=True, null=True)
    nacionalidad = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'paso'


class Pconsejeria(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    id = models.CharField(max_length=10, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    alcoholydrogas = models.TextField(blank=True, null=True)
    fisicaymental = models.TextField(blank=True, null=True)
    areasdelavida = models.TextField(blank=True, null=True)
    metas = models.TextField(blank=True, null=True)
    objetivos = models.TextField(blank=True, null=True)
    compromiso = models.TextField(blank=True, null=True)
    logros = models.TextField(blank=True, null=True)
    metasareavida = models.TextField(blank=True, null=True)
    prevencion = models.TextField(blank=True, null=True)
    consejero = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pconsejeria'


class Psicosis(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    pp1 = models.SmallIntegerField(blank=True, null=True)
    pp2 = models.SmallIntegerField(blank=True, null=True)
    pp3 = models.SmallIntegerField(blank=True, null=True)
    pp4 = models.SmallIntegerField(blank=True, null=True)
    pp5 = models.SmallIntegerField(blank=True, null=True)
    pp6 = models.SmallIntegerField(blank=True, null=True)
    pp7 = models.SmallIntegerField(blank=True, null=True)
    pp8 = models.SmallIntegerField(blank=True, null=True)
    pp9 = models.SmallIntegerField(blank=True, null=True)
    pp10 = models.SmallIntegerField(blank=True, null=True)
    pp11 = models.SmallIntegerField(blank=True, null=True)
    pp12 = models.SmallIntegerField(blank=True, null=True)
    pp13 = models.SmallIntegerField(blank=True, null=True)
    pp14 = models.SmallIntegerField(blank=True, null=True)
    pp15 = models.SmallIntegerField(blank=True, null=True)
    pp16 = models.SmallIntegerField(blank=True, null=True)
    pp17 = models.SmallIntegerField(blank=True, null=True)
    fechapsicosis = models.DateField(blank=True, null=True)
    puntajepsicosis = models.SmallIntegerField(blank=True, null=True)
    consejeropsicosis = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'psicosis'


class Razones(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    hora = models.TimeField(blank=True, null=True)
    nodesesion = models.SmallIntegerField(blank=True, null=True)
    factores = models.TextField(blank=True, null=True)
    motivos = models.TextField(blank=True, null=True)
    sabias = models.CharField(max_length=1, blank=True, null=True)
    cualesriesgos = models.TextField(blank=True, null=True)
    motivosaexponerte = models.TextField(blank=True, null=True)
    razonesidetificadas = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    consejero = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'razones'


class Recetas(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    historial = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recetas'


class Recibos(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    expediente = models.CharField(max_length=10, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    importe = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    quienpago = models.CharField(max_length=40, blank=True, null=True)
    del_field = models.DateField(db_column='del', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    al = models.DateField(blank=True, null=True)
    observaciones = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recibos'


class Recibosotros(models.Model):
    numero = models.SmallIntegerField(blank=True, null=True)
    expediente = models.CharField(max_length=10, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    importe = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    quienpago = models.CharField(max_length=40, blank=True, null=True)
    observaciones = models.CharField(max_length=50, blank=True, null=True)
    del_field = models.DateField(db_column='del', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    al = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recibosotros'


class Riesgo(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    fechariesgo = models.DateField(blank=True, null=True)
    consejeroiesgo = models.SmallIntegerField(blank=True, null=True)
    pr1 = models.SmallIntegerField(blank=True, null=True)
    pr2 = models.SmallIntegerField(blank=True, null=True)
    pr3 = models.SmallIntegerField(blank=True, null=True)
    pr4 = models.SmallIntegerField(blank=True, null=True)
    pr5 = models.SmallIntegerField(blank=True, null=True)
    pr6 = models.SmallIntegerField(blank=True, null=True)
    pr7 = models.SmallIntegerField(blank=True, null=True)
    pr8 = models.SmallIntegerField(blank=True, null=True)
    pr9 = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'riesgo'


class Rpertenencias(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    pertenencias = models.TextField(blank=True, null=True)
    quienrecibe = models.CharField(max_length=20, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    responsable = models.CharField(max_length=20, blank=True, null=True)
    testigo = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rpertenencias'


class Rseguimiento(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    consejero = models.SmallIntegerField(blank=True, null=True)
    sesion = models.SmallIntegerField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    periodo = models.SmallIntegerField(blank=True, null=True)
    otro = models.CharField(max_length=10, blank=True, null=True)
    tipo = models.SmallIntegerField(blank=True, null=True)
    objetivo = models.CharField(max_length=40, blank=True, null=True)
    plann = models.TextField(blank=True, null=True)
    tareas = models.TextField(blank=True, null=True)
    aspectos = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    siguientecita = models.DateField(blank=True, null=True)
    consumo = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rseguimiento'


class Sdevida(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    fechasdevida = models.DateField(blank=True, null=True)
    sp1 = models.SmallIntegerField(blank=True, null=True)
    sp2 = models.SmallIntegerField(blank=True, null=True)
    sp3 = models.SmallIntegerField(blank=True, null=True)
    sp4 = models.SmallIntegerField(blank=True, null=True)
    sp5 = models.SmallIntegerField(blank=True, null=True)
    sp6 = models.SmallIntegerField(blank=True, null=True)
    sp7 = models.SmallIntegerField(blank=True, null=True)
    sp8 = models.SmallIntegerField(blank=True, null=True)
    sp9 = models.SmallIntegerField(blank=True, null=True)
    sp10 = models.SmallIntegerField(blank=True, null=True)
    sp11 = models.SmallIntegerField(blank=True, null=True)
    sp12 = models.SmallIntegerField(blank=True, null=True)
    consejerosdevida = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sdevida'


class Seguimiento(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    fechayhora = models.DateField(blank=True, null=True)
    seguimiento = models.SmallIntegerField(blank=True, null=True)
    periodo = models.SmallIntegerField(blank=True, null=True)
    tipo = models.SmallIntegerField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    conquienvive = models.CharField(max_length=1, blank=True, null=True)
    situacionlaboral = models.SmallIntegerField(blank=True, null=True)
    viveotro = models.CharField(max_length=20, blank=True, null=True)
    laboralotro = models.CharField(max_length=20, blank=True, null=True)
    quemanifiesta = models.SmallIntegerField(blank=True, null=True)
    s1 = models.SmallIntegerField(blank=True, null=True)
    fh1 = models.CharField(max_length=20, blank=True, null=True)
    f1 = models.SmallIntegerField(blank=True, null=True)
    fo1 = models.CharField(max_length=10, blank=True, null=True)
    fr1 = models.CharField(max_length=20, blank=True, null=True)
    ca1 = models.CharField(max_length=20, blank=True, null=True)
    co1 = models.CharField(max_length=20, blank=True, null=True)
    s2 = models.SmallIntegerField(blank=True, null=True)
    fh2 = models.CharField(max_length=20, blank=True, null=True)
    f2 = models.CharField(max_length=20, blank=True, null=True)
    fo2 = models.CharField(max_length=20, blank=True, null=True)
    fr2 = models.CharField(max_length=20, blank=True, null=True)
    ca2 = models.CharField(max_length=20, blank=True, null=True)
    co2 = models.CharField(max_length=20, blank=True, null=True)
    s3 = models.SmallIntegerField(blank=True, null=True)
    fh3 = models.CharField(max_length=20, blank=True, null=True)
    f3 = models.CharField(max_length=20, blank=True, null=True)
    fr3 = models.CharField(max_length=20, blank=True, null=True)
    ca3 = models.CharField(max_length=20, blank=True, null=True)
    co3 = models.CharField(max_length=20, blank=True, null=True)
    s4 = models.SmallIntegerField(blank=True, null=True)
    fh4 = models.CharField(max_length=20, blank=True, null=True)
    f4 = models.CharField(max_length=20, blank=True, null=True)
    fr4 = models.CharField(max_length=20, blank=True, null=True)
    ca4 = models.CharField(max_length=20, blank=True, null=True)
    co4 = models.CharField(max_length=20, blank=True, null=True)
    s5 = models.SmallIntegerField(blank=True, null=True)
    fh5 = models.CharField(max_length=20, blank=True, null=True)
    f5 = models.CharField(max_length=20, blank=True, null=True)
    fr5 = models.CharField(max_length=20, blank=True, null=True)
    ca5 = models.CharField(max_length=20, blank=True, null=True)
    co5 = models.CharField(max_length=20, blank=True, null=True)
    s6 = models.SmallIntegerField(blank=True, null=True)
    fh6 = models.CharField(max_length=20, blank=True, null=True)
    f6 = models.CharField(max_length=20, blank=True, null=True)
    fr6 = models.CharField(max_length=20, blank=True, null=True)
    ca6 = models.CharField(max_length=20, blank=True, null=True)
    co6 = models.CharField(max_length=20, blank=True, null=True)
    s7 = models.SmallIntegerField(blank=True, null=True)
    fh7 = models.CharField(max_length=20, blank=True, null=True)
    f7 = models.CharField(max_length=20, blank=True, null=True)
    fr7 = models.CharField(max_length=20, blank=True, null=True)
    ca7 = models.CharField(max_length=20, blank=True, null=True)
    co7 = models.CharField(max_length=20, blank=True, null=True)
    s8 = models.SmallIntegerField(blank=True, null=True)
    fh8 = models.CharField(max_length=20, blank=True, null=True)
    f8 = models.CharField(max_length=20, blank=True, null=True)
    fr8 = models.CharField(max_length=20, blank=True, null=True)
    ca8 = models.CharField(max_length=20, blank=True, null=True)
    co8 = models.CharField(max_length=20, blank=True, null=True)
    s9 = models.SmallIntegerField(blank=True, null=True)
    fh9 = models.CharField(max_length=20, blank=True, null=True)
    f9 = models.CharField(max_length=20, blank=True, null=True)
    fr9 = models.CharField(max_length=20, blank=True, null=True)
    ca9 = models.CharField(max_length=20, blank=True, null=True)
    co9 = models.CharField(max_length=20, blank=True, null=True)
    s10 = models.SmallIntegerField(blank=True, null=True)
    fh10 = models.CharField(max_length=20, blank=True, null=True)
    f10 = models.CharField(max_length=20, blank=True, null=True)
    fr10 = models.CharField(max_length=20, blank=True, null=True)
    ca10 = models.CharField(max_length=20, blank=True, null=True)
    co10 = models.CharField(max_length=20, blank=True, null=True)
    s11 = models.SmallIntegerField(blank=True, null=True)
    fh11 = models.CharField(max_length=20, blank=True, null=True)
    f11 = models.CharField(max_length=20, blank=True, null=True)
    fr11 = models.CharField(max_length=20, blank=True, null=True)
    ca11 = models.CharField(max_length=20, blank=True, null=True)
    co11 = models.CharField(max_length=20, blank=True, null=True)
    obstaculos = models.CharField(max_length=40, blank=True, null=True)
    problemasdesalud = models.SmallIntegerField(blank=True, null=True)
    cual = models.CharField(max_length=40, blank=True, null=True)
    toimandomedicamento = models.SmallIntegerField(blank=True, null=True)
    cualmedicamento = models.CharField(max_length=40, blank=True, null=True)
    diasenhospital = models.SmallIntegerField(blank=True, null=True)
    sehasentidotriste = models.SmallIntegerField(blank=True, null=True)
    causa = models.CharField(max_length=40, blank=True, null=True)
    pensado = models.SmallIntegerField(blank=True, null=True)
    dequeforma = models.CharField(max_length=40, blank=True, null=True)
    quitarselavida = models.SmallIntegerField(blank=True, null=True)
    cuandoocurrio = models.CharField(max_length=40, blank=True, null=True)
    ansioso = models.SmallIntegerField(blank=True, null=True)
    ansiosoporque = models.CharField(max_length=40, blank=True, null=True)
    sinohaconsumido = models.CharField(max_length=50, blank=True, null=True)
    utilizado = models.SmallIntegerField(blank=True, null=True)
    tratamiento = models.SmallIntegerField(blank=True, null=True)
    quetratamiento = models.CharField(max_length=40, blank=True, null=True)
    metas = models.CharField(max_length=60, blank=True, null=True)
    calidaddevida = models.SmallIntegerField(blank=True, null=True)
    comparacion = models.SmallIntegerField(blank=True, null=True)
    estudioantidoping = models.CharField(max_length=40, blank=True, null=True)
    observaciones = models.CharField(max_length=60, blank=True, null=True)
    consejero = models.SmallIntegerField(blank=True, null=True)
    calleynumero = models.CharField(max_length=40, blank=True, null=True)
    colonia = models.CharField(max_length=20, blank=True, null=True)
    ciudad = models.CharField(max_length=10, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    pais = models.CharField(max_length=3, blank=True, null=True)
    estadocivil = models.CharField(max_length=1, blank=True, null=True)
    otrassustancias = models.CharField(max_length=20, blank=True, null=True)
    suicidarse = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seguimiento'


class Situacionfamiliar(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    quienesintegran = models.TextField(blank=True, null=True)
    hacercosasjuntos = models.SmallIntegerField(blank=True, null=True)
    nadiesepreocupa = models.SmallIntegerField(blank=True, null=True)
    soncalidos = models.SmallIntegerField(blank=True, null=True)
    expresaropciones = models.SmallIntegerField(blank=True, null=True)
    esdesagradable = models.SmallIntegerField(blank=True, null=True)
    enconjunto = models.SmallIntegerField(blank=True, null=True)
    meescucha = models.SmallIntegerField(blank=True, null=True)
    platicoproblemas = models.SmallIntegerField(blank=True, null=True)
    expresamoscarino = models.SmallIntegerField(blank=True, null=True)
    nuncaseresuelven = models.SmallIntegerField(blank=True, null=True)
    conflictograve = models.SmallIntegerField(blank=True, null=True)
    cual = models.CharField(max_length=20, blank=True, null=True)
    papa = models.SmallIntegerField(blank=True, null=True)
    cosumiopapa = models.CharField(max_length=10, blank=True, null=True)
    problemapapa = models.CharField(max_length=20, blank=True, null=True)
    mama = models.SmallIntegerField(blank=True, null=True)
    consumiomama = models.CharField(max_length=10, blank=True, null=True)
    problemamama = models.CharField(max_length=20, blank=True, null=True)
    hermano = models.SmallIntegerField(blank=True, null=True)
    consumiohermano = models.CharField(max_length=10, blank=True, null=True)
    problemahermano = models.CharField(max_length=20, blank=True, null=True)
    amigo = models.SmallIntegerField(blank=True, null=True)
    consumioamigo = models.CharField(max_length=10, blank=True, null=True)
    problemaamigo = models.CharField(max_length=20, blank=True, null=True)
    pareja = models.SmallIntegerField(blank=True, null=True)
    consumiopareja = models.CharField(max_length=10, blank=True, null=True)
    problemapareja = models.CharField(max_length=20, blank=True, null=True)
    familiar = models.SmallIntegerField(blank=True, null=True)
    quien = models.CharField(max_length=10, blank=True, null=True)
    consumiofamiliar = models.CharField(max_length=10, blank=True, null=True)
    problemafamiliar = models.CharField(max_length=20, blank=True, null=True)
    cuandoesta = models.SmallIntegerField(blank=True, null=True)
    ayudarian = models.CharField(max_length=20, blank=True, null=True)
    dejadodehacer = models.CharField(max_length=60, blank=True, null=True)
    relacionadas = models.CharField(max_length=60, blank=True, null=True)
    diasnotrabajados = models.SmallIntegerField(blank=True, null=True)
    vecesperdioempleo = models.SmallIntegerField(blank=True, null=True)
    mejormuerto = models.SmallIntegerField(blank=True, null=True)
    ultimomesintentado = models.SmallIntegerField(blank=True, null=True)
    haintentado = models.SmallIntegerField(blank=True, null=True)
    presentaenfermedad = models.SmallIntegerField(blank=True, null=True)
    cualenfermedad = models.CharField(max_length=20, blank=True, null=True)
    derivadaporuso = models.SmallIntegerField(blank=True, null=True)
    siendoatendido = models.SmallIntegerField(blank=True, null=True)
    cualpadecimiento = models.CharField(max_length=20, blank=True, null=True)
    medicado = models.SmallIntegerField(blank=True, null=True)
    cualmedicina = models.CharField(max_length=30, blank=True, null=True)
    estadointernado = models.SmallIntegerField(blank=True, null=True)
    porque = models.CharField(max_length=20, blank=True, null=True)
    porconsumo = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'situacionfamiliar'


class Tratamientos(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    recibio = models.SmallIntegerField(blank=True, null=True)
    a1 = models.SmallIntegerField(blank=True, null=True)
    d1 = models.SmallIntegerField(blank=True, null=True)
    h1 = models.CharField(max_length=15, blank=True, null=True)
    c1 = models.SmallIntegerField(blank=True, null=True)
    r1 = models.CharField(max_length=20, blank=True, null=True)
    a2 = models.SmallIntegerField(blank=True, null=True)
    d2 = models.SmallIntegerField(blank=True, null=True)
    h2 = models.CharField(max_length=15, blank=True, null=True)
    c2 = models.SmallIntegerField(blank=True, null=True)
    r2 = models.CharField(max_length=20, blank=True, null=True)
    a3 = models.SmallIntegerField(blank=True, null=True)
    d3 = models.SmallIntegerField(blank=True, null=True)
    h3 = models.CharField(max_length=15, blank=True, null=True)
    c3 = models.SmallIntegerField(blank=True, null=True)
    r3 = models.CharField(max_length=20, blank=True, null=True)
    a4 = models.SmallIntegerField(blank=True, null=True)
    d4 = models.SmallIntegerField(blank=True, null=True)
    h4 = models.CharField(max_length=15, blank=True, null=True)
    c4 = models.SmallIntegerField(blank=True, null=True)
    r4 = models.CharField(max_length=20, blank=True, null=True)
    a5 = models.SmallIntegerField(blank=True, null=True)
    d5 = models.SmallIntegerField(blank=True, null=True)
    h5 = models.CharField(max_length=15, blank=True, null=True)
    c5 = models.SmallIntegerField(blank=True, null=True)
    r5 = models.CharField(max_length=20, blank=True, null=True)
    a6 = models.SmallIntegerField(blank=True, null=True)
    d6 = models.SmallIntegerField(blank=True, null=True)
    h6 = models.CharField(max_length=15, blank=True, null=True)
    c6 = models.SmallIntegerField(blank=True, null=True)
    r6 = models.CharField(max_length=20, blank=True, null=True)
    a7 = models.SmallIntegerField(blank=True, null=True)
    d7 = models.SmallIntegerField(blank=True, null=True)
    h7 = models.CharField(max_length=15, blank=True, null=True)
    c7 = models.SmallIntegerField(blank=True, null=True)
    r7 = models.CharField(max_length=20, blank=True, null=True)
    a8 = models.SmallIntegerField(blank=True, null=True)
    d8 = models.SmallIntegerField(blank=True, null=True)
    h8 = models.CharField(max_length=15, blank=True, null=True)
    c8 = models.SmallIntegerField(blank=True, null=True)
    r8 = models.CharField(max_length=20, blank=True, null=True)
    cual = models.CharField(max_length=20, blank=True, null=True)
    cual1 = models.CharField(max_length=20, blank=True, null=True)
    cual2 = models.CharField(max_length=20, blank=True, null=True)
    stisfecho = models.SmallIntegerField(blank=True, null=True)
    meta1 = models.CharField(max_length=100, blank=True, null=True)
    meta2 = models.CharField(max_length=100, blank=True, null=True)
    meta3 = models.CharField(max_length=100, blank=True, null=True)
    meta4 = models.CharField(max_length=100, blank=True, null=True)
    meta5 = models.CharField(max_length=100, blank=True, null=True)
    meta6 = models.CharField(max_length=100, blank=True, null=True)
    meta7 = models.CharField(max_length=100, blank=True, null=True)
    meta8 = models.CharField(max_length=100, blank=True, null=True)
    meta9 = models.CharField(max_length=100, blank=True, null=True)
    meta10 = models.CharField(max_length=100, blank=True, null=True)
    problemas = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tratamientos'


class Usodrogas(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    ad1 = models.CharField(max_length=1, blank=True, null=True)
    ad2 = models.CharField(max_length=1, blank=True, null=True)
    ad3 = models.CharField(max_length=1, blank=True, null=True)
    ad4 = models.CharField(max_length=1, blank=True, null=True)
    ad5 = models.CharField(max_length=1, blank=True, null=True)
    ad6 = models.CharField(max_length=1, blank=True, null=True)
    ad7 = models.CharField(max_length=1, blank=True, null=True)
    ad8 = models.CharField(max_length=1, blank=True, null=True)
    ad9 = models.CharField(max_length=1, blank=True, null=True)
    ad10 = models.CharField(max_length=1, blank=True, null=True)
    ad11 = models.CharField(max_length=1, blank=True, null=True)
    ad12 = models.CharField(max_length=1, blank=True, null=True)
    ad13 = models.CharField(max_length=1, blank=True, null=True)
    ad14 = models.CharField(max_length=1, blank=True, null=True)
    ad15 = models.CharField(max_length=1, blank=True, null=True)
    ad16 = models.CharField(max_length=1, blank=True, null=True)
    ad17 = models.CharField(max_length=1, blank=True, null=True)
    ad18 = models.CharField(max_length=1, blank=True, null=True)
    ad19 = models.CharField(max_length=1, blank=True, null=True)
    ad20 = models.CharField(max_length=1, blank=True, null=True)
    fechacad = models.DateField(blank=True, null=True)
    consejerocad = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usodrogas'


class Usuarios(models.Model):
    usuario = models.SmallIntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=30, blank=True, null=True)
    cargo = models.CharField(max_length=20, blank=True, null=True)
    permisos = models.CharField(max_length=5, blank=True, null=True)
    password = models.CharField(max_length=10, blank=True, null=True)
    cedula = models.CharField(max_length=20, blank=True, null=True)
    expedidapor = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'


class Valorizacion(models.Model):
    expediente = models.CharField(max_length=10, blank=True, null=True)
    principalsustancia = models.CharField(max_length=20, blank=True, null=True)
    hacecuanto = models.CharField(max_length=20, blank=True, null=True)
    cantidadpromedio = models.CharField(max_length=20, blank=True, null=True)
    razonesconsumo = models.TextField(blank=True, null=True)
    razon1 = models.CharField(max_length=20, blank=True, null=True)
    razon2 = models.CharField(max_length=20, blank=True, null=True)
    razon3 = models.CharField(max_length=20, blank=True, null=True)
    psicosis = models.TextField(blank=True, null=True)
    deteccionyriesgo = models.TextField(blank=True, null=True)
    ansiedad = models.TextField(blank=True, null=True)
    depresion = models.TextField(blank=True, null=True)
    satisfacciondevida = models.TextField(blank=True, null=True)
    medico = models.TextField(blank=True, null=True)
    psiquiatrica = models.TextField(blank=True, null=True)
    psicologica = models.TextField(blank=True, null=True)
    consejero = models.SmallIntegerField(blank=True, null=True)
    supervisor = models.SmallIntegerField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'valorizacion'
