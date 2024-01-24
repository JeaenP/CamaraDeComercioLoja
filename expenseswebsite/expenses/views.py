import datetime
from datetime import timedelta
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from expenses.models import Expense, Lineas, TipoSocio, Genero, Comite, Estado, EstadoCivil, Aseguradora, Recaudador, Pago, Nacionalidad, Clase
from django.http import JsonResponse
from django.core.paginator import Paginator
import json 
from django.http import JsonResponse, HttpResponse
import folium
from geopy.geocoders import GoogleV3
from django import forms
import csv
import xlwt
from django.template.loader import render_to_string
import tempfile
from django.db.models import Sum
from reportlab.pdfgen import canvas
from django.template import Template, Context
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
from xhtml2pdf import pisa
import datetime
from django.template.loader import get_template
from django.db.models import Count
# Create your views here.

  

def search_finanza(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            cedula_ruc__istartswith=search_str) 
        
        data = expenses.values()
        
        page_size = 7
        paginated_data = data[:page_size]
        return JsonResponse(list(paginated_data), safe=False)
    

def search_expenses(request):
    if request.method == 'POST':
        search_data = json.loads(request.body)
        search_str = search_data.get('searchText')
        search_month = search_data.get('searchMonth')
        search_vigencia = search_data.get('searchVigencia')
        search_estado = search_data.get('searchEstado')
        search_tipo = search_data.get('searchTipo')
        search_edad = search_data.get('searchEdad')
        expenses = Expense.objects.filter(
            Q(cedula_ruc__istartswith=search_str) |
            Q(nombre__icontains=search_str) |
            Q(representantelegal__icontains=search_str) |
            Q(genero__icontains=search_str) 
        )

        if search_month != '0':
            expenses = expenses.filter(fecha_nacimiento__month=search_month)

        if search_vigencia:
            expenses = expenses.filter(nmesesvigencia__gte=search_vigencia)

        if search_estado != '0':
            expenses = expenses.filter(estado = search_estado)
        
        if search_tipo != '0':
            expenses = expenses.filter(tipo_socio = search_tipo)

        if search_edad:
            search_edad = int(search_edad)
            today = datetime.datetime.now()
            birthdate_filter = today - timedelta(days=search_edad * 365)
            expenses = expenses.filter(fecha_nacimiento__lte=birthdate_filter)

        total_expenses = expenses.count()

        paginator = Paginator(expenses, 50)

        page = request.GET.get('page')
        data = paginator.get_page(page).object_list.values()
        response_data = {
            'total_expenses': total_expenses,
            'expenses_data': list(data),
        }
        return JsonResponse(response_data, safe=False)
    
    
@login_required(login_url = '/authentication/login')
@never_cache
def index(request):
    expensesByPage = 20
    expenses = Expense.objects.all().order_by('-razon_social')
    paginator = Paginator(expenses, expensesByPage)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    totalExpenses = Expense.objects.all().count()
    context= {
        'expenses': expenses,
        'page_obj': page_obj,
        'expensesByPage': expensesByPage,
        'totalExpenses': totalExpenses
    }
    return render(request, 'expenses/index.html', context)

@login_required(login_url = '/authentication/login')
@never_cache
def add_pago(request, id): 
    fecha = datetime.datetime.now().date()
    expense = Expense.objects.get(pk=id)
    nombre = expense.nombre
    context = {
        'values': request.POST,
        'expense': expense,
        'nombre': nombre,
        'fecha': fecha
    }
    if request.method == 'GET':
        return render(request, "expenses/add_pago.html", context)
    if request.method == 'POST':
        monto = request.POST['monto']
        if not monto:
            messages.error(request, 'El monto es obligatorio')
            return render(request, "expenses/add_pago.html", context)
        
        mes = request.POST['mes']
        if not mes:
            messages.error(request, 'El mes del pago es obligatorio')
            return render(request, "expenses/add_pago.html", context)  
        
        

    Pago.objects.create(expense = expense, monto = monto, fecha = fecha, mes = mes)
    messages.success(request, '¡Pago ingresado existosamente!')
    return redirect('historial-pagos', id=expense.id)


