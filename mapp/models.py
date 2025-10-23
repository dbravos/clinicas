from django.db import models
from djmoney.models.fields import MoneyField
from django.utils import timezone
from datetime import date
import calendar
# Create your models here.
from django.core.validators import MinValueValidator, MaxValueValidator

# models.py - AGREGA esto al inicio del archivo
from django.db import models


class ClinicaManager(models.Manager):
    def get_queryset(self):
        # Obtener la clínica actual de la sesión
        def get_clinica_actual():
            try:
                from django.contrib.sessions.models import Session
                from django.contrib.auth.models import AnonymousUser
                from django.db import connection

                # Verificar si hay una sesión activa
                if hasattr(self, '_request'):
                    return self._request.session.get('clinica_actual', 'Demostracion')

                # Intentar obtener de thread local
                import threading
                if hasattr(threading.current_thread(), '_clinica_actual'):
                    return threading.current_thread()._clinica_actual

            except:
                pass
            return 'Demostracion'

        clinica_actual = get_clinica_actual()
        return super().get_queryset().filter(clinica=clinica_actual)


class Usuarios(models.Model):

    usuario = models.BigIntegerField(verbose_name='No. Usuario',null=True,blank=True, default='',editable=False)
    nombre = models.CharField(max_length=30, verbose_name='Nombre',null=True,blank=True, default='')
    cargo = models.CharField(max_length=20,verbose_name='Cargo', null=True,blank=True, default='')
    permisos=models.CharField(max_length=5,verbose_name='Permisos',null=True,blank=True, default='')
    password=models.CharField(max_length=10,verbose_name='Password',null=True,blank=True, default='')
    cedula=models.CharField(max_length=20,verbose_name='Cedula',null=True,blank=True, default='')
    expedidapor=models.CharField(max_length=30,verbose_name='Expedida por',null=True,blank=True, default='')
    clinica=models.CharField(max_length=30,verbose_name='Clinica',null=True,blank=True, default='Demostracion')
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO

class Estados(models.Model):

    edo = models.CharField(verbose_name='ID',null=True,blank=True, default='',max_length=3)
    nombre = models.CharField(max_length=20, verbose_name='Nombre',null=True,blank=True, default='')
    pais = models.CharField(max_length=3,verbose_name='Pais', null=True,blank=True, default='')
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True, default="Demostracion")
    objects = ClinicaManager()

class DatosGrales(models.Model):

    nombre = models.CharField(max_length=30, verbose_name='Nombre',null=True,blank=True, default='')
    calleynumero = models.CharField(max_length=50,verbose_name='Calle y numero', null=True,blank=True, default='')
    colonia=models.CharField(max_length=50,verbose_name='Colonia',null=True,blank=True, default='')
    ciudad=models.CharField(max_length=50,verbose_name='Ciudad',null=True,blank=True, default='')
    estado=models.CharField(max_length=2,verbose_name='Estado',null=True,blank=True, default='')
    telefono=models.CharField(max_length=50,verbose_name='Telefono',null=True,blank=True, default='')
    sitioweb = models.CharField(max_length=50, verbose_name='Sitio WEB', null=True, blank=True, default='')
    correoelectronico = models.EmailField(max_length=50, verbose_name='Correo electronico', null=True, blank=True, default='')
    rfc = models.CharField(max_length=13, verbose_name='RFC', null=True, blank=True, default='')
    cp = models.CharField(max_length=6, verbose_name='Codigo Postal', null=True, blank=True, default='')
    expediente = models.SmallIntegerField( verbose_name='Expediente actual', null=True, blank=True, default=None)
    recibo = models.SmallIntegerField(verbose_name='Ultimo recibo emitido', null=True, blank=True, default=0)
    receta = models.SmallIntegerField(verbose_name='Folio Receta', null=True, blank=True, default=0)
    recibootros = models.SmallIntegerField(verbose_name='Ultimo recibo otros', null=True, blank=True, default=0)
    sesiong = models.SmallIntegerField( verbose_name='Ultima sesion grupal', null=True, blank=True, default=0)
    responsable = models.CharField(max_length=30, verbose_name='Responsable', null=True, blank=True, default='')
    cedula = models.CharField(max_length=20, verbose_name='Cedula', null=True, blank=True, default='')
    cargo = models.CharField(max_length=20, verbose_name='Cargo', null=True, blank=True, default='')
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True, default='Demostracion')
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO

class Internos(models.Model):


    opcionesSexo=[('F','Femenino'),('M','Masculino')]
    opcionesEstadocivil=[('S','Soltero'),('C','Casado'),('V','Viudo'),('D','Divorciado')]
    opcionesIngreso=[('V','Voluntario'),('I','Involuntario'),('O','Obligatorio')]
    opcionesAcude=[('S','Solo'),('A','Amigo'),('F','Familiar'),('O','Otro')]
    opcionesProviene=[('D','Domiclio particular'),('P','Institucion publica'),('C','Institucion privada'),('O','Otra')]
    opcionesPorcual=[('A','Alcohol'),('B','Anfetaminas'),('C','Secantes'),('D','Marihuana'),('E','Rohypnol'),('F','Analgesicos'),
                     ('G','Disolventes'),('H','Cocaina'),('I','Opcio'),('J','Cristal')]


    numeroexpediente = models.CharField(max_length=10, verbose_name='No.Expediente',unique=True)
    fechaingreso = models.DateField(verbose_name='Fecha de ingreso', null=True, blank=True,default=date.today)
    fsalidareal = models.DateField(verbose_name='Fecha de salida', null=True, blank=True )
    apaterno = models.CharField(max_length=20,verbose_name='Apellido paterno', null=True, blank=True, default='')
    amaterno = models.CharField(max_length=20,verbose_name="Apellido  materno", null=True, blank=True, default='')
    nombre = models.CharField(max_length=20,verbose_name="Nombre", null=True, blank=True, default='' )
    nombrecompleto = models.CharField(max_length=60,verbose_name='Nombre completo', null=True, blank=True, default='')
    edad = models.SmallIntegerField(verbose_name='Edad', null=True, blank=True)
    sexo = models.CharField(max_length=1,verbose_name='Sexo',choices=opcionesSexo, null=True,  default='M')
    estadocivil = models.CharField(max_length=1,verbose_name='Edo civil',choices=opcionesEstadocivil,null=True,  default='S' )
    calleynumero = models.CharField(max_length=40,verbose_name='Domicilio actual', null=True, blank=True, default='')
    colonia = models.CharField(max_length=30,verbose_name='Colonia actual', null=True, blank=True, default='')
    ciudad = models.CharField(max_length=10,verbose_name='Ciudad actual', null=True, blank=True, default='')
    estado = models.CharField(max_length=2,verbose_name='Estado actual', null=True, blank=True, default='')
    pais = models.CharField(max_length=2,verbose_name='Pais actual', null=True, blank=True, default='')
    telefono = models.CharField(max_length=20,verbose_name='Telefono', null=True, blank=True, default='')
    escolaridad = models.CharField(max_length=20,verbose_name='Escolaridad', null=True, blank=True, default='')
    ocupacion = models.CharField(max_length=20,verbose_name='Ocupacion', null=True, blank=True, default='')
    tiempodesempleado = models.CharField(max_length=10,verbose_name='Tiempo desempleado', null=True, blank=True, default='')
    conquienvive = models.CharField(max_length=1,verbose_name='Con quien vive', null=True, blank=True, default='')
    responsable = models.CharField(max_length=40,verbose_name='Nombre', null=True, blank=True, default='')
    rcalle = models.CharField(max_length=40,verbose_name='Domicilio ', null=True, blank=True, default='')
    rcolonia = models.CharField(max_length=30,verbose_name='Colonia ', null=True, blank=True, default='')
    rciudad = models.CharField(max_length=10,verbose_name='Ciudad ', null=True, blank=True, default='')
    restado = models.CharField(max_length=2,verbose_name='Estado ', null=True, blank=True, default='')
    rpais = models.CharField(max_length=3,verbose_name='Pais', null=True, blank=True, default='')
    rtelefono = models.CharField(max_length=20,verbose_name='Telefono', null=True, blank=True, default='')
    dpadres = models.BooleanField(verbose_name='Padres', null=True, default=False)
    dhijos = models.BooleanField(verbose_name='Hijos', null=True, default=False)
    dconyugue = models.BooleanField(verbose_name='Cónyugue', null=True, default=False)
    dotros = models.BooleanField(verbose_name='Otros', null=True, default=False)
    comentarios = models.TextField(verbose_name='Comentarios', null=True, blank=True, default='')
    serviciosmedicos = models.CharField(max_length=20,verbose_name='Servicios medicos', null=True, blank=True, default='')
    afiliasion = models.CharField(max_length=10,verbose_name='Afiliacion', null=True, blank=True, default='')
    codigopostal = models.CharField(max_length=6,verbose_name='Codigo postal', null=True, blank=True, default='')
    telefonotrabajo = models.CharField(max_length=15,verbose_name='Tel. Trabajo', null=True, blank=True, default='')
    tipoingreso = models.CharField(max_length=1,verbose_name='Tipo ingreso',choices=opcionesIngreso, null=True, default='V')
    proviene = models.CharField(max_length=1,verbose_name='Proviene',choices=opcionesProviene, null=True,default='D')
    provieneotro = models.CharField(max_length=20,verbose_name='Otro', null=True, blank=True)
    acudecon = models.CharField(max_length=1,verbose_name='Acude con',choices=opcionesAcude,null=True, default='S')
    acudeotro = models.CharField(max_length=20,verbose_name='Otro', null=True, blank=True, default='')
    enfermedadesotro = models.CharField(max_length=20,verbose_name='Otras enfermedades', null=True, blank=True, default='')
    tomamedicinas = models.BooleanField(verbose_name='Toma medicinas', null=True, blank=True, default=False)
    especifique = models.CharField(max_length=20,verbose_name='Especifique', null=True, blank=True, default='')
    porcualingresa = models.CharField(max_length=1,choices=opcionesPorcual,verbose_name='Por cual sustancia ingresa', null=True, blank=True, default='')
    embarazo = models.BooleanField(verbose_name='Embarazo', null=True,blank=True)
    psiquiatricas = models.BooleanField(verbose_name='Psiquiátricas', null=True, default=False,blank=True)
    fisicas = models.BooleanField(verbose_name='Físicas', null=True, default=False,blank=True)
    contagiosas = models.BooleanField(verbose_name='Contagiosas', null=True, default=False,blank=True)
    padecimientos = models.BooleanField(verbose_name='Padecimientos', null=True, default=False,blank=True)
    basiloscopia = models.BooleanField(verbose_name='Basiloscopía', null=True, default=False,blank=True)
    alcohol = models.BooleanField(verbose_name='Alcohol', null=True, default=False,blank=True)
    anfetaminas = models.BooleanField(verbose_name='Anfetaminas', null=True, default=False,blank=True)
    secantes = models.BooleanField(verbose_name='Secantes', null=True, default=False,blank=True)
    marihuana = models.BooleanField(verbose_name='Marihuana', null=True, default=False,blank=True)
    rohypnol = models.BooleanField(verbose_name='Rohypnol', null=True, default=False,blank=True)
    analgesicos = models.BooleanField(verbose_name='Analgesicos', null=True, default=False,blank=True)
    disolventes = models.BooleanField(verbose_name='Disolventes', null=True, default=False,blank=True)
    cocaina = models.BooleanField(verbose_name='Cocaina', null=True, default=False,blank=True)
    opio = models.BooleanField(verbose_name='Opio', null=True, default=False,blank=True)
    cristal = models.BooleanField(verbose_name='Cristal', null=True, default=False,blank=True)
    numeroreuniones = models.SmallIntegerField(verbose_name='No. Reuniones', null=True, default=0,blank=True)
    diversasactividades = models.CharField(max_length=30,verbose_name='Diversas actividades', null=True, blank=True)
    duracion = models.CharField(max_length=15,verbose_name='Duracion', null=True, blank=True)
    quieninformo = models.CharField(max_length=30,verbose_name='Quien informa', null=True, blank=True)
    aportacioninicial = models.DecimalField(max_digits=10,verbose_name='Aportacion  inicial', decimal_places=2, null=True,blank=True)
    aportaciontotal = models.DecimalField(max_digits=10,verbose_name='Aportacion  total', decimal_places=2, null=True,blank=True)
    lugarnac = models.CharField(max_length=20,verbose_name='Lugar de nacimiento', null=True, blank=True)
    estadonac = models.CharField(max_length=3,verbose_name='Estado de nacimiento', null=True, blank=True)
    paisnac = models.CharField(max_length=3,verbose_name='Pais de nacimiento', null=True, blank=True)
    Motivoegreso = models.TextField(verbose_name='Motivo de egreso', null=True, blank=True)
    resumenanexo = models.TextField(verbose_name='Resumen anexo', null=True, blank=True)
    estadodesalud = models.TextField(verbose_name='Estado de salud', null=True, blank=True)
    prevencionrecaidas = models.TextField(verbose_name='Prevencion a recaidas', null=True, blank=True)
    periodopago = models.SmallIntegerField(verbose_name='Periodo de pago', null=True, blank=True,default=0)
    reciboinicial = models.SmallIntegerField(verbose_name='Recibo inicial', null=True, blank=True,default=0)
    proxsesconind = models.DateField(verbose_name='Próxima sesión individual', null=True, blank=True)
    proxsesconfam = models.DateField(verbose_name='Próxima sesión familiar' , null=True, blank=True)
    proxsescongru = models.DateField(verbose_name='Próxima sesión grupal', null=True, blank=True)
    proximasesionps = models.DateField(verbose_name='Próxima sesión PS', null=True, blank=True)
    proximasesiong = models.DateField(verbose_name='Próxima sesión G', null=True, blank=True)
    proxseseg = models.DateField(verbose_name='Próxima sesión EG', null=True, blank=True)
    fechariesgo = models.DateField(verbose_name='Fecha de riesgo', null=True, blank=True)
    nacionalidad = models.CharField(max_length=15, verbose_name='Nacionalidad', null=True, blank=True)
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True,default="Demostracion")
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO


    def __str__(self):
        return self.nombrecompleto

