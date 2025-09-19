from django.urls import path
from . import views

app_name = 'ddt_app'

urlpatterns = [
    # Homepage
    path('', views.home, name='home'),
    
    # DDT CRUD
    path('ddt/create/', views.ddt_create, name='ddt_create'),
    path('ddt/<int:ddt_id>/', views.ddt_detail, name='ddt_detail'),
    path('ddt/<int:ddt_id>/edit/', views.ddt_edit, name='ddt_edit'),
    path('ddt/<int:ddt_id>/delete/', views.ddt_delete, name='ddt_delete'),
    path('ddt/<int:ddt_id>/pdf/', views.ddt_pdf, name='ddt_pdf'),
    
    # API endpoints
    path('api/destinazioni/<int:destinatario_id>/', views.get_destinazioni, name='get_destinazioni'),
    path('api/sedi-mittente/<int:mittente_id>/', views.get_sedi_mittente, name='get_sedi_mittente'),
    path('api/articoli/', views.get_articoli, name='get_articoli'),
    path('api/next-ddt-number/', views.generate_next_ddt_number, name='next_ddt_number'),
    path('api/health/', views.health_check, name='health_check'),
    
    # Destinazioni
    path('destinazioni/<int:destinatario_id>/', views.destinazione_list, name='destinazione_list'),
    path('destinazioni/<int:destinatario_id>/create/', views.destinazione_create, name='destinazione_create'),
    path('destinazioni/edit/<int:destinazione_id>/', views.destinazione_edit, name='destinazione_edit'),
    
    # Formato numerazione DDT
    path('formato-numerazione/', views.formato_numerazione_manage, name='formato_numerazione_manage'),
    
    # Gestione Mittenti
    path('mittenti/', views.mittente_list, name='mittente_list'),
    path('mittenti/create/', views.mittente_create, name='mittente_create'),
    path('destinatari/create/', views.destinatario_create, name='destinatario_create'),
    path('vettori/create/', views.vettore_create, name='vettore_create'),
    path('mittenti/<int:mittente_id>/', views.mittente_detail, name='mittente_detail'),
    path('mittenti/<int:mittente_id>/edit/', views.mittente_edit, name='mittente_edit'),
    path('mittenti/<int:mittente_id>/delete/', views.mittente_delete, name='mittente_delete'),
    path('mittenti/<int:mittente_id>/sede/create/', views.sede_mittente_create, name='sede_mittente_create'),
    path('sede-mittente/<int:sede_id>/edit/', views.sede_mittente_edit, name='sede_mittente_edit'),
    path('sede-mittente/<int:sede_id>/delete/', views.sede_mittente_delete, name='sede_mittente_delete'),
    
    # Gestione Destinatari
    path('destinatari/', views.destinatario_list, name='destinatario_list'),
    path('destinatari/<int:destinatario_id>/', views.destinatario_detail, name='destinatario_detail'),
    path('destinatari/<int:destinatario_id>/edit/', views.destinatario_edit, name='destinatario_edit'),
    path('destinatari/<int:destinatario_id>/delete/', views.destinatario_delete, name='destinatario_delete'),
    
    # Gestione Vettori
    path('vettori/', views.vettore_list, name='vettore_list'),
    path('vettori/<int:vettore_id>/', views.vettore_detail, name='vettore_detail'),
    path('vettori/<int:vettore_id>/edit/', views.vettore_edit, name='vettore_edit'),
    path('vettori/<int:vettore_id>/delete/', views.vettore_delete, name='vettore_delete'),
    path('vettori/<int:vettore_id>/targa/create/', views.targa_vettore_create, name='targa_vettore_create'),
    path('targa-vettore/<int:targa_id>/edit/', views.targa_vettore_edit, name='targa_vettore_edit'),
    path('targa-vettore/<int:targa_id>/delete/', views.targa_vettore_delete, name='targa_vettore_delete'),
    
    # Gestione Causali di Trasporto
    path('causali/', views.causale_list, name='causale_list'),
    path('causali/create/', views.causale_create, name='causale_create'),
    path('causali/<int:causale_id>/', views.causale_detail, name='causale_detail'),
    path('causali/<int:causale_id>/edit/', views.causale_edit, name='causale_edit'),
    path('causali/<int:causale_id>/delete/', views.causale_delete, name='causale_delete'),
]