@login_required(login_url = '/authentication/login')
@never_cache
def add_expense(request):

    lineas = Lineas.objects.all()
    comites = Comite.objects.all()
    tipossocio = TipoSocio.objects.all()
    generos = Genero.objects.all()
    estados = Estado.objects.all()
    estadoscivil = EstadoCivil.objects.all()
    aseguradoras = Aseguradora.objects.all()
    recaudadores = Recaudador.objects.all()
    nacionalidades = Nacionalidad.objects.all()
    clases = Clase.objects.all()


    context = {
        'values': request.POST,
        'lineas': lineas,
        'comites': comites,
        'tipossocio': tipossocio,
        'generos': generos,
        'estados': estados,
        'estadoscivil': estadoscivil,
        'aseguradoras': aseguradoras,
        'recaudadores': recaudadores,
        'nacionalidades': nacionalidades,
        'clases': clases
    }

    if request.method == 'GET':
        return render(request, "expenses/add_expense.html", context)
    if request.method == 'POST':
        
        cedula_ruc = request.POST['cedula_ruc']
        if not cedula_ruc:
            messages.error(request, 'La cedula/RUC es obligatoria')
            return render(request, "expenses/add_expense.html", context)
        
        fecha_nacimiento = request.POST['fecha_nacimiento']
        if not fecha_nacimiento:
            messages.error(request, 'La fecha de nacimiento es obligatoria')
            return render(request, "expenses/add_expense.html", context)       
        
        telefonos = request.POST['telefonos']

        pertenece_comite = request.POST['pertenece_comite']
        if not pertenece_comite:
            messages.error(request, 'Seleccione si pertenece a Comité')
            return render(request, "expenses/add_expense.html", context) 

        dir_comercial = request.POST['dir_comercial']
        if not dir_comercial:
            messages.error(request, 'La dirección comercial es obligatoria')
            return render(request, "expenses/add_expense.html", context)

        tipo_socio = request.POST['tipo_socio']
        if not tipo_socio:
            messages.error(request, 'El tipo de socio es obligatorio')
            return render(request, "expenses/add_expense.html", context) 

        genero = request.POST['genero']
        if not genero:
            messages.error(request, 'El género del socio es obligatorio')
            return render(request, "expenses/add_expense.html", context)

        estado = request.POST['estado']
        if not estado:
            messages.error(request, 'El estado es obligatorio')
            return render(request, "expenses/add_expense.html", context) 

        nacionalidad = request.POST['nacionalidad']
        if not nacionalidad:
            messages.error(request, 'La nacionalidad es obligatoria')
            return render(request, "expenses/add_expense.html", context) 

        movil = request.POST['movil']
        if not movil:
            messages.error(request, 'El teléfono móvil de contacto es obligatorio')
            return render(request, "expenses/add_expense.html", context)

        nombre = request.POST['nombre']
        if not nombre:
            messages.error(request, 'El nombre es obligatorio')
            return render(request, "expenses/add_expense.html", context)  

        conyuge = request.POST['conyuge'] 

        razon_social = request.POST['razon_social']
        if not razon_social:
            messages.error(request, 'La razón social es obligatorio')
            return render(request, "expenses/add_expense.html", context)                            
        
        fecha_inscripcion = request.POST['fecha_inscripcion']
        if not fecha_inscripcion:
            messages.error(request, 'La fecha de inscripción es obligatoria')
            return render(request, "expenses/add_expense.html", context)
        
        actividad = request.POST['actividad']
        if not actividad:
            messages.error(request, 'La actividad es obligatoria')
            return render(request, "expenses/add_expense.html", context)
        
        email = request.POST['email']
        if not email:
            messages.error(request, 'La dirección de correo electrónico es obligatoria')
            return render(request, "expenses/add_expense.html", context)

        dir_domicilio = request.POST['dir_domicilio']
        if not dir_domicilio:
            messages.error(request, 'La dirección del domicilio es obligatoria')
            return render(request, "expenses/add_expense.html", context)
        
        recaudador = request.POST['recaudador']
        if not recaudador:
            messages.error(request, 'El nombre del recaudador es obligatorio')
            return render(request, "expenses/add_expense.html", context)
        
        linea_negocio = request.POST['linea_negocio']
        if not linea_negocio:
            messages.error(request, 'La línea del negocio es obligatoria')
            return render(request, "expenses/add_expense.html", context)
        
        aseguradora = request.POST['aseguradora']
        if not aseguradora:
            messages.error(request, 'El nombre de la aseguradora es obligatorio')
            return render(request, "expenses/add_expense.html", context)        

        estado_civil = request.POST['estado_civil']

        nombre_comercial = request.POST['nombre_comercial']
        if not nombre_comercial:
            messages.error(request, 'El nombre comercial es obligatorio')
            return render(request, "expenses/add_expense.html", context) 

        representantelegal = request.POST['representantelegal']

        idclase = request.POST['idclase']
        if not idclase:
            messages.error(request, 'El id de clase es obligatorio')
            return render(request, "expenses/add_expense.html", context) 
    
        if Expense.objects.filter(cedula_ruc=cedula_ruc).exists():
            messages.error(request, 'Cèdula en uso, intente nuevamente')
            return render(request, "expenses/add_expense.html", context)
        

    
        Expense.objects.create(cedula_ruc = cedula_ruc, fecha_nacimiento = fecha_nacimiento, telefonos = telefonos, pertenece_comite = pertenece_comite, dir_comercial = dir_comercial, tipo_socio = tipo_socio, genero = genero, estado = estado, nacionalidad = nacionalidad, movil = movil, nombre = nombre, conyuge = conyuge,
                               razon_social = razon_social, fecha_inscripcion = fecha_inscripcion, actividad = actividad, email = email, dir_domicilio = dir_domicilio, recaudador = recaudador, linea_negocio = linea_negocio, aseguradora = aseguradora, estado_civil = estado_civil, nombre_comercial = nombre_comercial, representantelegal = representantelegal, idclase = idclase)
        messages.success(request, '¡Socio ingresado existosamente!')
        return redirect('index')

    


