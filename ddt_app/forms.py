from django import forms
from django.forms import inlineformset_factory
from .models import DDT, DDTRiga, Mittente, SedeMittente, Destinatario, Destinazione, Vettore, Autista, TargaVettore, Articolo, FormatoNumerazioneDDT, CausaleTrasporto


class DDTForm(forms.ModelForm):
    """Form per la creazione e modifica dei DDT"""
    
    # Campo nascosto per gestire la destinazione
    destinazione_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rimuovi il campo destinazione originale e usa solo il campo nascosto
        if 'destinazione' in self.fields:
            del self.fields['destinazione']
        
        # Configura le scelte per trasporto_mezzo
        self.fields['trasporto_mezzo'].widget = forms.RadioSelect(choices=[
            ('mittente', 'Mittente'),
            ('vettore', 'Vettore'),
            ('destinatario', 'Destinatario'),
        ])
        
        # Filtra le sedi del mittente e le causali attive
        self.fields['sede_mittente'].queryset = SedeMittente.objects.filter(attiva=True)
        self.fields['causale_trasporto'].queryset = CausaleTrasporto.objects.filter(attiva=True)
        
        # Aggiungi classi CSS ai campi select
        self.fields['mittente'].widget.attrs.update({'class': 'form-control'})
        self.fields['destinatario'].widget.attrs.update({'class': 'form-control'})
        self.fields['vettore'].widget.attrs.update({'class': 'form-control'})
        self.fields['causale_trasporto'].widget.attrs.update({'class': 'form-control'})
        
        # Configura i campi autista e targa_vettore
        self.fields['autista'].queryset = Autista.objects.none()
        self.fields['targa_vettore'].queryset = TargaVettore.objects.none()
        self.fields['targa_vettore_2'].queryset = TargaVettore.objects.none()
        self.fields['autista'].required = False
        self.fields['targa_vettore'].required = False
        self.fields['targa_vettore_2'].required = False
        
        # Se è una modifica, imposta i queryset basati sul vettore esistente
        if self.instance and self.instance.pk and self.instance.vettore:
            self.fields['autista'].queryset = Autista.objects.filter(vettore=self.instance.vettore, attivo=True)
            self.fields['targa_vettore'].queryset = TargaVettore.objects.filter(vettore=self.instance.vettore, attiva=True)
            self.fields['targa_vettore_2'].queryset = TargaVettore.objects.filter(vettore=self.instance.vettore, attiva=True)
        elif 'vettore' in self.data:
            try:
                vettore_id = int(self.data.get('vettore'))
                if vettore_id:
                    self.fields['autista'].queryset = Autista.objects.filter(vettore_id=vettore_id, attivo=True)
                    self.fields['targa_vettore'].queryset = TargaVettore.objects.filter(vettore_id=vettore_id, attiva=True)
                    self.fields['targa_vettore_2'].queryset = TargaVettore.objects.filter(vettore_id=vettore_id, attiva=True)
            except (ValueError, TypeError):
                pass
        
        # Aggiungi JavaScript per mostrare/nascondere il campo note centrali
        self.fields['note_centrali'].widget.attrs.update({
            'data-toggle': 'note-centrali',
            'placeholder': 'Inserisci le note da mostrare al centro delle righe della tabella prodotti...'
        })
        
        # Se è una modifica, imposta i valori iniziali
        if self.instance and self.instance.pk:
            self.fields['trasporto_mezzo'].initial = self.instance.trasporto_mezzo
            
            # Carica le sedi del mittente esistente
            if self.instance.mittente:
                self.fields['sede_mittente'].queryset = SedeMittente.objects.filter(
                    mittente=self.instance.mittente, 
                    attiva=True
                )
    
    def clean_destinazione_id(self):
        destinazione_id = self.cleaned_data.get('destinazione_id')
        
        if not destinazione_id:
            raise forms.ValidationError("Devi selezionare una destinazione.")
        
        try:
            destinazione = Destinazione.objects.get(id=destinazione_id)
            return destinazione
        except Destinazione.DoesNotExist:
            raise forms.ValidationError("Destinazione non valida.")
    
    def clean(self):
        cleaned_data = super().clean()
        destinatario = cleaned_data.get('destinatario')
        destinazione = cleaned_data.get('destinazione_id')
        trasporto_mezzo = cleaned_data.get('trasporto_mezzo')
        vettore = cleaned_data.get('vettore')
        mittente = cleaned_data.get('mittente')
        
        # Verifica che la destinazione appartenga al destinatario selezionato
        if destinatario and destinazione:
            if destinazione.destinatario != destinatario:
                raise forms.ValidationError("La destinazione selezionata non appartiene al destinatario scelto.")
        
        # Logica per il campo vettore basato su trasporto_mezzo
        if trasporto_mezzo == 'vettore':
            if not vettore:
                raise forms.ValidationError("Devi selezionare un vettore quando il trasporto è a mezzo vettore.")
        elif trasporto_mezzo == 'mittente':
            if not mittente:
                raise forms.ValidationError("Devi selezionare un mittente quando il trasporto è a mezzo mittente.")
        elif trasporto_mezzo == 'destinatario':
            if not destinatario:
                raise forms.ValidationError("Devi selezionare un destinatario quando il trasporto è a mezzo destinatario.")
        
        # Validazione autista e targa quando è selezionato un vettore
        if vettore:
            autista = cleaned_data.get('autista')
            targa_vettore = cleaned_data.get('targa_vettore')
            targa_vettore_2 = cleaned_data.get('targa_vettore_2')
            
            # Validazione autista (opzionale)
            if autista:
                if hasattr(autista, 'vettore') and autista.vettore != vettore:
                    raise forms.ValidationError("L'autista selezionato non appartiene al vettore scelto.")
            
            # Validazione targa 1 (opzionale)
            if targa_vettore:
                if hasattr(targa_vettore, 'vettore') and targa_vettore.vettore != vettore:
                    raise forms.ValidationError("La targa 1 selezionata non appartiene al vettore scelto.")
            
            # Validazione targa 2 (opzionale)
            if targa_vettore_2:
                if hasattr(targa_vettore_2, 'vettore') and targa_vettore_2.vettore != vettore:
                    raise forms.ValidationError("La targa 2 selezionata non appartiene al vettore scelto.")
            
            # Validazione che le due targhe siano diverse
            if targa_vettore and targa_vettore_2 and targa_vettore == targa_vettore_2:
                raise forms.ValidationError("Le due targhe devono essere diverse.")
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        destinazione = self.cleaned_data.get('destinazione_id')
        
        if destinazione:
            instance.destinazione = destinazione
        
        if commit:
            instance.save()
        
        return instance
    
    class Meta:
        model = DDT
        fields = [
            'numero', 'data_documento', 'mittente', 'sede_mittente', 'destinatario',
            'causale_trasporto', 'luogo_destinazione', 'trasporto_mezzo',
            'data_ritiro', 'vettore', 'autista', 'targa_vettore', 'targa_vettore_2', 'annotazioni', 'note_centrali'
        ]
        widgets = {
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Es: 2024-0001'
            }),
            'data_documento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'data_ritiro': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'sede_mittente': forms.Select(attrs={
                'class': 'form-control'
            }),
            'causale_trasporto': forms.Select(attrs={
                'class': 'form-control'
            }),
            'luogo_destinazione': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Indirizzo completo di destinazione',
                'rows': 3
            }),
            'trasporto_mezzo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'annotazioni': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Note aggiuntive...'
            }),
            'note_centrali': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Note da inserire al centro delle righe della tabella prodotti...'
            }),
            'autista': forms.Select(attrs={
                'class': 'form-control'
            }),
            'targa_vettore': forms.Select(attrs={
                'class': 'form-control'
            }),
            'targa_vettore_2': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class DDTRigaForm(forms.ModelForm):
    """Form per le righe dei DDT"""
    
    class Meta:
        model = DDTRiga
        fields = ['articolo', 'quantita', 'descrizione', 'ordine']
        widgets = {
            'articolo': forms.Select(attrs={
                'class': 'form-control articolo-select',
                'data-live-search': 'true'
            }),
            'quantita': forms.NumberInput(attrs={
                'class': 'form-control quantita-input',
                'step': '0.01',
                'min': '0'
            }),
            'descrizione': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descrizione aggiuntiva...'
            }),
            'ordine': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordina gli articoli per categoria e nome
        self.fields['articolo'].queryset = Articolo.objects.all().order_by('categoria', 'nome')


