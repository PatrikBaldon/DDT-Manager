from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Mittente, SedeMittente, Destinatario, Destinazione, Vettore, Autista, TargaVettore, Articolo, 
    DDT, DDTRiga, Configurazione, CausaleTrasporto
)


class SedeMittenteInline(admin.TabularInline):
    model = SedeMittente
    extra = 1


@admin.register(Mittente)
class MittenteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'piva', 'telefono', 'email', 'logo_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['nome', 'piva', 'cf']
    readonly_fields = ['created_at', 'updated_at', 'logo_preview']
    inlines = [SedeMittenteInline]
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.logo.url)
        return "Nessun logo"
    logo_preview.short_description = "Logo"


@admin.register(SedeMittente)
class SedeMittenteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'mittente', 'citta', 'provincia', 'codice_stalla', 'sede_legale', 'attiva']
    list_filter = ['sede_legale', 'attiva', 'provincia', 'created_at']
    search_fields = ['nome', 'mittente__nome', 'citta', 'codice_stalla']
    readonly_fields = ['created_at', 'updated_at']


class DestinazioneInline(admin.TabularInline):
    model = Destinazione
    extra = 1


@admin.register(Destinatario)
class DestinatarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'citta', 'provincia', 'piva', 'created_at']
    list_filter = ['provincia', 'created_at']
    search_fields = ['nome', 'citta', 'piva', 'cf']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [DestinazioneInline]


class TargaVettoreInline(admin.TabularInline):
    model = TargaVettore
    extra = 1


@admin.register(Vettore)
class VettoreAdmin(admin.ModelAdmin):
    list_display = ['nome', 'telefono', 'autorizzazione_animali_vivi', 'licenza_bdn', 'created_at']
    list_filter = ['provincia', 'autorizzazione_animali_vivi', 'created_at']
    search_fields = ['nome', 'piva', 'cf', 'licenza_bdn']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [TargaVettoreInline]


@admin.register(Autista)
class AutistaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cognome', 'vettore', 'patente', 'attivo', 'created_at']
    list_filter = ['attivo', 'vettore', 'created_at']
    search_fields = ['nome', 'cognome', 'patente', 'vettore__nome']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TargaVettore)
class TargaVettoreAdmin(admin.ModelAdmin):
    list_display = ['targa', 'vettore', 'tipo_veicolo', 'attiva', 'created_at']
    list_filter = ['attiva', 'tipo_veicolo', 'created_at']
    search_fields = ['targa', 'vettore__nome', 'tipo_veicolo']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Articolo)
class ArticoloAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'um', 'prezzo_unitario', 'created_at']
    list_filter = ['categoria', 'um', 'created_at']
    search_fields = ['nome', 'categoria']
    readonly_fields = ['created_at', 'updated_at']


class DDTRigaInline(admin.TabularInline):
    model = DDTRiga
    extra = 1
    fields = ['ordine', 'articolo', 'quantita', 'descrizione']


@admin.register(DDT)
class DDTAdmin(admin.ModelAdmin):
    list_display = ['numero', 'data_documento', 'mittente', 'destinatario', 'causale_trasporto', 'vettore', 'autista', 'targa_vettore', 'targa_vettore_2', 'created_at']
    list_filter = ['data_documento', 'causale_trasporto', 'mittente', 'destinatario', 'created_at']
    search_fields = ['numero', 'mittente__nome', 'destinatario__nome']
    readonly_fields = ['created_at', 'updated_at', 'totale_quantita', 'totale_valore']
    inlines = [DDTRigaInline]
    date_hierarchy = 'data_documento'
    
    fieldsets = (
        ('Informazioni Generali', {
            'fields': ('numero', 'data_documento', 'causale_trasporto')
        }),
        ('Mittente e Destinatario', {
            'fields': ('mittente', 'sede_mittente', 'destinatario', 'destinazione', 'luogo_destinazione')
        }),
        ('Trasporto', {
            'fields': ('trasporto_mezzo', 'data_ritiro', 'vettore', 'autista', 'targa_vettore', 'targa_vettore_2')
        }),
        ('Note e Totali', {
            'fields': ('annotazioni', 'totale_quantita', 'totale_valore')
        }),
        ('Metadati', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(CausaleTrasporto)
class CausaleTrasportoAdmin(admin.ModelAdmin):
    list_display = ['codice', 'descrizione', 'attiva', 'created_at']
    list_filter = ['attiva', 'created_at']
    search_fields = ['codice', 'descrizione']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Configurazione)
class ConfigurazioneAdmin(admin.ModelAdmin):
    list_display = ['chiave', 'valore', 'descrizione', 'updated_at']
    search_fields = ['chiave', 'descrizione']
    readonly_fields = ['created_at', 'updated_at']

