from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
import json
import os
from .models import DDT, DDTRiga, Mittente, SedeMittente, Destinatario, Destinazione, Vettore, TargaVettore, Articolo, FormatoNumerazioneDDT, CausaleTrasporto
from .forms import DDTForm, DDTRigaFormSet, DestinazioneForm, FormatoNumerazioneDDTForm, MittenteForm, DestinatarioForm, VettoreForm, CausaleTrasportoForm
from .pdf_generator import generate_ddt_pdf
from .pdf_generator_advanced import create_ddt_pdf
from .utils import genera_numero_ddt, get_prossimo_numero_ddt


def home(request):
    """Homepage con lista dei DDT"""
    ddt_list = DDT.objects.all().order_by('-data_documento', '-numero')
    
    # Filtri
    search = request.GET.get('search', '')
    if search:
        ddt_list = ddt_list.filter(
            Q(numero__icontains=search) |
            Q(mittente__nome__icontains=search) |
            Q(destinatario__nome__icontains=search)
        )
    
    # Paginazione
    paginator = Paginator(ddt_list, 20)
    page_number = request.GET.get('page')
    ddt_page = paginator.get_page(page_number)
    
    context = {
        'ddt_list': ddt_page,
        'search': search,
    }
    return render(request, 'ddt_app/home.html', context)


def ddt_detail(request, ddt_id):
    """Dettaglio di un DDT"""
    ddt = get_object_or_404(DDT, id=ddt_id)
    context = {
        'ddt': ddt,
    }
    return render(request, 'ddt_app/ddt_detail.html', context)


def ddt_create(request):
    """Creazione di un nuovo DDT"""
    if request.method == 'POST':
        form = DDTForm(request.POST)
        formset = DDTRigaFormSet(request.POST)
        
        # Controlla se si stanno usando note centrali invece di righe articoli
        tipo_articoli = request.POST.get('tipo_articoli', 'righe')
        
        # Se si usano note centrali, non validare il formset delle righe
        if tipo_articoli == 'note':
            if form.is_valid():
                try:
                    ddt = form.save(commit=False)
                    
                    # Popola automaticamente il luogo di destinazione se non specificato
                    if ddt.destinazione and not ddt.luogo_destinazione:
                        luogo_destinazione = ddt.destinazione.nome
                        if ddt.destinazione.codice_stalla:
                            luogo_destinazione += '\nCodice Stalla: ' + ddt.destinazione.codice_stalla
                        luogo_destinazione += '\n' + ddt.destinazione.indirizzo
                        ddt.luogo_destinazione = luogo_destinazione
                    
                    ddt.save()
                    
                    # Non salvare il formset se si usano note centrali
                    
                    messages.success(request, f'DDT {ddt.numero} creato con successo!')
                    return redirect('ddt_app:ddt_detail', ddt_id=ddt.id)
                except Exception as e:
                    messages.error(request, f'Errore durante il salvataggio: {e}')
        else:
            # Validazione normale con formset per righe articoli
            if form.is_valid() and formset.is_valid():
                # Controlla che ci sia almeno una riga compilata
                has_valid_row = False
                for form_data in formset.forms:
                    if form_data.cleaned_data and not form_data.cleaned_data.get('DELETE', False):
                        # Controlla se la riga ha almeno articolo e quantità
                        articolo = form_data.cleaned_data.get('articolo')
                        quantita = form_data.cleaned_data.get('quantita')
                        if articolo and quantita and quantita > 0:
                            has_valid_row = True
                            break
                
                if not has_valid_row:
                    messages.error(request, 'Devi compilare almeno una riga articolo o utilizzare le note centrali.')
                    context = {
                        'form': form,
                        'formset': formset,
                        'title': 'Nuovo DDT',
                    }
                    return render(request, 'ddt_app/ddt_form.html', context)
                
                try:
                    ddt = form.save(commit=False)
                    
                    # Popola automaticamente il luogo di destinazione se non specificato
                    if ddt.destinazione and not ddt.luogo_destinazione:
                        luogo_destinazione = ddt.destinazione.nome
                        if ddt.destinazione.codice_stalla:
                            luogo_destinazione += '\nCodice Stalla: ' + ddt.destinazione.codice_stalla
                        luogo_destinazione += '\n' + ddt.destinazione.indirizzo
                        ddt.luogo_destinazione = luogo_destinazione
                    
                    ddt.save()
                    
                    formset.instance = ddt
                    # Filtra le righe vuote e imposta l'ordine corretto
                    for i, form_data in enumerate(formset.forms):
                        if form_data.cleaned_data and not form_data.cleaned_data.get('DELETE', False):
                            articolo = form_data.cleaned_data.get('articolo')
                            quantita = form_data.cleaned_data.get('quantita')
                            if not articolo or not quantita or quantita <= 0:
                                form_data.cleaned_data['DELETE'] = True
                            else:
                                # Imposta l'ordine in base alla posizione nel formset
                                form_data.cleaned_data['ordine'] = i + 1
                    formset.save()
                    
                    messages.success(request, f'DDT {ddt.numero} creato con successo!')
                    return redirect('ddt_app:ddt_detail', ddt_id=ddt.id)
                except Exception as e:
                    messages.error(request, f'Errore durante il salvataggio: {e}')
    else:
        form = DDTForm()
        # Crea un formset con una riga vuota per iniziare
        formset = DDTRigaFormSet(queryset=DDTRiga.objects.none())
        
        # Genera automaticamente il numero DDT se non specificato
        if not form.initial.get('numero'):
            form.initial['numero'] = get_prossimo_numero_ddt()
        
        # Inizializza il campo destinazione_id
        form.fields['destinazione_id'].initial = ''
    
    context = {
        'form': form,
        'formset': formset,
        'title': 'Nuovo DDT',
    }
    return render(request, 'ddt_app/ddt_form.html', context)


