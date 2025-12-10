from django import forms
import datetime
from mapp.models import Internos,DatosGrales,Usuarios,Einicial,Assist,Cfisicas,Cmentales,Crelaciones,\
                        Tratamientos,SituacionFamiliar,Psicosis,Sdevida,Usodrogas,Ansiedad,Depresion,Marcadores,\
                        Riesgos,Razones,Valorizacion,CIndividual,CFamiliar,CGrupal,PConsejeria,TareaConsejeria,\
                        HojaAtencionPs,NotasEvolucionPS,Medico,Recetas,HistoriaClinica,Clinicas,Seguimiento,Estados,\
                        NotasSeguimiento

from django.utils import timezone
from django.forms import widgets,NumberInput
from datetime import date, timedelta

class Internosf(forms.ModelForm):

    class Meta:
        model=Internos
        fields=['numeroexpediente','fechaingreso','fsalidareal','nombrecompleto','edad','sexo',
                'estadocivil','lugarnac','estadonac','paisnac',
                'calleynumero','colonia','ciudad','estado','pais','codigopostal','telefono',
                'escolaridad','ocupacion','telefonotrabajo','tiempodesempleado','tipoingreso']


        widgets = {
            'fechaingreso': forms.DateInput(attrs={'type': 'date'}),
            'fsalidareal': forms.DateInput(attrs={'type': 'date'}),
            'tipoingreso': forms.RadioSelect(choices=Internos.opcionesIngreso,attrs={'class':'opciones-radio'}),
            'sexo': forms.RadioSelect(choices=Internos.opcionesSexo,attrs={'class':'opciones-radio'}),
            'estadocivil': forms.RadioSelect(choices=Internos.opcionesEstadocivil,attrs={'class': 'opciones-radio'})
        }

class IntResponsablef(forms.ModelForm):

    class Meta:
        model=Internos
        fields=['responsable','rcalle','rcolonia','rciudad',
                'restado','rpais','rtelefono']

class IntSalidasf(forms.ModelForm):
    fsalidareal = forms.DateField(
        initial=datetime.date.today,
        widget=forms.DateInput(attrs={
            'class': 'form-control form-control-sm',
            'type': 'date',  # ✅ Input nativo de fecha
        }),
        input_formats=['%Y-%m-%d'],  # ✅ Formato internacional estándar
        label='Fecha de salida'
    )
    class Meta:
        model=Internos
        fields=['fsalidareal','Motivoegreso','resumenanexo','estadodesalud','prevencionrecaidas']
        widgets={'Motivoegreso': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
                 'resumenanexo': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
                 'estadodesalud': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
                 'prevencionrecaidas': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3})}



class IntDependientesf(forms.ModelForm):

    class Meta:
        model=Internos
        fields=['dpadres','dconyugue','dhijos','dotros','comentarios']
        widgets={'dpadres':forms.CheckboxInput(attrs={'class':'opciones-check'}),
               'dhijos':forms.CheckboxInput(attrs={'class':'opciones-check'}),
               'dconyugue':forms.CheckboxInput(attrs={'class':'opciones-check'}),
               'dotros':forms.CheckboxInput(attrs={'class':'opciones-check'})
               }

class IntProvienef(forms.ModelForm):

    aportaciontotal = forms.DecimalField(decimal_places=2, widget=forms.TextInput(attrs={'class': 'dinero'}),
                                         label='Aportacion total')
    aportacioninicial = forms.DecimalField(decimal_places=2, widget=forms.TextInput(attrs={'class': 'dinero'}),
                                           label='Aportacion inicial')
    class Meta:
        model = Internos
        fields = ['proviene','provieneotro','acudecon','acudeotro','tomamedicinas',
                  'especifique','padecimientos','embarazo','psiquiatricas','fisicas','contagiosas',
                  'enfermedadesotro','basiloscopia','alcohol','anfetaminas','secantes','marihuana',
                  'rohypnol','analgesicos','disolventes','cocaina','opio','cristal','porcualingresa','numeroreuniones',
                  'diversasactividades', 'duracion','aportaciontotal', 'aportacioninicial','quieninformo']

        widgets={'embarazo':forms.CheckboxInput(),
                 'psiquiatricas':forms.CheckboxInput(),
                 'fisicas':forms.CheckboxInput(),
                 'contagiosas':forms.CheckboxInput(),
                 'basiloscopia': forms.CheckboxInput(),
                 'alcohol': forms.CheckboxInput(),
                 'anfetaminas': forms.CheckboxInput(),
                 'secantes': forms.CheckboxInput(),
                 'marihuana': forms.CheckboxInput(),
                 'rohypnol': forms.CheckboxInput(),
                 'analgesicos': forms.CheckboxInput(),
                 'disolventes': forms.CheckboxInput(),
                 'cocaina': forms.CheckboxInput(),
                 'opio': forms.CheckboxInput(),
                 'cristal': forms.CheckboxInput(),
                 'tomamedicinas': forms.CheckboxInput(),
                 'padecimientos': forms.CheckboxInput()

                  }


class DatosGralesf(forms.ModelForm):
    class Meta:
        model = DatosGrales
        exclude = ['logo_url', 'recibo', 'receta', 'recibootros', 'sesiong', 'expediente']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    # Modificamos el init para recibir 'permisos'
    def __init__(self, *args, **kwargs):
        # 1. Extraemos el permiso directo que mandaremos desde la vista
        # Si no llega nada, asumimos 'None'
        self.permisos_usuario = kwargs.pop('permisos', None)

        super(DatosGralesf, self).__init__(*args, **kwargs)

        # 2. Tu lógica de validación usando el dato de la sesión
        # Ajusta 'admin' al valor exacto que guardaste en el login (ej. 'Administrador', 'ADMIN', etc.)
        es_admin = False

        # Validamos que exista el dato y que sea igual al rol de administrador
        if self.permisos_usuario and self.permisos_usuario == 'admin':
            es_admin = True

        # 3. Si no es admin, borramos el campo
        if not es_admin:
            self.fields.pop('password', None)
            self.fields.pop('clinica', None)





class Usuariosf(forms.ModelForm):
    # Define el ChoiceField AQUÍ, fuera del Meta
    cargo = forms.ChoiceField(
        choices=Usuarios.opcionesCargo,
        widget=forms.Select(attrs={
            'class': 'form-control form-control-md',
            'maxlength': '20'
        })
    )

    class Meta:
        model = Usuarios
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'maxlength': 30}),
            'permisos': forms.TextInput(attrs={'maxlength': 5}),
            'password': forms.PasswordInput(attrs={'maxlength': 10}),
            'cedula': forms.TextInput(attrs={'maxlength': 20}),
            'expedidapor': forms.TextInput(attrs={'maxlength': 30})
        }

    def clean(self):
        cleaned_data = super().clean()
        for field in self.fields:
            if cleaned_data.get(field) is None:
                cleaned_data[field] = ''
        return cleaned_data

