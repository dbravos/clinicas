from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .forms import LeadForm
from .models import Lead

def home(request):

    mensaje = None

    if request.method == 'POST':
        form = LeadForm(request.POST)

        if form.is_valid():
            lead = form.save()

            # 📩 Email al prospecto
            send_mail(
                subject="Gracias por solicitar una demo - FreshStart",
                message=f"""
Hola {lead.nombre},

Gracias por tu interés en FreshStart.

En breve nos pondremos en contacto para agendar una demostración personalizada.

Saludos,
Equipo FreshStart
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[lead.email],
                fail_silently=False,
            )

            # 📩 Notificación para ti
            send_mail(
                subject="Nuevo Lead FreshStart",
                message=f"""
Nuevo lead registrado:

Nombre: {lead.nombre}
Clínica: {lead.clinica}
Email: {lead.email}
Teléfono: {lead.telefono}
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["dbrasan@gmail.com"],
                fail_silently=False,
            )

            mensaje = "Gracias. Te contactaremos pronto."
            form = LeadForm()

    else:
        form = LeadForm()

    return render(request, 'landing/home.html', {
        'form': form,
        'mensaje': mensaje
    })


def lista_leads(request):
    clinica_actual = request.session.get('clinica_actual')

    leads = Lead.objects.all().order_by('-fecha_registro')

    return render(request, 'landing/lista_leads.html', {
        'leads': leads
    })