def ddt_edit(request, ddt_id):
    """Modifica di un DDT esistente"""
    ddt = get_object_or_404(DDT, id=ddt_id)
    
    if request.method == 'POST':
        form = DDTForm(request.POST, instance=ddt)
        formset = DDTRigaFormSet(request.POST, instance=ddt)
        
        # Controlla se si stanno usando note centrali invece di righe articoli
        tipo_articoli = request.POST.get('tipo_articoli', 'righe')
        
        # Se si usano note centrali, non validare il formset delle righe
        if tipo_articoli == 'note':
            if form.is_valid():
                ddt = form.save(commit=False)
                
                # Popola automaticamente il luogo di destinazione se non specificato
                if ddt.destinazione and not ddt.luogo_destinazione:
                    luogo_destinazione = ddt.destinazione.nome
                    if ddt.destinazione.codice_stalla:
                        luogo_destinazione += '\nCodice Stalla: ' + ddt.destinazione.codice_stalla
                    luogo_destinazione += '\n' + ddt.destinazione.indirizzo
                    ddt.luogo_destinazione = luogo_destinazione
                
                ddt.save()
                # Non salvare il formset se si usano note centrali
                
                messages.success(request, f'DDT {ddt.numero} aggiornato con successo!')
                return redirect('ddt_app:ddt_detail', ddt_id=ddt.id)
        else:
            # Validazione normale con formset per righe articoli
            if form.is_valid() and formset.is_valid():
                # Controlla che ci sia almeno una riga compilata
                has_valid_row = False
                for form_data in formset.forms:
                    if form_data.cleaned_data and not form_data.cleaned_data.get('DELETE', False):
                        # Controlla se la riga ha almeno articolo e quantità
                        articolo = form_data.cleaned_data.get('articolo')
                        quantita = form_data.cleaned_data.get('quantita')
                        if articolo and quantita and quantita > 0:
                            has_valid_row = True
                            break
                
                if not has_valid_row:
                    messages.error(request, 'Devi compilare almeno una riga articolo o utilizzare le note centrali.')
                    context = {
                        'form': form,
                        'formset': formset,
                        'ddt': ddt,
                        'title': f'Modifica DDT {ddt.numero}',
                    }
                    return render(request, 'ddt_app/ddt_form.html', context)
                
                ddt = form.save(commit=False)
                
                # Popola automaticamente il luogo di destinazione se non specificato
                if ddt.destinazione and not ddt.luogo_destinazione:
                    luogo_destinazione = ddt.destinazione.nome
                    if ddt.destinazione.codice_stalla:
                        luogo_destinazione += '\nCodice Stalla: ' + ddt.destinazione.codice_stalla
                    luogo_destinazione += '\n' + ddt.destinazione.indirizzo
                    ddt.luogo_destinazione = luogo_destinazione
                
                ddt.save()
                formset.instance = ddt
                # Filtra le righe vuote e imposta l'ordine corretto
                for i, form_data in enumerate(formset.forms):
                    if form_data.cleaned_data and not form_data.cleaned_data.get('DELETE', False):
                        articolo = form_data.cleaned_data.get('articolo')
                        quantita = form_data.cleaned_data.get('quantita')
                        if not articolo or not quantita or quantita <= 0:
                            form_data.cleaned_data['DELETE'] = True
                        else:
                            # Imposta l'ordine in base alla posizione nel formset
                            form_data.cleaned_data['ordine'] = i + 1
                formset.save()
                
                messages.success(request, f'DDT {ddt.numero} aggiornato con successo!')
                return redirect('ddt_app:ddt_detail', ddt_id=ddt.id)
    else:
        form = DDTForm(instance=ddt)
        formset = DDTRigaFormSet(instance=ddt, queryset=ddt.righe.all())
        
        # Imposta il valore del campo destinazione_id
        if ddt.destinazione:
            form.fields['destinazione_id'].initial = ddt.destinazione.id
    
    context = {
        'form': form,
        'formset': formset,
        'ddt': ddt,
        'title': f'Modifica DDT {ddt.numero}',
    }
    return render(request, 'ddt_app/ddt_form.html', context)