@login_required(login_url = '/authentication/login')
@never_cache
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    lineas = Lineas.objects.all()
    comites = Comite.objects.all()
    tipossocio = TipoSocio.objects.all()
    generos = Genero.objects.all()
    estados = Estado.objects.all()
    estadoscivil = EstadoCivil.objects.all()
    aseguradoras = Aseguradora.objects.all()
    recaudadores = Recaudador.objects.all()
    nacionalidades = Nacionalidad.objects.all()
    clases = Clase.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'lineas': lineas,
        'comites': comites,
        'tipossocio': tipossocio,
        'generos': generos,
        'estados': estados,
        'estadoscivil': estadoscivil,
        'aseguradoras': aseguradoras,
        'recaudadores': recaudadores,
        'nacionalidades': nacionalidades,
        'clases': clases,
        'pertenece_comite': request.POST.get('pertenece_comite', ''),
    }
    if request.method == 'GET':  
        return render(request, 'expenses/edit-expense.html', context)
    
    if request.method == 'POST': 
        cedula_ruc = request.POST['cedula_ruc']
        if not cedula_ruc:
            messages.error(request, 'La cedula/RUC es obligatoria')
            return render(request, "expenses/edit-expense.html", context)
        
        fecha_nacimiento = request.POST['fecha_nacimiento']
        if not fecha_nacimiento:
            messages.error(request, 'La fecha de nacimiento es obligatoria')
            return render(request, "expenses/edit-expense.html", context)       
        
        telefonos = request.POST['telefonos']

        pertenece_comite = request.POST['pertenece_comite']
        if not pertenece_comite:
            messages.error(request, 'Seleccione una opción')
            return render(request, "expenses/edit-expense.html", context) 

        dir_comercial = request.POST['dir_comercial']
        if not dir_comercial:
            messages.error(request, 'La dirección comercial es obligatoria')
            return render(request, "expenses/edit-expense.html", context)

        tipo_socio = request.POST['tipo_socio']
        if not tipo_socio:
            messages.error(request, 'El tipo de socio es obligatorio')
            return render(request, "expenses/edit-expense.html", context) 

        genero = request.POST['genero']
        if not genero:
            messages.error(request, 'El género del socio es obligatorio')
            return render(request, "expenses/edit-expense.html", context)

        estado = request.POST['estado']
        if not estado:
            messages.error(request, 'El estado es obligatorio')
            return render(request, "expenses/edit-expense.html", context) 

        nacionalidad = request.POST['nacionalidad']
        if not nacionalidad:
            messages.error(request, 'La nacionalidad es obligatoria')
            return render(request, "expenses/edit-expense.html", context) 

        movil = request.POST['movil']
        if not movil:
            messages.error(request, 'El teléfono móvil de contacto es obligatorio')
            return render(request, "expenses/edit-expense.html", context)

        nombre = request.POST['nombre']
        if not nombre:
            messages.error(request, 'El nombre es obligatorio')
            return render(request, "expenses/edit-expense.html", context)  

        conyuge = request.POST['conyuge'] 

        razon_social = request.POST['razon_social']
        if not razon_social:
            messages.error(request, 'La razón social es obligatorio')
            return render(request, "expenses/edit-expense.html", context)                            
        
        fecha_inscripcion = request.POST['fecha_inscripcion']
        if not fecha_inscripcion:
            messages.error(request, 'La fecha de inscripción es obligatoria')
            return render(request, "expenses/edit-expense.html", context)
        
        actividad = request.POST['actividad']
        if not actividad:
            messages.error(request, 'La actividad es obligatoria')
            return render(request, "expenses/edit-expense.html", context)
        
        email = request.POST['email']
        if not email:
            messages.error(request, 'La dirección de correo electrónico es obligatoria')
            return render(request, "expenses/edit-expense.html", context)

        dir_domicilio = request.POST['dir_domicilio']
        if not dir_domicilio:
            messages.error(request, 'La dirección del domicilio es obligatoria')
            return render(request, "expenses/edit-expense.html", context)
        
        recaudador = request.POST['recaudador']
        if not recaudador:
            messages.error(request, 'El nombre del recaudador es obligatorio')
            return render(request, "expenses/edit-expense.html", context)
        
        linea_negocio = request.POST['linea_negocio']
        if not linea_negocio:
            messages.error(request, 'La línea del negocio es obligatoria')
            return render(request, "expenses/edit-expense.html", context)
        
        aseguradora = request.POST['aseguradora']
        if not aseguradora:
            messages.error(request, 'El nombre de la aseguradora es obligatorio')
            return render(request, "expenses/edit-expense.html", context)        

        estado_civil = request.POST['estado_civil']

        nombre_comercial = request.POST['nombre_comercial']
        if not nombre_comercial:
            messages.error(request, 'El nombre comercial es obligatorio')
            return render(request, "expenses/edit-expense.html", context) 

        representantelegal = request.POST['representantelegal']

        idclase = request.POST['idclase']
        if not idclase:
            messages.error(request, 'El id de clase es obligatorio')
            return render(request, "expenses/edit-expense.html", context) 
    
        
        
        expense.cedula_ruc = cedula_ruc 
        expense.fecha_nacimiento = fecha_nacimiento
        expense.telefonos = telefonos 
        expense.pertenece_comite = pertenece_comite
        expense.dir_comercial = dir_comercial 
        expense.tipo_socio = tipo_socio
        expense.genero = genero 
        expense.estado = estado
        expense.nacionalidad = nacionalidad
        expense.movil = movil
        expense.nombre = nombre
        expense.conyuge = conyuge
        expense.razon_social = razon_social
        expense.fecha_inscripcion = fecha_inscripcion 
        expense.actividad = actividad
        expense.email = email 
        expense.dir_domicilio = dir_domicilio
        expense.recaudador = recaudador 
        expense.linea_negocio = linea_negocio 
        expense.aseguradora = aseguradora
        expense.estado_civil = estado_civil
        expense.nombre_comercial = nombre_comercial 
        expense.representantelegal = representantelegal
        expense.idclase = idclase
        expense.save()
        
        messages.success(request, 'Socio actualizado existosamente!')
        return redirect('index')
    


