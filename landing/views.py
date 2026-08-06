from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .forms import LeadForm
from .models import Lead
import requests


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    print("IP REAL:", ip)

    return ip

def get_city(ip):

    if ip in ['127.0.0.1', '::1']:
        return "Localhost"

    try:
        r = requests.get(
            f"https://ipapi.co/{ip}/json/",
            timeout=5
        )

        print("STATUS:", r.status_code)
        print("DATA:", r.text)

        if r.status_code != 200:
            return "Ubicación no disponible"

        data = r.json()

        ciudad = data.get("city")
        region = data.get("region")
        pais = data.get("country_name")

        partes = [p for p in [ciudad, region, pais] if p]

        if partes:
            return ", ".join(partes)

        return "Ubicación no disponible"

    except Exception as e:
        print("ERROR GEO:", e)
        return "Ubicación no disponible"


def home(request):

    mensaje = None

    if not request.session.get('visit_logged') :

        request.session['visit_logged'] = True

        ip = get_client_ip(request)

        try:
            ciudad = get_city(ip)
        except:
            ciudad = "Ubicación no disponible"

        try:
            send_mail(
                subject="Nueva visita a FreshStart",
                message=f"""
    Nueva visita detectada

    IP: {ip}
    Ubicación: {ciudad}
    Ruta: {request.path}
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["info@freshstart.mx"],
                fail_silently=False,
            )

            print("VISITA REGISTRADA")

        except Exception as e:
            print("ERROR VISITA:", e)

    # ===========================
    # FORMULARIO DEMO
    # ===========================
    if request.method == 'POST':

        form = LeadForm(request.POST)

        if form.is_valid():

            lead = form.save()

            ip = get_client_ip(request)
            ciudad = get_city(ip)

            try:

                # Correo al prospecto
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

                # Correo interno
                send_mail(
                    subject="Nuevo Lead FreshStart",
                    message=f"""
Nuevo lead registrado

Nombre: {lead.nombre}
Clínica: {lead.clinica}
Email: {lead.email}
Teléfono: {lead.telefono}

IP: {ip}
Ubicación: {ciudad}
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=["info@freshstart.mx"],
                    fail_silently=False,
                )

                print("EMAIL ENVIADO")

                mensaje = "Gracias. Te contactaremos pronto."

            except Exception as e:
                print("ERROR SMTP:", e)
                mensaje = f"Error enviando correo: {e}"

            form = LeadForm()

        else:

            print(form.errors)

            if 'email' in form.errors:
                mensaje = "Este correo ya solicitó una demo anteriormente."
            else:
                mensaje = "Verifica tus datos e inténtalo nuevamente."

    else:
        form = LeadForm()

    return render(request, 'landing/home.html', {
        'form': form,
        'mensaje': mensaje
    })


def lista_leads(request):

    leads = Lead.objects.all().order_by('-fecha_registro')

    return render(request, 'landing/lista_leads.html', {
        'leads': leads
    })