# Formset per le righe del DDT
DDTRigaFormSet = inlineformset_factory(
    DDT, DDTRiga,
    form=DDTRigaForm,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=False
)


class MittenteForm(forms.ModelForm):
    """Form per la gestione dei mittenti"""
    
    class Meta:
        model = Mittente
        fields = ['nome', 'piva', 'cf', 'telefono', 'email', 'pec', 'logo', 'note']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'piva': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '11'}),
            'cf': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '16', 'style': 'text-transform: uppercase'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'pec': forms.EmailInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class DestinatarioForm(forms.ModelForm):
    """Form per la gestione dei destinatari"""
    
    class Meta:
        model = Destinatario
        fields = ['nome', 'indirizzo', 'cap', 'citta', 'provincia', 'piva', 'cf', 'telefono', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'indirizzo': forms.TextInput(attrs={'class': 'form-control'}),
            'cap': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '5'}),
            'citta': forms.TextInput(attrs={'class': 'form-control'}),
            'provincia': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2', 'style': 'text-transform: uppercase'}),
            'piva': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '11'}),
            'cf': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '16', 'style': 'text-transform: uppercase'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class VettoreForm(forms.ModelForm):
    """Form per la gestione dei vettori"""
    
    class Meta:
        model = Vettore
        fields = ['nome', 'indirizzo', 'cap', 'citta', 'provincia', 'piva', 'cf', 'telefono', 'email', 'autorizzazione_animali_vivi', 'licenza_bdn', 'note']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'indirizzo': forms.TextInput(attrs={'class': 'form-control'}),
            'cap': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '5'}),
            'citta': forms.TextInput(attrs={'class': 'form-control'}),
            'provincia': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2', 'style': 'text-transform: uppercase'}),
            'piva': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '11'}),
            'cf': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '16', 'style': 'text-transform: uppercase'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'autorizzazione_animali_vivi': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'licenza_bdn': forms.TextInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AutistaForm(forms.ModelForm):
    """Form per la gestione degli autisti"""
    
    class Meta:
        model = Autista
        fields = ['nome', 'cognome', 'patente', 'attivo', 'note']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cognome': forms.TextInput(attrs={'class': 'form-control'}),
            'patente': forms.TextInput(attrs={'class': 'form-control'}),
            'attivo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ArticoloForm(forms.ModelForm):
    """Form per la gestione degli articoli"""
    
    class Meta:
        model = Articolo
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'um': forms.Select(attrs={'class': 'form-control'}),
            'prezzo_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opzioni per unità di misura
        self.fields['um'].widget = forms.Select(
            choices=[
                ('', 'Seleziona unità...'),
                ('kg', 'kg - Chilogrammi'),
                ('hg', 'hg - Ettogrammi'),
                ('g', 'g - Grammi'),
                ('pz', 'pz - Pezzi'),
                ('l', 'l - Litri'),
                ('ml', 'ml - Millilitri'),
                ('m', 'm - Metri'),
                ('cm', 'cm - Centimetri'),
                ('m²', 'm² - Metri quadri'),
                ('m³', 'm³ - Metri cubi'),
            ],
            attrs={'class': 'form-control'}
        )