class Einicialf(forms.ModelForm):

    mayortiempo = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False)

    mayortiempo6 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False)

    class Meta:
        model=Einicial
        fields ='__all__'
        widgets={'expediente': forms.HiddenInput(),'consumo1':forms.CheckboxInput(attrs={'class':'form-check-input','role':'switch'}),
            'consumo2':forms.CheckboxInput(attrs={'class':'form-check-input','role':'switch'}),
            'consumo3':forms.CheckboxInput(attrs={'class':'form-check-input','role':'switch'}),
            'consumo4':forms.CheckboxInput(attrs={'class':'form-check-input','role':'switch'}),
            'consumo5': forms.CheckboxInput(attrs={'class':'form-check-input','role':'switch'}),
            'consumo6': forms.CheckboxInput(attrs={'class':'form-check-input','role':'switch'}),
            'consumo7': forms.CheckboxInput(attrs={'class':'form-check-input','role':'switch'}),
            'consumo8': forms.CheckboxInput(attrs={'class':'form-check-input','role':'switch'}),
            'consumo9': forms.CheckboxInput(attrs={'class':'form-check-input','role':'switch'}),
            'consumo10': forms.CheckboxInput(attrs={'class':'form-check-input','role':'switch'}),
            'principalsustancia': forms.RadioSelect(choices=Einicial.opcionesSustancias, attrs={'class': 'form-check-input'}),
            'cualalcohol':forms.RadioSelect(choices=Einicial.opcionesAlcohol, attrs={'class': 'form-check-input'}),
            'normalmentecomo':forms.RadioSelect(choices=Einicial.opcionesComo, attrs={'class': 'form-check-input'}),
            'detenervoluntariamente':forms.RadioSelect(choices=SituacionFamiliar.opcionesConflicto,attrs={'class': 'form-check-input'}),
            'edesagradables':forms.RadioSelect(choices=Einicial.opcionesPorque,attrs={'class': 'form-check-input'}),
            'enfermedad':forms.RadioSelect(choices=Einicial.opcionesPorque,attrs={'class': 'form-check-input'}),
            'necesidadfisica':forms.RadioSelect(choices=Einicial.opcionesPorque,attrs={'class': 'form-check-input'}),
            'probando':forms.RadioSelect(choices=Einicial.opcionesPorque,attrs={'class': 'form-check-input'}),
            'conflictos':forms.RadioSelect(choices=Einicial.opcionesPorque,attrs={'class': 'form-check-input'}),
            'agradablesotros':forms.RadioSelect(choices=Einicial.opcionesPorque,attrs={'class': 'form-check-input'}),
            'presion':forms.RadioSelect(choices=Einicial.opcionesPorque,attrs={'class': 'form-check-input'}),
            'eagradables':forms.RadioSelect(choices=Einicial.opcionesPorque,attrs={'class': 'form-check-input'}),
            'tamanoproblema':forms.RadioSelect(choices=Einicial.opcionesTamano,attrs={'class': 'form-check-input'}),
            'tamanoproblemad':forms.RadioSelect(choices=Einicial.opcionesTamano,attrs={'class': 'form-check-input'}),
            'quetanimportante':forms.RadioSelect(choices=Einicial.opcionesImportante,attrs={'class': 'form-check-input'}),
            'piensaque':forms.RadioSelect(choices=Einicial.opcionesImportante,attrs={'class': 'form-check-input'}),
            'dispuesto':forms.RadioSelect(choices=Einicial.opcionesImportante,attrs={'class': 'form-check-input'})
            }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Hacer readonly los campos de default
            campos_readonly = ['consejero', 'nombreconsejero', 'expediente', 'clinica']
            for campo in campos_readonly:
                if campo in self.fields:
                    self.fields[campo].widget.attrs['readonly'] = True
                    self.fields[campo].widget.attrs['class'] = 'form-control bg-light'



class SituacionFamiliarf(forms.ModelForm):

    class Meta:
        model=SituacionFamiliar
        fields ='__all__'
        widgets = {'expediente': forms.HiddenInput(),
                   'quienesintegran' :  forms.Textarea(attrs={'rows':3,'cols':40,'class':'form-control'}),
                   'hacercosasjuntos': forms.RadioSelect(choices=SituacionFamiliar.opcionesAcuerdooNo,attrs={'class': 'form-check-input'}),
                   'nadiesepreocupa': forms.RadioSelect(choices=SituacionFamiliar.opcionesAcuerdooNo,attrs={'class': 'form-check-input'}),
                   'soncalidos': forms.RadioSelect(choices=SituacionFamiliar.opcionesAcuerdooNo,attrs={'class': 'form-check-input'}),
                   'expresaropiniones': forms.RadioSelect(choices=SituacionFamiliar.opcionesAcuerdooNo,attrs={'class': 'form-check-input'}),
                   'esdesagradable': forms.RadioSelect(choices=SituacionFamiliar.opcionesAcuerdooNo,attrs={'class': 'form-check-input'}),
                   'enconjunto': forms.RadioSelect(choices=SituacionFamiliar.opcionesAcuerdooNo,attrs={'class': 'form-check-input'}),
                   'meescucha': forms.RadioSelect(choices=SituacionFamiliar.opcionesAcuerdooNo,attrs={'class': 'form-check-input'}),
                   'platicoproblemas': forms.RadioSelect(choices=SituacionFamiliar.opcionesAcuerdooNo, attrs={'class': 'form-check-input'}),
                   'expresamoscarino': forms.RadioSelect(choices=SituacionFamiliar.opcionesAcuerdooNo,attrs={'class': 'form-check-input'}),
                   'nuncaseresuelven': forms.RadioSelect(choices=SituacionFamiliar.opcionesAcuerdooNo,attrs={'class': 'form-check-input'}),
                   'cuandoesta': forms.RadioSelect(choices=SituacionFamiliar.opcionesCuandoesta, attrs={'class': 'form-check-input'}),
                   'conflictograve': forms.RadioSelect(choices=SituacionFamiliar.opcionesConflicto, attrs={'class': 'form-check-input'}),
                   'papa':forms.RadioSelect(choices=SituacionFamiliar.opcionesConflicto, attrs={'class': 'form-check-input'}),
                   'mama':forms.RadioSelect(choices=SituacionFamiliar.opcionesConflicto, attrs={'class': 'form-check-input'}),
                   'hermano':forms.RadioSelect(choices=SituacionFamiliar.opcionesConflicto, attrs={'class': 'form-check-input'}),
                   'amigo':forms.RadioSelect(choices=SituacionFamiliar.opcionesConflicto, attrs={'class': 'form-check-input'}),
                   'pareja':forms.RadioSelect(choices=SituacionFamiliar.opcionesConflicto, attrs={'class': 'form-check-input'}),
                   'familiar':forms.RadioSelect(choices=SituacionFamiliar.opcionesConflicto, attrs={'class': 'form-check-input'}),
                   'mejormuerto':forms.RadioSelect(choices=SituacionFamiliar.opcionesConflicto, attrs={'class': 'form-check-input'}),
                   'haintentado':forms.RadioSelect(choices=SituacionFamiliar.opcionesConflicto, attrs={'class': 'form-check-input'}),
                   'ultimomesintentado':forms.RadioSelect(choices=SituacionFamiliar.opcionesConflicto, attrs={'class': 'form-check-input'}),
                   'presentaenfermedad':forms.RadioSelect(choices=SituacionFamiliar.opcionesConflicto, attrs={'class': 'form-check-input'}),
                   'derivadaporuso':forms.RadioSelect(choices=SituacionFamiliar.opcionesConflicto, attrs={'class': 'form-check-input'}),
                   'siendoatendido':forms.RadioSelect(choices=SituacionFamiliar.opcionesConflicto, attrs={'class': 'form-check-input'}),
                   'medicado':forms.RadioSelect(choices=SituacionFamiliar.opcionesConflicto, attrs={'class': 'form-check-input'}),
                   'estadointernado':forms.RadioSelect(choices=SituacionFamiliar.opcionesConflicto, attrs={'class': 'form-check-input'}),
                   'porconsumo':forms.RadioSelect(choices=SituacionFamiliar.opcionesConflicto, attrs={'class': 'form-check-input'}),
                   'algunavez':forms.RadioSelect(choices=SituacionFamiliar.opcionesConflicto, attrs={'class': 'form-check-input'})
                   }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Hacer readonly los campos de default
            campos_readonly = ['consejero', 'nombreconsejero', 'expediente', 'clinica']
            for campo in campos_readonly:
                if campo in self.fields:
                    self.fields[campo].widget.attrs['readonly'] = True
                    self.fields[campo].widget.attrs['class'] = 'form-control bg-light'