def ddt_delete(request, ddt_id):
    """Eliminazione di un DDT"""
    ddt = get_object_or_404(DDT, id=ddt_id)
    
    if request.method == 'POST':
        numero = ddt.numero
        ddt.delete()
        messages.success(request, f'DDT {numero} eliminato con successo!')
        return redirect('ddt_app:home')
    
    context = {
        'ddt': ddt,
    }
    return render(request, 'ddt_app/ddt_confirm_delete.html', context)


def ddt_pdf(request, ddt_id):
    """Generazione PDF del DDT"""
    ddt = get_object_or_404(DDT, id=ddt_id)
    
    try:
        # Usa il generatore avanzato che supporta le note centrali
        pdf_path = create_ddt_pdf(ddt_id)
        
        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="DDT_{ddt.numero}.pdf"'
            return response
    except Exception as e:
        messages.error(request, f'Errore nella generazione del PDF: {str(e)}')
        return redirect('ddt_app:ddt_detail', ddt_id=ddt_id)


@csrf_exempt
@require_http_methods(["GET"])
def get_destinazioni(request, destinatario_id):
    """API per ottenere le destinazioni di un destinatario"""
    try:
        destinatario = get_object_or_404(Destinatario, id=destinatario_id)
        destinazioni = destinatario.destinazioni.all()
        
        data = [{
            'id': dest.id,
            'nome': dest.nome,
            'indirizzo': dest.indirizzo,
            'codice_stalla': dest.codice_stalla,
            'note': dest.note
        } for dest in destinazioni]
        
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_articoli(request):
    """API per ottenere la lista degli articoli"""
    try:
        search = request.GET.get('search', '')
        articoli = Articolo.objects.all()
        
        if search:
            articoli = articoli.filter(
                Q(nome__icontains=search) |
                Q(categoria__icontains=search)
            )
        
        data = [{
            'id': art.id,
            'nome': art.nome,
            'categoria': art.categoria,
            'um': art.um,
            'prezzo_unitario': float(art.prezzo_unitario),
            'note': art.note
        } for art in articoli]
        
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def get_sedi_mittente(request, mittente_id):
    """API endpoint per ottenere le sedi di un mittente"""
    try:
        sedi = SedeMittente.objects.filter(mittente_id=mittente_id, attiva=True).order_by('nome')
        data = []
        for sede in sedi:
            data.append({
                'id': sede.id,
                'nome': sede.nome,
                'indirizzo': sede.indirizzo,
                'citta': sede.citta,
                'provincia': sede.provincia,
                'codice_stalla': sede.codice_stalla,
                'sede_legale': sede.sede_legale
            })
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def generate_next_ddt_number(request):
    """Genera il prossimo numero DDT"""
    try:
        next_ddt_number = get_prossimo_numero_ddt()
        return JsonResponse({'numero': next_ddt_number})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def destinazione_create(request, destinatario_id):
    """Creazione di una nuova destinazione per un destinatario"""
    destinatario = get_object_or_404(Destinatario, id=destinatario_id)
    
    if request.method == 'POST':
        form = DestinazioneForm(request.POST)
        if form.is_valid():
            destinazione = form.save(commit=False)
            destinazione.destinatario = destinatario
            destinazione.save()
            
            messages.success(request, f'Destinazione "{destinazione.nome}" creata con successo!')
            return redirect('ddt_app:destinazione_list', destinatario_id=destinatario_id)
    else:
        form = DestinazioneForm()
    
    context = {
        'form': form,
        'destinatario': destinatario,
        'title': f'Nuova Destinazione per {destinatario.nome}',
    }
    return render(request, 'ddt_app/destinazione_form.html', context)