class Einicial(models.Model):


    opcionesConsumo = [(0, 'No'), (1, 'Si')]
    opcionesForma = [(0,'Ingerida'),(1,'Inyectada'),(2,'Fumada'),(3,'Inhalada'),(4,'Otras')]
    opcionesTabaco = [(0, 'Nunca'), (1, 'Actualmente'), (2, 'Exfumador mas de un año'), (3, 'Exfumador menos de un año')]
    opcionesSustancias = [(0, 'Alcohol  '), (1, 'Tabaco   '), (2, 'Marihuana'), (3, 'Cocaina  '), (4, 'Crack    '),
                       (5, 'Pastillas'),(6, 'Otras    ')]
    opcionesAlcohol = [(0, 'Cerveza'), (1, 'Vino'), (2, 'Pulque'), (3, 'Coolers'), (4, 'Destilado')]
    opcionesComo = [(0, 'Solo'), (1, 'Acmpñado'), (2, 'Publico'), (3, 'Privado')]
    opcionesPorque = [(1, '1'), (2, '2'), (3, '3'), (4, '4'),(5, '5'),(6, '6'), (7, '7'),(8,'8')]
    opcionesImportante=[(1,'Nada'),(2,'Poco'),(3,'Algo'),(4,'Importante'),(5,'Muy')]
    opcionesPiensaque = [(1, 'No es su intencion dejar de consumir'), (2, 'Esta indeciso de dejar de consumir'), (3, 'Esta decidido a dejar de consumir'), (4, 'Ya haciendo algo para dejar de consumir')]
    opcionesDispuesto = [(1, 'Nada dispuesto/a'), (2, 'Poco dispuesto/a'), (3, 'Algo dispuesto/a'), (4, 'Dispuesto/a'), (5, 'Muy dispuesto/a')]
    opcionesTamano= [(1, 'Sin problema'),(2, 'Pequeño problema (preocupado pero sin consecuencias)'),(3, 'Problema (algunas consecuencias negativas, no serias)'),(4, 'Gran problema (con consecuencias serias)')]
    opcionesMeses = [('Ene', 'Ene'), ('Feb', 'Feb'), ('Mar', 'Mar'), ('Abr', 'Abr'), ('May', 'May'), ('Jun', 'Jun'),
                     ('Jul', 'Jul'), ('Ago', 'Ago'), ('Sep', 'Sep'), ('Oct', 'Oct'), ('Nov', 'Nov'), ('Dic', 'Dic')]
    opcionesYears = [(str(axo), str(axo)) for axo in range(2000, 2051)]


    expediente = models.CharField(max_length=10, primary_key=True, verbose_name='No.Expediente', unique=True,null=False,blank=True)
    consumo1 = models.BooleanField(verbose_name='Alcohol',null=True,blank=True,default=False)
    forma1 = models.SmallIntegerField(verbose_name='Forma de consumo',choices=opcionesForma,null=True,blank=True,default=0)
    frecuencia1 = models.CharField(verbose_name='Frecuencia de consumo',null=True,blank=True,max_length=20)
    cantidad1= models.CharField(verbose_name='Cantidad que consume',null=True,blank=True,max_length=20)
    edad1 = models.SmallIntegerField(verbose_name='Edad inicio de consumo',null=True,blank=True)
    consumo2 = models.BooleanField(verbose_name='Marihuana', null=True, blank=True, default=False)
    forma2 = models.SmallIntegerField(verbose_name='Forma de consumo', choices=opcionesForma, null=True, blank=True)
    frecuencia2 = models.CharField(verbose_name='Frecuencia de consumo', null=True, blank=True, max_length=20)
    cantidad2 = models.CharField(verbose_name='Cantidad que consume', null=True, blank=True, max_length=20)
    edad2 = models.SmallIntegerField(verbose_name='Edad inicio de consumo', null=True, blank=True)

    consumo3 = models.BooleanField(verbose_name='Cocaina', null=True, blank=True, default=False)
    forma3 = models.SmallIntegerField(verbose_name='Forma de consumo', choices=opcionesForma, null=True, blank=True)
    frecuencia3 = models.CharField(verbose_name='Frecuencia de consumo', null=True, blank=True, max_length=20)
    cantidad3 = models.CharField(verbose_name='Cantidad que consume', null=True, blank=True, max_length=20)
    edad3 = models.SmallIntegerField(verbose_name='Edad inicio de consumo', null=True, blank=True)
    consumo4 = models.BooleanField(verbose_name='Heroina', null=True, blank=True, default=False)
    forma4 = models.SmallIntegerField(verbose_name='Forma de consumo', choices=opcionesForma, null=True, blank=True)
    frecuencia4 = models.CharField(verbose_name='Frecuencia de consumo', null=True, blank=True, max_length=20)
    cantidad4 = models.CharField(verbose_name='Cantidad que consume', null=True, blank=True, max_length=20)
    edad4 = models.SmallIntegerField(verbose_name='Edad inicio de consumo', null=True, blank=True)
    consumo5 = models.BooleanField(verbose_name='Metanfetaminas anfetaminas', null=True, blank=True, default=False)
    forma5 = models.SmallIntegerField(verbose_name='Forma de consumo', choices=opcionesForma, null=True, blank=True)
    frecuencia5 = models.CharField(verbose_name='Frecuencia de consumo', null=True, blank=True, max_length=20)
    cantidad5 = models.CharField(verbose_name='Cantidad que consume', null=True, blank=True, max_length=20)
    edad5 = models.SmallIntegerField(verbose_name='Edad inicio de consumo', null=True, blank=True)
    consumo6 = models.BooleanField(verbose_name='Inhalables', null=True, blank=True, default=False)
    forma6 = models.SmallIntegerField(verbose_name='Forma de consumo', choices=opcionesForma, null=True, blank=True)
    frecuencia6 = models.CharField(verbose_name='Frecuencia de consumo', null=True, blank=True, max_length=20)
    cantidad6 = models.CharField(verbose_name='Cantidad que consume', null=True, blank=True, max_length=20)
    edad6 = models.SmallIntegerField(verbose_name='Edad inicio de consumo', null=True, blank=True)
    consumo7 = models.BooleanField(verbose_name='Alucinogenos', null=True, blank=True, default=False)
    forma7 = models.SmallIntegerField(verbose_name='Forma de consumo', choices=opcionesForma, null=True, blank=True)
    frecuencia7 = models.CharField(verbose_name='Frecuencia de consumo', null=True, blank=True, max_length=20)
    cantidad7 = models.CharField(verbose_name='Cantidad que consume', null=True, blank=True, max_length=20)
    edad7 = models.SmallIntegerField(verbose_name='Edad inicio de consumo', null=True, blank=True)
    consumo8 = models.BooleanField(verbose_name='Drogas de diseño', null=True, blank=True, default=False)
    forma8 = models.SmallIntegerField(verbose_name='Forma de consumo', choices=opcionesForma, null=True, blank=True)
    frecuencia8 = models.CharField(verbose_name='Frecuencia de consumo', null=True, blank=True, max_length=20)
    cantidad8 = models.CharField(verbose_name='Cantidad que consume', null=True, blank=True, max_length=20)
    edad8 = models.SmallIntegerField(verbose_name='Edad inicio de consumo', null=True, blank=True)
    consumo9 = models.BooleanField(verbose_name='Medicamentos estimulantes', null=True, blank=True, default=False)
    forma9 = models.SmallIntegerField(verbose_name='Forma de consumo', choices=opcionesForma, null=True, blank=True)
    frecuencia9 = models.CharField(verbose_name='Frecuencia de consumo', null=True, blank=True, max_length=20)
    cantidad9 = models.CharField(verbose_name='Cantidad que consume', null=True, blank=True, max_length=20)
    edad9 = models.SmallIntegerField(verbose_name='Edad inicio de consumo', null=True, blank=True)
    consumo10 = models.BooleanField(verbose_name='Medicamentos depresores', null=True, blank=True, default=False)
    forma10 = models.SmallIntegerField(verbose_name='Forma de consumo', choices=opcionesForma, null=True, blank=True)
    frecuencia10 = models.CharField(verbose_name='Frecuencia de consumo', null=True, blank=True, max_length=20)
    cantidad10 = models.CharField(verbose_name='Cantidad que consume', null=True, blank=True, max_length=20)
    edad10 = models.SmallIntegerField(verbose_name='Edad inicio de consumo', null=True, blank=True)
    consumo11 = models.SmallIntegerField(verbose_name='Tabaco', null=True, blank=True, choices=opcionesTabaco)
    frecuencia11 = models.CharField(verbose_name='Frecuencia de consumo', null=True, blank=True, max_length=20)
    cantidad11 = models.CharField(verbose_name='Cantidad que consume', null=True, blank=True, max_length=20)
    edad11 = models.SmallIntegerField(verbose_name='Edad inicio de consumo', null=True, blank=True)
    otrassustancias=models.CharField(verbose_name='Otras sustancias',max_length=50,null=True,blank=True)
    principalsustancia=models.SmallIntegerField(verbose_name='Principal sustancia',choices=opcionesSustancias,null=True, default=1)
    otrasustanciap=models.CharField(verbose_name='Tipo',max_length=30,null=True,blank=True)
    cantidadpromedio = models.CharField(verbose_name='Cantidad promedio de consumo por ocasion',max_length=30,null=True,blank=True)
    hacecuanto=models.CharField(verbose_name='Hace cuanto consume',max_length=30,null=True,blank=True)
    cualalcohol =models.SmallIntegerField(verbose_name='Bebida Alcoholica',choices=opcionesAlcohol,null=True,  default=1)
    cualdestilado =models.CharField(verbose_name='Tipo de destilado',max_length=15,null=True,blank=True)
    normalmentecomo=models.SmallIntegerField(verbose_name='Normalmente como consume',choices=opcionesComo,null=True,  default=1)
    enquelugares=models.CharField(verbose_name='En que lugares consume',max_length=15,null=True,blank=True)
    detenervoluntariamente=models.BooleanField(verbose_name='Una vez que comienza a consumir puede detenerse voluntariamente',null=True,default=True)
    gastomalcohol=models.DecimalField(verbose_name='Gasto mensual Alcohol',max_digits=10,decimal_places=2,null=True,blank=True)
    gastomtabaco=models.DecimalField(verbose_name='Gasto mensual Tabaco',max_digits=10,decimal_places=2,null=True,blank=True)
    gastomdrogas=models.DecimalField(verbose_name='Gasto mensual Drogas',max_digits=10,decimal_places=2,null=True,blank=True)
    edesagradables=models.SmallIntegerField(verbose_name='Emociones desagradables',choices=opcionesPorque,null=True, default=1)
    eagradables=models.SmallIntegerField(verbose_name='Emociones agradables',choices=opcionesPorque,null=True, default=1)
    enfermedad=models.SmallIntegerField(verbose_name='Enfermedad',choices=opcionesPorque,null=True,  default=1)
    necesidadfisica=models.SmallIntegerField(verbose_name='Necesidad fisica',choices=opcionesPorque,null=True, default=1)
    probando=models.SmallIntegerField(verbose_name='Probando',choices=opcionesPorque,null=True,  default=1)
    conflictos=models.SmallIntegerField(verbose_name='Conflictos',choices=opcionesPorque,null=True,   default=1)
    agradablesotros=models.SmallIntegerField(verbose_name='Momentos agradables',choices=opcionesPorque,null=True,  default=1)
    presion=models.SmallIntegerField(verbose_name='Presion social',choices=opcionesPorque,null=True,  default=1)
    tamanoproblema=models.SmallIntegerField(verbose_name='Tamaño del problema Alcohol',choices=opcionesTamano,null=True,  default=1)
    tamanoproblemad=models.SmallIntegerField(verbose_name='Tamaño del problema Drogas',choices=opcionesTamano,null=True,   default=1)
    tipoproblema=models.CharField(verbose_name='Tipo de problema',max_length=15,null=True,blank=True)
    maximotiempo=models.CharField(verbose_name='Maximo tiempo',max_length=15,null=True,blank=True)
    cuandoocurriom=models.CharField(verbose_name='Mes',choices=opcionesMeses,max_length=3,null=True,blank=True)
    cuandoocurrioa=models.CharField(verbose_name='Año',max_length=4,choices=opcionesYears,null=True,blank=True)
    motivo=models.CharField(verbose_name='Motivo',max_length=30,null=True,blank=True)
    mayortiempo=models.CharField(verbose_name='Mayor tiempo',max_length=15,null=True,blank=True)
    cuandoocurriom6 = models.CharField(verbose_name='Mes',choices=opcionesMeses, max_length=3, null=True, blank=True)
    cuandoocurrioa6 = models.CharField(verbose_name='Año', max_length=4,choices=opcionesYears, null=True, blank=True)
    motivo6 = models.CharField(verbose_name='Motivo', max_length=30, null=True, blank=True)
    quetanimportante=models.SmallIntegerField(verbose_name='Que tan importante',choices=opcionesImportante,null=True, default=1)
    quetanseguro= models.SmallIntegerField(verbose_name='Que tan seguro',validators=[MinValueValidator(1), MaxValueValidator(10)],null=True,blank=True)
    piensaque=models.SmallIntegerField(verbose_name='Actualmente piensa que ',choices=opcionesPiensaque,null=True, default=1)
    dispuesto=models.SmallIntegerField(verbose_name='Que tan dispuesto esta ',choices=opcionesDispuesto,null=True, default=1)
    razon1=models.CharField(verbose_name='Razon 1',max_length=50,null=True,blank=True)
    razon2=models.CharField(verbose_name='Razon 2',max_length=50,null=True,blank=True)
    razon3=models.CharField(verbose_name='Razon 3',max_length=50,null=True,blank=True)
    clinica=models.CharField(verbose_name='Clinica',max_length=30,null=True,blank=True,default="Demostracion")
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO

    @property
    def resumen_razones_principales(self):

        importancia_mapa = {
            8: "Máxima Prioridad",
            7: "Muy Alta Prioridad",
            6: "Alta Prioridad",
            5: "Prioridad Media",
            4: "Prioridad Baja",
            3: "Poca Prioridad",
            2: "Mínima Prioridad",
            1: "Sin Prioridad",
        }

        # --- PASO 2: Recolectar los datos de todos los campos relevantes en una lista ---
        # Cada elemento será una tupla: (valor_numerico, nombre_del_campo)
        razones_con_valor = [
            (self.edesagradables or 1, 'edesagradables'),
            (self.eagradables or 1, 'eagradables'),
            (self.enfermedad or 1, 'enfermedad'),
            (self.necesidadfisica or 1, 'necesidadfisica'),
            (self.probando or 1, 'probando'),
            (self.conflictos or 1, 'conflictos'),
            (self.agradablesotros or 1, 'agradablesotros'),
            (self.presion or 1, 'presion'),
            # ... añade más campos aquí si los tienes ...
        ]

        # --- PASO 3: Ordenar la lista por el valor numérico, de mayor a menor (de 8 a 1) ---
        razones_con_valor.sort(key=lambda tupla: tupla[0], reverse=True)

        # --- PASO 4: Tomar solo los 3 primeros elementos de la lista ya ordenada ---
        top_3_razones = razones_con_valor[:3]

        # --- PASO 5: Procesar estos 3 ganadores para crear la lista final de diccionarios ---
        datos_finales = []
        for valor, nombre_campo in top_3_razones:
            # Solo procesamos si el valor es significativo (mayor que 1, por ejemplo)
            # Puedes ajustar o quitar esta condición si quieres mostrar incluso los de valor 1
            if valor > 1:
                # Obtenemos el verbose_name del campo a partir de su nombre
                campo = self._meta.get_field(nombre_campo)
                nombre_legible = campo.verbose_name

                # Traducimos el valor numérico a un texto legible
                texto_valor = importancia_mapa.get(valor, str(valor))  # Si no está en el mapa, muestra el número

                # Creamos el diccionario estructurado
                razon_data = {
                    'nombre': nombre_legible,
                    'severidad': texto_valor
                }
                datos_finales.append(razon_data)

        return datos_finales

class Assist(models.Model):


    opcionesSioNo = [(0, 'No'), (1, 'Si')]
    opcionesCinco =[(0,'Nunca'),(3,'Una o Dos veces'),(4,'Mensualmente'),(5,'Semanalmente'),(6,'Diario o casi diario')]
    opcionesTres =[(0,'Nunca'),(6,'Si en los ultimos tres meses'),(3,'Si pero NO en los ultimos tres meses')]
    opcionesRiesgo=[(0,'Bajo'),(1,'Moderado'),(2,'Alto')]
    expediente=models.CharField(max_length=10, primary_key=True, verbose_name='No.Expediente', unique=True)
    p1s1=models.SmallIntegerField(verbose_name='a) Tabaco (cigarrillos,tabaco de mascar,puro,etc)',choices=opcionesSioNo,null=True,default=0)
    p1s2=models.SmallIntegerField(verbose_name='b) Bebidas alcoholicas (cerveza,licores,vino,etc.)',choices=opcionesSioNo,null=True,default=0)
    p1s3=models.SmallIntegerField(verbose_name='c) Cannabis (marihuana,mota,hierba,hachis,etc.)',choices=opcionesSioNo,null=True,default=0)
    p1s4=models.SmallIntegerField(verbose_name='d) Cocaina (coca,crack,etc.)',choices=opcionesSioNo,null=True,default=0)
    p1s5=models.SmallIntegerField(verbose_name='e) Estimulantes del tipo anfetamina (speed,anfetamina,extasis,etc.)',choices=opcionesSioNo,null=True,default=0)
    p1s6=models.SmallIntegerField(verbose_name='f) Inhalantes (oxido nitroso,pegamentos,gasolina,solventes para pintura,etc.)',choices=opcionesSioNo,null=True,default=0)
    p1s7=models.SmallIntegerField(verbose_name='g) Sedantes o pastillas para dormir (diazepam,alprazolam,flunitrazepam,midalozam,etc.)',choices=opcionesSioNo,null=True,default=0)
    p1s8=models.SmallIntegerField(verbose_name='h) Alucinogenos (LSD,acidos,hongos,ketamina,etc.)',choices=opcionesSioNo,null=True,default=0)
    p1s9=models.SmallIntegerField(verbose_name='i) Opiaceos (heroina,metadona,morfina,brupernifina,codeina,etc.)',choices=opcionesSioNo,null=True,default=0)
    p1s10=models.SmallIntegerField(verbose_name='j) Otras (especifique) ',choices=opcionesSioNo,null=True,default=0)
    asistotras=models.CharField(max_length=20,verbose_name='',null=True,blank=True)
    p2s1=models.SmallIntegerField(verbose_name='a) Tabaco (cigarrillos,tabaco de mascar,puro,etc)',choices=opcionesCinco,null=True,default=0)
    p2s2=models.SmallIntegerField(verbose_name='b) Bebidas alcoholicas (cerveza,licores,vino,etc.)',choices=opcionesCinco,null=True,default=0)
    p2s3=models.SmallIntegerField(verbose_name='c) Cannabis (marihuana,mota,hierba,hachis,etc.)',choices=opcionesCinco,null=True,default=0)
    p2s4=models.SmallIntegerField(verbose_name='d) Cocaina (coca,crack,etc.)',choices=opcionesCinco,null=True,default=0)
    p2s5=models.SmallIntegerField(verbose_name='e) Estimulantes del tipo anfetamina (speed,anfetamina,extasis,etc.)',choices=opcionesCinco,null=True,default=0)
    p2s6=models.SmallIntegerField(verbose_name='f) Inhalantes (oxido nitroso,pegamentos,gasolina,solventes para pintura,etc.)',choices=opcionesCinco,null=True,default=0)
    p2s7=models.SmallIntegerField(verbose_name='g) Sedantes o pastillas para dormir (diazepam,alprazolam,flunitrazepam,midalozam,etc.)',choices=opcionesCinco,null=True,default=0)
    p2s8=models.SmallIntegerField(verbose_name='h) Alucinogenos (LSD,acidos,hongos,ketamina,etc.)',choices=opcionesCinco,null=True,default=0)
    p2s9=models.SmallIntegerField(verbose_name='i) Opiaceos (heroina,metadona,morfina,brupernifina,codeina,etc.)',choices=opcionesCinco,null=True,default=0)
    p2s10=models.SmallIntegerField(verbose_name='j) Otras (especifique)',choices=opcionesCinco,null=True,default=0)
    asistotras2=models.CharField(max_length=20,verbose_name='',null=True,blank=True)
    p3s1=models.SmallIntegerField(verbose_name='a) Tabaco (cigarrillos,tabaco de mascar,puro,etc)',choices=opcionesCinco,null=True,default=0)
    p3s2=models.SmallIntegerField(verbose_name='b) Bebidas alcoholicas (cerveza,licores,vino,etc.)',choices=opcionesCinco,null=True,default=0)
    p3s3=models.SmallIntegerField(verbose_name='c) Cannabis (marihuana,mota,hierba,hachis,etc.)',choices=opcionesCinco,null=True,default=0)
    p3s4=models.SmallIntegerField(verbose_name='d) Cocaina (coca,crack,etc.)',choices=opcionesCinco,null=True,default=0)
    p3s5=models.SmallIntegerField(verbose_name='e) Estimulantes del tipo anfetamina (speed,anfetamina,extasis,etc.)',choices=opcionesCinco,null=True,default=0)
    p3s6=models.SmallIntegerField(verbose_name='f) Inhalantes (oxido nitroso,pegamentos,gasolina,solventes para pintura,etc.)',choices=opcionesCinco,null=True,default=0)
    p3s7=models.SmallIntegerField(verbose_name='g) Sedantes o pastillas para dormir (diazepam,alprazolam,flunitrazepam,midalozam,etc.)',choices=opcionesCinco,null=True,default=0)
    p3s8=models.SmallIntegerField(verbose_name='h) Alucinogenos (LSD,acidos,hongos,ketamina,etc.)',choices=opcionesCinco,null=True,default=0)
    p3s9=models.SmallIntegerField(verbose_name='i) Opiaceos (heroina,metadona,morfina,brupernifina,codeina,etc.)',choices=opcionesCinco,null=True,default=0)
    p3s10=models.SmallIntegerField(verbose_name='j) Otras (especifique)',choices=opcionesCinco,null=True,default=0)
    asistotras3=models.CharField(max_length=20,verbose_name='',null=True,blank=True)
    p4s1=models.SmallIntegerField(verbose_name='a) Tabaco (cigarrillos,tabaco de mascar,puro,etc)',choices=opcionesCinco,default=0)
    p4s2=models.SmallIntegerField(verbose_name='b) Bebidas alcoholicas (cerveza,licores,vino,etc.)',choices=opcionesCinco,null=True,default=0)
    p4s3=models.SmallIntegerField(verbose_name='c) Cannabis (marihuana,mota,hierba,hachis,etc.)',choices=opcionesCinco,null=True,default=0)
    p4s4=models.SmallIntegerField(verbose_name='d) Cocaina (coca,crack,etc.)',choices=opcionesCinco,null=True,default=0)
    p4s5=models.SmallIntegerField(verbose_name='e) Estimulantes del tipo anfetamina (speed,anfetamina,extasis,etc.)',choices=opcionesCinco,null=True,default=0)
    p4s6=models.SmallIntegerField(verbose_name='f) Inhalantes (oxido nitroso,pegamentos,gasolina,solventes para pintura,etc.)',choices=opcionesCinco,null=True,default=0)
    p4s7=models.SmallIntegerField(verbose_name='g) Sedantes o pastillas para dormir (diazepam,alprazolam,flunitrazepam,midalozam,etc.)',choices=opcionesCinco,null=True,default=0)
    p4s8=models.SmallIntegerField(verbose_name='h) Alucinogenos (LSD,acidos,hongos,ketamina,etc.)',choices=opcionesCinco,null=True,default=0)
    p4s9=models.SmallIntegerField(verbose_name='i) Opiaceos (heroina,metadona,morfina,brupernifina,codeina,etc.)',choices=opcionesCinco,null=True,default=0)
    p4s10=models.SmallIntegerField(verbose_name='j) Otras (especifique)',choices=opcionesCinco,null=True,default=0)
    asistotras4=models.CharField(max_length=20,verbose_name='',null=True,blank=True)
    p5s1=models.SmallIntegerField(verbose_name='a) Tabaco (cigarrillos,tabaco de mascar,puro,etc)',choices=opcionesCinco,null=True,default=0)
    p5s2=models.SmallIntegerField(verbose_name='b) Bebidas alcoholicas (cerveza,licores,vino,etc.)',choices=opcionesCinco,null=True,default=0)
    p5s3=models.SmallIntegerField(verbose_name='c) Cannabis (marihuana,mota,hierba,hachis,etc.)',choices=opcionesCinco,null=True,default=0)
    p5s4=models.SmallIntegerField(verbose_name='d) Cocaina (coca,crack,etc.)',choices=opcionesCinco,null=True,default=0)
    p5s5=models.SmallIntegerField(verbose_name='e) Estimulantes del tipo anfetamina (speed,anfetamina,extasis,etc.)',choices=opcionesCinco,null=True,default=0)
    p5s6=models.SmallIntegerField(verbose_name='f) Inhalantes (oxido nitroso,pegamentos,gasolina,solventes para pintura,etc.)',choices=opcionesCinco,null=True,default=0)
    p5s7=models.SmallIntegerField(verbose_name='g) Sedantes o pastillas para dormir (diazepam,alprazolam,flunitrazepam,midalozam,etc.)',choices=opcionesCinco,null=True,default=0)
    p5s8=models.SmallIntegerField(verbose_name='h) Alucinogenos (LSD,acidos,hongos,ketamina,etc.)',choices=opcionesCinco,null=True,default=0)
    p5s9=models.SmallIntegerField(verbose_name='i) Opiaceos (heroina,metadona,morfina,brupernifina,codeina,etc.)',choices=opcionesCinco,null=True,default=0)
    p5s10=models.SmallIntegerField(verbose_name='j) Otras (especifique)',choices=opcionesCinco,null=True,default=0)
    asistotras5=models.CharField(max_length=20,verbose_name='',null=True,blank=True)
    p7s1=models.SmallIntegerField(verbose_name='a) Tabaco (cigarrillos,tabaco de mascar,puro,etc)',choices=opcionesTres,null=True,default=0)
    p7s2=models.SmallIntegerField(verbose_name='b) Bebidas alcoholicas (cerveza,licores,vino,etc.)',choices=opcionesTres,null=True,default=0)
    p7s3=models.SmallIntegerField(verbose_name='c) Cannabis (marihuana,mota,hierba,hachis,etc.)',choices=opcionesTres,null=True,default=0)
    p7s4=models.SmallIntegerField(verbose_name='d) Cocaina (coca,crack,etc.)',choices=opcionesTres,null=True,default=0)
    p7s5=models.SmallIntegerField(verbose_name='e) Estimulantes del tipo anfetamina (speed,anfetamina,extasis,etc.)',choices=opcionesTres,null=True,default=0)
    p7s6=models.SmallIntegerField(verbose_name='f) Inhalantes (oxido nitroso,pegamentos,gasolina,solventes para pintura,etc.)',choices=opcionesTres,null=True,default=0)
    p7s7=models.SmallIntegerField(verbose_name='g) Sedantes o pastillas para dormir (diazepam,alprazolam,flunitrazepam,midalozam,etc.)',choices=opcionesTres,null=True,default=0)
    p7s8=models.SmallIntegerField(verbose_name='h) Alucinogenos (LSD,acidos,hongos,ketamina,etc.)',choices=opcionesTres,null=True,default=0)
    p7s9=models.SmallIntegerField(verbose_name='i) Opiaceos (heroina,metadona,morfina,brupernifina,codeina,etc.)',choices=opcionesTres,null=True,default=0)
    p7s10=models.SmallIntegerField(verbose_name='j) Otras (especifique)',choices=opcionesTres,null=True,default=0)
    asistotras7=models.CharField(max_length=20,verbose_name='',null=True,blank=True)
    p8s1=models.SmallIntegerField(verbose_name='Habitos a inyectarse?',choices=opcionesTres,null=True,default=0)
    p6s1=models.SmallIntegerField(verbose_name='a) Tabaco (cigarrillos,tabaco de mascar,puro,etc',choices=opcionesTres,null=True,default=0)
    p6s2=models.SmallIntegerField(verbose_name='b) Bebidas alcoholicas (cerveza,licores,vino,etc.)',choices=opcionesTres,null=True,default=0)
    p6s3=models.SmallIntegerField(verbose_name='c) Cannabis (marihuana,mota,hierba,hachis,etc.)',choices=opcionesTres,null=True,default=0)
    p6s4=models.SmallIntegerField(verbose_name='d) Cocaina (coca,crack,etc.)',choices=opcionesTres,null=True,default=0)
    p6s5=models.SmallIntegerField(verbose_name='e) Estimulantes del tipo anfetamina (speed,anfetamina,extasis,etc.)',choices=opcionesTres,null=True,default=0)
    p6s6=models.SmallIntegerField(verbose_name='f) Inhalantes (oxido nitroso,pegamentos,gasolina,solventes para pintura,etc.)',choices=opcionesTres,null=True,default=0)
    p6s7=models.SmallIntegerField(verbose_name='g) Sedantes o pastillas para dormir (diazepam,alprazolam,flunitrazepam,midalozam,etc.)',choices=opcionesTres,null=True,default=0)
    p6s8=models.SmallIntegerField(verbose_name='h) Alucinogenos (LSD,acidos,hongos,ketamina,etc.)',choices=opcionesTres,null=True,default=0)
    p6s9=models.SmallIntegerField(verbose_name='i) Opiaceos (heroina,metadona,morfina,brupernifina,codeina,etc.)',choices=opcionesTres,null=True,default=0)
    p6s10=models.SmallIntegerField(verbose_name='j) Otras (especifique)',choices=opcionesTres,null=True,default=0)
    asistotras6=models.CharField(max_length=20,verbose_name='',null=True,blank=True)
    asistotras8=models.CharField(max_length=20,verbose_name='',null=True,blank=True)
    habitosinyectarse=models.SmallIntegerField(verbose_name='Habito a inyectarse?',choices= [(0, ''), (1, '')],null=True)
    puntos1=models.SmallIntegerField(verbose_name='a) Tabaco (cigarrillos,tabaco de mascar,puro,etc',null=True,blank=True)
    puntos2=models.SmallIntegerField(verbose_name='b) Bebidas alcoholicas (cerveza,licores,vino,etc.)',null=True,blank=True)
    puntos3=models.SmallIntegerField(verbose_name='c) Cannabis (marihuana,mota,hierba,hachis,etc.)',null=True,blank=True)
    puntos4=models.SmallIntegerField(verbose_name='d) Cocaina (coca,crack,etc.)',null=True,blank=True)
    puntos5=models.SmallIntegerField(verbose_name='e) Estimulantes del tipo anfetamina (speed,anfetamina,extasis,etc.)',null=True,blank=True)
    puntos6=models.SmallIntegerField(verbose_name='f) Inhalantes (oxido nitroso,pegamentos,gasolina,solventes para pintura,etc.)',null=True,blank=True)
    puntos7=models.SmallIntegerField(verbose_name='g) Sedantes o pastillas para dormir (diazepam,alprazolam,flunitrazepam,midalozam,etc.',null=True,blank=True)
    puntos8=models.SmallIntegerField(verbose_name='h) Alucinogenos (LSD,acidos,hongos,ketamina,etc.)',null=True,blank=True)
    puntos9=models.SmallIntegerField(verbose_name='i) Opiaceos (heroina,metadona,morfina,brupernifina,codeina,etc.)',null=True,blank=True)
    puntos10=models.SmallIntegerField(verbose_name='j) Otras ',null=True,blank=True)
    consejeroassist=models.SmallIntegerField(verbose_name='Consejero',null=True,blank=True)
    riesgo1=models.SmallIntegerField(verbose_name='',null=True,blank=True)
    riesgo2=models.SmallIntegerField(verbose_name='',null=True,blank=True)
    riesgo3=models.SmallIntegerField(verbose_name='',null=True,blank=True)
    riesgo4=models.SmallIntegerField(verbose_name='',null=True,blank=True)
    riesgo5=models.SmallIntegerField(verbose_name='',null=True,blank=True)
    riesgo6=models.SmallIntegerField(verbose_name='',null=True,blank=True)
    riesgo7=models.SmallIntegerField(verbose_name='',null=True,blank=True)
    riesgo8=models.SmallIntegerField(verbose_name='',null=True,blank=True)
    riesgo9=models.SmallIntegerField(verbose_name='',null=True,blank=True)
    riesgo10=models.SmallIntegerField(verbose_name='',null=True,blank=True)
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True,default="Demostracion")
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO

    def calcular_puntos(self):
        """Calcula automáticamente todos los puntos basados en los campos pXsY"""
        for i in range(1, 11):  # Para cada sustancia (1-10)
            total = 0
            # Suma p2sX + p3sX + p4sX + p5sX + p6sX + p7sX
            for j in [2, 3, 4, 5, 6, 7]:  # Las preguntas relevantes
                field_name = f'p{j}s{i}'
                value = getattr(self, field_name, 0) or 0  # Usa 0 si es None
                total += value
                setattr(self, f'puntos{i}', total)

    def calcular_riesgos(self):
       """Calcula automáticamente los niveles de riesgo (0-2) para todos los puntos"""
       for i in range(1, 11):  # Para riesgo1 hasta riesgo10
           puntos = getattr(self, f'puntos{i}', 0) or 0  # Obtenemos puntos con valor por defecto 0
           riesgo = 0 if puntos <= 3 else (1 if puntos <= 26 else 2)
           setattr(self, f'riesgo{i}', riesgo)


    def save(self, *args, **kwargs):
        """Sobrescribe el save para calcular puntos automáticamente"""
        self.calcular_puntos()  # Actualiza todos los cálculos
        self.calcular_riesgos() # metodo para calkcular riesgos
        super().save(*args, **kwargs)  # Guarda normalmente



    def __str__(self):
        return f"Assist para {self.expediente}"


    class Meta:
        verbose_name = "Cuestionario ASSIST"
        verbose_name_plural = "Cuestionarios ASSIST"
        ordering = ['expediente']


