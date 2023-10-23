
import datetime
from pyexpat.errors import messages
from django.http.response import JsonResponse
from django.db.models import Sum
from django.shortcuts import redirect, get_object_or_404, render
from .models import demanda_diarias, InfoMed, StockMed, AdminMed, SaldoAnterior, indi_mensuales, admin_indi, indi_mensuales, DemandaReal
from .forms import DateRangeForm, InfoMedForm, MedicamentoForm, DemandaForm, admin_indiForm, DateRangeForms
from datetime import date, timedelta
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import authenticate, login
from django.db.models.functions import Coalesce
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# Create your views here.

#---------vista para inicio de sesion----------
#def login(request):
    #return render(request, 'appWeb/login.html')

def crear(request):
    return render(request, 'appWeb/crear_user.html')


#---------vista para el menuprincipal----------
def menuprincipal_(request):
    return render(request, 'appWeb/menuprincipal.html')

#def redirect_to_menu(request):
    return redirect('menuprincipal')


@login_required
def login_view(request):
     if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('menuprincipal')
     else:
         form = AuthenticationForm()  # Redirige a la página de inicio
     return render(request, 'appWeb/login.html', {'form': form})
     
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  # Asegúrate de usar la contraseña del formulario
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Llama a login con el objeto de usuario autenticado
                return redirect('login')  # Cambia 'dashboard' a la URL deseada
    else:
        form = UserCreationForm()
    return render(request, 'appWeb/signup.html', {'form': form})



#--------------------------------------MEDICAMENTOS--------------------------------------------

#---------vista para ingresar la informacion del medicamento.----------
def InfoMed_(request):
    data = {
        'form': InfoMedForm()
    }
    if request.method == 'POST':
        formMed = InfoMedForm(data=request.POST)
        if formMed.is_valid():
            formMed.save()
            data["mensaje"]= "Medicamento ingresado"
        else:
            data["form"] = formMed
    return render(request, 'appWeb/control_medicamentos/InfoMed.html', data)


#---------vista para buscar medicamentos antes de ingresar las entregas y no entregas----------
def buscar_medicamento(request):
    medicamentos = []

    if request.method == 'POST':
        medicamento_form = MedicamentoForm(request.POST)
        if medicamento_form.is_valid():
            nombre_medicamento = medicamento_form.cleaned_data['nombre']
            medicamentos = InfoMed.objects.filter(nombre__icontains=nombre_medicamento)
    else:
        medicamento_form = MedicamentoForm()
    
    return render(request, 'appWeb/control_medicamentos/buscar_medicamento.html', {'medicamento_form': medicamento_form, 'medicamentos':medicamentos})


#---------vista para ingresar demanda diaria real. entregados, no entregados----------
def ingresar_datos(request, medicamento_codigo):
    medicamento = get_object_or_404(InfoMed, pk=medicamento_codigo)
    demanda_form = DemandaForm()

    if request.method == 'POST':
        demanda_form = DemandaForm(request.POST)
        if demanda_form.is_valid():
            demanda = demanda_form.save(commit=False)
            demanda.codigo = medicamento

            # se obtiene la cantidad entregada desde el formulario
            cantidad_entregada = demanda.entregado

            # se actualiza el campo de stock en StockMed
            stock_medicamento = StockMed.objects.get(codigo=medicamento)
            stock_medicamento.stock -= cantidad_entregada
            stock_medicamento.save()

            demanda.save()
            return redirect('buscar_medicamento')  # Redirige a la página de búsqueda
        
    return render(request, 'appWeb/control_medicamentos/ingresar_datos.html', {'medicamento': medicamento, 'demanda_form': demanda_form})



#-----------listas json-------------------
def list_demandadiaria_(_request):
    demanda = list(demanda_diarias.objects.values())
    data = {'demanda': demanda}
    return JsonResponse(data)

def listmensual(_request):
    mensual = list(demanda_diarias.objects.values())
    data = {'mensual': mensual}
    return JsonResponse(data)