def destinazione_edit(request, destinazione_id):
    """Modifica di una destinazione"""
    destinazione = get_object_or_404(Destinazione, id=destinazione_id)
    
    if request.method == 'POST':
        form = DestinazioneForm(request.POST, instance=destinazione)
        if form.is_valid():
            form.save()
            
            messages.success(request, f'Destinazione "{destinazione.nome}" aggiornata con successo!')
            return redirect('ddt_app:destinazione_list', destinatario_id=destinazione.destinatario.id)
    else:
        form = DestinazioneForm(instance=destinazione)
    
    context = {
        'form': form,
        'destinazione': destinazione,
        'title': f'Modifica Destinazione {destinazione.nome}',
    }
    return render(request, 'ddt_app/destinazione_form.html', context)


def destinazione_list(request, destinatario_id):
    """Lista delle destinazioni di un destinatario"""
    destinatario = get_object_or_404(Destinatario, id=destinatario_id)
    destinazioni = destinatario.destinazioni.all().order_by('nome')
    
    context = {
        'destinatario': destinatario,
        'destinazioni': destinazioni,
    }
    return render(request, 'ddt_app/destinazione_list.html', context)


def formato_numerazione_manage(request):
    """Gestione del formato di numerazione DDT (unico formato)"""
    # Ottieni o crea l'unico formato di numerazione
    formato, created = FormatoNumerazioneDDT.objects.get_or_create(
        defaults={
            'formato': 'aaaa-num',
            'numero_iniziale': 1,
            'lunghezza_numero': 4,
            'attivo': True
        }
    )
    
    if request.method == 'POST':
        form = FormatoNumerazioneDDTForm(request.POST, instance=formato)
        if form.is_valid():
            # Il formato è sempre attivo (unico formato)
            formato = form.save(commit=False)
            formato.attivo = True
            formato.save()
            
            messages.success(request, f'Formato di numerazione "{formato.get_formato_display()}" aggiornato con successo!')
            return redirect('ddt_app:formato_numerazione_manage')
    else:
        form = FormatoNumerazioneDDTForm(instance=formato)
    
    context = {
        'form': form,
        'formato': formato,
        'title': 'Configurazione Formato Numerazione DDT',
    }
    return render(request, 'ddt_app/formato_numerazione_form.html', context)