class Cfisicasf(forms.ModelForm):


    class Meta:
        model=Cfisicas
        fields ='__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        prefix = 'cfisicas_'
        for field in self.fields.values():  # 👈 Esta línea lo resuelve
            field.required = False  # Desactiva todos los campos requeridos

        # Configuración común para campos pX
        for i in range(1, 27):
            field_name = f'fp{i}'
            if field_name in self.fields:
               self.fields[field_name].widget = forms.RadioSelect(
                    choices=Cfisicas.opcionesSioNo,
                    attrs={'class': 'form-check-input',
                           'id': f'{prefix}{field_name}'}
                    )

            # Configuración común para campos pXa
        for i in range(1, 27):
            field_name = f'fp{i}a'
            if field_name in self.fields:
               self.fields[field_name].widget = forms.RadioSelect(
                    choices=Cfisicas.opcionesAfectado,
                    attrs={'class': 'form-check-input',
                           'id': f'{prefix}{field_name}'}  # ID único
                    )

            self.fields['fpr1'].widget =forms.RadioSelect(choices=Cfisicas.opcionesSioNo,attrs={'class': 'form-check-input','id': 'fpr1'})
            self.fields['fpr2'].widget =forms.RadioSelect(choices=Cfisicas.opcionesSioNo,attrs={'class': 'form-check-input','id': 'fpr2'})
            self.fields['fpr3'].widget =forms.RadioSelect(choices=Cfisicas.opcionesSioNo,attrs={'class': 'form-check-input','id': 'fpr3'})
            self.fields['fpr4'].widget =forms.RadioSelect(choices=Cfisicas.opcionesSioNo,attrs={'class': 'form-check-input','id': 'fpr4'})

            self.fields['expediente'].widget = forms.HiddenInput()
            self.fields['comoesrelacion'].widget = forms.RadioSelect(choices=Cfisicas.opcionesComoeslarelacion, attrs={'class': 'form-check-input'})
            self.fields['comovepapa'].widget = forms.RadioSelect(choices=Cfisicas.opcionesComoloven, attrs={'class': 'form-check-input'})
            self.fields['comovemama'].widget = forms.RadioSelect(choices=Cfisicas.opcionesComoloven, attrs={'class': 'form-check-input'})
            self.fields['comovemaestros'].widget = forms.RadioSelect(choices=Cfisicas.opcionesComoloven, attrs={'class': 'form-check-input'})
            self.fields['comoveamigos'].widget = forms.RadioSelect(choices=Cfisicas.opcionesComoloven, attrs={'class': 'form-check-input'})
            self.fields['comovepareja'].widget = forms.RadioSelect(choices=Cfisicas.opcionesComoloven, attrs={'class': 'form-check-input'})
            self.fields['comovehermanos'].widget = forms.RadioSelect(choices=Cfisicas.opcionesComoloven, attrs={'class': 'form-check-input'})
            self.fields['relacionconhermanos'].widget = forms.RadioSelect(choices=Cfisicas.opcionesComoeslarelacion, attrs={'class': 'form-check-input'})
            self.fields['papa'].widget=forms.CheckboxInput(attrs={'class':'form-check-input','role':'switch'})
            self.fields['mama'].widget=forms.CheckboxInput(attrs={'class':'form-check-input','role':'switch'})

            campos_readonly = ['consejero', 'nombreconsejero', 'expediente', 'clinica']
            for campo in campos_readonly:
                if campo in self.fields:
                    self.fields[campo].widget.attrs['readonly'] = True
                    self.fields[campo].widget.attrs['class'] = self.fields[campo].widget.attrs.get('class',
                                                                                                   '') + ' bg-light'


class Cmentalesf(forms.ModelForm):


    class Meta:
        model = Cmentales
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():  # 👈 Esta línea lo resuelve
            field.required = False  # Desactiva todos los campos requeridos
        # Configuración común para campos pX
        for i in range(1, 35):
            field_name = f'p{i}'
            if field_name in self.fields:
               self.fields[field_name].widget = forms.RadioSelect(
                    choices=Cmentales.opcionesSioNo,
                    attrs={'class': 'form-check-input'}
                )

        # Configuración común para campos pXa
        for i in range(1, 35):
            field_name = f'p{i}a'
            if field_name in self.fields:
                self.fields[field_name].required = False
                self.fields[field_name].widget = forms.RadioSelect(
                    choices=Cmentales.opcionesAfectado,
                    attrs={'class': 'form-check-input'}
                )

        # Campo expediente como hidden
        self.fields['expediente'].widget = forms.HiddenInput()

        campos_readonly = ['consejero', 'nombreconsejero', 'expediente', 'clinica']
        for campo in campos_readonly:
            if campo in self.fields:
                self.fields[campo].widget.attrs['readonly'] = True
                self.fields[campo].widget.attrs['class'] = self.fields[campo].widget.attrs.get('class',
                                                                                               '') + ' bg-light'