#-----------Vista para agregar entradas de nivel superior-------
def entrada_superior_(request):
    medicamentos = []
    medicamento_seleccionado = None

    if request.method == "POST":
        #búsqueda por nombre
        nombre_busqueda = request.POST.get("nombre_busqueda", "")
        medicamentos = InfoMed.objects.filter(nombre__icontains=nombre_busqueda)

        #actualización de la cantidad
        medicamento_id = request.POST.get("medicamento_id")
        cantidad_nueva = request.POST.get("cantidad_nueva")
        fecha = request.POST.get("fecha")
        

        if medicamento_id and cantidad_nueva:
            medicamento_seleccionado = InfoMed.objects.get(pk=medicamento_id)
            cantidad_nueva = int(cantidad_nueva)

            # Verificar si existe una entrada en stockMed para el medicamento
            stock_medicamento, created = StockMed.objects.get_or_create(codigo=medicamento_seleccionado, defaults={'stock': 0})

            # Actualizar el campo stock en stockMed
            stock_medicamento.stock += cantidad_nueva
            stock_medicamento.save()

            # Crear un nuevo registro en AdminMed para el ingreso
            nuevo_registro_admin_med = AdminMed(
                codigo=medicamento_seleccionado,
                cantidad=cantidad_nueva,
                fecha =fecha
            )
            nuevo_registro_admin_med.save()

            return redirect("entrada_superior_")  # Redirigir para evitar reenvíos del formulario

    return render(request, "appWeb/control_medicamentos/entrada_superior.html", {
        "medicamentos": medicamentos,
        "medicamento_seleccionado": medicamento_seleccionado,
    })

#---------------------------------------INDICADORES------------------------------

#---------vista para ingresar la informacion de los indicadores.----------
def admin_indi_(request):
    data = {
        'form': admin_indiForm()
    }
    if request.method == 'POST':
        formIndi = admin_indiForm(data=request.POST)
        if formIndi.is_valid():
            formIndi.save()
            data["mensaje"]= "Indicador ingresado"
        else:
            data["form"] = formIndi
    return render(request, 'appWeb/control_indicadores/admin_indi.html', data)


#--------------vista para guardar la informacion de indicadores de auxiliares-------------
def guardar_indicadores(request):

    indicadores = admin_indi.objects.all()
    if request.method == 'POST':
        # Procesa el formulario y guarda los datos en indi_mensuales
        for indicador in indicadores:
            meta_mes = request.POST.get(f'indicador_{indicador.codigo}')
            if meta_mes is not None:
                indi_mensual = indi_mensuales(codigo=indicador, metaMes=meta_mes, fecha=timezone.now())
                indi_mensual.save()
    return render(request, 'appWeb/control_indicadores/ingresoindimensual.html', {'indicadores': indicadores})



#-------------------------------------REPORTERIA-----------------------------------

#-----------Vista para el menu de reportes-------
def menurepo_(request):
    return render(request, 'appWeb/reporteria/menurepo.html')


#---------vista de informe principal de demanda diaria real ----------
def demanda_diaria_(request):

    if request.method == 'POST':
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']

        # Realiza la consulta SQL
        entregas = demanda_diarias.objects.filter(
            fecha__range=[fecha_inicio, fecha_fin]
        ).values('codigo_id','codigo__nombre','codigo__concentracion','codigo__presentacion').annotate(
            suma_entregado=Sum('entregado'),
            suma_no_entregado=Sum('no_entregado')
           
        )
    
        return render(request, 'appWeb/reporteria/demanda_diaria.html', {'entregas': entregas})

    return render(request, 'appWeb/reporteria/demanda_diaria.html')