class DestinazioneForm(forms.ModelForm):
    """Form per la gestione delle destinazioni"""
    
    class Meta:
        model = Destinazione
        fields = ['nome', 'indirizzo', 'codice_stalla', 'note']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'indirizzo': forms.TextInput(attrs={'class': 'form-control'}),
            'codice_stalla': forms.TextInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class FormatoNumerazioneDDTForm(forms.ModelForm):
    """Form per la configurazione del formato di numerazione DDT"""
    
    class Meta:
        model = FormatoNumerazioneDDT
        fields = ['formato', 'formato_personalizzato', 'numero_iniziale', 'lunghezza_numero', 'attivo']
        widgets = {
            'formato': forms.Select(attrs={'class': 'form-control'}),
            'formato_personalizzato': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Es: {anno}-{numero} o {mese:02d}-{numero}'
            }),
            'numero_iniziale': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'lunghezza_numero': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '10'
            }),
            'attivo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aggiungi JavaScript per mostrare/nascondere il campo personalizzato
        self.fields['formato_personalizzato'].widget.attrs.update({
            'data-show-when': 'custom'
        })


class CausaleTrasportoForm(forms.ModelForm):
    """Form per la gestione delle causali di trasporto"""
    
    class Meta:
        model = CausaleTrasporto
        fields = ['codice', 'descrizione', 'attiva', 'note']
        widgets = {
            'codice': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'es: VEN'}),
            'descrizione': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'es: Vendita'}),
            'attiva': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