class Crelacionesf(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():  # 👈 Esta línea lo resuelve
            field.required = False  # Desactiva todos los campos requeridos

    class Meta:
        model=Crelaciones
        fields ='__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

            # Configuración común para campos pX
        for i in range(1, 52):
            field_name = f'rp{i}'
            if field_name in self.fields:
               self.fields[field_name].widget = forms.RadioSelect(
               choices=Crelaciones.opcionesSioNo,
               attrs={'class': 'form-check-input'}
                    )

            # Configuración común para campos pXa
        for i in range(1, 52):
            field_name = f'rp{i}a'
            if field_name in self.fields:
               self.fields[field_name].widget = forms.RadioSelect(
               choices=Crelaciones.opcionesAfectado,
               attrs={'class': 'form-check-input'}
               )

            # Campo expediente como hidden
        self.fields['expediente'].widget = forms.HiddenInput()
        self.fields['fechaduracionycausa'].widget = forms.TextInput(attrs={'class': 'form-control',  # Clase de Bootstrap para estilo
                'size': '50',             # Atributo HTML 'size': ancho aproximado en caracteres
                 'maxlength' : '50'})

        campos_readonly = ['consejero', 'nombreconsejero', 'expediente', 'clinica']
        for campo in campos_readonly:
            if campo in self.fields:
                self.fields[campo].widget.attrs['readonly'] = True
                self.fields[campo].widget.attrs['class'] = self.fields[campo].widget.attrs.get('class',
                                                                                               '') + ' bg-light'

class Tratamientosf(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():  # 👈 Esta línea lo resuelve
            field.required = False  # Desactiva todos los campos requeridos

        campos_readonly = ['consejero', 'nombreconsejero', 'expediente', 'clinica']
        for campo in campos_readonly:
            if campo in self.fields:
                self.fields[campo].widget.attrs['readonly'] = True
                self.fields[campo].widget.attrs['class'] = self.fields[campo].widget.attrs.get('class',
                                                                                               '') + ' bg-light'
    class Meta:
        model=Tratamientos
        fields ='__all__'
        widgets = {'expediente': forms.HiddenInput(),
               'satisfecho': forms.RadioSelect(attrs={'class': 'form-check-input'}),
               'recibio': forms.RadioSelect( attrs={'class': 'form-check-input'}),
               'a1':forms.RadioSelect( attrs={'class': 'form-check-input'}),
               'a2':forms.RadioSelect( attrs={'class': 'form-check-input'}),
               'a3':forms.RadioSelect( attrs={'class': 'form-check-input'}),
               'a4':forms.RadioSelect( attrs={'class': 'form-check-input'}),
               'a5':forms.RadioSelect( attrs={'class': 'form-check-input'}),
               'a6':forms.RadioSelect( attrs={'class': 'form-check-input'}),
               'a7':forms.RadioSelect( attrs={'class': 'form-check-input'}),
               'a8':forms.RadioSelect( attrs={'class': 'form-check-input'}),
               'd1': forms.RadioSelect( attrs={'class': 'form-check-input'}),
               'd2': forms.RadioSelect( attrs={'class': 'form-check-input'}),
               'd3': forms.RadioSelect( attrs={'class': 'form-check-input'}),
               'd4': forms.RadioSelect( attrs={'class': 'form-check-input'}),
               'd5': forms.RadioSelect( attrs={'class': 'form-check-input'}),
               'd6': forms.RadioSelect( attrs={'class': 'form-check-input'}),
               'd7': forms.RadioSelect( attrs={'class': 'form-check-input'}),
               'd8': forms.RadioSelect( attrs={'class': 'form-check-input'}),
               'c1': forms.RadioSelect(attrs={'class': 'form-check-input'}),
               'c2': forms.RadioSelect(attrs={'class': 'form-check-input'}),
               'c3': forms.RadioSelect(attrs={'class': 'form-check-input'}),
               'c4': forms.RadioSelect(attrs={'class': 'form-check-input'}),
               'c5': forms.RadioSelect(attrs={'class': 'form-check-input'}),
               'c6': forms.RadioSelect(attrs={'class': 'form-check-input'}),
               'c7': forms.RadioSelect(attrs={'class': 'form-check-input'}),
               'c8': forms.RadioSelect(attrs={'class': 'form-check-input'}),
               'h1': forms.TextInput(attrs={'class': 'form-control'}),
               'h2': forms.TextInput(attrs={'class': 'form-control'}),
               'h3': forms.TextInput(attrs={'class': 'form-control'}),
               'h4': forms.TextInput(attrs={'class': 'form-control'}),
               'h5': forms.TextInput(attrs={'class': 'form-control'}),
               'h6': forms.TextInput(attrs={'class': 'form-control'}),
               'h7': forms.TextInput(attrs={'class': 'form-control'}),
               'h8': forms.TextInput(attrs={'class': 'form-control'}),
               'r1': forms.TextInput(attrs={'class': 'form-control'}),
               'r2': forms.TextInput(attrs={'class': 'form-control'}),
               'r3': forms.TextInput(attrs={'class': 'form-control'}),
               'r4': forms.TextInput(attrs={'class': 'form-control'}),
               'r5': forms.TextInput(attrs={'class': 'form-control'}),
               'r6': forms.TextInput(attrs={'class': 'form-control'}),
               'r7': forms.TextInput(attrs={'class': 'form-control'}),
               'r8': forms.TextInput(attrs={'class': 'form-control'}),
               'problemas': forms.Textarea(attrs={'rows': 10,'class': 'form-control bg-hover','cols': 40}),
               'observaciones': forms.Textarea(attrs={'rows':10,'class': 'form-control bg-hover','cols': 40})
                }



class Assistf(forms.ModelForm):

    class Meta:
        model = Assist
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():  # 👈 Esta línea lo resuelve
            field.required = False  # Desactiva todos los campos requeridos

          # Generación dinámica de campos p1s1 a p9s10
        for i in range(1, 8):  # p1s1 a p9s10 (i: 1-9)
            if i==1:
               opcionesReales=Assist.opcionesSioNo
            elif i<7:
               opcionesReales=Assist.opcionesCinco
            else :
               opcionesReales=Assist.opcionesTres

        for j in range(1, 11):  # s1 a s10 (j: 1-10)
            field_name = f'p{i}s{j}'
            model_field = self._meta.model._meta.get_field(field_name)
            self.fields[field_name] = forms.ChoiceField(
            choices=opcionesReales,

            widget=forms.RadioSelect(
            attrs={'class': 'form-check-input',
                        'id': f'id_{field_name}',
                       }
                ),
            required=False,  # Cambia a True si es obligatorio
            label = model_field.verbose_name
            )

            self.fields['asistotras'] = forms.CharField(max_length=20)
            self.fields['asistotras2'] = forms.CharField(max_length=20, required=False,widget=forms.TextInput(attrs={'readonly': True}))
            self.fields['asistotras3'] = forms.CharField(max_length=20, required=False,widget=forms.TextInput(attrs={'readonly': True}))
            self.fields['asistotras4'] = forms.CharField(max_length=20, required=False,widget=forms.TextInput(attrs={'readonly': True}))
            self.fields['asistotras5'] = forms.CharField(max_length=20, required=False,widget=forms.TextInput(attrs={'readonly': True}))
            self.fields['asistotras6'] = forms.CharField(max_length=20, required=False,widget=forms.TextInput(attrs={'readonly': True}))
            self.fields['asistotras7'] = forms.CharField(max_length=20, required=False,widget=forms.TextInput(attrs={'readonly': True}))
            self.fields['habitosinyectarse'].widget = forms.RadioSelect(choices= [(0, ''), (1, '')],attrs={'class': 'form-check-input'})
            self.fields['p8s1'].widget = forms.RadioSelect(choices=Assist.opcionesTres,attrs={'class': 'form-check-input'})


class Psicosisf(forms.ModelForm):
    class Meta:
        model = Psicosis
        fields = '__all__'
        widgets = {
           'pspuntos': forms.HiddenInput(attrs={
           'id': 'id_psicosisf_pspuntos',

        })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 1. Primero hacer todos los campos no requeridos
        for field in self.fields.values():
            field.required = False

        # 2. Configurar campos readonly

        # 3. Configurar campos dinámicos - CORREGIDO
        for j in range(1, 18):
            field_name = f'pp{j}'
            if field_name in self.fields:  # ✅ VERIFICAR si existe primero
                model_field = self._meta.model._meta.get_field(field_name)
                # ✅ Actualizar el campo EXISTENTE en lugar de reemplazarlo
                self.fields[field_name].widget = forms.RadioSelect(
                    attrs={
                        'class': 'form-check-input',
                        'id': f'id_{field_name}',
                    }
                )
                self.fields[field_name].choices = Psicosis.opcionesQuesiente
                self.fields[field_name].label = model_field.verbose_name



class Usodrogasf(forms.ModelForm):

    class Meta:
        model = Usodrogas
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():  # 👈 Esta línea lo resuelve
            field.required = False  # Desactiva todos los campos requeridos

          # Generación dinámica de campos p1s1 a p9s10
        campos_readonly = ['consejero', 'nombreconsejero', 'expediente', 'clinica']
        for campo in campos_readonly:
            if campo in self.fields:
                self.fields[campo].widget.attrs['readonly'] = True
                self.fields[campo].widget.attrs['class'] = self.fields[campo].widget.attrs.get('class',
                                                                                               '') + ' bg-light'

        for j in range(1, 21):
            field_name = f'udp{j}'
            model_field = self._meta.model._meta.get_field(field_name)
            self.fields[field_name] = forms.ChoiceField(
            choices=Usodrogas.opcionesSioNo,
            widget=forms.RadioSelect(
            attrs={'class': 'form-check-input',
                        'id': f'id_{field_name}',
                       }
                ),
            required=False,  # Cambia a True si es obligatorio
            label = model_field.verbose_name
            )

class Sdevidaf(forms.ModelForm):

    class Meta:
        model = Sdevida
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():  # 👈 Esta línea lo resuelve
            field.required = False  # Desactiva todos los campos requeridos

          # Generación dinámica de campos p1s1 a p9s10

        campos_readonly = ['consejero', 'nombreconsejero', 'expediente', 'clinica']
        for campo in campos_readonly:
            if campo in self.fields:
                self.fields[campo].widget.attrs['readonly'] = True
                self.fields[campo].widget.attrs['class'] = self.fields[campo].widget.attrs.get('class',
                                                                                               '') + ' bg-light'
        for j in range(1, 13):
            field_name = f'svp{j}'
            model_field = self._meta.model._meta.get_field(field_name)
            self.fields[field_name] = forms.ChoiceField(
            choices=Sdevida.opcionesSatisfecho,
            widget=forms.RadioSelect(
            attrs={'class': 'form-check-input',
                        'id': f'id_{field_name}',
                       }
                ),
            required=False,  # Cambia a True si es obligatorio
            label = model_field.verbose_name
            )

class Ansiedadf(forms.ModelForm):

    class Meta:
        model = Ansiedad
        fields = '__all__'

        widgets = {
            'anpuntos': forms.HiddenInput(attrs={
            'id': 'id_ansiedadf_anpuntos',
          })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():  # 👈 Esta línea lo resuelve
            field.required = False  # Desactiva todos los campos requeridos

          # Generación dinámica de campos p1s1 a p9s10
        campos_readonly = ['consejero', 'nombreconsejero', 'expediente', 'clinica']
        for campo in campos_readonly:
            if campo in self.fields:
                self.fields[campo].widget.attrs['readonly'] = True
                self.fields[campo].widget.attrs['class'] = self.fields[campo].widget.attrs.get('class',
                                                                                               '') + ' bg-light'

        for j in range(1, 22):
            field_name = f'anp{j}'
            model_field = self._meta.model._meta.get_field(field_name)
            self.fields[field_name] = forms.ChoiceField(
            choices=Ansiedad.opcionesAnsiedad,
            widget=forms.RadioSelect(
            attrs={'class': 'form-check-input',
                        'id': f'id_{field_name}',
                       }
                ),
            required=False,  # Cambia a True si es obligatorio
            label = model_field.verbose_name
            )

class Depresionf(forms.ModelForm):

    class Meta:
        model = Depresion
        fields = '__all__'

        widgets = {
            'deppuntos': forms.HiddenInput(attrs={
            'id': 'id_depresionf_deppuntos',
         })
       }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():  # 👈 Esta línea lo resuelve
            field.required = False  # Desactiva todos los campos requeridos

          # Generación dinámica de campos p1s1 a p9s10

        campos_readonly = ['consejero', 'nombreconsejero', 'expediente', 'clinica']
        for campo in campos_readonly:
            if campo in self.fields:
                self.fields[campo].widget.attrs['readonly'] = True
                self.fields[campo].widget.attrs['class'] = self.fields[campo].widget.attrs.get('class',
                                                                                               '') + ' bg-light'
        for j in range(1, 22):
            field_name = f'dep{j}'
            opciones = getattr(Depresion, f'opcionesP{j}', [])
            model_field = self._meta.model._meta.get_field(field_name)
            self.fields[field_name] = forms.ChoiceField(
            choices=opciones,
            widget=forms.RadioSelect(
            attrs={'class': 'form-check-input',
                        'id': f'id_{field_name}',
                       }
                ),
            required=False,  # Cambia a True si es obligatorio
            label = model_field.verbose_name
            )


class Marcadoresf(forms.ModelForm):

    class Meta:
        model = Marcadores
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():  # 👈 Esta línea lo resuelve
            field.required = False  # Desactiva todos los campos requeridos

        campos_readonly = ['consejero', 'nombreconsejero', 'expediente', 'clinica']
        for campo in campos_readonly:
            if campo in self.fields:
                self.fields[campo].widget.attrs['readonly'] = True
                self.fields[campo].widget.attrs['class'] = self.fields[campo].widget.attrs.get('class',
                                                                                               '') + ' bg-light'
        nombre_sustancia = None
        # Nos aseguramos de que el formulario esté asociado a un objeto guardado
        # y que el campo 'quedroga' tenga un valor.
        if self.instance and self.instance.pk and self.instance.quedrogausa is not None:
            # ¡Esta es la función mágica de Django!
            nombre_sustancia = self.instance.get_quedrogausa_display()

        for j in range(1, 18):
            field_name = f'marcador{j}'

            if field_name not in self.fields:
                continue

            model_field = self._meta.model._meta.get_field(field_name)
            label_original = model_field.verbose_name

            # 3. CONSTRUIR LA ETIQUETA DINÁMICA
            nueva_etiqueta = label_original
            # Solo si obtuvimos un nombre de sustancia, hacemos el reemplazo
            if nombre_sustancia:
                nueva_etiqueta = label_original.replace('[sustancia]', nombre_sustancia)

            # 4. CREAR/ACTUALIZAR EL CAMPO DEL FORMULARIO
            # En lugar de recrear el campo desde cero, es más seguro y limpio
            # simplemente actualizar la etiqueta del campo que ya existe.
            self.fields[field_name].label = nueva_etiqueta
            self.fields[field_name] = forms.ChoiceField(
            choices=Marcadores.opcionesSioNo,
            widget=forms.RadioSelect(
            attrs={'class': 'form-check-input',
                        'id': f'id_{field_name}',
                       }
                ),
            required=False,  # Cambia a True si es obligatorio
            label = model_field.verbose_name
            )

        self.fields['quedrogausa'].widget = forms.RadioSelect(choices=Marcadores.opcionesSustancia,
                                                                    attrs={'class': 'form-check-input'})
        self.fields['masdecincoveces'].widget = forms.RadioSelect(choices=Marcadores.opcionesSioNo,
                                                                    attrs={'class': 'form-check-input'})

class Riesgosf(forms.ModelForm):

    class Meta:
        model = Riesgos
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():  # 👈 Esta línea lo resuelve
            field.required = False  # Desactiva todos los campos requeridos

        campos_readonly = ['consejero', 'nombreconsejero', 'expediente', 'clinica']
        for campo in campos_readonly:
            if campo in self.fields:
                self.fields[campo].widget.attrs['readonly'] = True
                self.fields[campo].widget.attrs['class'] = self.fields[campo].widget.attrs.get('class',
                                                                                               '') + ' bg-light'

        for j in range(1, 10):
            field_name = f'riesgosP{j}'


            model_field = self._meta.model._meta.get_field(field_name)
            label_original = model_field.verbose_name
            if j == 1:
                opcionesReales = Riesgos.opcionesFrecuencia
            elif j == 2:
                opcionesReales = Riesgos.opcionesCuantas
            elif j < 8:
                opcionesReales = Riesgos.opcionesSeisoMas
            else:
                opcionesReales = Riesgos.opcionesOtras



            self.fields[field_name] = forms.ChoiceField(
            choices=opcionesReales,
            widget=forms.RadioSelect(
            attrs={'class': 'form-check-input',
                        'id': f'id_{field_name}',
                       }
                ),
            required=False,  # Cambia a True si es obligatorio
            label = model_field.verbose_name
            )


class Razonesf(forms.ModelForm):

    sabias = forms.ChoiceField(
        choices=[(1, 'Si'), (0, 'No')],
        widget=forms.RadioSelect(
            attrs={'class': 'form-check-input'}
        ),
        label="¿Sabías cuáles eran los riesgos?"
        )

    class Meta:
        model = Razones
        fields = '__all__'

        widgets = { 'factores': forms.Textarea(attrs={'rows':4,'cols':40}),
                    'motivos': forms.Textarea(attrs={'rows':4,'cols':40}),
                    'cuales': forms.Textarea(attrs={'rows':4,'cols':40}),
                    'quemotivos': forms.Textarea(attrs={'rows':4,'cols':40}),
                    'querazones': forms.Textarea(attrs={'rows':4,'cols':40}),
                    'observaciones': forms.Textarea(attrs={'rows':4,'cols':40}),
                    }


class Valorizacionf(forms.ModelForm):


    mainsustance = forms.CharField(
        label="Principal sustancia:",
        required=False,  # 'required' se define aquí
        widget=forms.TextInput(
            attrs={
                'readonly': True,
                # Atributos solo para HTML van aquí, como 'class', 'placeholder', etc.
            }
        )
    )

    class Meta:
          model = Valorizacion
          fields = '__all__'


          widgets = { 'razonesdeconsumo': forms.Textarea(attrs={'rows':4,'cols':40,'readonly': True}),
                    'psicosis': forms.Textarea(attrs={'rows':4,'cols':40, 'readonly':True}),
                    'deteccionyriesgos': forms.Textarea(attrs={'rows':4,'cols':40,'readonly': True}),
                    'ansiedad': forms.Textarea(attrs={'rows':4,'cols':40,'readonly':True}),
                    'depresion': forms.Textarea(attrs={'rows':4,'cols':40,'readonly':True}),
                    'satisfacciondevida': forms.Textarea(attrs={'rows':4,'cols':40,'readonly':True}),
                    'medico': forms.Textarea(attrs={'rows':4,'cols':23}),
                    'psiquiatrica': forms.Textarea(attrs={'rows':4,'cols':23}),
                    'psicologica': forms.Textarea(attrs={'rows':4,'cols':23}),
                    'hacecuanto': forms.TextInput(attrs={'readonly':True,
                                                         'class':'form-control rounded-pill'}),
                    'cantidadpromedio': forms.TextInput(attrs={'readonly':True,
                                                               'class': 'form-control rounded-pill'
                                                               }),
                    'razon1': forms.TextInput(attrs={'readonly':True,
                                                     'class': 'form-control rounded-pill'
                                                     }),
                    'razon2': forms.TextInput(attrs={'readonly':True,
                                                     'class': 'form-control rounded-pill'
                                                     }),
                    'razon3': forms.TextInput(attrs={'readonly':True,
                                                     'class': 'form-control rounded-pill'
                                                     }),
                    }

class ExpedienteSoloForm(forms.Form):
    expediente = forms.CharField(max_length=10, label='No.Expediente')


class CIndividualf(forms.ModelForm):
    class Meta:
        model = CIndividual
        exclude = ['expediente', 'clinica', 'consejero', 'sesion']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'proximasesion': forms.DateInput(attrs={'type': 'date'}),
        }

class CFamiliarf(forms.ModelForm):
    class Meta:
        model = CFamiliar
        exclude = ['expediente', 'clinica', 'consejero', 'sesion']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'proximasesion': forms.DateInput(attrs={'type': 'date'}),
        }

class CGrupalf(forms.ModelForm):
    class Meta:
        model = CGrupal
        fields = [
            'sesion', 'diasestancia', 'fecha', 'proximasesion', 'consejero',
            'tema_sesion', 'dinamica_utilizada', 'objetivo', 'aspectos',
            'resultados', 'seesperan', 'tareas', 'quesetrabajo', 'observaciones'
        ]
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
            'proximasesion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
            'sesion': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'diasestancia': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'consejero': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'tema_sesion': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'dinamica_utilizada': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'objetivo': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'aspectos': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'resultados': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'seesperan': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'tareas': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'quesetrabajo': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
        }

class PConsejeriaf(forms.ModelForm):
    class Meta:
        model = PConsejeria
        fields = ['expediente', 'fecha','consejero','alcoholydrogas', 'fisicaymental', 'areasdelavida',
                  'metas', 'objetivos', 'compromiso', 'logros', 'metasareasdevida', 'prevencion']

        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
            'consejero': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'alcoholydrogas': forms.Textarea(attrs={'class':'form-control form-control-sm', 'rows': 3}),
            'fisicaymental': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'areasdelavida': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'metas': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'objetivos': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'compromiso': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'logros': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'metasareasdevida': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'prevencion': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),}

