from django.urls import path 
from . import views 
from django.views.decorators.csrf import csrf_exempt, csrf_protect

urlpatterns = [


    path('', views.home_view, name='home'),
    path('index', views.index, name='index'),
    path('financiero', views.financiero_view, name='financiero'),
    path('historial-pagos/<int:id>', views.historial_pagos, name='historial-pagos'),
    path('add-expense', views.add_expense, name='add-expenses'),
    path('add-pago/<int:id>', views.add_pago, name='add-pago'),
    path('edit-expense/<int:id>', views.expense_edit, name='expense-edit'),
    path('expense-finanzas/<int:id>', views.expense_finanzas, name='expense-finanzas'),
    path('expense-comercial-map/<int:id>', views.expense_comercial_map, name='expense-comercial-map'),
    path('expense-domicilio-map/<int:id>', views.expense_domicilio_map, name='expense-domicilio-map'),
    path('actualizar_coordenadas/<int:id>', views.actualizar_coordenadas, name="actualizar-coordenadas"),
    path('expense-delete/<int:id>', views.delete_expense, name='expense-delete'),
    path('get_ciudades/', views.get_ciudades, name='get_ciudades'),
    path('search-expenses', csrf_exempt(views.search_expenses), name="search_expenses"),
    path('search-finanza', csrf_exempt(views.search_finanza), name="search_finanza"),
    path('expense_linea_negocio_summary', views.expense_linea_negocio_summary,
         name="expense_linea_negocio_summary"),
    path('stats', views.stats_view,name="stats"),
    path('home', views.home_view,name="home"),
    path('reports', views.reports_view,name="reports"),
    path('export_csv', views.export_csv,name="export-csv"),
    path('export_excel', views.export_excel,name="export-excel"),
    path('export_pdf', views.export_pdf,name="export-pdf"),
]
