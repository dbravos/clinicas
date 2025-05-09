from django import forms
from mapp.models import Internos,DatosGrales,Usuarios,Einicial,Assist
from django.utils import timezone
from django.forms import widgets


class Internosf(forms.ModelForm):

    class Meta:
        model=Internos
        fields=['numeroexpediente','fechaingreso','fsalidareal','nombrecompleto','edad','sexo',
                'estadocivil','lugarnac','estadonac','paisnac',
                'calleynumero','colonia','ciudad','estado','pais','codigopostal','telefono',
                'escolaridad','ocupacion','telefonotrabajo','tiempodesempleado','tipoingreso',
                'conquienvive']

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
        model=DatosGrales
        fields='__all__'
        correoelectronico=forms.EmailField()

class Usuariosf(forms.ModelForm):
    class Meta:
        model=Usuarios
        fields='__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'maxlength': 30}),
            'cargo' : forms.TextInput(attrs={'maxlength': 20}),
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
    class Meta:
        model=Einicial
        fields='__all__'
        widgets={'consumo1':forms.CheckboxInput(),
            'consumo2':forms.CheckboxInput(),
            'consumo3':forms.CheckboxInput(),
            'consumo4':forms.CheckboxInput(),
            'consumo5': forms.CheckboxInput(),
            'consumo6': forms.CheckboxInput(),
            'consumo7': forms.CheckboxInput(),
            'consumo8': forms.CheckboxInput(),
            'consumo9': forms.CheckboxInput(),
            'conusmo10': forms.CheckboxInput()
            }

class Assistf(forms.ModelForm):
            class Meta:
                model = Assist
                fields = '__all__'