def delete_expense(request, id):
    expense=Expense.objects.get(pk = id)
    expense.delete()
    messages.success(request, 'Socio Eliminado')
    return redirect('index')

def get_ciudades(request):
    provincia_nombre = request.GET.get('provincia', None)

    if provincia_nombre:
        provincia = Provincia.objects.get(nombre=provincia_nombre)
        ciudades = Ciudad.objects.filter(provincia=provincia)
        ciudades_data = [{'value': ciudad.nombre, 'label': ciudad.nombre} for ciudad in ciudades]
        return JsonResponse(ciudades_data, safe=False)
    else:
        return JsonResponse({'error': 'Provincia no especificada'}, status=400)


def expense_linea_negocio_summary(request):
    expenses = Expense.objects.all()
    finalrep = {}

    # Obtener el recuento de Expense por tipo_socio
    tipo_socio_counts = expenses.values('tipo_socio').annotate(count=Count('tipo_socio'))

    # Crear un diccionario final con los resultados
    for tipo_socio_count in tipo_socio_counts:
        tipo_socio = tipo_socio_count['tipo_socio']
        count = tipo_socio_count['count']
        finalrep[tipo_socio] = count

    return JsonResponse({'expense_linea_negocio_data': finalrep}, safe=False)


@login_required(login_url = '/authentication/login')
@never_cache
def reports_view(request):
    expensesByPage = 9
    tipo_filter = request.GET.get('tipoFilter')
    if tipo_filter and tipo_filter != '0':
        expenses = expenses.filter(tipo_socio=tipo_filter)
    expenses = Expense.objects.all().order_by('-razon_social')
    paginator = Paginator(expenses, expensesByPage)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    totalExpenses = Expense.objects.all().count()
    context= {
        'expenses': expenses,
        'page_obj': page_obj,
        'expensesByPage': expensesByPage,
        'totalExpenses': totalExpenses
    }
    return render(request, 'expenses/reports.html', context)

