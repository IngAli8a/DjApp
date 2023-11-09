from django.urls import path, include
from .import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', auth_views.LoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('menuprincipal/', views.menuprincipal_, name="menuprincipal"),
    #path('redirect_to_menu/', views.redirect_to_menu, name='redirect_to_menu'),
    path('menuprincipal/InfoMed/', views.InfoMed_, name="InfoMed"),
    path('list_demandadiaria/', views.list_demandadiaria_, name="list_demandadiaria" ),
    path('menuprincipal/admin_indi/', views.admin_indi_, name="admin_indi"),
    path('menuprincipal/buscar_medicamento/', views.buscar_medicamento, name='buscar_medicamento'),
    path('ingresar_datos/<int:medicamento_codigo>/', views.ingresar_datos, name='ingresar_datos'),
    path('menuprincipal/menurepo/mostrar_indicadores/', views.mostrar_indicadores, name = 'mostrar_indicadores'),
    path('listmensual/', views.listmensual, name="listmensual" ),
    path('menuprincipal/menurepo/', views.menurepo_, name="menurepo"),
     path('menuprincipal/menurepo/demanda_diaria/', views.demanda_diaria_, name='demanda_diaria'),
    path('menuprincipal/InfoMed/entrada_superior/', views.entrada_superior_, name="entrada_superior_"),
    path('menuprincipal/menurepo/informe_mensual/', views.informe_bres, name="informe_mensual"),
    path('menuprincipal/guardar_indicadores/', views.guardar_indicadores, name="guardar_indicadores"),
    #path('registro/', views.registro, name="registro")
    path('menuprincipal/menurepo/informe_productos/', views.informe_productos, name="informe_productos"),
    path('menuprincipal/crear_user/', views.crear, name="crear_user"),
    path('menuprincipal/menurepo/calculate/', views.calculate_data, name='calculate'),
    path('borrar_datos/', views.borrar_datos, name='borrar_datos')
]