from django.db import models
from django.utils import timezone
from datetime import date

# Create your models here.

class Usuarios(models.Model):
    objects = models.Manager()
    usuario = models.BigIntegerField(verbose_name='No. Usuario',null=True,blank=True, default='',editable=False)
    nombre = models.CharField(max_length=30, verbose_name='Nombre',null=True,blank=True, default='')
    cargo = models.CharField(max_length=20,verbose_name='Cargo', null=True,blank=True, default='')
    permisos=models.CharField(max_length=5,verbose_name='Permisos',null=True,blank=True, default='')
    password=models.CharField(max_length=10,verbose_name='Password',null=True,blank=True, default='')
    cedula=models.CharField(max_length=20,verbose_name='Cedula',null=True,blank=True, default='')
    expedidapor=models.CharField(max_length=30,verbose_name='Expedida por',null=True,blank=True, default='')

class Estados(models.Model):
    objects = models.Manager()
    edo = models.CharField(verbose_name='ID',null=True,blank=True, default='',max_length=3)
    nombre = models.CharField(max_length=20, verbose_name='Nombre',null=True,blank=True, default='')
    pais = models.CharField(max_length=3,verbose_name='Pais', null=True,blank=True, default='')

class DatosGrales(models.Model):
    objects = models.Manager()
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
    expediente = models.SmallIntegerField( verbose_name='Expediente actual', null=True, blank=True, default='')
    recibo = models.SmallIntegerField(verbose_name='U recibo emitido', null=True, blank=True, default='')
    receta = models.SmallIntegerField(verbose_name='Folio Receta', null=True, blank=True, default='')
    recibootros = models.SmallIntegerField(verbose_name='U recibo otros', null=True, blank=True, default='')
    sesiong = models.SmallIntegerField( verbose_name='U sesion grupal', null=True, blank=True, default='')
    responsable = models.CharField(max_length=30, verbose_name='Responsable', null=True, blank=True, default='')
    cedula = models.CharField(max_length=20, verbose_name='Cedula', null=True, blank=True, default='')
    cargo = models.CharField(max_length=20, verbose_name='Cargo', null=True, blank=True, default='')


class Internos(models.Model):

    objects = models.Manager()

    opcionesSexo=[('F','Femenino'),('M','Masculino')]
    opcionesEstadocivil=[('S','Soltero'),('C','Casado'),('V','Viudo'),('D','Divorciado')]
    opcionesIngreso=[('V','Voluntario'),('I','Involuntario'),('O','Obligatorio')]
    opcionesAcude=[('S','Solo'),('A','Amigo'),('F','Familiar'),('O','Otro')]
    opcionesProviene=[('D','Domiclio particular'),('P','Institucion publica'),('C','Institucion privada'),('O','Otra')]
    opcionesPorcual=[('A','Alcohol'),('B','Anfetaminas'),('C','Secantes'),('D','Marihuana'),('E','Rohypnol'),('F','Analgesicos'),
                     ('G','Disolventes'),('H','Cocaina'),('I','Opcio'),('J','Cristal')]

    numeroexpediente = models.CharField(max_length=10, verbose_name='No.Expediente', null=True, blank=True)
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
    numeroreuniones = models.SmallIntegerField(verbose_name='No. Reuniones', null=True, default=False,blank=True)
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
    periodopago = models.SmallIntegerField(verbose_name='Periodo de pago', null=True, blank=True)
    reciboinicial = models.SmallIntegerField(verbose_name='Recibo inicial', null=True, blank=True)
    proxsesconind = models.DateField(verbose_name='Próxima sesión individual', null=True, blank=True)
    proxsesconfam = models.DateField(verbose_name='Próxima sesión familiar' , null=True, blank=True)
    proxsescongru = models.DateField(verbose_name='Próxima sesión grupal', null=True, blank=True)
    proximasesionps = models.DateField(verbose_name='Próxima sesión PS', null=True, blank=True)
    proximasesiong = models.DateField(verbose_name='Próxima sesión G', null=True, blank=True)
    proxseseg = models.DateField(verbose_name='Próxima sesión EG', null=True, blank=True)
    fechariesgo = models.DateField(verbose_name='Fecha de riesgo', null=True, blank=True)
    nacionalidad = models.CharField(max_length=15, verbose_name='Nacionalidad', null=True, blank=True)



    def __str__(self):
        return self.nombrecompleto