# ===== GESTIONE MITTENTI =====

def mittente_list(request):
    """Lista dei mittenti"""
    mittenti = Mittente.objects.all().order_by('nome')
    
    # Filtri
    search = request.GET.get('search', '')
    if search:
        mittenti = mittenti.filter(
            Q(nome__icontains=search) |
            Q(piva__icontains=search) |
            Q(cf__icontains=search)
        )
    
    # Paginazione
    paginator = Paginator(mittenti, 10)
    page_number = request.GET.get('page')
    mittenti = paginator.get_page(page_number)
    
    context = {
        'mittenti': mittenti,
        'search': search,
    }
    return render(request, 'ddt_app/mittente_list.html', context)


def mittente_detail(request, mittente_id):
    """Dettaglio mittente con sedi"""
    mittente = get_object_or_404(Mittente, id=mittente_id)
    sedi = mittente.sedi.all().order_by('nome')
    
    context = {
        'mittente': mittente,
        'sedi': sedi,
    }
    return render(request, 'ddt_app/mittente_detail.html', context)


def mittente_edit(request, mittente_id):
    """Modifica mittente"""
    mittente = get_object_or_404(Mittente, id=mittente_id)
    
    if request.method == 'POST':
        form = MittenteForm(request.POST, instance=mittente)
        if form.is_valid():
            form.save()
            messages.success(request, f'Mittente "{mittente.nome}" aggiornato con successo!')
            return redirect('ddt_app:mittente_detail', mittente_id=mittente.id)
    else:
        form = MittenteForm(instance=mittente)
    
    context = {
        'form': form,
        'mittente': mittente,
        'title': f'Modifica Mittente {mittente.nome}',
    }
    return render(request, 'ddt_app/mittente_form.html', context)


def mittente_delete(request, mittente_id):
    """Elimina mittente"""
    mittente = get_object_or_404(Mittente, id=mittente_id)
    
    if request.method == 'POST':
        try:
            nome = mittente.nome
            mittente.delete()
            messages.success(request, f'Mittente "{nome}" eliminato con successo!')
            return redirect('ddt_app:mittente_list')
        except Exception as e:
            if 'ProtectedError' in str(type(e)):
                messages.error(request, f'Impossibile eliminare il mittente "{mittente.nome}" perché è referenziato da DDT esistenti. Elimina prima i DDT associati.')
            else:
                messages.error(request, f'Errore durante l\'eliminazione: {str(e)}')
            return redirect('ddt_app:mittente_detail', mittente_id=mittente.id)
    
    context = {
        'mittente': mittente,
    }
    return render(request, 'ddt_app/mittente_confirm_delete.html', context)


def sede_mittente_create(request, mittente_id):
    """Crea nuova sede per un mittente"""
    mittente = get_object_or_404(Mittente, id=mittente_id)
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        indirizzo = request.POST.get('indirizzo')
        cap = request.POST.get('cap')
        citta = request.POST.get('citta')
        provincia = request.POST.get('provincia')
        codice_stalla = request.POST.get('codice_stalla', '')
        sede_legale = request.POST.get('sede_legale') == 'on'
        attiva = request.POST.get('attiva', 'on') == 'on'
        note = request.POST.get('note', '')
        
        sede = SedeMittente.objects.create(
            mittente=mittente,
            nome=nome,
            indirizzo=indirizzo,
            cap=cap,
            citta=citta,
            provincia=provincia,
            codice_stalla=codice_stalla,
            sede_legale=sede_legale,
            attiva=attiva,
            note=note
        )
        
        messages.success(request, f'Sede "{sede.nome}" creata con successo!')
        return redirect('ddt_app:mittente_detail', mittente_id=mittente.id)
    
    context = {
        'mittente': mittente,
    }
    return render(request, 'ddt_app/sede_mittente_form.html', context)