def export_csv(request):
    
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename = Socios' + str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Cedula', 'Razon Social', 'Fecha de nacimiento', 'Fecha de inscripcion', 'Nombre comercial', 'Actividad', 'Telefono', 'Email', 'Pertenece comite', 'Direccion comercial', 'Direccion domicilio', 'Numero de meses vigencia', 'Tipo de socio', 'Recaudador', 'Genero', 'Linea de negocio', 'Estado', 'Aseguradora', 'Nacionalidad', 'Estado civil', 'Movil', 'Nombre', 'Representante legal', 'Conyuge' ])
    
    expenses = Expense.objects.all()
    



    for expense in expenses:
        writer.writerow([expense.cedula_ruc, expense.razon_social, expense.fecha_nacimiento,  expense.fecha_inscripcion, expense.nombre_comercial, expense.actividad, expense.telefonos, expense.email, expense.pertenece_comite, expense.dir_comercial, expense.dir_domicilio, expense.nmesesvigencia, expense.tipo_socio, expense.recaudador, expense.genero,  expense.linea_negocio, expense.estado, expense.aseguradora, expense.nacionalidad, expense.estado_civil, expense.movil, expense.nombre, expense.representantelegal, expense.conyuge])

    return response

def export_excel(request):
    response= HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename = Socios' + str(datetime.datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding = 'utf-8')
    ws = wb.add_sheet('Socios')
    row_num = 0 
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Cedula', 'Razon Social', 'Fecha de nacimiento', 'Fecha de inscripcion', 'Nombre comercial', 'Actividad', 'Telefono', 'Email', 'Pertenece comite', 'Direccion comercial', 'Direccion domicilio', 'Numero de meses vigencia', 'Tipo de socio', 'Recaudador', 'Genero', 'Linea de negocio', 'Estado', 'Aseguradora', 'Nacionalidad', 'Estado civil', 'Movil', 'Nombre', 'Representante legal', 'Conyuge' ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = Expense.objects.all().values_list('cedula_ruc', 'razon_social', 'fecha_nacimiento', 'fecha_inscripcion', 'nombre_comercial', 'actividad', 'telefonos', 'email', 'pertenece_comite', 'dir_comercial', 'dir_domicilio', 'nmesesvigencia', 'tipo_socio', 'recaudador', 'genero', 'linea_negocio', 'estado', 'aseguradora', 'nacionalidad', 'estado_civil', 'movil', 'nombre', 'representantelegal', 'conyuge')

    for row in rows: 
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response