class TareaConsejeriaf(forms.ModelForm):
    class Meta:
        model = TareaConsejeria
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'rows': 2,
                'cols': 60,  # ← Aumenta de 40 a 60 (más ancho)
                'class': 'form-control',
                'placeholder': 'Describe la tarea escaneada...',
                'style': 'width: 100%;'  # ← Ocupa todo el ancho disponible
            })
        }





class HojaAtencionPsf(forms.ModelForm):
    class Meta:
        model = HojaAtencionPs
        fields = ['expediente', 'fecha','psicologo','lateralidad', 'motivo', 'antecedentes',
                  'instrumentos', 'observaciones', 'resultados', 'diagnostico']

        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
            'psicologo': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'lateralidad': forms.RadioSelect(attrs={'class':'form-check-input'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'antecedentes': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'instrumentos': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'resultados': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
        }

class NotasEvolucionPSf(forms.ModelForm):
    class Meta:
        model = NotasEvolucionPS

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            for field in self.fields.values():  # 👈 Esta línea lo resuelve
                field.required = False  # Desactiva todos los campos requeridos


        fields = [
            'expediente','sesion', 'status','fecha', 'proximasesion', 'psicologo',
            'objetivo', 'resumen', 'resultado', 'objetivoyplan','actividades',
            'observaciones','individualogrupal','selograron'
        ]
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
            'proximasesion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
            'sesion': forms.NumberInput(attrs={'class': 'form-control form-control-sm','readonly':'readonly'}),
            'psicologo': forms.NumberInput(attrs={'class': 'form-control form-control-sm','readonly':'readonly'}),
            'objetivo': forms.Textarea(attrs={'class': 'form-control form-control-sm','rows': 3}),
            'resumen': forms.Textarea(attrs={'class': 'form-control form-control-sm','rows': 3}),
            'resultado': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'objetivoyplan': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'actividades': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'individualogrupal': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'quesetrabajo': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'selograron': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

        }