#-----Vista para informe BRES------
def informe_bres(request):
    form = DateRangeForms() 
    fecha_inicio= None
    fecha_fin =  None # Utiliza tu formulario personalizado para las fechas
    if request.method == 'POST':
        # Validar el formulario
        form = DateRangeForms(request.POST)
        if form.is_valid():
            fecha_inicio = request.POST['fecha_inicio']
            fecha_fin = request.POST['fecha_fin']
        # logica para cada medicamento
        medicamentos = InfoMed.objects.all()
        informe_bres_data = []
        demanda_real_meses = []

        for medicamento in medicamentos:
            # Obtener el "SALDO ANTERIOR" del mes pasado
        
                # Asegúrate de que fecha_inicio sea un objeto datetime
              
                if fecha_inicio is not None and isinstance(fecha_inicio, datetime):
                    # Realiza la consulta de la base de datos
                    saldo_anterior_obj = SaldoAnterior.objects.filter(codigo=medicamento, fecha__range=[fecha_inicio, fecha_fin]).order_by('-fecha').first()
                    saldo_anterior_seleccionado = saldo_anterior_obj.saldoAnterior if saldo_anterior_obj else 0

                    # Obtener el "ENTRADAS DE NIVEL SUPERIOR" dentro del rango de fechas seleccionado
                    entrada_nivel_superior = AdminMed.objects.filter(
                        codigo=medicamento,
                        fecha__gte=fecha_inicio,
                        fecha__lte=fecha_fin
                    ).aggregate(Sum('cantidad'))['cantidad__sum'] or 0
                else:
                    # Maneja el caso en el que fecha_inicio no sea una fecha válida
                    # Puedes establecer valores predeterminados o manejarlo de acuerdo a tus necesidades
                    saldo_anterior_seleccionado = 0
                    entrada_nivel_superior = 0




             # Obtener el "ENTREGADO A USUARIO" y "NO ENTREGADO A USUARIO" dentro del rango de fechas seleccionado
                entregado_usuario = demanda_diarias.objects.filter(
                    codigo=medicamento,
                    fecha__range=[fecha_inicio, fecha_fin]
                ).aggregate(Sum('entregado'))['entregado__sum'] or 0
                no_entregado_usuario = demanda_diarias.objects.filter(
                    codigo=medicamento,
                    fecha__range=[fecha_inicio, fecha_fin]
                ).aggregate(Sum('no_entregado'))['no_entregado__sum'] or 0

              # Obtener la "DEMANDA REAL" del medicamento para el rango de fechas seleccionado
            
                if fecha_inicio is not None and isinstance(fecha_inicio, datetime) and isinstance(fecha_fin, datetime):
                    demanda_real_obj = DemandaReal.objects.filter(
                        codigo=medicamento,
                        fecha__gte=fecha_inicio,
                        fecha__lte=fecha_fin
                    ).aggregate(Sum('demanda_real'))['demanda_real__sum'] or 0
                else:
                    demanda_real_obj = 0  
                                    
            # Calcular el "SALDO MES SIGUIENTE"
                saldo_mes_siguiente = saldo_anterior_seleccionado + entrada_nivel_superior - entregado_usuario

            # Obtener la "EXISTENCIA FISICA EN BODEGA" del medicamento
                existencia_en_bodega = StockMed.objects.get(codigo=medicamento).stock
            
            # Calcular el "PROMEDIO MENSUAL DE DEMANDA REAL"
                if fecha_inicio and fecha_fin:
                    
                # Realiza la consulta de la base de datos
                    demanda_real_meses = DemandaReal.objects.filter(
                        codigo=medicamento,
                        fecha__gte=fecha_inicio,
                        fecha__lte=fecha_fin
                ).values_list('demanda_real', flat=True)

            # Calcula el promedio mensual dividiendo la suma de la demanda real entre la cantidad de meses en el rango
                total_demanda_real = sum(demanda_real_meses)
                cantidad_meses = len(demanda_real_meses)
                if cantidad_meses != 0:
                        demanda_real_promedio = total_demanda_real / cantidad_meses
                else:
                        demanda_real_promedio = 0

                #Calcular MESES DE EXISTENCIA DIPONIBLE
                # Verificar si demanda_real_promedio no es cero antes de realizar la división
                if demanda_real_promedio != 0:
                    meses_en_existencia_disponible = saldo_mes_siguiente / demanda_real_promedio
                else:
                    meses_en_existencia_disponible = 0  # Valor predeterminado si demanda_real_promedio es cero

                #CANTIDAD MAXIMA
                cantidad_maxima = demanda_real_promedio * 3

                #CANTIDAD A SOLICITAR
                cantidad_a_solicitar = saldo_mes_siguiente - cantidad_maxima

                #Obtener CANTIDAD RECIBIDA si hay.
               
                cantidad_recibida = 0 

                informe_bres_data.append({
                    'medicamento': medicamento,
                    'cantidad_mes_pasado': saldo_anterior_seleccionado,
                    'entrada_nivel_superior': entrada_nivel_superior,
                    'entregado_usuario': entregado_usuario,
                    'no_entregado_usuario': no_entregado_usuario,
                    'demanda_real': demanda_real_obj,
                    'saldo_mes_siguiente': saldo_mes_siguiente,
                    'existencia_en_bodega': existencia_en_bodega,
                    'demanda_real_promedio': demanda_real_meses,
                    'meses_en_existencia_disponible' : meses_en_existencia_disponible,
                    'cantidad_maxima' : cantidad_maxima,
                    'cantidad_a_solicitar' : cantidad_a_solicitar,
                    'cantidad_recibida' : cantidad_recibida
                })
        return render(request, 'appWeb/reporteria/informe_mensual.html', {'informe_bres_data': informe_bres_data, 'form': form,})

    return render(request, 'appWeb/reporteria/informe_mensual.html', {'form': form})

        