def export_pdf(request):
    expenses = Expense.objects.all()
    context = {'expenses': expenses, 'current_date': datetime.datetime.now()}
    template = get_template('expenses/pdf-output.html') 
    html_content = template.render(context)
    pdf_buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=pdf_buffer)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', content_type='text/plain')
    pdf_buffer.seek(0)
    response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=Socios' + str(datetime.datetime.now()) + '.pdf'
    return response

@login_required(login_url = '/authentication/login')
@never_cache
def home_view(request):
    return render(request, 'expenses/home.html')

def financiero_view(request):
    expensesByPage = 7
    expenses = Expense.objects.all().order_by('emitidas')
    paginator = Paginator(expenses, expensesByPage)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    totalCuota = expenses.aggregate(totalCuota=Sum('cuota_total'))
    valortotalcuota = totalCuota['totalCuota']
    context= {
        'expenses': expenses,
        'page_obj': page_obj,
        'expensesByPage': expensesByPage,
        'valortotalcuota': valortotalcuota
    }
    return render(request, 'expenses/financiero.html', context)

def expense_finanzas(request, id):
    expense = Expense.objects.get(pk=id)
    nombre = expense.nombre
    context = {
        'nombre': nombre,
        'expense': expense
    }

    return render(request, 'expenses/expense-finanzas.html', context)

def expense_comercial_map(request, id):
    expense = Expense.objects.get(pk=id)
    nombre = expense.nombre
    context = {
        'nombre': nombre,
        'expense': expense
    }

    return render(request, 'expenses/expense-comercial-map.html', context)

def expense_domicilio_map(request, id):
    expense = Expense.objects.get(pk=id)
    nombre = expense.nombre
    context = {
        'nombre': nombre,
        'expense': expense
    }

    return render(request, 'expenses/expense-domicilio-map.html', context)

def actualizar_coordenadas(request, expense_id):
    if request.method == 'POST':
        latitud = request.POST.get('latitud')
        longitud = request.POST.get('longitud')
        expense = Expense.objects.get(pk=expense_id)
        expense.latitud_domicilio = latitud
        expense.longitud_domicilio = longitud
        expense.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Método no permitido'})

def historial_pagos(request, id):
    expense = Expense.objects.get(pk=id)
    expensesByPage = 12
    expenses = Pago.objects.filter(expense=expense)
    paginator = Paginator(expenses, expensesByPage)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)


    
    nombre = expense.nombre
    pagos = Pago.objects.filter(expense=expense)
    valor = pagos.aggregate(valor=Sum('monto'))
    totalaportado = valor['valor']
    context = {
        'expense': expense,
        'pagos': pagos,
        'totalaportado': totalaportado,
        'nombre': nombre,
        'page_obj': page_obj
    } 
    return render(request, 'expenses/historial-pagos.html', context)