class Medicof(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['expediente', 'fecha','medico','motivo','padecimiento', 'sintomas', 'tratamientos','TA','FC','FR','temperatura','peso',
                  'talla','exploracion', 'examenmental', 'diagnostico', 'pronostico','tratamientosugerido']

        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
            'medico': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'padecimiento': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'sintomas': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'tratamientos': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'TA': forms.TextInput(attrs={'class': 'form-control form-control-sm','style':'max-width : 100px'}),
            'FC': forms.TextInput(attrs={'class': 'form-control form-control-sm','style':'max-width : 100px'}),
            'FR': forms.TextInput(attrs={'class': 'form-control form-control-sm','style':'max-width : 100px'}),
            'temperatura': forms.TextInput(attrs={'class': 'form-control form-control-sm','style':'max-width : 100px'}),
            'peso': forms.TextInput(attrs={'class': 'form-control form-control-sm','style':'max-width : 100px'}),
            'talla': forms.TextInput(attrs={'class': 'form-control form-control-sm','style':'max-width : 100px'}),
            'exploracion': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'examenmental': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'pronostico': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'tratamientosugerido': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),

        }

class Recetasf(forms.ModelForm):
    class Meta:
        model = Recetas
        fields = ['expediente','historial']

        widgets = {
            'historial': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),}