#---------------vista de informe de indicadores mensuales--------------
def mostrar_indicadores(request):
    indicadores = admin_indi.objects.all()

    # Calcular el acumulado para cada indicador
    for indicador in indicadores:
        if Decimal(indicador.metaIndi) >= 1:
            acumulado = indi_mensuales.objects.filter(
                codigo=indicador,
                fecha__month__in=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            ).aggregate(acumulado=Coalesce(Sum('metaMes'), 0) + 100)

            indicador.acumulado = acumulado['acumulado'] / Decimal(indicador.metaIndi)
       # Calcular el valor "Ideal" si el acumulado no es None
            ideal_count = indi_mensuales.objects.filter(
                codigo=indicador,
                fecha__month__in=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            ).count()

            if indicador.acumulado is not None:
                indicador.ideal = (100 / 12) * ideal_count
            else:
                indicador.ideal = None
        else:
            indicador.acumulado = None
            indicador.ideal = None

    mensuales = indi_mensuales.objects.all()
    return render(request, 'appWeb/reporteria/mostrar_indicadores.html', {'indicadores': indicadores, 'mensuales': mensuales})


#------------vista para visualizar el stock------------------
def informe_productos(request):
    productos = InfoMed.objects.all()

    stock_data = []

    for producto in productos:
        stock_obj = StockMed.objects.get(codigo=producto)
        stock_data.append({
            'nombre': producto.nombre,
            'concentracion': producto.concentracion,
            'presentacion': producto.presentacion,
            'stock': stock_obj.stock
        })
    return render(request, 'appWeb/reporteria/informe_productos.html', {'productos': stock_data})


#----------vista de todas las demandas diarias-----------------
def resumen_mensual_actualizar(request):
    entregas_meses = demanda_diarias.objects.values(
        'codigo__nombre', 'fecha__year', 'fecha__month'
    ).annotate(
        total_entregado=Sum('entregado'),
        total_no_entregado=Sum('no_entregado')
    ).order_by('fecha__year', 'fecha__month')

    for entrega_mes in entregas_meses:
        codigo = InfoMed.objects.get(nombre=entrega_mes['codigo__nombre'])
        fecha = date(entrega_mes['fecha__year'], entrega_mes['fecha__month'], 1)
        demanda_total = entrega_mes['total_entregado'] + entrega_mes['total_no_entregado']
        # Verificar si ya existe una entrada para la fecha y el medicamento, y actualizarla si es necesario
        demanda_real, created = DemandaReal.objects.get_or_create(codigo=codigo, fecha=fecha)
        demanda_real.demanda_real = demanda_total
        demanda_real.save()

    return render(request, 'appWeb/reporteria/resumen_mensualddr.html', {'entregas_meses': entregas_meses})