def expense_list(request):
    template_name = 'index.html'

    # Aquí recuperas tus objetos de gastos (ajusta según tu modelo)
    expenses = Expense.objects.all()

    # Aquí puedes agregar las coordenadas a los objetos de gastos
    geolocator = GoogleV3(api_key='AIzaSyAWcxXZO36iZusfLvs4CZeOLplPir5DlvY')
    for expense in expenses:
        if expense.dir_comercial:
            location = geolocator.geocode(expense.dir_comercial)
            if location:
                expense.latitud_comercial = location.latitude
                expense.longitud_comercial = location.longitude

    # Aquí creas los mapas y los agregas al contexto
    maps = []
    for expense in expenses:
        m = folium.Map(location=[expense.latitud_comercial, expense.longitud_comercial], zoom_start=13)
        folium.Marker([expense.latitud_comercial, expense.longitud_comercial], popup=expense.nombre).add_to(m)
        maps.append(m._repr_html_())

    context = {'maps': maps}
    return render(request, template_name, context)


def stats_view(request):
    anio_actual = datetime.datetime.now().year
    mes_actual = datetime.datetime.now().month
    total_socios = Expense.objects.all().count()
    total_socios_oro = Expense.objects.filter(tipo_socio='SOCIO ORO').count()
    oro_socios_75_anios = Expense.objects.filter(tipo_socio='SOCIO ORO', fecha_nacimiento__year=(anio_actual - 75)).count()
    socios_por_tipo = Expense.objects.values('tipo_socio').annotate(cantidad=Count('id'))
    socios_30_anios_aporte_cumplidos = Expense.objects.filter(nmesesaportados__gte=360).count()
    socios_30_anios_aporte_este_anio = Expense.objects.filter(nmesesaportados__gte=349, nmesesaportados__lt=360).count()
    socios_30_anios_aporte_este_mes = Expense.objects.filter(nmesesaportados=359).count()
    socios_por_genero = Expense.objects.values('genero').annotate(cantidad=Count('id'))
    socios_cumplen_75_anios_este_anio = Expense.objects.filter( fecha_nacimiento__year=(anio_actual - 74)).count()
    socios_cumplen_75_anios_este_mes = Expense.objects.filter(fecha_nacimiento__year=(anio_actual - 74), fecha_nacimiento__month=mes_actual).count()
    socios_inscritos_este_anio = Expense.objects.filter(fecha_inscripcion__year=anio_actual).count()
    socios_inscritos_este_mes = Expense.objects.filter(fecha_inscripcion__year=anio_actual, fecha_inscripcion__month=mes_actual).count()


    fecha_hace_un_anio = datetime.datetime.now() - timedelta(days=365)

    # Filtra los pagos realizados en el último año
    pagos_ultimo_anio = Pago.objects.filter(mes__gte=fecha_hace_un_anio)

    print(pagos_ultimo_anio)

    # Crea una lista con el monto de pago para cada mes del último año
    datos_line_chart = [0] * 12  # Inicializa la lista con ceros para cada mes
    for pago in pagos_ultimo_anio:
        mes_pago = pago.mes.month
        datos_line_chart[mes_pago - 1] += pago.monto

    print(datos_line_chart)
    context = {
        'total_socios_oro' : total_socios_oro,
        'oro_socios_75_anios' : oro_socios_75_anios,
        'socios_por_tipo': socios_por_tipo,
        'socios_30_anios_aporte_cumplidos': socios_30_anios_aporte_cumplidos,
        'socios_30_anios_aporte_este_anio': socios_30_anios_aporte_este_anio,
        'socios_30_anios_aporte_este_mes': socios_30_anios_aporte_este_mes,
        'total_socios': total_socios,
        'socios_por_genero': socios_por_genero,
        'socios_cumplen_75_anios_este_anio': socios_cumplen_75_anios_este_anio,
        'socios_cumplen_75_anios_este_mes': socios_cumplen_75_anios_este_mes,
        'socios_inscritos_este_anio': socios_inscritos_este_anio,
        'socios_inscritos_este_mes': socios_inscritos_este_mes,
        'datos_line_chart': datos_line_chart,


    }

    return render(request, 'expenses/stats.html', context)
    