def sede_mittente_edit(request, sede_id):
    """Modifica sede mittente"""
    sede = get_object_or_404(SedeMittente, id=sede_id)
    
    if request.method == 'POST':
        sede.nome = request.POST.get('nome')
        sede.indirizzo = request.POST.get('indirizzo')
        sede.cap = request.POST.get('cap')
        sede.citta = request.POST.get('citta')
        sede.provincia = request.POST.get('provincia')
        sede.codice_stalla = request.POST.get('codice_stalla', '')
        sede.sede_legale = request.POST.get('sede_legale') == 'on'
        sede.attiva = request.POST.get('attiva', 'on') == 'on'
        sede.note = request.POST.get('note', '')
        sede.save()
        
        messages.success(request, f'Sede "{sede.nome}" aggiornata con successo!')
        return redirect('ddt_app:mittente_detail', mittente_id=sede.mittente.id)
    
    context = {
        'sede': sede,
    }
    return render(request, 'ddt_app/sede_mittente_form.html', context)


def sede_mittente_delete(request, sede_id):
    """Elimina sede mittente"""
    sede = get_object_or_404(SedeMittente, id=sede_id)
    mittente_id = sede.mittente.id
    sede_nome = sede.nome
    
    if request.method == 'POST':
        sede.delete()
        messages.success(request, f'Sede "{sede_nome}" eliminata con successo!')
        return redirect('ddt_app:mittente_detail', mittente_id=mittente_id)
    
    context = {
        'sede': sede,
    }
    return render(request, 'ddt_app/sede_mittente_confirm_delete.html', context)


# ===== GESTIONE DESTINATARI =====

def destinatario_list(request):
    """Lista dei destinatari"""
    destinatari = Destinatario.objects.all().order_by('nome')
    
    # Filtri
    search = request.GET.get('search', '')
    if search:
        destinatari = destinatari.filter(
            Q(nome__icontains=search) |
            Q(piva__icontains=search) |
            Q(cf__icontains=search)
        )
    
    # Paginazione
    paginator = Paginator(destinatari, 10)
    page_number = request.GET.get('page')
    destinatari = paginator.get_page(page_number)
    
    context = {
        'destinatari': destinatari,
        'search': search,
    }
    return render(request, 'ddt_app/destinatario_list.html', context)


def destinatario_detail(request, destinatario_id):
    """Dettaglio destinatario con destinazioni"""
    destinatario = get_object_or_404(Destinatario, id=destinatario_id)
    destinazioni = destinatario.destinazioni.all().order_by('nome')
    
    context = {
        'destinatario': destinatario,
        'destinazioni': destinazioni,
    }
    return render(request, 'ddt_app/destinatario_detail.html', context)


def destinatario_edit(request, destinatario_id):
    """Modifica destinatario"""
    destinatario = get_object_or_404(Destinatario, id=destinatario_id)
    
    if request.method == 'POST':
        form = DestinatarioForm(request.POST, instance=destinatario)
        if form.is_valid():
            form.save()
            messages.success(request, f'Destinatario "{destinatario.nome}" aggiornato con successo!')
            return redirect('ddt_app:destinatario_detail', destinatario_id=destinatario.id)
    else:
        form = DestinatarioForm(instance=destinatario)
    
    context = {
        'form': form,
        'destinatario': destinatario,
        'title': f'Modifica Destinatario {destinatario.nome}',
    }
    return render(request, 'ddt_app/destinatario_form.html', context)