# Dentro de tu clase Assist en models.py

# ... (todo tu modelo hasta el final) ...

# --- AÑADE ESTA PROPIEDAD AL FINAL DE LA CLASE ---
    @property
    def resumen_riesgos_principales(self):
        """
    Analiza los campos 'puntos1' a 'puntos10', identifica los 5 más altos,
    determina su nivel de riesgo y devuelve una lista de diccionarios
    con el verbose_name de la sustancia, su puntuación y el nivel de riesgo.
    """

    # --- PASO 1: Define el mapa para traducir el nivel de riesgo numérico a texto ---
        riesgo_mapa = {
             0: "Bajo",
             1: "Moderado",
             2: "Alto"
             }

    # --- PASO 2: Recolectar los datos de todos los campos 'puntos' ---
    # Cada elemento será una tupla: (puntuacion_numerica, nombre_del_campo)
        puntuaciones_por_sustancia = []
        for i in range(1, 11):
            nombre_campo = f'puntos{i}'
            puntuacion = getattr(self, nombre_campo, 0) or 0  # Obtiene el valor, con 0 por defecto

        # Solo nos interesan las sustancias con puntuación mayor a 0
            if puntuacion > 0:
               puntuaciones_por_sustancia.append((puntuacion, nombre_campo))

    # Si no hay ninguna sustancia con puntuación, devolvemos una lista vacía
        if not puntuaciones_por_sustancia:
           return []

    # --- PASO 3: Ordenar la lista por la puntuación, de mayor a menor ---
        puntuaciones_por_sustancia.sort(key=lambda tupla: tupla[0], reverse=True)

    # --- PASO 4: Tomar solo los 5 primeros elementos (los top 5) ---
        top_5_sustancias = puntuaciones_por_sustancia[:5]

    # --- PASO 5: Procesar estos 5 para crear la lista final de diccionarios ---
        datos_finales = []
        for puntuacion, nombre_campo in top_5_sustancias:
            campo = self._meta.get_field(nombre_campo)
            verbose_name_completo = campo.verbose_name

            # Encontramos la posición del primer paréntesis
            indice_parentesis = verbose_name_completo.find('(')

            # Si se encuentra un paréntesis, cortamos hasta ahí. Si no, tomamos el resto.
            if indice_parentesis != -1:
                # Cortamos desde el 4º carácter HASTA la posición del paréntesis
                nombre_sustancia_crudo = verbose_name_completo[3:indice_parentesis]
            else:
                # Plan B: si no hay paréntesis, solo cortamos los 3 primeros caracteres
                nombre_sustancia_crudo = verbose_name_completo[3:]

            # Limpiamos espacios en blanco de los extremos y capitalizamos
            nombre_sustancia = nombre_sustancia_crudo.strip().capitalize()


        # Determinamos el nivel de riesgo basado en la puntuación
        # La misma lógica que en tu método calcular_riesgos()
            if puntuacion <= 3:  # Tu regla era "menor de 4", que es lo mismo que <= 3 para enteros
               nivel_riesgo_num = 0
            elif puntuacion <= 26:  # Tu regla era "hasta 26"
               nivel_riesgo_num = 1
            else:  # Mayor de 26
               nivel_riesgo_num = 2

        # Traducimos el nivel de riesgo numérico a texto usando el mapa
            texto_riesgo = riesgo_mapa.get(nivel_riesgo_num, "desconocido")

        # Creamos un diccionario estructurado con toda la información útil
            riesgo_data = {
                'nombre': nombre_sustancia,  # El verbose_name, ej: "a) Tabaco (...)"
                'puntuacion': puntuacion,  # La puntuación total, ej: 28
                'riesgo': texto_riesgo  # El texto del riesgo, ej: "Alto"
              }
            datos_finales.append(riesgo_data)

        return datos_finales

class SituacionFamiliar(models.Model):


    opcionesAcuerdooNo = [(5, '5'), (4, '4'), (3, '3'), (2, '2'), (1, '1')]
    opcionesCuandoesta = [(1, 'No'), (2, 'Si, pero solo mis amigos'), (3, 'Si, pero solo mi familia'), (4, 'Si, tanto mi familia como mis amigos')]
    opcionesConflicto =[(1,'Si'),(0,'No')]
    expediente=models.CharField(max_length=10, primary_key=True, verbose_name='No.Expediente',null=False, blank=True, unique=True)
    quienesintegran=models.TextField(verbose_name='Quienes integran su familia (con quienes mas contacto tenga)',null=True,blank=True)
    hacercosasjuntos=models.SmallIntegerField(verbose_name='',choices=opcionesAcuerdooNo,null=True,default=1)
    nadiesepreocupa=models.SmallIntegerField(verbose_name='',choices=opcionesAcuerdooNo,null=True,   default=1)
    soncalidos=models.SmallIntegerField(verbose_name='',choices=opcionesAcuerdooNo,null=True,  default=1)
    expresaropiniones=models.SmallIntegerField(verbose_name='',choices=opcionesAcuerdooNo,null=True,  default=1)
    esdesagradable=models.SmallIntegerField(verbose_name='',choices=opcionesAcuerdooNo,null=True,   default=1)
    enconjunto=models.SmallIntegerField(verbose_name='',choices=opcionesAcuerdooNo,null=True,  default=1)
    meescucha=models.SmallIntegerField(verbose_name='',choices=opcionesAcuerdooNo,null=True,  default=1)
    platicoproblemas=models.SmallIntegerField(verbose_name='',choices=opcionesAcuerdooNo,null=True,   default=1)
    expresamoscarino=models.SmallIntegerField(verbose_name='',choices=opcionesAcuerdooNo,null=True,  default=1)
    nuncaseresuelven=models.SmallIntegerField(verbose_name='',choices=opcionesAcuerdooNo,null=True,  default=1)
    conflictograve=models.SmallIntegerField(verbose_name='Conflicto grave',null=True,choices=opcionesConflicto,default=0)
    cual=models.CharField(max_length=40,verbose_name='Cual',null=True,blank=True)
    papa=models.SmallIntegerField(verbose_name='Papa',choices=opcionesConflicto,null=True,default=0)
    cosumiopapa=models.CharField(max_length=15,verbose_name='Sustancia que consumio papa',null=True,blank=True)
    problemapapa=models.CharField(max_length=20,verbose_name='Problema causado a papa',null=True,blank=True)
    mama = models.SmallIntegerField(verbose_name='Mama', choices=opcionesConflicto, null=True, default=0)
    cosumiomama = models.CharField(max_length=15, verbose_name='Sustancia que consumio mama', null=True, blank=True)
    problemamama = models.CharField(max_length=20, verbose_name='Problema causado a mama', null=True, blank=True)
    hermano = models.SmallIntegerField(verbose_name='Hermano', choices=opcionesConflicto, null=True, default=0)
    cosumiohermano = models.CharField(max_length=15, verbose_name='Sustancia que consumio hermano(a)', null=True, blank=True)
    problemahermano = models.CharField(max_length=20, verbose_name='Problema causado a hermano(a)', null=True, blank=True)
    amigo = models.SmallIntegerField(verbose_name='Amigo', choices=opcionesConflicto, null=True, default=0)
    cosumioamigo = models.CharField(max_length=15, verbose_name='Sustancia que consumio amigo(a)', null=True,blank=True)
    problemaamigo = models.CharField(max_length=20, verbose_name='Problema causado a amigo(a)', null=True,blank=True)
    pareja = models.SmallIntegerField(verbose_name='Pareja', choices=opcionesConflicto, null=True, default=0)
    cosumiopareja = models.CharField(max_length=15, verbose_name='Sustancia que consumio pareja', null=True,blank=True)
    problemapareja = models.CharField(max_length=20, verbose_name='Problema causado a pareja', null=True, blank=True)
    familiar = models.SmallIntegerField(verbose_name='Familiar', choices=opcionesConflicto, null=True, default=0)
    cosumiofamiliar = models.CharField(max_length=15, verbose_name='Sustancia que consumio familiar', null=True,blank=True)
    problemafamiliar = models.CharField(max_length=20, verbose_name='Problema causado a familiar', null=True, blank=True)
    cuandoesta=models.SmallIntegerField(verbose_name='Cuando esta con:',choices=opcionesCuandoesta,null=True, default=1)
    ayudarian = models.CharField(max_length=60, verbose_name='Quienes le ayudarian', null=True, blank=True)
    dejadodehacer = models.CharField(max_length=60, verbose_name='Actividades que ha dejado de hacer', null=True, blank=True)
    relacionadas = models.CharField(max_length=60, verbose_name='Actividades relacionadas con el acohol/drogas', null=True, blank=True)
    diasnotrabajados = models.SmallIntegerField(verbose_name='Dias no trabajados', null=True,blank=True,default=0)
    vecesperdioempleo = models.SmallIntegerField(verbose_name='Veces que perdio el empleo',  null=True,blank=True,default=0)
    mejormuerto = models.SmallIntegerField(verbose_name='A pensado que es mejor estar muerto',choices=opcionesConflicto,null=True,default=0)
    ultimomesintentado = models.SmallIntegerField(verbose_name='A intentado suicidarse en el ultimo mes',choices=opcionesConflicto,null=True,default=0)
    haintentado = models.SmallIntegerField(verbose_name='Alguna vez en la vida ha intentado suicidarse?',choices=opcionesConflicto,null=True,default=0)
    presentaenfermedad = models.SmallIntegerField(verbose_name='Presenta alguna enfermedad?',choices=opcionesConflicto,null=True,default=0)
    cualenfermedad=models.CharField(max_length=30,verbose_name='Cual enfermedad',null=True,blank=True)
    derivadaporuso = models.SmallIntegerField(verbose_name='Enfermedad derivada por uso?',choices=opcionesConflicto, null=True,  default=0)
    siendoatendido = models.SmallIntegerField(verbose_name='Actualmente esta siendo atendido?',choices=opcionesConflicto, null=True, default=0)
    cualpadecimiento = models.CharField(max_length=30, verbose_name='Cual enfermedad', null=True, blank=True)
    medicado = models.SmallIntegerField(verbose_name='Estad miedicado actualmente?',choices=opcionesConflicto, null=True,  default=0)
    cualmedicina = models.CharField(max_length=60, verbose_name='Cual medicamento y cual es la razon', null=True, blank=True)
    estadointernado = models.SmallIntegerField(verbose_name='En los ultimos 12 meses ha estado internado en algun hospitalo?',choices=opcionesConflicto, null=True, default=0)
    porque = models.CharField(max_length=60, verbose_name='Por que?', null=True,blank=True)
    porconsumo = models.SmallIntegerField(verbose_name='Ha sido por problemas de consumo?',choices=opcionesConflicto, null=True,  default=0)
    clinica=models.CharField(max_length=30,verbose_name='Clinica',null=True,blank=True,default="Demostracion")
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO

class Cfisicas(models.Model):


    opcionesAfectado = [(1, 'Nada'), (2, 'Poco'), (3, 'Regular'), (4, 'Bastante')]
    opcionesComoeslarelacion = [(1, 'Muy buena'), (2, 'Buena'), (3, 'Regular'), (4, 'Mala'), (5, ' Muy mala')]
    opcionesComoloven = [(1, 'Lo ve bien'), (2, 'Ni bien ni mal'), (3, 'Lo ve mal')]
    opcionesSioNo = [(1, 'Si'), (0, 'No')]

    expediente=models.CharField(max_length=10, primary_key=True,null=False, blank=True, verbose_name='No.Expediente', unique=True)
    fp1 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Alteraciones en el ritmo cardiaco', null=True, default=0)
    fp1a = models.SmallIntegerField(choices=opcionesAfectado, null=True,   default=1)
    fp2 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Presion arterial (baja o alta)', null=True, default=0)
    fp2a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  default=1)
    fp3 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Insuficiencia cardiaca', null=True, default=0)
    fp3a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  default=1)
    fp4 =models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Infarto',null=True,default=0)
    fp4a=models.SmallIntegerField(choices=opcionesAfectado,null=True,   default=1)
    fp5=models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Varices esofagicas (se hacen anchas las venas del esofago)', null=True, default=0)
    fp5a = models.SmallIntegerField(choices=opcionesAfectado, null=True,   default=1)
    fp6 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Otro', null=True, default=0)
    fp6a = models.SmallIntegerField(verbose_name='Otro',choices=opcionesAfectado, null=True,  default=1)
    fp7=models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Desnutricion',null=True,default=0)
    fp7a=models.SmallIntegerField(choices=opcionesAfectado,null=True,   default=1)
    fp8 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Diabetes', null=True, default=0)
    fp8a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  default=1)
    fp9 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Gastritis', null=True, default=0)
    fp9a = models.SmallIntegerField(choices=opcionesAfectado, null=True,   default=1)
    fp10 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Hepatitis', null=True, default=0)
    fp10a = models.SmallIntegerField(choices=opcionesAfectado, null=True,   default=1)
    fp11 =models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Higado graso',null=True,default=0)
    fp11a=models.SmallIntegerField(choices=opcionesAfectado,null=True,  default=1)
    fp12=models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Ulceras', null=True, default=0)
    fp12a = models.SmallIntegerField(choices=opcionesAfectado, null=True,   default=1)
    fp13 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Acido urico', null=True, default=0)
    fp13a = models.SmallIntegerField(choices=opcionesAfectado, null=True,   default=1)
    fp14 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Cirrosis', null=True, default=0)
    fp14a = models.SmallIntegerField(choices=opcionesAfectado, null=True,   default=1)
    fp15 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Pancreatitis', null=True, default=0)
    fp15a = models.SmallIntegerField(choices=opcionesAfectado, null=True,   default=1)
    fp16 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Perdida de apetito', null=True, default=0)
    fp16a = models.SmallIntegerField(choices=opcionesAfectado, null=True,   default=1)
    fp17 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Otro', null=True, default=0)
    fp17a = models.SmallIntegerField(choices=opcionesAfectado, null=True,   default=1)
    fp18 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Descalcificacion', null=True, default=0)
    fp18a = models.SmallIntegerField(choices=opcionesAfectado, null=True,   default=1)
    fp19 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Fracturas', null=True, default=0)
    fp19a = models.SmallIntegerField(choices=opcionesAfectado, null=True,   default=1)
    fp20 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Perdida de dientes', null=True, default=0)
    fp20a = models.SmallIntegerField(choices=opcionesAfectado, null=True,   default=1)
    fp21 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Otro', null=True, default=0)
    fp21a = models.SmallIntegerField(choices=opcionesAfectado, null=True,   default=1)
    fp22 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Efisema pulmonar obstructiva', null=True,default=0)
    fp22a = models.SmallIntegerField(choices=opcionesAfectado, null=True,   default=1)
    fp23 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Tos', null=True, default=0)
    fp23a = models.SmallIntegerField(choices=opcionesAfectado, null=True,   default=1)
    fp24 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Neumonia', null=True, default=0)
    fp24a = models.SmallIntegerField(choices=opcionesAfectado, null=True,   default=1)
    fp25 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Tuberculosis', null=True, default=0)
    fp25a = models.SmallIntegerField(choices=opcionesAfectado, null=True,   default=1)
    fp26 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Otro', null=True, default=0)
    fp26a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  default=1)
    fotro = models.CharField(max_length=20,verbose_name='Otro',null=True,blank=True)
    fotro1 = models.CharField(max_length=20,verbose_name='Otro',null=True,blank=True)
    fotro2 = models.CharField(max_length=20,verbose_name='Otro',null=True,blank=True)
    fotro3 = models.CharField(max_length=20,verbose_name='Otro',null=True,blank=True)
    papa = models.BooleanField(verbose_name='Papa', null=True, blank=True, default=False)
    papaedad = models.SmallIntegerField(null=True,blank=True,default=0)
    papaescolaridad = models.CharField(max_length=20,null=True,blank=True)
    papasededica = models.CharField(max_length=20,null=True,blank=True)
    mama = models.BooleanField(verbose_name='Mama', null=True, blank=True, default=False)
    mamaedad = models.SmallIntegerField(null=True, blank=True,default=0)
    mamaescolaridad = models.CharField(max_length=20, null=True, blank=True)
    mamasededica = models.CharField(max_length=20, null=True, blank=True)
    comoesrelacion = models.SmallIntegerField(verbose_name='Como describes la relacion con tus padres?',choices=opcionesComoeslarelacion,null=True,  blank=True, default=1)
    cuantoshermanos = models.SmallIntegerField(verbose_name='Cuantos hermanos tienes',null=True,blank=True,default=1)
    quelugarocupas = models.SmallIntegerField(verbose_name='Que lugar ocupas',null=True,blank=True,default=1)
    relacionconhermanos = models.SmallIntegerField(verbose_name='Como es la relacion con tus hermanos',choices=opcionesComoeslarelacion, null=True,  blank=True, default=1)
    comovemama = models.SmallIntegerField(verbose_name='Mi madre o sustituta',choices=opcionesComoloven, null=True,  blank=True, default=1)
    comovepapa = models.SmallIntegerField(verbose_name='Mi padre o sustituto',choices=opcionesComoloven, null=True,  blank=True, default=1)
    comovemaestros = models.SmallIntegerField(verbose_name='Mis maestros/as o patrones/as',choices=opcionesComoloven, null=True,  blank=True, default=1)
    comoveamigos = models.SmallIntegerField(verbose_name='Mis amistades',choices=opcionesComoloven, null=True,  blank=True, default=1)
    comovepareja = models.SmallIntegerField(verbose_name='Mi pareja',choices=opcionesComoloven, null=True,  blank=True, default=1)
    comovehermanos = models.SmallIntegerField(verbose_name='Mis hermanos/as',choices=opcionesComoloven, null=True,  blank=True, default=1)
    fpr1 = models.SmallIntegerField(verbose_name='La mayoria de las veces tus padres/sustitutos saben en donde estas y que estas haciendo?',choices=opcionesSioNo,null=True, default=0)
    fpr2 = models.SmallIntegerField(verbose_name='Saben tus padres y/o sustitutos como sientes y piensas?',choices=opcionesSioNo,null=True, default=0)
    fpr3 = models.SmallIntegerField(verbose_name='Discutes frecuentemente con tus padrs y/o sustitutos levantando la voz o gritando?',choices=opcionesSioNo,null=True, default=0)
    fpr4 = models.SmallIntegerField(verbose_name='Estan de acuerdo tus padres y/o sustitutos en cuanto a la forma como te deben de dirigir? ',choices=opcionesSioNo,null=True, default=0)
    fpn1 = models.SmallIntegerField(verbose_name='Tus padres y/o sustitutos saben que consumes alcohol y/o drogas?',choices=opcionesSioNo,null=True, default=0)
    fpn2 = models.SmallIntegerField(verbose_name='Tus padres y/o sustitutos te han puesto las reglas muy claras en cuanto al consumo de alcohol y/o drogas?',choices=opcionesSioNo,null=True, default=0)
    fpn3 = models.SmallIntegerField(verbose_name='Es imprtante para ti cumplir con las normas que tienen tus padres y/o sustitutos acerca de tomar alchol y/o consumir drogas?',choices=opcionesSioNo,null=True, default=0)
    rsexuales = models.SmallIntegerField(verbose_name='Has tenido relaciones sexuales despues de consumir alcohol y/o drogas?',choices=opcionesSioNo,null=True, default=0)
    involucrado = models.SmallIntegerField(verbose_name='Te has involucrado en una situacion de abuso fisico a consecuencia de haber consumido alcohol y/o drogas?',choices=opcionesSioNo,null=True, default=0)
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True,default="Demostracion")
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO

    @property
    def consecuencias_fisicas(self):
        """
        Procesa las consecuencias físicas, las ordena por severidad de mayor a menor,
        y devuelve un string con las 3 más importantes, usando el `verbose_name`
        de cada campo como descripción.
        """
        consecuencias_presentes = []

        # Mapa para conectar los campos "Otro" con su respectivo campo de texto.
        mapa_otros = {
            6: 'fotro',
            17: 'fotro1',
            21: 'fotro2',
            26: 'fotro3',
        }

        severidad_mapa = {
            1: "Nada",
            2: "Poco",
            3: "Regular",
            4: "Bastante"
        }

        # 1. Recolectar todas las consecuencias que están marcadas como "Sí" (valor 1).
        for i in range(1, 27):
            nombre_campo_fp = f'fp{i}'
            nombre_campo_severidad = f'fp{i}a'

            existe = getattr(self, nombre_campo_fp)
            severidad = getattr(self, nombre_campo_severidad) or 1

            if existe == 1 and severidad > 0:
                campo = self._meta.get_field(nombre_campo_fp)
                nombre_consecuencia = campo.verbose_name

                if i in mapa_otros:
                    nombre_campo_otro = mapa_otros[i]
                    texto_otro = getattr(self, nombre_campo_otro)
                    if texto_otro and texto_otro.strip():
                        nombre_consecuencia = f"Otro: {texto_otro.strip()}"

                texto_severidad = severidad_mapa.get(severidad, "desconocido")

                # Creamos un diccionario con los datos estructurados
                consecuencia_data = {
                    'nombre': nombre_consecuencia,
                    'severidad': texto_severidad
                }

                consecuencias_presentes.append((severidad, consecuencia_data))

        if not consecuencias_presentes:
            return "Sin consecuencias significativas registradas."

        consecuencias_presentes.sort(key=lambda tupla: tupla[0], reverse=True)
        top_5_consecuencias = consecuencias_presentes[:5]
        nombres_finales = [nombre for severidad, nombre in top_5_consecuencias]
        return nombres_finales

    def __str__(self):
        return f"Registro para expediente {self.expediente}"
    # --- FIN DEL CÓDIGO A PEGAR ---

class Cmentales(models.Model):


    opcionesAfectado = [(1, 'Nada'), (2, 'Poco'), (3, 'Regular'), (4, 'Bastante')]
    opcionesSioNo = [(1, 'Si'), (0, 'No')]

    expediente=models.CharField(max_length=10, primary_key=True,null=False, blank=True, verbose_name='No.Expediente', unique=True)
    p1 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Alucinaciones (ver,oir,sentir,saborear,oler cosas que no existen)', null=True, default=0)
    p1a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  default=1)
    p2 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Insomnio', null=True, default=0)
    p2a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  default=1)
    p3 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Lagunas mentales (olvidos por episodios en tiempos que los que no supo que ocurrio)',  null=True, default=0)
    p3a = models.SmallIntegerField(choices=opcionesAfectado, null=True,   default=1)
    p4 =models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Convulsiones (el cuerpo de una persona rapida e incuntrolablemente)',null=True,default=0)
    p4a=models.SmallIntegerField(choices=opcionesAfectado,null=True,default=1)
    p5=models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Delirios (tener ideas de persecucion, grandeza etc.)', null=True, default=0)
    p5a = models.SmallIntegerField(choices=opcionesAfectado, null=True,   default=1)
    p6 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Problemas visuales', null=True, default=0)
    p6a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  default=1)
    p7=models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Dificultad para caminar',null=True,default=0)
    p7a=models.SmallIntegerField(choices=opcionesAfectado,null=True,default=1)
    p8 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Temblor', null=True, default=0)
    p8a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  default=1)
    p9 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Incordinacion motora', null=True, default=0)
    p9a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  default=1)
    p10 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Coma (la persona esta y es inconciente y es incapaz de moverse y responder a su ambiente)', null=True, default=0)
    p10a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  default=1)
    p11 =models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Golpes',null=True,default=0)
    p11a=models.SmallIntegerField(choices=opcionesAfectado,null=True,default=1)
    p12=models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Caidas', null=True, default=0)
    p12a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  default=1)
    p13 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Confusion mental (dificultad para pensar con claridad y rapidamente)', null=True, default=0)
    p13a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  default=1)
    p14 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Confabulaciones (hay un acuerdo entre personas para en su contra', null=True, default=0)
    p14a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  default=1)
    p15 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Accidentes', null=True, default=0)
    p15a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  default=1)
    p16 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Otro', null=True, default=0)
    p16a = models.SmallIntegerField(choices=opcionesAfectado, null=True,   default=1)
    p17 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Ideas confusas (no se entienden las ideas, pues combina cosas y ' +
                                                                      'personas al expresarse)', null=True, default=0)
    p17a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  default=1)
    p18 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Problemas para poner atencion y mantenerla', null=True, default=0)
    p18a = models.SmallIntegerField(choices=opcionesAfectado, null=True,   default=1)
    p19 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Problemas de memoria', null=True, default=0)
    p19a = models.SmallIntegerField(choices=opcionesAfectado, null=True,   default=1)
    p20 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Problemas de toma de decisiones', null=True, default=0)
    p20a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  default=1)
    p21 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Otro', null=True, default=0)
    p21a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  default=1)
    p22 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Ansiedad', null=True, default=0)
    p22a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    p23 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Celos', null=True, default=0)
    p23a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    p24 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Culpa', null=True, default=0)
    p24a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    p25 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Depresion', null=True, default=0)
    p25a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    p26 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Desesperacion ', null=True, default=0)
    p26a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    p27 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Ideas suicidas', null=True, default=0)
    p27a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    p28 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Inseguridad', null=True, default=0)
    p28a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    p29 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Intentos suicidas', null=True, default=0)
    p29a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    p30 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Irritabilidad', null=True, default=0)
    p30a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    p31 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Cambios drasticos de estado de animoTemor', null=True, default=0)
    p31a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    p32 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='TemorSentimientos de dañar a otro(a)', null=True, default=0)
    p32a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    p33 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Sentimientos de dañar a otro(a)', null=True, default=0)
    p33a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    p34 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Otro', null=True, default=0)
    p34a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    otro = models.CharField(max_length=20,verbose_name='Otro',null=True,blank=True)
    otro1 = models.CharField(max_length=20,verbose_name='Otro',null=True,blank=True)
    otro2 = models.CharField(max_length=20,verbose_name='Otro',null=True,blank=True)
    otro3 = models.CharField(max_length=20,verbose_name='Otro',null=True,blank=True)
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True, default="Demostracion")
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO

    @property
    def consecuencias_emocionales(self):
        """
        Procesa las consecuencias físicas, las ordena por severidad de mayor a menor,
        y devuelve un string con las 3 más importantes, usando el `verbose_name`
        de cada campo como descripción.
        """
        consecuencias_presentes = []

        # Mapa para conectar los campos "Otro" con su respectivo campo de texto.
        mapa_otros = {
            17: 'otro',
            21: 'otro2',
            34: 'otro3',
        }
        severidad_mapa = {
            1: "Nada",
            2: "Poco",
            3: "Regular",
            4: "Bastante"
        }
        # 1. Recolectar todas las consecuencias que están marcadas como "Sí" (valor 1).
        for i in range(1, 35):
            nombre_campo_fp = f'p{i}'
            nombre_campo_severidad = f'p{i}a'

            existe = getattr(self, nombre_campo_fp)
            severidad = getattr(self, nombre_campo_severidad) or 1

            if existe == 1 and severidad > 0:
                campo = self._meta.get_field(nombre_campo_fp)
                nombre_consecuencia = campo.verbose_name

                if i in mapa_otros:
                    nombre_campo_otro = mapa_otros[i]
                    texto_otro = getattr(self, nombre_campo_otro)
                    if texto_otro and texto_otro.strip():
                        nombre_consecuencia = f"Otro: {texto_otro.strip()}"


                texto_severidad = severidad_mapa.get(severidad, "desconocido")
                consecuencia_data = {
                    'nombre': nombre_consecuencia,
                    'severidad': texto_severidad
                }

                consecuencias_presentes.append((severidad, consecuencia_data))

        if not consecuencias_presentes:
            return "Sin consecuencias significativas registradas."

        consecuencias_presentes.sort(key=lambda tupla: tupla[0], reverse=True)
        top_5_consecuencias = consecuencias_presentes[:5]
        nombres_finales = [nombre for severidad, nombre in top_5_consecuencias]
        return nombres_finales

    def __str__(self):
        return f"Registro para expediente {self.expediente}"
    # --- FIN DEL CÓDIGO A PEGAR ---


class Crelaciones(models.Model):


    opcionesAfectado = [(1, 'Nada'), (2, 'Poco'), (3, 'Regular'), (4, 'Bastante')]
    opcionesSioNo = [(1, 'Si'), (0, 'No')]

    expediente=models.CharField(max_length=10,primary_key=True, null=False,blank=True, verbose_name='No.Expediente', unique=True)

    rp1 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Aislamiento', null=True, default=0)
    rp1a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp2 = models.SmallIntegerField(verbose_name='Correrle de la casa',choices=opcionesSioNo, null=True, default=0)
    rp2a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp3 = models.SmallIntegerField(verbose_name='Divorcio',choices=opcionesSioNo, null=True, default=0)
    rp3a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp4 =models.SmallIntegerField(verbose_name='Mentiras',choices=opcionesSioNo,null=True,default=0)
    rp4a=models.SmallIntegerField(choices=opcionesAfectado,null=True,blank=True,default=1)
    rp5=models.SmallIntegerField(verbose_name='Perdida de confianza', choices=opcionesSioNo,null=True, default=0)
    rp5a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp6 = models.SmallIntegerField(verbose_name='Perdida de amistades',choices=opcionesSioNo, null=True, default=0)
    rp6a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp7=models.SmallIntegerField(verbose_name='Perdida de comunicacion',choices=opcionesSioNo,null=True,default=0)
    rp7a=models.SmallIntegerField(choices=opcionesAfectado,null=True,blank=True,default=1)
    rp8 = models.SmallIntegerField(verbose_name='Ruptura de relaciones de pareja',choices=opcionesSioNo, null=True, default=0)
    rp8a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp9 = models.SmallIntegerField(verbose_name='Separaciones',choices=opcionesSioNo, null=True, default=0)
    rp9a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp10 = models.SmallIntegerField(verbose_name='Vivir fuera de la casa',choices=opcionesSioNo, null=True, default=0)
    rp10a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp11 =models.SmallIntegerField(verbose_name='Otro',choices=opcionesSioNo,null=True,default=0)
    rp11a=models.SmallIntegerField(choices=opcionesAfectado,null=True,blank=True,default=1)
    rp12=models.SmallIntegerField(verbose_name='Agresion fisica',choices=opcionesSioNo, null=True, default=0)
    rp12a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp13 = models.SmallIntegerField(verbose_name='Riñas,peleas',choices=opcionesSioNo, null=True, default=0)
    rp13a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp14 = models.SmallIntegerField(verbose_name='Gritos',choices=opcionesSioNo, null=True, default=0)
    rp14a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp15 = models.SmallIntegerField(verbose_name='Lesiones',choices=opcionesSioNo, null=True, default=0)
    rp15a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp16 = models.SmallIntegerField(verbose_name='Golpes que requieran hospitalizacion',choices=opcionesSioNo, null=True, default=0)
    rp16a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp17 = models.SmallIntegerField(verbose_name='Insultos',choices=opcionesSioNo, null=True, default=0)
    rp17a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp18 = models.SmallIntegerField(verbose_name='Romper objetos',choices=opcionesSioNo, null=True, default=0)
    rp18a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp19 = models.SmallIntegerField(verbose_name='Otro',choices=opcionesSioNo, null=True, default=0)
    rp19a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp20 = models.SmallIntegerField(verbose_name='Demanda por robo',choices=opcionesSioNo, null=True, default=0)
    rp20a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp21 = models.SmallIntegerField(verbose_name='Homicidio',choices=opcionesSioNo, null=True, default=0)
    rp21a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp22 = models.SmallIntegerField(verbose_name='Intento de homicidio', choices=opcionesSioNo,null=True, default=0)
    rp22a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp23 = models.SmallIntegerField(verbose_name='Detenciones',choices=opcionesSioNo, null=True, default=0)
    rp23a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp24 = models.SmallIntegerField(verbose_name='Encarcelamiento', choices=opcionesSioNo,null=True, default=0)
    rp24a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp25 = models.SmallIntegerField(verbose_name='Fecha,duracion y causas',choices=opcionesSioNo, null=True, default=0)
    rp25a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp26 = models.SmallIntegerField(verbose_name='Manejo de armas',choices=opcionesSioNo, null=True, default=0)
    rp26a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp27 = models.SmallIntegerField(verbose_name='Robo',choices=opcionesSioNo, null=True, default=0)
    rp27a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp28 = models.SmallIntegerField(verbose_name='Venta o transportacion de sustancias adictivas',choices=opcionesSioNo, null=True, default=0)
    rp28a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp29 = models.SmallIntegerField(verbose_name='Otro ',choices=opcionesSioNo, null=True, default=0)
    rp29a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp30 = models.SmallIntegerField(verbose_name='Deudas',choices=opcionesSioNo, null=True, default=0)
    rp30a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp31 = models.SmallIntegerField(verbose_name='Gasto excesivo',choices=opcionesSioNo, null=True, default=0)
    rp31a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp32 = models.SmallIntegerField(verbose_name='Empeñar',choices=opcionesSioNo, null=True, default=0)
    rp32a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp33 = models.SmallIntegerField(verbose_name='Pedir prestado',choices=opcionesSioNo, null=True, default=0)
    rp33a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp34 = models.SmallIntegerField(verbose_name='Otro',choices=opcionesSioNo, null=True, default=0)
    rp34a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp35 = models.SmallIntegerField(verbose_name='Accidentes laborales',choices=opcionesSioNo, null=True, default=0)
    rp35a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp36 = models.SmallIntegerField(verbose_name='Ausentismos',choices=opcionesSioNo, null=True, default=0)
    rp36a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp37 = models.SmallIntegerField(verbose_name='Cambio de puesto',choices=opcionesSioNo, null=True, default=0)
    rp37a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp38 = models.SmallIntegerField(verbose_name='Despido',choices=opcionesSioNo, null=True, default=0)
    rp38a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp39 = models.SmallIntegerField(verbose_name='Desempleo',choices=opcionesSioNo, null=True, default=0)
    rp39a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp40 = models.SmallIntegerField(verbose_name='Problemas con compañeros/as',choices=opcionesSioNo, null=True, default=0)
    rp40a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp41 = models.SmallIntegerField(verbose_name='Problemas con superiores',choices=opcionesSioNo, null=True, default=0)
    rp41a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp42 = models.SmallIntegerField(verbose_name='Retardos',choices=opcionesSioNo, null=True, default=0)
    rp42a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp43 = models.SmallIntegerField(verbose_name='Suspension laboral', choices=opcionesSioNo,null=True, default=0)
    rp43a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp44 = models.SmallIntegerField(verbose_name='Suspension de pago',choices=opcionesSioNo, null=True, default=0)
    rp44a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp45 = models.SmallIntegerField(verbose_name='Otro',choices=opcionesSioNo, null=True, default=0)
    rp45a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp46 = models.SmallIntegerField(verbose_name='Expulsiones',choices=opcionesSioNo, null=True, default=0)
    rp46a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp47 = models.SmallIntegerField(verbose_name='Inasistencias',choices=opcionesSioNo, null=True, default=0)
    rp47a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp48 = models.SmallIntegerField(verbose_name='Reprobar año',choices=opcionesSioNo, null=True, default=0)
    rp48a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp49 = models.SmallIntegerField(verbose_name='Reprobar materia',choices=opcionesSioNo, null=True, default=0)
    rp49a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp50 = models.SmallIntegerField(verbose_name='Retardos', choices=opcionesSioNo,null=True, default=0)
    rp50a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rp51 = models.SmallIntegerField(verbose_name='Otro',choices=opcionesSioNo, null=True, default=0)
    rp51a = models.SmallIntegerField(choices=opcionesAfectado, null=True,  blank=True, default=1)
    rotro = models.CharField(max_length=20,verbose_name='Otro',null=True,blank=True)
    rotro1 = models.CharField(max_length=20,verbose_name='Otro',null=True,blank=True)
    rotro2 = models.CharField(max_length=20,verbose_name='Otro',null=True,blank=True)
    rotro3 = models.CharField(max_length=20,verbose_name='Otro',null=True,blank=True)
    rotro4 = models.CharField(max_length=20,verbose_name='Otro',null=True,blank=True)
    rotro5 = models.CharField(max_length=20,verbose_name='Otro',null=True,blank=True)
    fechaduracionycausa = models.CharField(max_length=50,verbose_name='Fecha duracion y causa',null=True,blank=True)
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True, default="Demostracion")
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO


    # Dentro de tu modelo (ej. Cfisicas o un nuevo modelo de Relaciones)

    # --- INICIA EL CÓDIGO A PEGAR ---
    def _procesar_consecuencias_por_rango(self, start, end, prefijo='rp', mapa_otros=None):
        """
        MÉTODO AYUDANTE INTERNO.
        Este método no es una propiedad pública. Es una herramienta que procesa
        un rango específico de consecuencias y devuelve una lista ordenada por severidad.
        """
        if mapa_otros is None:
            mapa_otros = {}

        severidad_mapa = {
            1: "Nada",
            2: "Poco",
            3: "Regular",
            4: "Bastante"
        }
        consecuencias_presentes = []

        # 1. Recolectar consecuencias solo dentro del rango especificado (ej. de 1 a 10)
        for i in range(start, end + 1):
            nombre_campo = f'{prefijo}{i}'
            nombre_severidad = f'{prefijo}{i}a'

            # Usamos try/except por si algún campo no existe, para evitar que el programa se rompa.
            try:
                existe = getattr(self, nombre_campo)
                severidad = getattr(self, nombre_severidad) or 1
            except AttributeError:
                continue  # Si el campo no existe, simplemente lo saltamos y continuamos el bucle.

            if existe == 1 and severidad > 0:
                campo = self._meta.get_field(nombre_campo)
                nombre_consecuencia = campo.verbose_name

                # Lógica para campos "Otro"
                if i in mapa_otros:
                    nombre_campo_otro = mapa_otros[i]
                    texto_otro = getattr(self, nombre_campo_otro, '')  # Usamos default '' para seguridad
                    if texto_otro and texto_otro.strip():
                        nombre_consecuencia = f"Otro: {texto_otro.strip()}"

                texto_severidad = severidad_mapa.get(severidad, "desconocido")

                consecuencia_data = {
                    'nombre': nombre_consecuencia,
                    'severidad': texto_severidad
                }
                consecuencias_presentes.append((severidad, consecuencia_data))

        # 2. Ordenar la lista por severidad, de mayor a menor.
        consecuencias_presentes.sort(key=lambda tupla: tupla[0], reverse=True)

        top_5_consecuencias = consecuencias_presentes[:5]
        # 3. Devolver solo la lista de nombres. La plantilla manejará si está vacía.

        datos_finales = [data for severidad, data in top_5_consecuencias]

        return datos_finales

        # --- PROPIEDADES PÚBLICAS ---
        # Ahora definimos cada una de las 6 listas que necesitas.
        # Cada una es una simple llamada al método ayudante con los parámetros correctos.

    @property
    def consecuencias_relaciones(self):  # Rango 1-10
       # ¡IMPORTANTE! Debes definir aquí el mapa_otros SOLO para este rango.
        mapa = {11: 'rotro', 19: 'otro1'}  # El campo 11 está fuera de este rango, lo pongo de ejemplo
        # En tu caso, si el campo "otro" es el 10, sería: mapa = { 10: 'rotro' }
        return self._procesar_consecuencias_por_rango(1, 20, prefijo='rp', mapa_otros=mapa)

    @property
    def consecuencias_legal(self):  # Rango 11-19
        mapa = {25: 'fechaduracionycausa', 29: 'rotro2', }
        return self._procesar_consecuencias_por_rango(20, 29, prefijo='rp', mapa_otros=mapa)

    @property
    def consecuencias_economicos(self):  # Rango 20-34
        mapa = {34: 'rotro3'}
        return self._procesar_consecuencias_por_rango(30, 34, prefijo='rp', mapa_otros=mapa)

    @property
    def consecuencias_laboralyescolar(self):  # Rango 35-45
        mapa = {45: 'rotro4', 51: 'otro5'}
        return self._procesar_consecuencias_por_rango(35, 51, prefijo='rp', mapa_otros=mapa)


