from config.wsgi import *
from django.template.loader import get_template
from weasyprint import HTML, CSS
from config import settings


def printTicket():
    template = get_template("ticket.html")
    context = {"name": "Reporte"}
    html_template = template.render(context)
    css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap/css/bootstrap.min.css')
    HTML(string=html_template).write_pdf(target="ticket.pdf", stylesheets=[CSS(css_url)])


printTicket()