def destinatario_delete(request, destinatario_id):
    """Elimina destinatario"""
    destinatario = get_object_or_404(Destinatario, id=destinatario_id)
    
    if request.method == 'POST':
        try:
            nome = destinatario.nome
            destinatario.delete()
            messages.success(request, f'Destinatario "{nome}" eliminato con successo!')
            return redirect('ddt_app:destinatario_list')
        except Exception as e:
            if 'ProtectedError' in str(type(e)):
                messages.error(request, f'Impossibile eliminare il destinatario "{destinatario.nome}" perché è referenziato da DDT esistenti. Elimina prima i DDT associati.')
            else:
                messages.error(request, f'Errore durante l\'eliminazione: {str(e)}')
            return redirect('ddt_app:destinatario_detail', destinatario_id=destinatario.id)
    
    context = {
        'destinatario': destinatario,
    }
    return render(request, 'ddt_app/destinatario_confirm_delete.html', context)


# ===== GESTIONE VETTORI =====

def vettore_list(request):
    """Lista dei vettori"""
    vettori = Vettore.objects.all().order_by('nome')
    
    # Filtri
    search = request.GET.get('search', '')
    if search:
        vettori = vettori.filter(
            Q(nome__icontains=search) |
            Q(autista__icontains=search) |
            Q(piva__icontains=search)
        )
    
    # Paginazione
    paginator = Paginator(vettori, 10)
    page_number = request.GET.get('page')
    vettori = paginator.get_page(page_number)
    
    context = {
        'vettori': vettori,
        'search': search,
    }
    return render(request, 'ddt_app/vettore_list.html', context)


def vettore_detail(request, vettore_id):
    """Dettaglio vettore con targhe"""
    vettore = get_object_or_404(Vettore, id=vettore_id)
    targhe = vettore.targhe.all().order_by('targa')
    
    context = {
        'vettore': vettore,
        'targhe': targhe,
    }
    return render(request, 'ddt_app/vettore_detail.html', context)


def vettore_edit(request, vettore_id):
    """Modifica vettore"""
    vettore = get_object_or_404(Vettore, id=vettore_id)
    
    if request.method == 'POST':
        form = VettoreForm(request.POST, instance=vettore)
        if form.is_valid():
            form.save()
            messages.success(request, f'Vettore "{vettore.nome}" aggiornato con successo!')
            return redirect('ddt_app:vettore_detail', vettore_id=vettore.id)
    else:
        form = VettoreForm(instance=vettore)
    
    context = {
        'form': form,
        'vettore': vettore,
        'title': f'Modifica Vettore {vettore.nome}',
    }
    return render(request, 'ddt_app/vettore_form.html', context)


def vettore_delete(request, vettore_id):
    """Elimina vettore"""
    vettore = get_object_or_404(Vettore, id=vettore_id)
    
    if request.method == 'POST':
        try:
            nome = vettore.nome
            vettore.delete()
            messages.success(request, f'Vettore "{nome}" eliminato con successo!')
            return redirect('ddt_app:vettore_list')
        except Exception as e:
            if 'ProtectedError' in str(type(e)):
                messages.error(request, f'Impossibile eliminare il vettore "{vettore.nome}" perché è referenziato da DDT esistenti. Elimina prima i DDT associati.')
            else:
                messages.error(request, f'Errore durante l\'eliminazione: {str(e)}')
            return redirect('ddt_app:vettore_detail', vettore_id=vettore.id)
    
    context = {
        'vettore': vettore,
    }
    return render(request, 'ddt_app/vettore_confirm_delete.html', context)


def targa_vettore_create(request, vettore_id):
    """Crea nuova targa per un vettore"""
    vettore = get_object_or_404(Vettore, id=vettore_id)
    
    if request.method == 'POST':
        targa = request.POST.get('targa')
        tipo_veicolo = request.POST.get('tipo_veicolo', '')
        attiva = request.POST.get('attiva', 'on') == 'on'
        note = request.POST.get('note', '')
        
        targa_obj = TargaVettore.objects.create(
            vettore=vettore,
            targa=targa,
            tipo_veicolo=tipo_veicolo,
            attiva=attiva,
            note=note
        )
        
        messages.success(request, f'Targa "{targa_obj.targa}" creata con successo!')
        return redirect('ddt_app:vettore_detail', vettore_id=vettore.id)
    
    context = {
        'vettore': vettore,
    }
    return render(request, 'ddt_app/targa_vettore_form.html', context)