class Tratamientos(models.Model):


    opcionesSatisfecho = [(1, 'Muy satisfecho'), (2, 'Satisfecho'), (3, 'Inseguro'), (4, 'Insatisfecho'), (5, 'Muy insatisfecho')]

    opcionesSioNo = [(1, 'Si'), (0, 'No')]

    expediente=models.CharField(max_length=10,primary_key=True, null=False, blank=True,verbose_name='No.Expediente', unique=True)
    recibio = models.SmallIntegerField(choices=opcionesSioNo,null=True, default=0)
    a1 = models.SmallIntegerField(verbose_name='Centro de desintoxicacion',choices=opcionesSioNo,null=True, default=0)
    d1 = models.SmallIntegerField(choices=opcionesSioNo,null=True, default=0)
    c1 = models.SmallIntegerField(choices=opcionesSioNo,null=True, default=0)
    h1 = models.CharField(max_length=15,null=True,blank=True)
    r1 = models.CharField(max_length=15,null=True,blank=True)
    a2 = models.SmallIntegerField(verbose_name='Tratamiento de consulta, ayuda mutua,mixto, profesional ',choices=opcionesSioNo,null=True, default=0)
    d2 = models.SmallIntegerField(choices=opcionesSioNo,null=True, default=0)
    c2 = models.SmallIntegerField(choices=opcionesSioNo,null=True, default=0)
    h2 = models.CharField(max_length=15,null=True,blank=True)
    r2 = models.CharField(max_length=15,null=True,blank=True)
    a3 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Alternativo o religioso ',null=True, default=0)
    d3 = models.SmallIntegerField(choices=opcionesSioNo,null=True, default=0)
    c3 = models.SmallIntegerField(choices=opcionesSioNo,null=True, default=0)
    h3 = models.CharField(max_length=15,null=True,blank=True)
    r3 = models.CharField(max_length=15,null=True,blank=True)
    a4 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Tratamiento de internamiento (ayuda mutua,mixto,profesional,alternativos o religioso)',null=True, default=0)
    d4 = models.SmallIntegerField(choices=opcionesSioNo,null=True, default=0)
    c4 = models.SmallIntegerField(choices=opcionesSioNo,null=True, default=0)
    h4 = models.CharField(max_length=15,null=True,blank=True)
    r4 = models.CharField(max_length=15,null=True,blank=True)
    a5 = models.SmallIntegerField(verbose_name='Tratamiento medico',choices=opcionesSioNo,null=True, default=0)
    d5 = models.SmallIntegerField(choices=opcionesSioNo,null=True, default=0)
    c5 = models.SmallIntegerField(choices=opcionesSioNo,null=True, default=0)
    h5 = models.CharField(max_length=15,null=True,blank=True)
    r5 = models.CharField(max_length=15,null=True,blank=True)
    a6 = models.SmallIntegerField(verbose_name='Tratamiento psiquiatrico ',choices=opcionesSioNo,null=True, default=0)
    d6 = models.SmallIntegerField(choices=opcionesSioNo,null=True, default=0)
    c6 = models.SmallIntegerField(choices=opcionesSioNo,null=True, default=0)
    h6 = models.CharField(max_length=15,null=True,blank=True)
    r6 = models.CharField(max_length=15,null=True,blank=True)
    a7 = models.SmallIntegerField(verbose_name='Tratamiento psicologico ',choices=opcionesSioNo,null=True, default=0)
    d7 = models.SmallIntegerField(choices=opcionesSioNo,null=True, default=0)
    c7 = models.SmallIntegerField(choices=opcionesSioNo,null=True, default=0)
    h7 = models.CharField(max_length=15,null=True,blank=True)
    r7 = models.CharField(max_length=15,null=True,blank=True)
    a8 = models.SmallIntegerField(verbose_name='Otro ',choices=opcionesSioNo,null=True, default=0)
    d8 = models.SmallIntegerField(choices=opcionesSioNo,null=True, default=0)
    c8 = models.SmallIntegerField(choices=opcionesSioNo,null=True, default=0)
    h8 = models.CharField(max_length=15,null=True,blank=True)
    r8 = models.CharField(max_length=15,null=True,blank=True)
    cual = models.CharField(verbose_name='Espesifique',max_length=20, null=True, blank=True)
    cual1 = models.CharField(verbose_name='Espesifique',max_length=20, null=True, blank=True)
    cual2 = models.CharField(verbose_name='Otro',max_length=20, null=True, blank=True)
    satisfecho=models.SmallIntegerField(verbose_name='Que tan satisfecho se encuentra con su estilo de vida',choices=opcionesSatisfecho,null=True,  default=1)
    meta1=models.CharField(verbose_name='Consumo de drogas ',max_length=100,null=True,blank=True)
    meta2=models.CharField(verbose_name='Salud fisica (alimentacion, ejercicio, descanso)',max_length=100,null=True,blank=True)
    meta3=models.CharField(verbose_name='Trabajo y/o Escuela',max_length=100,null=True,blank=True)
    meta4=models.CharField(verbose_name='Manejo de dinero',max_length=100,null=True,blank=True)
    meta5=models.CharField(verbose_name='Relaciones de pareja',max_length=100,null=True,blank=True)
    meta6=models.CharField(verbose_name='Situacion legal',max_length=100,null=True,blank=True)
    meta7=models.CharField(verbose_name='Vida emocional',max_length=100,null=True,blank=True)
    meta8=models.CharField(verbose_name='Comunicacion',max_length=100,null=True,blank=True)
    meta9=models.CharField(verbose_name='Social,recreativas(relacion con amistades y actividades de esparcimiento)',max_length=100,null=True,blank=True)
    meta10=models.CharField(verbose_name='Relaciones de pareja',max_length=100,null=True,blank=True)
    problemas=models.TextField(verbose_name='Problemas presentados durante la sesion (al comunicarse, su actitud)',null=True,blank=True)
    observaciones=models.TextField(verbose_name='Observaciones :',null=True,blank=True)
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True, default="Demostracion")
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO


class Psicosis(models.Model):


    opcionesQuesiente = [(0, 'Nada'), (1, 'Muy poco'), (2, 'Poco'), (3, 'Bastante'), (4, 'Mucho')]

    expediente=models.CharField(max_length=10, primary_key=True,null=False, blank=True, verbose_name='No.Expediente', unique=True)
    pp1 = models.SmallIntegerField(choices=opcionesQuesiente,verbose_name='Perder la confianza en la mayoria de las personas', null=True, default=0)
    pp2 = models.SmallIntegerField(choices=opcionesQuesiente,verbose_name='Sentir que me vigilan o hablan de mi', null=True, default=0)
    pp3 = models.SmallIntegerField(choices=opcionesQuesiente,verbose_name='Tener ideas o pensamientos que los demas no los entienden', null=True, default=0)
    pp4 =models.SmallIntegerField(choices=opcionesQuesiente,verbose_name='Sentir que los demas no me valoran como merezco',null=True,default=0)
    pp5=models.SmallIntegerField(choices=opcionesQuesiente,verbose_name='Sentir que se aprovechan de mi si me dejo', null=True, default=0)
    pp6 = models.SmallIntegerField(choices=opcionesQuesiente,verbose_name='Sentir que alguien puede controlar mis pensamientos', null=True, default=0)
    pp7=models.SmallIntegerField(choices=opcionesQuesiente,verbose_name='Escuchar voces que otras personas no pueden oir',null=True,default=0)
    pp8 = models.SmallIntegerField(choices=opcionesQuesiente,verbose_name='Creer que la gente sabe lo que estoy pensando', null=True, default=0)
    pp9 = models.SmallIntegerField(choices=opcionesQuesiente,verbose_name='Tener ideas o pensamientos que no son los mios', null=True, default=0)
    pp10 = models.SmallIntegerField(choices=opcionesQuesiente,verbose_name='Sentirme Solo/a aun estando con gente', null=True, default=0)
    pp11 =models.SmallIntegerField(choices=opcionesQuesiente,verbose_name='Pensar cosas sobre el sexo que me molestan',null=True,default=0)
    pp12=models.SmallIntegerField(choices=opcionesQuesiente,verbose_name='Ver cosas que otros no pueden ver', null=True, default=0)
    pp13 = models.SmallIntegerField(choices=opcionesQuesiente,verbose_name='Sentir que debo ser castigado/a por mis pecados', null=True, default=0)
    pp14 = models.SmallIntegerField(choices=opcionesQuesiente,verbose_name='Sentir que algo anda mal en mi cuerpo', null=True, default=0)
    pp15 = models.SmallIntegerField(choices=opcionesQuesiente,verbose_name='Sentirme alejado/a de las demas personas', null=True, default=0)
    pp16 = models.SmallIntegerField(choices=opcionesQuesiente,verbose_name='Sentir algo caminando o moviendose en mi cuerpo que no se pueda ver', null=True, default=0)
    pp17 = models.SmallIntegerField(choices=opcionesQuesiente,verbose_name='Pensar que en mi cabeza hay algo que no funciona bien', null=True, default=0)
    psfecha = models.DateField(verbose_name="Fecha de custionario",default=date.today,null=True,blank="True")
    psconsejero = models.SmallIntegerField(verbose_name="Consejero",blank=True,null=True)
    pspuntos = models.SmallIntegerField(verbose_name="Puntaje",null=True,blank=True)
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True, default="Demostracion")
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO


    @property
    def sintomas_psicosis(self):

        sintomas_presentes = []

        severidad_mapa = {
            0: "Nada",
            1: "Muy Poco",
            2: "Poco",
            3: "Bastante",
            4: "Mucho"
        }

        # 1. Recolectar todas las consecuencias que están marcadas como "Sí" (valor 1).
        for i in range(1, 18):
            nombre_campo_pp = f'pp{i}'
            severidad = getattr(self, nombre_campo_pp)

            campo = self._meta.get_field(nombre_campo_pp)
            nombre_consecuencia = campo.verbose_name
           # Creamos un diccionario con los datos estructurados

            sintomas_presentes.append((severidad, nombre_consecuencia))

        if not sintomas_presentes:
            return "Sin sintomas significativos registradas."

        sintomas_presentes.sort(key=lambda tupla: tupla[0], reverse=True)
        top_5_sintomas = sintomas_presentes[:5]

        datos_finales = []
        for severidad, nombre_sintoma in top_5_sintomas:
            texto_severidad = severidad_mapa.get(severidad, "desconocido")
            datos_finales.append({
                'nombre': nombre_sintoma,
                'severidad': texto_severidad
            })


        # Unimos todas las líneas en un solo string, separadas por un salto de línea
        resumen_final = datos_finales

        return resumen_final

    def __str__(self):
        return f"Registro para expediente {self.expediente}"
    # --- FIN DEL CÓDIGO A PEGAR ---


class Sdevida(models.Model):

    opcionesSatisfecho = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'),(6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')]

    expediente=models.CharField(max_length=10, primary_key=True,null=False, blank=True, verbose_name='No.Expediente', unique=True)
    svp1 = models.SmallIntegerField(choices=opcionesSatisfecho,verbose_name='Consumo de drogas', null=True, default=0)
    svp2 = models.SmallIntegerField(choices=opcionesSatisfecho,verbose_name='Progreso en el trabajo o en la escuela',null=True, default=0)
    svp3 = models.SmallIntegerField(choices=opcionesSatisfecho,verbose_name='Manejo de dinero', null=True, default=0)
    svp4 =models.SmallIntegerField(choices=opcionesSatisfecho,verbose_name='Vida social/recreativa',null=True,default=0)
    svp5=models.SmallIntegerField(choices=opcionesSatisfecho,verbose_name='Salud fisica', null=True, default=0)
    svp6 = models.SmallIntegerField(choices=opcionesSatisfecho,verbose_name='Relaciones familiares y/o matrimoniales', null=True, default=0)
    svp7=models.SmallIntegerField(choices=opcionesSatisfecho,verbose_name='Situacion legal',null=True,default=0)
    svp8 = models.SmallIntegerField(choices=opcionesSatisfecho,verbose_name='Vida emocional', null=True, default=0)
    svp9 = models.SmallIntegerField(choices=opcionesSatisfecho,verbose_name='Comunicacion', null=True, default=0)
    svp10 = models.SmallIntegerField(choices=opcionesSatisfecho,verbose_name='Ejercicio fisico', null=True, default=0)
    svp11 =models.SmallIntegerField(choices=opcionesSatisfecho,verbose_name='Vida espiritual y moral',null=True,default=0)
    svp12=models.SmallIntegerField(choices=opcionesSatisfecho,verbose_name='Satisfaccion en general', null=True, default=0)
    svfecha = models.DateField(verbose_name="Fecha de custionario",default=date.today,null=True,blank="True")
    svconsejero = models.SmallIntegerField(verbose_name="Consejero",blank=True,null=True)
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True, default="Demostracion")
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO


    @property
    def satisfaccion_vida(self):

        def traducir_valor_a_satisfaccion(valor):
            if valor >= 1 and valor <= 5:
                return "Completamente Insatisfecho"
            elif valor >= 6 and valor <= 7:
                return "Insatisfecho"
            elif valor == 8 :
                return "Satisfecho"
            elif valor >8:
                return "Totalmente Satisfecho"
            else:
                return "No evaluado"

    # --- PASO 1: Recolectar todas las áreas con su puntuación ---
        areas_con_puntuacion = []
        for i in range(1, 13):
            nombre_campo = f'svp{i}'
            puntuacion = getattr(self, nombre_campo, 0) or 0

        # Solo procesamos áreas que han sido evaluadas (puntuación > 0)
            if puntuacion > 0:
               areas_con_puntuacion.append((puntuacion, nombre_campo))

    # Si no hay ninguna área evaluada, devolvemos una lista vacía
        if not areas_con_puntuacion:
          return []

    # --- PASO 2 (CLAVE): Ordenar por puntuación de MENOR a MAYOR ---
    # `reverse=False` es el comportamiento por defecto, pero lo ponemos para claridad.
    # Los valores más bajos (mayor insatisfacción) quedarán al principio.
        areas_con_puntuacion.sort(key=lambda tupla: tupla[0], reverse=False)

    # --- PASO 3: Tomar solo los 5 primeros (los top 5 de insatisfacción) ---
        top_5_insatisfechos = areas_con_puntuacion[:5]

    # --- PASO 4: Procesar estos 5 para crear la lista final ---
        datos_finales = []
        for puntuacion, nombre_campo in top_5_insatisfechos:
            campo = self._meta.get_field(nombre_campo)
            nombre_area = campo.verbose_name

            texto_satisfaccion = traducir_valor_a_satisfaccion(puntuacion)

            satisfaccion_data = {
               'area': nombre_area,
               'nivel': texto_satisfaccion,
               'puntuacion': puntuacion
        }

            datos_finales.append(satisfaccion_data)

        return datos_finales