class HistoriaClinicaf(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = '__all__'
        widgets = {
            'expediente': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '10'
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control form-control-sm',
                'type': 'date'
            }),
            'medico': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm'
            }),
            # Campos booleanos para padres
            'padresPadecimientosCronicos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'padresInfectoContagiosos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'padresAlergias': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'padresTraumaticos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'padresConsumos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'padresMentales': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'padresOtros': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            # Campos booleanos para hermanos
            'hermanosPadecimientosCronicos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'hermanosInfectoContagiosos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'hermanosAlergias': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'hermanosTraumaticos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'hermanosConsumos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'hermanosMentales': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'hermanosOtros': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            # Campos booleanos para conyugue
            'conyuguePadecimientosCronicos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'conyugueInfectoContagiosos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'conyugueAlergias': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'conyugeTraumaticos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'conyugueConsumos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'conyugueMentales': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'conyugueOtros': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            # Campos booleanos para hijos
            'hijosPadecimientosCronicos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'hijosInfectoContagiosos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'hijosAlergias': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'hijosTraumaticos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'hijosConsumos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'hijosMentales': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'hijosOtros': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            # Campos booleanos para colaterales
            'colateralesPadecimientosCronicos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'colateralesInfectoContagiosos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'colateralesAlergias': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'colateralesTraumaticos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'colateralesConsumos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'colateralesMentales': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'colateralesOtros': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            # Campos booleanos para convivientes
            'convivientesPadecimientosCronicos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'convivientesInfectoContagiosos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'convivientesAlergias': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'convivientesTraumaticos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'convivientesConsumos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'convivientesMentales': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'convivientesOtros': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            # Campos booleanos para habitacion
            'habitacionUrbana': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'habitacionRural': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'habitacionTodoslosServicios': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'habitacionMovilidad': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            # Campos booleanos varios
            'alimentacion': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'actividadFisica': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'quirurgico': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'hospitalizaciones': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'transfuciones': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'tratamientoRecidencia': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'dietaNormal': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            # Campos de selección
            'frecuenciaBath': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'inmunizacion': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'cabeza': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'cabello': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'pupilas': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'faringe': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'amigdalas': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'adenomegalias': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'cuello': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'traquea': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'tiroides': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'adenomegaliasCuello': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'pulsos': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'torax': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'movsRespiratorios': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'camposPulmonares': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'ruidosCardiacos': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'adenomagliasAxilar': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'abdomen': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'doloralPalpar': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'viceromegalias': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'peristalsis': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'miembrossuperiores': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'miembrosinferiores': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'genitales': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'edadAparente': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'posicion': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'actitud': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'fluidez': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'lenguaje': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'funcionesIntelectuales': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'memoria': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'afectividad': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'sensopercepcion': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'ideacion': forms.Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            # Campos de texto corto
            'enfermedadActual': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '50'
            }),
            'alergias': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '50'
            }),
            'traumaticos': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '50'
            }),
            'adiccion': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '50'
            }),
            'internamientoporAdiccion': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '50'
            }),
            'padecimientoActual': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '50'
            }),
            'digestivo': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100'
            }),
            'cardiovascular': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100'
            }),
            'respiratorio': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100'
            }),
            'urinario': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100'
            }),
            'genital': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100'
            }),
            'hematologico': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100'
            }),
            'endocrino': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100'
            }),
            'osteomuscular': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100'
            }),
            'nervioso': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100'
            }),
            'sensorial': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100'
            }),
            'psicomatico': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100'
            }),
            # Signos vitales
            'TA': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '10'
            }),
            'FC': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '10'
            }),
            'FR': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '10'
            }),
            'temperatura': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '10'
            }),
            'PCO2': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '10'
            }),
            'IMC': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '10'
            }),
            'glucosa': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '10'
            }),
            'peso': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '10'
            }),
            'talla': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '10'
            }),
            # Campos de observaciones
            'cicatriz': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '30'
            }),
            'observaciones': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100'
            }),
            'observacionesCuello': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100'
            }),
            'observacionesAxilar': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100'
            }),
            'observacionesAbdomen': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100'
            }),
            'observacionesMiembros': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100'
            }),
            'observacionesGenitales': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100'
            }),
            'observacionesInspeccion': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100'
            }),
            'observacionesLenguaje': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100'
            }),
            'observacionesFunciones': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100'
            }),
            'observacionesAfectividad': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100'
            }),
            'observacionesSensopercepcion': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100'
            }),
            'observacionesIdeacion': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100'
            }),
            'dependenciaA': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100'
            }),
            # Campos de texto largo
            'observacionesDependencia': forms.Textarea(attrs={
                'class': 'form-control form-control-sm',
                'rows': 3
            }),
            'pronosticoParalaVida': forms.Textarea(attrs={
                'class': 'form-control form-control-sm',
                'rows': 3
            }),
            'otroTratamiento': forms.Textarea(attrs={
                'class': 'form-control form-control-sm',
                'rows': 3
            }),
            'justificacion': forms.Textarea(attrs={
                'class': 'form-control form-control-sm',
                'rows': 3
            }),
            'observacionesTratamiento': forms.Textarea(attrs={
                'class': 'form-control form-control-sm',
                'rows': 3
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegurar que todos los campos tengan clases CSS
        for field_name, field in self.fields.items():



            if 'class' not in field.widget.attrs:
                if isinstance(field.widget, (forms.Select, forms.NumberInput, forms.TextInput, forms.Textarea)):
                    field.widget.attrs['class'] = 'form-control form-control-sm'
                elif isinstance(field.widget, forms.CheckboxInput):
                    field.widget.attrs['class'] = 'form-check-input'

            for field in self.fields.values():  # 👈 Esta línea lo resuelve
                field.required = False  # Desac


class ClinicaLoginForm(forms.Form):
    clinica_id = forms.CharField(
        label="ID de tu Clínica",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: CLINICA001'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean_clinica_id(self):
        clinica_id = self.cleaned_data['clinica_id']
        return clinica_id.strip().upper()  # ← QUITA ESPACIOS Y CONVIERTE A MAYÚSCULAS



class Seguimientof(forms.ModelForm):
    class Meta:
        model = Seguimiento
        fields = '__all__'
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'expediente': forms.TextInput(attrs={'placeholder': 'Número de expediente'}),
            'viveotros': forms.TextInput(attrs={'placeholder': 'Especifique con quién vive'}),
            'causanohaconsumido': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describa los factores que han evitado el consumo'}),
            'obstaculos': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describa los obstáculos para mantener la abstinencia'}),
            'metasparelfuturo': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describa sus metas y objetivos futuros'}),
            'observaciones': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Observaciones relevantes sobre el usuario'}),
        }


class NotasSeguimientof(forms.ModelForm):
    class Meta:
        model = NotasSeguimiento
        fields = '__all__'
        widgets = {
                'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
                'proximasesion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
                'expediente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de expediente'}),
                'sesion': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
                'status': forms.Select(attrs={'class': 'form-select'}),
                'consejero': forms.Select(attrs={'class': 'form-select'}),
                'objetivo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Objetivo de la sesión'}),
                'consumodesustancias': forms.Textarea(
                    attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describa el consumo de sustancias'}),
                'plandeaccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                                      'placeholder': 'Plan de acción para situaciones de riesgo'}),
                'tareas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tareas asignadas'}),
                'aspectosqueserevisaran': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                                                'placeholder': 'Aspectos a revisar en la próxima sesión'}),
                'observaciones': forms.Textarea(
                    attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Comentarios y observaciones'}),
                'clinica': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Establecer valor por defecto para clínica si no existe
            if not self.instance.pk and not self.data.get('clinica'):
                self.initial['clinica'] = "Demostracion"


class ReporteFechaForm(forms.Form):
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha Inicio"
    )
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha Fin"
    )