def targa_vettore_edit(request, targa_id):
    """Modifica targa vettore"""
    targa = get_object_or_404(TargaVettore, id=targa_id)
    
    if request.method == 'POST':
        targa.targa = request.POST.get('targa')
        targa.tipo_veicolo = request.POST.get('tipo_veicolo', '')
        targa.attiva = request.POST.get('attiva', 'on') == 'on'
        targa.note = request.POST.get('note', '')
        targa.save()
        
        messages.success(request, f'Targa "{targa.targa}" aggiornata con successo!')
        return redirect('ddt_app:vettore_detail', vettore_id=targa.vettore.id)
    
    context = {
        'targa': targa,
    }
    return render(request, 'ddt_app/targa_vettore_form.html', context)


def targa_vettore_delete(request, targa_id):
    """Elimina targa vettore"""
    targa = get_object_or_404(TargaVettore, id=targa_id)
    vettore_id = targa.vettore.id
    targa_nome = targa.targa
    
    if request.method == 'POST':
        targa.delete()
        messages.success(request, f'Targa "{targa_nome}" eliminata con successo!')
        return redirect('ddt_app:vettore_detail', vettore_id=vettore_id)
    
    context = {
        'targa': targa,
    }
    return render(request, 'ddt_app/targa_vettore_confirm_delete.html', context)


# View per la gestione delle causali di trasporto
def causale_list(request):
    """Lista delle causali di trasporto"""
    search = request.GET.get('search', '')
    causali = CausaleTrasporto.objects.all()
    
    if search:
        causali = causali.filter(
            Q(codice__icontains=search) | 
            Q(descrizione__icontains=search)
        )
    
    causali = causali.order_by('codice')
    
    context = {
        'causali': causali,
        'search': search,
    }
    return render(request, 'ddt_app/causale_list.html', context)


def causale_create(request):
    """Creazione di una nuova causale di trasporto"""
    if request.method == 'POST':
        form = CausaleTrasportoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Causale di trasporto creata con successo!')
            return redirect('ddt_app:causale_list')
    else:
        form = CausaleTrasportoForm()
    
    context = {
        'form': form,
        'title': 'Nuova Causale di Trasporto',
    }
    return render(request, 'ddt_app/causale_form.html', context)


def causale_edit(request, causale_id):
    """Modifica di una causale di trasporto"""
    causale = get_object_or_404(CausaleTrasporto, id=causale_id)
    
    if request.method == 'POST':
        form = CausaleTrasportoForm(request.POST, instance=causale)
        if form.is_valid():
            form.save()
            messages.success(request, 'Causale di trasporto aggiornata con successo!')
            return redirect('ddt_app:causale_list')
    else:
        form = CausaleTrasportoForm(instance=causale)
    
    context = {
        'form': form,
        'causale': causale,
        'title': 'Modifica Causale di Trasporto',
    }
    return render(request, 'ddt_app/causale_form.html', context)


def causale_detail(request, causale_id):
    """Dettaglio di una causale di trasporto"""
    causale = get_object_or_404(CausaleTrasporto, id=causale_id)
    
    context = {
        'causale': causale,
    }
    return render(request, 'ddt_app/causale_detail.html', context)


def causale_delete(request, causale_id):
    """Eliminazione di una causale di trasporto"""
    causale = get_object_or_404(CausaleTrasporto, id=causale_id)
    
    if request.method == 'POST':
        causale.delete()
        messages.success(request, 'Causale di trasporto eliminata con successo!')
        return redirect('ddt_app:causale_list')
    
    context = {
        'causale': causale,
    }
    return render(request, 'ddt_app/causale_confirm_delete.html', context)