class Usodrogas(models.Model):

    opcionesSioNo = [(1, 'Si'), (0, 'No')]

    expediente=models.CharField(max_length=10, primary_key=True,null=False, blank=True, verbose_name='No.Expediente', unique=True)
    udp1 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Ha usado drogas diferentes de las que se usas epor razones medicas?', null=True, default=0)
    udp2 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Ha abusado de drogas de prescripcion medica?',null=True, default=0)
    udp3 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Ha abusado de drogas al mismo tiempo?', null=True, default=0)
    udp4 =models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Puede transcurrir una semana sin que use drogas?',null=True,default=0)
    udp5=models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Puede dejar de utilizar drogas cuando quiera?', null=True, default=0)
    udp6 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Ha tenido lagunas mentales o alucinaciones como resultado de uso de drogas?', null=True, default=0)
    udp7=models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Alguna vez se a sentido mal o culpable por su uso de drogas?',null=True,default=0)
    udp8 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Su pareja o familiares se quejan constantemente por su involucramiento en el uso de drogas?', null=True, default=0)
    udp9 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='El abuso de drogas ha creado problemas con su pareja o familiares?', null=True, default=0)
    udp10 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Ha perdido amistades por su uso de drogas?', null=True, default=0)
    udp11 =models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Ha descuidado a su familia o ha faltado a su trabajo como consecuencia del uso de drogas?',null=True,default=0)
    udp12=models.SmallIntegerField(choices=opcionesSioNo,verbose_name='Ha tenido problemas en el trabajo o escuela debido al uso de drogas?', null=True, default=0)
    udp13 = models.SmallIntegerField(choices=opcionesSioNo, verbose_name='Ha perdido algun trabajo debido al uso de drogas?', null=True, default=0)
    udp14 = models.SmallIntegerField(choices=opcionesSioNo, verbose_name='Se ha involucrado en peleas cuando esta bajo la influencia de drogas?',null=True, default=0)
    udp15 = models.SmallIntegerField(choices=opcionesSioNo, verbose_name='Se ha involucrado en actividades ilegales con tal de obtener drogas?', null=True, default=0)
    udp16 = models.SmallIntegerField(choices=opcionesSioNo, verbose_name='Lo han arrestado por posesion de drogas ilegales?', null=True, default=0)
    udp17 = models.SmallIntegerField(choices=opcionesSioNo, verbose_name='Alguna vez ha experiemntado el sindrome del retiro (sudoracion, taquicardia, ansiedad entre otros) cuando ha dejado de usar drogas?', null=True, default=0)
    udp18 = models.SmallIntegerField(choices=opcionesSioNo, verbose_name='Ha tenido problemas medicos como resultado del uso de drogas (ejemplo : perdida de memoria, hepatitis,convulciones, sangrado entre otros)', null=True, default=0)
    udp19 = models.SmallIntegerField(choices=opcionesSioNo, verbose_name='Ha pedido a alguien que le ayude a resolver su problema con las drogas?', null=True, default=0)
    udp20 = models.SmallIntegerField(choices=opcionesSioNo, verbose_name='Ha estado en un tratamiento especificamente relacionado con el uso de drogas?', null=True, default=0)
    udfecha = models.DateField(verbose_name="Fecha de custionario",default=date.today,null=True,blank="True")
    udconsejero = models.SmallIntegerField(verbose_name="Consejero",blank=True,null=True)
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True, default="Demostracion")
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO

class Ansiedad(models.Model):

    opcionesAnsiedad = [(0, 'Poco o Nada'), (1, 'Mas o Menos'),(2,'Moderadamente'),(3,'Severamente')]

    expediente=models.CharField(max_length=10, primary_key=True,null=False, blank=True, verbose_name='No.Expediente', unique=True)
    anp1 = models.SmallIntegerField(choices=opcionesAnsiedad,verbose_name='Etumecimiento, hormigueo de una o varias partes del cuerpo', null=True, default=0)
    anp2 = models.SmallIntegerField(choices=opcionesAnsiedad,verbose_name='Sentir oleadas de calor (bochorno)',null=True, default=0)
    anp3 = models.SmallIntegerField(choices=opcionesAnsiedad,verbose_name='Debilitamiento de piernas', null=True, default=0)
    anp4 =models.SmallIntegerField(choices=opcionesAnsiedad,verbose_name='Dificultad para relajarse',null=True,default=0)
    anp5=models.SmallIntegerField(choices=opcionesAnsiedad,verbose_name='Miedo a que pase lo peor', null=True, default=0)
    anp6 = models.SmallIntegerField(choices=opcionesAnsiedad,verbose_name='Sensacion de mareo', null=True, default=0)
    anp7=models.SmallIntegerField(choices=opcionesAnsiedad,verbose_name='Opresion en el pecho o latidos acelerados',null=True,default=0)
    anp8 = models.SmallIntegerField(choices=opcionesAnsiedad,verbose_name='Inseguridad', null=True, default=0)
    anp9 = models.SmallIntegerField(choices=opcionesAnsiedad,verbose_name='Terror', null=True, default=0)
    anp10 = models.SmallIntegerField(choices=opcionesAnsiedad,verbose_name='Nerviosismo', null=True, default=0)
    anp11 =models.SmallIntegerField(choices=opcionesAnsiedad,verbose_name='Sensacion de ahogo',null=True,default=0)
    anp12=models.SmallIntegerField(choices=opcionesAnsiedad,verbose_name='Manos temblorosas', null=True, default=0)
    anp13 = models.SmallIntegerField(choices=opcionesAnsiedad, verbose_name='Cuerpo tembloroso', null=True, default=0)
    anp14 = models.SmallIntegerField(choices=opcionesAnsiedad, verbose_name='Miedo a perder el control?',null=True, default=0)
    anp15 = models.SmallIntegerField(choices=opcionesAnsiedad, verbose_name='Dificultad para respirar', null=True, default=0)
    anp16 = models.SmallIntegerField(choices=opcionesAnsiedad, verbose_name='Miedo a morir', null=True, default=0)
    anp17 = models.SmallIntegerField(choices=opcionesAnsiedad, verbose_name='Asustado', null=True, default=0)
    anp18 = models.SmallIntegerField(choices=opcionesAnsiedad, verbose_name='Indigestion o malestar estomacal', null=True, default=0)
    anp19 = models.SmallIntegerField(choices=opcionesAnsiedad, verbose_name='Debilidad', null=True, default=0)
    anp20 = models.SmallIntegerField(choices=opcionesAnsiedad, verbose_name='Ruborizarse', null=True, default=0)
    anp21 = models.SmallIntegerField(choices=opcionesAnsiedad, verbose_name='Sudoracion (no debido al calor)', null=True, default=0)
    anfecha = models.DateField(verbose_name="Fecha de custionario",default=date.today,null=True,blank="True")
    anconsejero = models.SmallIntegerField(verbose_name="Consejero",blank=True,null=True)
    anpuntos = models.SmallIntegerField(verbose_name="Puntaje", null=True, blank=True)
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True, default="Demostracion")
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO

    @property
    def sintomas_ansiedad(self):

        sintomas_presentes = []

        severidad_mapa = {
            0: "Poco o nada",
            1: "Mas o menos",
            2: "Moderadamente",
            3: "Severamente",

        }

        # 1. Recolectar todas las consecuencias que están marcadas como "Sí" (valor 1).
        for i in range(1, 22):
            nombre_campo_pp = f'anp{i}'
            severidad = getattr(self, nombre_campo_pp)

            campo = self._meta.get_field(nombre_campo_pp)
            nombre_consecuencia = campo.verbose_name
            # Creamos un diccionario con los datos estructurados

            sintomas_presentes.append((severidad, nombre_consecuencia))

        if not sintomas_presentes:
            return "Sin sintomas significativos registradas."

        sintomas_presentes.sort(key=lambda tupla: tupla[0], reverse=True)
        top_5_sintomas = sintomas_presentes[:5]

        datos_finales = []
        for severidad, nombre_sintoma in top_5_sintomas:
            texto_severidad = severidad_mapa.get(severidad, "desconocido")
            datos_finales.append({
                'nombre': nombre_sintoma,
                'severidad': texto_severidad
            })

        # Unimos todas las líneas en un solo string, separadas por un salto de línea
        resumen_final = datos_finales

        return resumen_final

    def __str__(self):
        return f"Registro para expediente {self.expediente}"
    # --- FIN DEL CÓDIGO A PEGAR ---


class Depresion(models.Model):

    opcionesP1 = [(0, 'No me siento triste'), (1, 'Me siento triste'),(2,'Me siento triste todo el tiempo y no puedo evitarlo'),(3,'Estoy tan triste o infeliz que no puedo soportarlo')]
    opcionesP2 = [(0, 'No siento que me estan castigando'), (1, 'Siento que me podrian castigar'),(2,'Creo que me van a castigar'),(3,'Siento que se me esta castigando')]
    opcionesP3 = [(0, 'En general tengo esperanzas en mi futuro'), (1, 'Me siento sin esperanzas por mi futuro'),(2,'Siento que no puedo esperar nada del futuro'),(3,'Siento que el futuro no tiene esperanza y las cosas no pueden mejorar')]
    opcionesP4 = [(0, 'No estoy desilusionado(a) de mi mismo(a)'), (1, 'Esto desilusionado(a) de mi mismo(a)'),(2,'Estoy disgustado(a) de mi mismo(a)'),(3,'Me odio')]
    opcionesP5 = [(0, 'No me siento como un fracasado(a)'), (1, 'Siento que he fracasado mas que las personas en general'),(2,'Al repasar lo que he vivido todo lo que veo son muchos fracasos'),(3,'Siento que soy un completo fracaso como persona')]
    opcionesP6 = [(0, 'No me siento que sea peor que otras personas'), (1, 'Me critico a mi mismo(a) por mis debilidades y/o errores'),(2,'Me culpo todo el tiempo por mis fallas'),(3,'Me culpo por todo lo malo que sucede')]
    opcionesP7 = [(0, 'Obtengo tanta satisfaccion de las cosas como solia tenerla antes'), (1, 'No disfruto las cosas como antes'),(2,'Ya no obtengo verdadera satisfaccion de nada'),(3,'Estoy insastifecho(a) o aburrido(a) de todo')]
    opcionesP8 = [(0, 'No tengo pensamientos suicidas'), (1, 'Tengo pensamientos suicidas pero no los llevaria acabo'),(2,'Me gustaria suicidarme'),(3,'Me suicidaria si tuviera oportunidad')]
    opcionesP9 = [(0, 'No me siento culpable'), (1, 'Me siento culpable la gran parte del tiempo'),(2,'Me siento culpable casi todo el tiempo'),(3,'Me siento culpable todo el tiempo')]
    opcionesP10 = [(0, 'No lloro mas de lo normal'), (1, 'Lloro mas que antes'),(2,'Actualmente lloro todo el tiempo'),(3,'Antes podia llorar, pero ahora n o lo puedo hacer aunque tenga ganas')]
    opcionesP11 = [(0, 'No me siento irritable'), (1, 'Me enojo o me irrito mas facilmente que antes'),(2,'Me siento irritado todo el tiempo'),(3,'Ya no me irrito por las cosas que me irritaba antes')]
    opcionesP12 = [(0, 'Mi apetito es igual que siempre'), (1, 'Mi apetito ya no es tan bueno como antes'),(2,'Mi apetito esta muy mal ahora'),(3,'No tengo nada de apetito')]
    opcionesP13 = [(0, 'No he perdido interes en la gente'), (1, 'Estoy meno interesado(a) en la gente que antes'),(2,'He perdido mucho interes en la gente'),(3,'He perdido todo el interes en la gente')]
    opcionesP14 = [(0, 'No he perdido mucho peso ultimamente'), (1, 'He perdido mas de 2 Kilogramos'),(2,'He perdido mas de 5 Kilogramos'),(3,'He perdido mas de 8 Kilogramos')]
    opcionesP15 = [(0, 'Tomo decisiones tan bien como siempre lo he hecho'), (1, 'Dejo para despues varias decisiones que necesito tomar'),(2,'Ahora se me hace mas dificil tomar decisiones'),(3,'No puedo tomar decisiones')]
    opcionesP16 = [(0, 'No estoy mas preocupado(a) por mi saludo que antes'), (1, 'Estoy preocupado(a) por mi salud fisica, como dolores malestar estomacal o dificultad para respirar'),(2,'Estoy preocupado(a) por problemas de mi salud fisica y se ma hace dificil pensar en algo mas'),(3,'Estoy tan preocupado(a) por mis problemas de salud fisica que no puedo pensar en algo mas')]
    opcionesP17 = [(0, 'No me siento que me veo peor de como me veia antes'), (1, 'Estoy preocupado(a) por verme viejo(a) o poco atractivo(a)'),(2,'Siento que hay cambios definitivos en mi apariencia que me hacen ver poco atractivo(a)'),(3,'Creo me veo feo(a)')]
    opcionesP18 = [(0, 'Tengo el mismo interes que he tenido siempre en el sexo'), (1, 'Tengo menos interes en el sexo que antes'),(2,'Ahora tengo mucho menos interes en el sexo'),(3,'Ahora he perdido completamente el interes en el sexo')]
    opcionesP19 = [(0, 'Puedo trabajar tan bien como antes'), (1, 'Necesito esforzarme mas para empezar a hacer algo'),(2,'Me tengo que obligar para hacer algo'),(3,'No puedo hacer ningun trabajo')]
    opcionesP20 = [(0, 'Puedo dormir tan bien como antes'), (1, 'Ya no duermo tan bien como antes'),(2,'Me despierto una o dos horas antes de lo normal y me cuesta trabajo volverme a dormir'),(3,'Me despierto muchas horas antes de lo de costumbre y no puedo volverme a dormir')]
    opcionesP21 = [(0, 'No me canso mas de lo de costumbre'), (1, 'Me canso mas facilmente que antes'),(2,'Con cualquier cosa que haga me canso'),(3,'Estoy muy cansado para hacer cualquier cosa')]

    expediente=models.CharField(max_length=10, primary_key=True,null=False, blank=True, verbose_name='No.Expediente', unique=True)
    dep1 = models.SmallIntegerField(choices=opcionesP1,verbose_name='', null=True, default=0)
    dep2 = models.SmallIntegerField(choices=opcionesP2,verbose_name='',null=True, default=0)
    dep3 = models.SmallIntegerField(choices=opcionesP3,verbose_name='', null=True, default=0)
    dep4 =models.SmallIntegerField(choices=opcionesP4,verbose_name='',null=True,default=0)
    dep5=models.SmallIntegerField(choices=opcionesP5,verbose_name='', null=True, default=0)
    dep6 = models.SmallIntegerField(choices=opcionesP6,verbose_name='', null=True, default=0)
    dep7=models.SmallIntegerField(choices=opcionesP7,verbose_name='',null=True,default=0)
    dep8 = models.SmallIntegerField(choices=opcionesP8,verbose_name='', null=True, default=0)
    dep9 = models.SmallIntegerField(choices=opcionesP9,verbose_name='', null=True, default=0)
    dep10 = models.SmallIntegerField(choices=opcionesP10,verbose_name='', null=True, default=0)
    dep11 =models.SmallIntegerField(choices=opcionesP11,verbose_name='',null=True,default=0)
    dep12=models.SmallIntegerField(choices=opcionesP12,verbose_name='', null=True, default=0)
    dep13 = models.SmallIntegerField(choices=opcionesP13, verbose_name='', null=True, default=0)
    dep14 = models.SmallIntegerField(choices=opcionesP14, verbose_name='',null=True, default=0)
    dep15 = models.SmallIntegerField(choices=opcionesP15, verbose_name='', null=True, default=0)
    dep16 = models.SmallIntegerField(choices=opcionesP16, verbose_name='', null=True, default=0)
    dep17 = models.SmallIntegerField(choices=opcionesP17, verbose_name='', null=True, default=0)
    dep18 = models.SmallIntegerField(choices=opcionesP18, verbose_name='', null=True, default=0)
    dep19 = models.SmallIntegerField(choices=opcionesP19, verbose_name='', null=True, default=0)
    dep20 = models.SmallIntegerField(choices=opcionesP20, verbose_name='', null=True, default=0)
    dep21 = models.SmallIntegerField(choices=opcionesP21, verbose_name='', null=True, default=0)
    perderpeso = models.SmallIntegerField(choices=[(1,'Si'),(0,'No')],null=True, default=0)
    depfecha = models.DateField(verbose_name="Fecha de custionario",default=date.today,null=True,blank="True")
    depconsejero = models.SmallIntegerField(verbose_name="Consejero",blank=True,null=True)
    deppuntos = models.SmallIntegerField(verbose_name="Puntaje", null=True, blank=True)
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True, default="Demostracion")
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO


# Dentro de tu modelo Depresion

    @property
    def sintomas_depresion(self):

        sintomas_presentes = []

    # Recorremos los 21 campos de síntomas
        for i in range(1, 22):
            nombre_campo = f'dep{i}'
            severidad = getattr(self,nombre_campo, 0) or 0
            metodo_display_name = f'get_{nombre_campo}_display'

            if hasattr(self, metodo_display_name):
               metodo_display = getattr(self, metodo_display_name)
               texto_sintoma = metodo_display()
            else:
               texto_sintoma = f"Texto no encontrado para {nombre_campo}"

            sintomas_presentes.append((severidad, texto_sintoma))


        sintomas_presentes.sort(key=lambda tupla: tupla[0], reverse=True)
        top_5_sintomas = sintomas_presentes[:5]

        datos_finales = []
        for severidad, nombre_sintoma in top_5_sintomas:
            datos_finales.append({
               'nombre': nombre_sintoma,
               # 'severidad_valor': severidad # Puedes descomentar esto si necesitas el número en la plantilla
            })

        return datos_finales


# El __str__ debe estar al mismo nivel de indentación que la propiedad
    def __str__(self):
        return f"Registro para expediente {self.expediente}"


class Marcadores(models.Model):

    opcionesSioNo=[(1,'Si'),(0,'No')]
    opcionesSustancia=[(0,'Marihuana'),(1,'Anfetaminas'),(2,'Cristal,Ice'),(3,'Opio, Morfina'),(4,'Rivotril, Psicotropicos')]
    expediente=models.CharField(max_length=10, primary_key=True,null=False, blank=True, verbose_name='No.Expediente', unique=True)
    marcador1 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='1a.- Se dio cuenta que tenia que usar mas de [sustancia] para lograr el efecto deseado?', null=True, default=0)
    marcador2 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='1b.- Noto que la misma cantidad de [sustancia] le hacia menos efecto que antes?',null=True, default=0)
    marcador3 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='1c.- Alguna vez se dio cuenta que necesitaba mas cantidad de [sustancia] para lograr el mismo efecto?', null=True, default=0)
    marcador4 =models.SmallIntegerField(choices=opcionesSioNo,verbose_name='2a.- Ha sentido un deseo o la necesidad tan fuerte de consumir [sustancia] que no puede evitar hacerlo?',null=True,default=0)
    marcador5=models.SmallIntegerField(choices=opcionesSioNo,verbose_name='2b.- Ha deseado consumir [sustancia] deseperadamente que no podia pensar en mas? ', null=True, default=0)
    marcador6 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='3a.- Hubo ocasion en que quiso suspender o disminuir el consumo de [sustancia]', null=True, default=0)
    marcador7=models.SmallIntegerField(choices=opcionesSioNo,verbose_name='     Si fue asi, ha sido siempre capaz de disminuir su uso por lo menos durante un mes?',null=True,default=0)
    marcador8 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='3b.- Ha tenido periodos en los que el uso [sustancia] en mayor cantidad o por mas tiempo del que se proponia o se le hizo dificil suspender el consumo antes de sentirse intoxicado?', null=True, default=0)
    marcador9 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='4a.- En las horas o dias siguientes a suspender o disminuir el uso de [sustancia] alguna vez tuvo malestar, como temblores sudores, no poder dormir, dolores de estomago o de cabeza?', null=True, default=0)
    marcador10 = models.SmallIntegerField(choices=opcionesSioNo,verbose_name='4b.- Utilizo [sustancia] u otra droga para evitar tener malestares como los que se acaban de mencionar?', null=True, default=0)
    marcador11 =models.SmallIntegerField(choices=opcionesSioNo,verbose_name='5a.- Ha habido ocasiones en que dedicaba mucho tiempo en conseguir [sustancia]?',null=True,default=0)
    marcador12=models.SmallIntegerField(choices=opcionesSioNo,verbose_name='5b.- Ha pasado mucho tiempo consumiendo o recuperandose de los efectos de [sustancia]?', null=True, default=0)
    marcador13 = models.SmallIntegerField(choices=opcionesSioNo, verbose_name='5c.- Ha descuidado o suspendido actividades importantes como estudios, deportes, trabajo, compartir con amigos o familiares por conseguir o usar [sustancia]?', null=True, default=0)
    marcador14 = models.SmallIntegerField(choices=opcionesSioNo, verbose_name='6a.- Ha tenido problemas de salud como sobredosis accidental, tos persistente, convulciones, infecciones, hepatitis, abscesos, SIDA, problemas cardiacosu otra lesion relacionada con el uso de [sustancia]?',null=True, default=0)
    marcador15 = models.SmallIntegerField(choices=opcionesSioNo, verbose_name='6b.- Continuo usando [sustancia] aun despues de presentar estos problemas de salud?', null=True, default=0)
    marcador16 = models.SmallIntegerField(choices=opcionesSioNo, verbose_name='6c.- Ha tenido usted problemas psicologicos o sociales al uso de [sustancia], como sentirse deprimido, extraño o perseguido o presentar fracasos laborales, escolares, conflictos familiares, actos de violencia, accidentes, etc.', null=True, default=0)
    marcador17 = models.SmallIntegerField(choices=opcionesSioNo, verbose_name='6d.- Continuo consumiendo [sustancia] aun despues de saber que se relacionaba con algunos de estos problemas? ', null=True, default=0)
    quedrogausa = models.SmallIntegerField(choices=opcionesSustancia, verbose_name='Que tipo de droga consume?', null=True, default=0)
    masdecincoveces = models.SmallIntegerField(choices=opcionesSioNo, verbose_name='Uso en mas de cinco ocasiones?', null=True, default=0)

    marfecha = models.DateField(verbose_name="Fecha de custionario",default=date.today,null=True,blank="True")
    marconsejero = models.SmallIntegerField(verbose_name="Consejero",blank=True,null=True)
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True, default="Demostracion")
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO


class Riesgos(models.Model):

    opcionesFrecuencia=[(0,'Nunca'),(1,'Una vez al mes o menos'),(2,'Dos o cuatro veces al año'),(3,'Dos o tres veces a la semana')]
    opcionesCuantas=[(0,'1 o 2'),(1,'3 o 4'),(2,'5 o 6'),(3,'7 o 9'),(4,'10 o mas')]
    opcionesSeisoMas=[(0,'Nunca'),(1,'Menos de una vez al mes'),(2,'Mensualmente'),(3,'Semanalmente'),(4,'Diario o casi diario')]
    opcionesOtras=[(0,'No'),(1,'Si, pero no en el ultimo año'),(2,'Si, en el ultimo año')]
    expediente=models.CharField(max_length=10, primary_key=True,null=False, blank=True, verbose_name='No.Expediente', unique=True)
    riesgosP1 = models.SmallIntegerField(choices=opcionesFrecuencia,verbose_name='a).- Que tan frequente ingiere bebidas alcoholicas?', null=True, default=0)
    riesgosP2 = models.SmallIntegerField(choices=opcionesCuantas,verbose_name='b).- Cuantas copas toma en un dia tipico de los que toma?', null=True, default=0)
    riesgosP3 = models.SmallIntegerField(choices=opcionesSeisoMas,verbose_name='c).- Que tan frecuente tomas 6 o mas copas en la misma ocasion?', null=True, default=0)
    riesgosP4 = models.SmallIntegerField(choices=opcionesSeisoMas,verbose_name='d).- Durante el ultimo año, que tan frecuente dejo de hacer algo que deberia de haber echo por beber?', null=True, default=0)
    riesgosP5 = models.SmallIntegerField(choices=opcionesSeisoMas,verbose_name='e).- Durante el ultimo año, que tan frecuente bebio a la mañana siguiente despues de haber bebido en exceso el dia anterior?', null=True, default=0)
    riesgosP6 = models.SmallIntegerField(choices=opcionesSeisoMas,verbose_name='f).- Durante el ultimo año, que tan frecuente se sintio culpable o tuvo remordimiento por haber bebido ?', null=True, default=0)
    riesgosP7 = models.SmallIntegerField(choices=opcionesSeisoMas,verbose_name='g).- Durante el ultimo año, que tan frecuente se olvido algo de lo que habia pasado cuando estuvo bebiendo ?', null=True, default=0)
    riesgosP8 = models.SmallIntegerField(choices=opcionesOtras,verbose_name='h).- Se ha lastimado o alguien ha resultado lesionado como consecuencia de su ingestion de alcohol ?', null=True, default=0)
    riesgosP9 = models.SmallIntegerField(choices=opcionesOtras,verbose_name='i).- Algun familiar o doctor se ha preocupado por la forma de beber o le ha sugerido que le baje ?', null=True, default=0)
    riesgofecha = models.DateField(verbose_name="Fecha de custionario",default=date.today,null=True,blank=True)
    riesgoconsejero = models.SmallIntegerField(verbose_name="Consejero",blank=True,null=True)
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO

class Razones(models.Model):


    expediente=models.CharField(max_length=10, primary_key=True,null=False, blank=True, verbose_name='No.Expediente', unique=True)
    factores = models.TextField(verbose_name='Menciona factores que te indujeron a consumir sustancias por primera vez', null=True, blank=True, default='')
    motivos = models.TextField(verbose_name='Por que motivo(s) volviste a seguir consumiendo sustancias', null=True, blank=True, default='')
    sabias = models.SmallIntegerField(verbose_name='Sabias cuales eran los riesgos y complicaciones por el consumo de drogas?',choices=[(1,'Si'),(0,'No')],blank=True, default=0)
    cuales = models.TextField(verbose_name='Cuales eran los riesgos de seguir consumiendo?', null=True,blank=True, default='')
    quemotivos = models.TextField(verbose_name='Que motivos tenias para exponerte a seguir consumiendo?', null=True,blank=True, default='')
    querazones = models.TextField(verbose_name='Que razones identificas para tu consumo?', null=True,blank=True, default='')
    observaciones = models.TextField(verbose_name='Observaciones y/o comentarios', null=True,blank=True, default='')
    razonesfecha = models.DateField(verbose_name="Fecha de custionario", default=date.today, null=True, blank=True)
    razonesconsejero = models.SmallIntegerField(verbose_name="Consejero", blank=True, null=True)
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True, default="Demostracion")
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO



class Valorizacion(models.Model):

    opcionesSustancias = [(0, 'Alcohol  '), (1, 'Tabaco   '), (2, 'Marihuana'), (3, 'Cocaina  '), (4, 'Crack    '),
                       (5, 'Pastillas'),(6, 'Otras    ')]

    expediente = models.CharField(max_length=10, primary_key=True, null=False, blank=True, verbose_name='No.Expediente',unique=True)
    mainsustance=models.SmallIntegerField(verbose_name='Principal sustancia',choices=opcionesSustancias,null=True,blank=True, default=1)
    hacecuanto=models.CharField(verbose_name='Tiempo de consumir esta sustancia',max_length=30,null=True, blank=True)
    cantidadpromedio=models.CharField(verbose_name='Cantidad promedio de consumo',max_length=30,null=True, blank=True)
    razonesdeconsumo=models.TextField(verbose_name='Razones de consumo',null=True, blank=True)
    razon1=models.CharField(verbose_name='Razon 1',max_length=30,null=True, blank=True)
    razon2=models.CharField(verbose_name='Razon 2',max_length=30,null=True, blank=True)
    razon3=models.CharField(verbose_name='Razon 3',max_length=30,null=True, blank=True)
    medico = models.TextField(verbose_name='Medico', null=True, blank=True)
    psiquiatrica = models.TextField(verbose_name='Psiquiatrica', null=True, blank=True)
    psicologica = models.TextField(verbose_name='Psicologica', null=True, blank=True)
    valorizacionfecha = models.DateField(verbose_name="Fecha de custionario", default=date.today, null=True, blank=True)
    valorizacionconsejero = models.SmallIntegerField(verbose_name="Consejero", blank=True, null=True)
    ansiedad = models.CharField(verbose_name='Ansiedad', max_length=30, null=True, blank=True)
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True, default="Demostracion")
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO


class CIndividual(models.Model):


    expediente = models.CharField(max_length=10, null=True, blank=True,verbose_name='No.Expediente')
    sesion = models.SmallIntegerField(verbose_name='Numero de sesion', null=True, blank=True, default=1)
    diasestancia = models.SmallIntegerField(verbose_name='Dias estancia', null=True, blank=True, default=1)
    status = models.SmallIntegerField(verbose_name='Estatus de sesion', null=True, blank=True, default=0)
    fecha = models.DateField(verbose_name="Fecha de sesion", default=date.today, null=True,blank=True)
    proximasesion = models.DateField(verbose_name="Proxima sesion", default=date.today, null=True,blank=True)
    consejero = models.SmallIntegerField(verbose_name="Consejero", blank=True, null=True)
    objetivo = models.TextField(verbose_name='Objetivo', null=True, blank=True)
    aspectos = models.TextField(verbose_name='Aspectos', null=True, blank=True)
    resultados = models.TextField(verbose_name='Resultados', null=True, blank=True)
    seesperan = models.TextField(verbose_name='Resultados que se esperan', null=True, blank=True)
    tareas = models.TextField(verbose_name='Tareas', null=True, blank=True)
    quesetrabajo = models.TextField(verbose_name='Que se trabajo', null=True, blank=True)
    observaciones = models.TextField(verbose_name='Observaciones', null=True, blank=True)
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True, default="Demostracion")
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO


    def __str__(self):
        # Ahora 'expediente' es un CharField normal, no un objeto relacionado.
        return f"Expediente: {self.expediente}, Sesión: {self.sesion}"

    class Meta:
        verbose_name = "Sesión Individual"
        verbose_name_plural = "Sesiones Individuales"
        # ¡IMPORTANTE! Aquí es donde aseguramos que un expediente no tenga dos veces la misma sesión.
        unique_together = ('expediente', 'sesion')
        ordering = ['expediente', 'sesion']  # Ordenar por expediente y luego por número de sesión2

class CFamiliar(models.Model):


    expediente = models.CharField(max_length=10, null=True, blank=True, verbose_name='No.Expediente')
    sesion = models.SmallIntegerField(verbose_name='Numero de sesion', null=True, blank=True, default=1)
    diasestancia = models.SmallIntegerField(verbose_name='Dias estancia', null=True, blank=True, default=1)
    status = models.SmallIntegerField(verbose_name='Estatus de sesion', null=True, blank=True, default=0)
    fecha = models.DateField(verbose_name="Fecha de sesion", default=date.today, null=True, blank=True)
    proximasesion = models.DateField(verbose_name="Proxima sesion", default=date.today, null=True, blank=True)
    consejero = models.SmallIntegerField(verbose_name="Consejero", blank=True, null=True)
    objetivo = models.TextField(verbose_name='Objetivo', null=True, blank=True)
    aspectos = models.TextField(verbose_name='Aspectos', null=True, blank=True)
    resultados = models.TextField(verbose_name='Resultados', null=True, blank=True)
    seesperan = models.TextField(verbose_name='Resultados que se esperan', null=True, blank=True)
    tareas = models.TextField(verbose_name='Tareas', null=True, blank=True)
    quesetrabajo = models.TextField(verbose_name='Que se trabajo', null=True, blank=True)
    observaciones = models.TextField(verbose_name='Observaciones', null=True, blank=True)
    familiares = models.TextField(verbose_name='Familiares', null=True, blank=True)
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True, default="Demostracion")
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO

    def __str__(self):
       return f"Familiar - Expediente: {self.expediente}, Sesión: {self.sesion}"

    class Meta:
         verbose_name = "Sesión Familiar"
         verbose_name_plural = "Sesiones Familiares"
         unique_together = ('expediente', 'sesion')
         ordering = ['expediente', 'sesion']


class CGrupal(models.Model):

    # CAMPO EXPEDIENTE ELIMINADO - No aplica para grupales
    sesion = models.SmallIntegerField(verbose_name='Número de sesión', null=True, blank=True, default=1)
    diasestancia = models.SmallIntegerField(verbose_name='Días estancia', null=True, blank=True, default=1)
    status = models.SmallIntegerField(verbose_name='Estatus de sesión', null=True, blank=True, default=0)
    fecha = models.DateField(verbose_name="Fecha de sesión", default=date.today, null=True, blank=True)
    proximasesion = models.DateField(verbose_name="Próxima sesión", null=True, blank=True)
    consejero = models.SmallIntegerField(verbose_name="Consejero", blank=True, null=True)

    # NUEVOS CAMPOS ESPECÍFICOS PARA GRUPALES
    tema_sesion = models.CharField(max_length=200, verbose_name='Tema de la sesión', null=True, blank=True)
    dinamica_utilizada = models.CharField(max_length=100, verbose_name='Dinámica utilizada', null=True, blank=True)
    numero_participantes = models.SmallIntegerField(verbose_name='Número de participantes', default=0)

    # CAMPOS EXISTENTES (comunes a todos los tipos de sesión)
    objetivo = models.TextField(verbose_name='Objetivo', null=True, blank=True)
    aspectos = models.TextField(verbose_name='Aspectos', null=True, blank=True)
    resultados = models.TextField(verbose_name='Resultados', null=True, blank=True)
    seesperan = models.TextField(verbose_name='Resultados que se esperan', null=True, blank=True)
    tareas = models.TextField(verbose_name='Tareas', null=True, blank=True)
    quesetrabajo = models.TextField(verbose_name='Qué se trabajó', null=True, blank=True)
    observaciones = models.TextField(verbose_name='Observaciones', null=True, blank=True)
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True, default="Demostracion")
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO

    # RELACIÓN MUCHOS A MUCHOS CON INTERNOS
    participantes = models.ManyToManyField(
        'Internos',  # Asegúrate de que este sea el nombre de tu modelo de internos
        related_name='sesiones_grupales',
        verbose_name='Participantes del grupo'
    )

    # ELIMINADO: grupodeinternos (ahora se usa la relación ManyToMany)

    def __str__(self):
        return f"Sesión Grupal #{self.sesion} - {self.tema_sesion} - {self.fecha}"

    class Meta:
        verbose_name = "Sesión Grupal"
        verbose_name_plural = "Sesiones Grupales"
        # ELIMINADO: unique_together (no aplica para grupales)
        ordering = ['fecha', 'sesion']


class PConsejeria(models.Model):


    expediente = models.CharField(max_length=10, null=True, blank=True, verbose_name='No.Expediente')
    fecha = models.DateField(verbose_name="Fecha de sesion", default=date.today, null=True, blank=True)
    consejero = models.SmallIntegerField(verbose_name="Consejero", blank=True, null=True)
    alcoholydrogas = models.TextField(verbose_name='Consumo de alcohol y drogas', null=True, blank=True)
    fisicaymental = models.TextField(verbose_name='Salud fisica y mental', null=True, blank=True)
    areasdelavida = models.TextField(verbose_name='Situacion en diferentes areas de la vida (familiar,social,laboral y economica', null=True, blank=True)
    metas = models.TextField(verbose_name='Metas a mediano y/o largo plazo', null=True, blank=True)
    objetivos = models.TextField(verbose_name='Objetivos a corto,mediano y largo plazo', null=True, blank=True)
    compromiso = models.TextField(verbose_name='Compromiso del usuario a dejar el consumo', null=True, blank=True)
    logros = models.TextField(verbose_name='Logro y mantenimiento de la abstinencia', null=True, blank=True)
    metasareasdevida = models.TextField(verbose_name='Metas por area de vida', null=True, blank=True)
    prevencion = models.TextField(verbose_name='Prevencion de recaidas', null=True, blank=True)
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True, default="Demostracion")
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO

    def __str__(self):
        # Ahora 'expediente' es un CharField normal, no un objeto relacionado.
        return f"Expediente: {self.expediente}"

class TareaConsejeria(models.Model):

    expediente = models.CharField(max_length=10)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    descripcion = models.TextField(verbose_name="Descripción de la tarea")
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True, default="Demostracion")
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO

    imagen_tarea = models.ImageField(
        upload_to='tareas_consejeria/%Y/%m/%d/',
        verbose_name="Imagen escaneada de la tarea",
        blank=True,
        null=True
    )


    class Meta:
        verbose_name = "Tarea de Consejería"
        verbose_name_plural = "Tareas de Consejería"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Tarea {self.id} - {self.expediente}"

class HojaAtencionPs(models.Model):

    opcionesLateralidad = [('Derecha', 'Derecha'), ('Izquierda', 'Izquierda')]

    expediente = models.CharField(max_length=10, null=True, blank=True, verbose_name='No.Expediente')
    fecha = models.DateField(verbose_name="Fecha de atencion", default=date.today, null=True, blank=True)
    psicologo = models.SmallIntegerField(verbose_name="Psicologo", blank=True, null=True)
    lateralidad = models.CharField(verbose_name='Lateralidad',choices=opcionesLateralidad,max_length=10, null=True, default='Derecha' )
    motivo = models.CharField(verbose_name='Motivo',max_length=50, null=True, blank=True)
    antecedentes = models.TextField(verbose_name='Antecedentes', null=True, blank=True)
    instrumentos = models.TextField(verbose_name='Instrumentos', null=True, blank=True)
    observaciones = models.TextField(verbose_name='Observaciones', null=True, blank=True)
    resultados = models.TextField(verbose_name='Resultados', null=True, blank=True)
    diagnostico = models.TextField(verbose_name='Diagnosticos', null=True, blank=True)
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True, default="Demostracion")
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO


    def __str__(self):
        # Ahora 'expediente' es un CharField normal, no un objeto relacionado.
        return f"Expediente: {self.expediente}"


class NotasEvolucionPS(models.Model):


    opcionesQueTipo=[('Individual','Individual'),('Grupal','Grupal')]

    expediente = models.CharField(max_length=10, null=True, blank=True,verbose_name='No.Expediente')
    sesion = models.SmallIntegerField(verbose_name='Numero de sesion', null=True, blank=True, default=1)
    status = models.SmallIntegerField(verbose_name='Estatus de sesion', null=True, blank=True, default=0)
    fecha = models.DateField(verbose_name="Fecha de sesion", default=date.today, null=True,blank=True)
    proximasesion = models.DateField(verbose_name="Proxima sesion", default=date.today, null=True,blank=True)
    psicologo = models.SmallIntegerField(verbose_name="Psicologo", blank=True, null=True)
    objetivo = models.TextField(verbose_name='Objetivo', null=True, blank=True)
    resumen = models.TextField(verbose_name='Resumen', null=True, blank=True)
    resultado = models.TextField(verbose_name='Resultado', null=True, blank=True)
    objetivoyplan = models.TextField(verbose_name='Objetivo y plan terapeutico', null=True, blank=True)
    actividades = models.TextField(verbose_name='Actividades', null=True, blank=True)
    observaciones = models.TextField(verbose_name='Observaciones', null=True, blank=True)
    individualogrupal = models.CharField(verbose_name='Sesion Individual o Grupal',max_length=15,choices=opcionesQueTipo, null=True, default='Individual')
    selograron = models.BooleanField(verbose_name='Se logro objetivo?', null=True, default=False)
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True, default="Demostracion")

    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO

    def __str__(self):
        # Ahora 'expediente' es un CharField normal, no un objeto relacionado.
        return f"Expediente: {self.expediente}, Sesión: {self.sesion}"

    class Meta:
        verbose_name = "Sesión Individual"
        verbose_name_plural = "Sesiones Individuales"
        # ¡IMPORTANTE! Aquí es donde aseguramos que un expediente no tenga dos veces la misma sesión.
        unique_together = ('expediente', 'sesion')
        ordering = ['expediente', 'sesion']  # Ordenar por expediente y luego por número de sesión2



class Medico(models.Model):


    expediente = models.CharField(max_length=10, null=True, blank=True, verbose_name='No.Expediente')
    fecha = models.DateField(verbose_name="Fecha de atencion", default=date.today, null=True, blank=True)
    medico = models.SmallIntegerField(verbose_name="Medico", blank=True, null=True)
    motivo = models.CharField(verbose_name='Motivo',max_length=50, null=True, blank=True)
    padecimiento = models.TextField(verbose_name='Padecimiento actual (inicio y evolucion de cosnumo de sustancias)', null=True, blank=True)
    sintomas = models.TextField(verbose_name='Sintomas generales (intoxicacion, abstinencia, efectos secundarios, etc.)', null=True, blank=True)
    tratamientos = models.TextField(verbose_name='Tratamientos previos', null=True, blank=True)
    TA = models.CharField(verbose_name='TA',null=True,blank=True,max_length=10)
    FC = models.CharField(verbose_name='FC',null=True,blank=True,max_length=10)
    FR = models.CharField(verbose_name='FR',null=True,blank=True,max_length=10)
    temperatura = models.CharField(verbose_name='Temperatura',null=True,blank=True,max_length=10)
    peso = models.CharField(verbose_name='Peso',null=True,blank=True,max_length=10)
    talla = models.CharField(verbose_name='Talla',null=True,blank=True,max_length=10)
    exploracion = models.TextField(verbose_name='Exploracion y auscultacion', null=True, blank=True)
    examenmental = models.TextField(verbose_name='Examen mental (aspecto general, actitud,aliño, actividad motora,orientacion,concentracion,funciones cognitivas, etc.)', null=True, blank=True)
    diagnostico = models.TextField(verbose_name='Diagnostico', null=True, blank=True)
    pronostico = models.TextField(verbose_name='Pronostico', null=True, blank=True)
    tratamientosugerido = models.TextField(verbose_name='Tratamiento sugerido', null=True, blank=True)
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True, default="Demostracion")
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO


    def __str__(self):
        # Ahora 'expediente' es un CharField normal, no un objeto relacionado.
        return f"Expediente: {self.expediente}"


class Recetas(models.Model):


    expediente = models.CharField(max_length=10, null=True, blank=True, verbose_name='No.Expediente')
    historial = models.TextField(verbose_name='Historial de recetas', null=True, blank=True)
    clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True, default="Demostracion")
    objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO

    def __str__(self):
        # Ahora 'expediente' es un CharField normal, no un objeto relacionado.
        return f"Expediente: {self.expediente}"

class HistoriaClinica(models.Model):


      expediente = models.CharField(max_length=10, null=True, blank=True, verbose_name='No.Expediente')
      fecha = models.DateField(verbose_name="Fecha de atencion", default=date.today, null=True, blank=True)
      medico = models.SmallIntegerField(verbose_name="Medico", blank=True, null=True)
      padresPadecimientosCronicos = models.BooleanField(verbose_name='Padecimientos cronicos ', null=True, default=False)
      padresInfectoContagiosos = models.BooleanField(verbose_name='Infecto-contagiosos ', null=True, default=False)
      padresAlergias = models.BooleanField(verbose_name='Alergias ', null=True, default=False)
      padresTraumaticos = models.BooleanField(verbose_name='Eventos traumaticos ', null=True, default=False)
      padresConsumos = models.BooleanField(verbose_name='Consumo sustancias o adicciones', null=True, default=False)
      padresMentales = models.BooleanField(verbose_name='Otras enfermedades mentales', null=True, default=False)
      padresOtros = models.BooleanField(verbose_name='Otras enfermedades ', null=True, default=False)
      hermanosPadecimientosCronicos = models.BooleanField(verbose_name='Padecimientos cronicos ', null=True,default=False)
      hermanosInfectoContagiosos = models.BooleanField(verbose_name='Infecto-contagiosos ', null=True,default=False)
      hermanosAlergias = models.BooleanField(verbose_name='Alergias ', null=True, default=False)
      hermanosTraumaticos = models.BooleanField(verbose_name='Eventos traumaticos ', null=True,default=False)
      hermanosConsumos = models.BooleanField(verbose_name='Consumo sustancias o adicciones ', null=True,default=False)
      hermanosMentales = models.BooleanField(verbose_name='Otras enfermedades mentales ', null=True,default=False)
      hermanosOtros = models.BooleanField(verbose_name='Otras enfermedades ', null=True,default=False)
      conyuguePadecimientosCronicos = models.BooleanField(verbose_name='Padecimientos cronicos ', null=True,default=False)
      conyugueInfectoContagiosos = models.BooleanField(verbose_name='Infecto-contagiosos ', null=True,default=False)
      conyugueAlergias = models.BooleanField(verbose_name='Alergias ', null=True, default=False)
      conyugeTraumaticos = models.BooleanField(verbose_name='Eventos traumaticos ', null=True,default=False)
      conyugueConsumos = models.BooleanField(verbose_name='Consumo sustancias o adicciones ', null=True,default=False)
      conyugueMentales = models.BooleanField(verbose_name='Otras enfermedades mentales ', null=True,default=False)
      conyugueOtros = models.BooleanField(verbose_name='Otras enfermedades ', null=True,default=False)
      hijosPadecimientosCronicos = models.BooleanField(verbose_name='Padecimientos cronicos ', null=True,default=False)
      hijosInfectoContagiosos = models.BooleanField(verbose_name='Infecto-contagiosos ', null=True,default=False)
      hijosAlergias = models.BooleanField(verbose_name='Alergias ', null=True, default=False)
      hijosTraumaticos = models.BooleanField(verbose_name='Eventos traumaticos ', null=True,default=False)
      hijosConsumos = models.BooleanField(verbose_name='Consumo sustancias o adicciones', null=True,default=False)
      hijosMentales = models.BooleanField(verbose_name='Otras enfermedades mentales ', null=True,default=False)
      hijosOtros = models.BooleanField(verbose_name='Otras enfermedades ', null=True,default=False)
      colateralesPadecimientosCronicos = models.BooleanField(verbose_name='Padecimientos cronicos ', null=True,default=False)
      colateralesInfectoContagiosos = models.BooleanField(verbose_name='Infecto-contagiosos ', null=True,default=False)
      colateralesAlergias = models.BooleanField(verbose_name='Alergias ', null=True, default=False)
      colateralesTraumaticos = models.BooleanField(verbose_name='Eventos traumaticos ', null=True, default=False)
      colateralesConsumos = models.BooleanField(verbose_name='Consumo sustancias o adicciones ', null=True,default=False)
      colateralesMentales = models.BooleanField(verbose_name='Otras enfermedades mentales ', null=True,default=False)
      colateralesOtros = models.BooleanField(verbose_name='Otras enfermedades ', null=True, default=False)
      convivientesPadecimientosCronicos = models.BooleanField(verbose_name='Padecimientos cronicos ',null=True, default=False)
      convivientesInfectoContagiosos = models.BooleanField(verbose_name='Infecto-contagiosos ',null=True, default=False)
      convivientesAlergias = models.BooleanField(verbose_name='Alergias ', null=True, default=False)
      convivientesTraumaticos = models.BooleanField(verbose_name='Eventos traumaticos', null=True,default=False)
      convivientesConsumos = models.BooleanField(verbose_name='Consumo sustancias o adicciones ',null=True, default=False)
      convivientesMentales = models.BooleanField(verbose_name='Otras enfermedades mentales ',null=True, default=False)
      convivientesOtros = models.BooleanField(verbose_name='Otras enfermedades ', null=True,default=False)
      frecuenciaBath = models.SmallIntegerField(choices=[(0,'Diario'),(1,'Cada tercer dia'),(2,'irregular')],verbose_name='COn que frecuencia se  baña?',null=True, default=0)
      habitacionUrbana = models.BooleanField(verbose_name='Urbana', null=True,default=False)
      habitacionRural = models.BooleanField(verbose_name='Rural', null=True,default=False)
      habitacionTodoslosServicios = models.BooleanField(verbose_name='Todos los servicios', null=True,default=False)
      habitacionMovilidad = models.BooleanField(verbose_name='Contexto de movilidad', null=True,default=False)
      inmunizacion = models.SmallIntegerField(choices=[(0, 'Completa'), (1, 'Incompleta'), (2, 'Pendiente')],verbose_name='Inmunizacion', null=True, default=0)
      alimentacion = models.BooleanField(verbose_name='Alimentacion', null=True, default=False)
      actividadFisica = models.BooleanField(verbose_name='Actividad fisica', null=True, default=False)
      enfermedadActual = models.CharField(verbose_name='Enfermedad actual', max_length=50, null=True, blank=True)
      alergias = models.CharField(verbose_name='Alergias', max_length=50, null=True, blank=True)
      traumaticos = models.CharField(verbose_name='Traumaticos', max_length=50, null=True, blank=True)
      quirurgico = models.BooleanField(verbose_name='Quirurgico', null=True, default=False)
      hospitalizaciones = models.BooleanField(verbose_name='Hospitalizaciones', null=True, default=False)
      transfuciones = models.BooleanField(verbose_name='Transfuciones', null=True, default=False)
      adiccion = models.CharField(verbose_name='Adiccion', max_length=50, null=True, blank=True)
      internamientoporAdiccion = models.CharField(verbose_name='Internamiento por adiccion', max_length=50, null=True, blank=True)
      padecimientoActual = models.CharField(verbose_name='Padecimiento actual', max_length=50, null=True, blank=True)
      digestivo = models.CharField(verbose_name='Digestivo', max_length=100, null=True, blank=True)
      cardiovascular = models.CharField(verbose_name='Cardiovascular', max_length=100, null=True, blank=True)
      respiratorio = models.CharField(verbose_name='Respiratorio', max_length=100, null=True, blank=True)
      urinario = models.CharField(verbose_name='Urinario', max_length=100, null=True, blank=True)
      genital = models.CharField(verbose_name='Genital', max_length=100, null=True, blank=True)
      hematologico = models.CharField(verbose_name='Hematologico', max_length=100, null=True, blank=True)
      endocrino = models.CharField(verbose_name='Endocrino', max_length=100, null=True, blank=True)
      osteomuscular = models.CharField(verbose_name='Osteomuscular', max_length=100, null=True, blank=True)
      nervioso = models.CharField(verbose_name='Nervioso', max_length=100, null=True, blank=True)
      sensorial = models.CharField(verbose_name='Sensorial', max_length=100, null=True, blank=True)
      psicomatico = models.CharField(verbose_name='Psicomatico', max_length=100, null=True, blank=True)
      TA = models.CharField(verbose_name='TA', null=True, blank=True, max_length=10)
      FC = models.CharField(verbose_name='FC', null=True, blank=True, max_length=10)
      FR = models.CharField(verbose_name='FR', null=True, blank=True, max_length=10)
      temperatura = models.CharField(verbose_name='Temperatura', null=True, blank=True, max_length=10)
      PCO2 = models.CharField(verbose_name='PCO2', null=True, blank=True, max_length=10)
      IMC = models.CharField(verbose_name='IMC', null=True, blank=True, max_length=10)
      glucosa = models.CharField(verbose_name='Glucosa', null=True, blank=True, max_length=10)
      peso = models.CharField(verbose_name='Peso', null=True, blank=True, max_length=10)
      talla = models.CharField(verbose_name='Talla', null=True, blank=True, max_length=10)
      cabeza = models.SmallIntegerField(choices=[(0, 'Normocefalo'), (1, 'Edoxtosis'), (2, 'Exostosis')],verbose_name='Cabeza', null=True, default=0)
      cabello = models.SmallIntegerField(choices=[(0, 'Bien implantado'), (1, 'Alopecia')],verbose_name='Cabello', null=True, default=0)
      pupilas = models.SmallIntegerField(choices=[(0, 'Isocoricas'), (1, 'Anisocoricas')],verbose_name='Pupilas', null=True, default=0)
      faringe = models.SmallIntegerField(choices=[(0, 'Normal'), (1, 'Hiperemia'),(2,'Exudado purulento')],verbose_name='Fringe', null=True, default=0)
      amigdalas = models.SmallIntegerField(choices=[(0, 'Normales'), (1, 'Hipertroficas'),(2,'Exudado purulento')],verbose_name='Amigdalas', null=True, default=0)
      adenomegalias = models.SmallIntegerField(choices=[(0, 'No palpables'), (1, 'Submanibulares'),(2,'Retroaricular')],verbose_name='Nariz', null=True, default=0)
      cicatriz = models.CharField(verbose_name='Cicatriz', null=True, blank=True, max_length=30)
      observaciones = models.CharField(verbose_name='Observaciones', null=True, blank=True, max_length=100)
      cuello = models.SmallIntegerField(choices=[(0, 'Cilindrico'), (1, 'Alterado') ],verbose_name='Cuello', null=True, default=0)
      traquea = models.SmallIntegerField(choices=[(0, 'Central'), (1, 'Alterada')],verbose_name='Traquea', null=True, default=0)
      tiroides = models.SmallIntegerField(choices=[(0, 'Sin datos patologicos'), (1, 'Crecimiento tiroideo'),(2,'Alterada')],
                                          verbose_name='Tiroides', null=True, default=0)
      adenomegaliasCuello = models.SmallIntegerField(choices=[(0, 'No palpables'), (1, 'Posteriores'),(2,'Anteriores'),(3,'Supraclavicular')],
                                                     verbose_name='Adenomegalias', null=True, default=0)
      pulsos = models.SmallIntegerField(choices=[(0, 'Palpables'), (1, 'Simetricos'),(2,'Alterados')],
                                                     verbose_name='Pulsos', null=True, default=0)
      observacionesCuello = models.CharField(verbose_name='Observaciones', null=True, blank=True, max_length=100)
      torax = models.SmallIntegerField(choices=[(0, 'Normalineo'), (1, 'Tonel'),(2,'Excabado') ],
                                            verbose_name='Torax', null=True, default=0)
      movsRespiratorios = models.SmallIntegerField(choices=[(0, 'Simetricos'), (1, 'Asimetricos')],
                                                   verbose_name='Movimientos respiratoriosa', null=True, default=0)
      camposPulmonares = models.SmallIntegerField(choices=[(0, 'Bien ventilados'), (1, 'Alterados')],
                                          verbose_name='Campos pulmonares', null=True, default=0)
      ruidosCardiacos = models.SmallIntegerField(choices=[(0, 'Adecuados'), (1, 'Ritmicos'),(2,'Alterados')],
                                                 verbose_name='Ruidos cardiacos', null=True, default=0)
      adenomagliasAxilar = models.SmallIntegerField(choices=[(0, 'No palpables'), (1, 'Presentes')],
                                        verbose_name='Amigdalas axilar', null=True, default=0)
      observacionesAxilar = models.CharField(verbose_name='Observaciones', null=True, blank=True, max_length=100)
      abdomen = models.SmallIntegerField(choices=[(0, 'Plano'), (1, 'Robusto'),(2,'Blando y depresible'),(3,'Resistencia') ],
                                            verbose_name='Abdomen', null=True, default=0)
      doloralPalpar = models.SmallIntegerField(choices=[(0, 'Negado'), (1, 'Presente')],
                                                   verbose_name='Dolor a la palpacion', null=True, default=0)
      viceromegalias = models.SmallIntegerField(choices=[(0, 'No palpables'), (1, 'Hepatomegalia'),(2,'Esplenomegalia')],
                                          verbose_name='Viceromegalias', null=True, default=0)
      peristalsis = models.SmallIntegerField(choices=[(0, 'Normal'), (1, 'Meteorismos'),(2,'Alterada')],
                                                 verbose_name='Ruidos cardiacos', null=True, default=0)
      observacionesAbdomen = models.CharField(verbose_name='Observaciones', null=True, blank=True, max_length=100)
      miembrossuperiores = models.SmallIntegerField(choices=[(0, 'Integras'), (1, 'Simetricas'),(2,'Pulsos palpables'),(3,'Alteradas') ],
                                            verbose_name='Miembros superiores', null=True, default=0)
      miembrosinferiores = models.SmallIntegerField(choices=[(0, 'Integras'), (1, 'Simetricas'),(2,'Pulsos palpables'),(3,'Alteradas')],
                                            verbose_name='Miembros inferiores', null=True, default=0)
      observacionesMiembros = models.CharField(verbose_name='Observaciones', null=True, blank=True, max_length=100)
      genitales = models.SmallIntegerField(choices=[(0, 'Integros'), (1, 'Sin datos patologicos'), (2, 'Presencia de verrugas'), (3, 'Alterados')],
                                            verbose_name='Genitales', null=True, default=0)
      observacionesGenitales = models.CharField(verbose_name='Observaciones', null=True, blank=True, max_length=100)
      edadAparente = models.SmallIntegerField(choices=[(0, 'Igual'), (1, 'Mayor'), (2, 'Menor')],
                                            verbose_name='Edad aparente a la cronologia', null=True, default=0)
      posicion = models.SmallIntegerField(choices=[(0, 'Libremente'), (1, 'Escogida'), (2, 'Forzada'),(3,'Incomoda')],
                                              verbose_name='Posicion', null=True, default=0)
      actitud = models.SmallIntegerField(choices=[(0, 'Buena'), (1, 'Mala'), (2, 'Cooperador(a)'), (3, 'No cooperador(a)'),(4,'Con imposibilidad de responder')],
                                              verbose_name='Actitud', null=True, default=0)
      observacionesInspeccion = models.CharField(verbose_name='Observaciones', null=True, blank=True, max_length=100)
      fluidez = models.SmallIntegerField(choices=[(0, 'Retardo'), (1, 'Aceleracion'), (2, 'Articulado'), (3, 'Coherente')],
                                          verbose_name='Fluidez', null=True, default=0)
      lenguaje = models.SmallIntegerField(choices=[(0, 'Buena tonalidad'), (1, 'Riqueza de asociaciones'), (2, 'Presenta obsesiones'),
                                                   (3, 'Congruente'),(4, 'Refiere fobias'),(5, 'Cuenta con delirios')],
                                          verbose_name='Lenguaje', null=True, default=0)
      observacionesLenguaje = models.CharField(verbose_name='Observaciones', null=True, blank=True, max_length=100)
      funcionesIntelectuales = models.SmallIntegerField(choices=[(0, 'Orientado'), (1, 'Atento'), (2, 'Comprension adecuada'), (3, 'Concentrado')],
                                          verbose_name='Funciones Intelectuales', null=True, default=0)
      memoria = models.SmallIntegerField(choices=[(0, 'Buena'), (1, 'Regular'), (2, 'Mala'),
                                                   (3, 'Conacion'), (4, 'Volicion'), (5, 'Juicio critico')],
                                          verbose_name='Memoria', null=True, default=0)
      observacionesFunciones = models.CharField(verbose_name='Observaciones', null=True, blank=True, max_length=100)
      afectividad = models.SmallIntegerField(choices=[(0, 'Indiferencia'), (1, 'Tristesa'), (2, 'Euforia'),
                                                  (3, 'Labiliadad'), (4, 'Ansiedad'), (5, 'Disociacion'), (6, 'Sin datos patologicos')],
                                         verbose_name='Afectividad', null=True, default=0)
      observacionesAfectividad = models.CharField(verbose_name='Observaciones', null=True, blank=True, max_length=100)
      sensopercepcion = models.SmallIntegerField(choices=[(0, 'Ilusiones'), (1, 'Alucionaciones'), (2, 'Alucinosis'),
                                                      (3, 'Despersonalizacion'), (4, 'Micropsias'), (5, 'Extrañeza')],
                                                      verbose_name='Sensopercepcion', null=True, default=0)
      observacionesSensopercepcion = models.CharField(verbose_name='Observaciones', null=True, blank=True, max_length=100)
      ideacion = models.SmallIntegerField(choices=[(0, 'Delirios'), (1, 'Proyecto futuro'), (2, 'Sueño'),(3, 'Conciencia de enfermedad')],
                                                 verbose_name='Ideacion', null=True, default=0)
      observacionesIdeacion = models.CharField(verbose_name='Observaciones', null=True, blank=True,
                                                      max_length=100)
      dependenciaA = models.CharField(verbose_name='Dependencia A:', null=True, blank=True,
                                               max_length=100)
      observacionesDependencia = models.TextField(verbose_name='Tratamiento sugerido', null=True, blank=True)
      pronosticoParalaVida = models.TextField(verbose_name='Pronostico para la vida y funcion', null=True, blank=True)
      tratamientoRecidencia = models.BooleanField(verbose_name='Tratamiento de recidencia', null=True, default=False)
      dietaNormal = models.BooleanField(verbose_name='Dieta normal', null=True, default=False)
      otroTratamiento = models.TextField(verbose_name='Otro', null=True, blank=True)
      justificacion = models.TextField(verbose_name='Justificacion', null=True, blank=True)
      observacionesTratamiento = models.TextField(verbose_name='Observaciones', null=True, blank=True)
      clinica = models.CharField(max_length=30, verbose_name='Clinica', null=True, blank=True, default="Demostracion")
      objects = ClinicaManager()  # ← FILTRO AUTOMÁTICO

class Clinicas(models.Model):
    objects = models.Manager

    clinica = models.CharField(max_length=30, unique=True, verbose_name='ID Clínica')
    nombre = models.CharField(max_length=200)
    password = models.CharField(max_length=128)  # Para guardar contraseña
    numeroDeInternos = models.SmallIntegerField(default=0)

    def __str__(self):
        return f"{self.clinica} - {self.nombre}"

    def check_password(self, raw_password):
        # Verificación simple de contraseña
        return self.password == raw_password
