from django.db import models
from django.core.validators import RegexValidator


class Mittente(models.Model):
    """Modello per i mittenti dei DDT"""
    nome = models.CharField(max_length=200, verbose_name="Nome Azienda")
    piva = models.CharField(max_length=11, verbose_name="P.IVA", validators=[RegexValidator(r'^\d{11}$', 'P.IVA deve essere di 11 cifre')])
    cf = models.CharField(max_length=16, verbose_name="Codice Fiscale")
    telefono = models.CharField(max_length=20, verbose_name="Telefono")
    email = models.EmailField(verbose_name="Email")
    pec = models.EmailField(verbose_name="PEC", blank=True)
    note = models.TextField(blank=True, verbose_name="Note")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mittente"
        verbose_name_plural = "Mittenti"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class SedeMittente(models.Model):
    """Modello per le sedi dei mittenti"""
    mittente = models.ForeignKey(Mittente, on_delete=models.CASCADE, related_name='sedi')
    nome = models.CharField(max_length=200, verbose_name="Nome Sede")
    indirizzo = models.CharField(max_length=300, verbose_name="Indirizzo")
    cap = models.CharField(max_length=5, verbose_name="CAP", validators=[RegexValidator(r'^\d{5}$', 'CAP deve essere di 5 cifre')])
    citta = models.CharField(max_length=100, verbose_name="Città")
    provincia = models.CharField(max_length=2, verbose_name="Provincia", validators=[RegexValidator(r'^[A-Z]{2}$', 'Provincia deve essere di 2 lettere maiuscole')])
    codice_stalla = models.CharField(max_length=50, blank=True, verbose_name="Codice Stalla")
    sede_legale = models.BooleanField(default=False, verbose_name="Sede Legale")
    attiva = models.BooleanField(default=True, verbose_name="Attiva")
    note = models.TextField(blank=True, verbose_name="Note")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sede Mittente"
        verbose_name_plural = "Sedi Mittente"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.mittente.nome}"


class Destinazione(models.Model):
    """Modello per le destinazioni dei destinatari"""
    nome = models.CharField(max_length=200, verbose_name="Nome Destinazione")
    indirizzo = models.CharField(max_length=300, verbose_name="Indirizzo")
    codice_stalla = models.CharField(max_length=50, blank=True, verbose_name="Codice Stalla")
    note = models.TextField(blank=True, verbose_name="Note")
    destinatario = models.ForeignKey('Destinatario', on_delete=models.CASCADE, related_name='destinazioni')

    class Meta:
        verbose_name = "Destinazione"
        verbose_name_plural = "Destinazioni"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.destinatario.nome}"


class Destinatario(models.Model):
    """Modello per i destinatari dei DDT"""
    nome = models.CharField(max_length=200, verbose_name="Nome Azienda")
    indirizzo = models.CharField(max_length=300, verbose_name="Indirizzo")
    cap = models.CharField(max_length=5, verbose_name="CAP", validators=[RegexValidator(r'^\d{5}$', 'CAP deve essere di 5 cifre')])
    citta = models.CharField(max_length=100, verbose_name="Città")
    provincia = models.CharField(max_length=2, verbose_name="Provincia", validators=[RegexValidator(r'^[A-Z]{2}$', 'Provincia deve essere di 2 lettere maiuscole')])
    piva = models.CharField(max_length=11, verbose_name="P.IVA", validators=[RegexValidator(r'^\d{11}$', 'P.IVA deve essere di 11 cifre')])
    cf = models.CharField(max_length=16, verbose_name="Codice Fiscale")
    telefono = models.CharField(max_length=20, verbose_name="Telefono")
    email = models.EmailField(verbose_name="Email")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Destinatario"
        verbose_name_plural = "Destinatari"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Vettore(models.Model):
    """Modello per i vettori di trasporto"""
    nome = models.CharField(max_length=200, verbose_name="Nome Azienda")
    indirizzo = models.CharField(max_length=300, verbose_name="Indirizzo")
    cap = models.CharField(max_length=5, verbose_name="CAP", validators=[RegexValidator(r'^\d{5}$', 'CAP deve essere di 5 cifre')])
    citta = models.CharField(max_length=100, verbose_name="Città")
    provincia = models.CharField(max_length=2, verbose_name="Provincia", validators=[RegexValidator(r'^[A-Z]{2}$', 'Provincia deve essere di 2 lettere maiuscole')])
    piva = models.CharField(max_length=11, verbose_name="P.IVA", validators=[RegexValidator(r'^\d{11}$', 'P.IVA deve essere di 11 cifre')])
    cf = models.CharField(max_length=16, verbose_name="Codice Fiscale")
    telefono = models.CharField(max_length=20, verbose_name="Telefono")
    email = models.EmailField(verbose_name="Email")
    autista = models.CharField(max_length=100, verbose_name="Nome Autista")
    patente = models.CharField(max_length=20, verbose_name="Numero Patente")
    licenza_bdn = models.CharField(max_length=100, blank=True, verbose_name="Licenza BDN per Trasporto Animali Vivi")
    note = models.TextField(blank=True, verbose_name="Note")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Vettore"
        verbose_name_plural = "Vettori"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.autista}"


class TargaVettore(models.Model):
    """Modello per le targhe dei vettori"""
    vettore = models.ForeignKey(Vettore, on_delete=models.CASCADE, related_name='targhe')
    targa = models.CharField(max_length=10, verbose_name="Targa Veicolo")
    tipo_veicolo = models.CharField(max_length=50, blank=True, verbose_name="Tipo Veicolo")
    attiva = models.BooleanField(default=True, verbose_name="Attiva")
    note = models.TextField(blank=True, verbose_name="Note")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Targa Vettore"
        verbose_name_plural = "Targhe Vettore"
        ordering = ['targa']

    def __str__(self):
        return f"{self.targa} - {self.vettore.nome}"


class Articolo(models.Model):
    """Modello per gli articoli/prodotti"""
    nome = models.CharField(max_length=200, verbose_name="Nome Articolo")
    categoria = models.CharField(max_length=100, verbose_name="Categoria")
    um = models.CharField(max_length=10, verbose_name="Unità di Misura")
    prezzo_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prezzo Unitario")
    note = models.TextField(blank=True, verbose_name="Note")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Articolo"
        verbose_name_plural = "Articoli"
        ordering = ['categoria', 'nome']

    def __str__(self):
        return f"{self.nome} ({self.categoria})"


class DDT(models.Model):
    """Modello principale per i Documenti di Trasporto"""
    numero = models.CharField(max_length=50, unique=True, verbose_name="Numero DDT")
    data_documento = models.DateField(verbose_name="Data Documento")
    mittente = models.ForeignKey(Mittente, on_delete=models.PROTECT, verbose_name="Mittente")
    sede_mittente = models.ForeignKey(SedeMittente, on_delete=models.PROTECT, verbose_name="Sede Mittente", null=True, blank=True)
    destinatario = models.ForeignKey(Destinatario, on_delete=models.PROTECT, verbose_name="Destinatario")
    destinazione = models.ForeignKey(Destinazione, on_delete=models.PROTECT, verbose_name="Destinazione")
    causale_trasporto = models.ForeignKey('CausaleTrasporto', on_delete=models.PROTECT, verbose_name="Causale di Trasporto")
    luogo_destinazione = models.CharField(max_length=300, verbose_name="Luogo di Destinazione")
    trasporto_mezzo = models.CharField(
        max_length=20, 
        choices=[
            ('mittente', 'Mittente'),
            ('vettore', 'Vettore'),
            ('destinatario', 'Destinatario'),
        ],
        verbose_name="Trasporto a Mezzo di"
    )
    data_ritiro = models.DateField(verbose_name="Data Ritiro")
    vettore = models.ForeignKey(Vettore, on_delete=models.PROTECT, verbose_name="Vettore")
    targa_vettore = models.ForeignKey(TargaVettore, on_delete=models.PROTECT, verbose_name="Targa Veicolo", null=True, blank=True)
    annotazioni = models.TextField(blank=True, verbose_name="Annotazioni")
    # Campo per note centrali nelle righe della tabella
    note_centrali = models.TextField(
        blank=True, 
        verbose_name="Note Centrali",
        help_text="Note da inserire al centro delle righe della tabella prodotti"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "DDT"
        verbose_name_plural = "DDT"
        ordering = ['-data_documento', '-numero']

    def __str__(self):
        return f"DDT {self.numero} - {self.destinatario.nome}"

    @property
    def totale_quantita(self):
        """Calcola la quantità totale degli articoli nel DDT"""
        return sum(riga.quantita for riga in self.righe.all())

    @property
    def totale_valore(self):
        """Calcola il valore totale del DDT"""
        return sum(riga.quantita * riga.articolo.prezzo_unitario for riga in self.righe.all())
    
    @property
    def ha_righe_articoli(self):
        """Verifica se il DDT ha righe con articoli specifici"""
        return self.righe.exists()
    
    @property
    def usa_note_centrali(self):
        """Verifica se usare le note centrali invece delle righe articoli"""
        return bool(self.note_centrali) and not self.ha_righe_articoli


class DDTRiga(models.Model):
    """Modello per le righe degli articoli nei DDT"""
    ddt = models.ForeignKey(DDT, on_delete=models.CASCADE, related_name='righe', verbose_name="DDT")
    articolo = models.ForeignKey(Articolo, on_delete=models.PROTECT, verbose_name="Articolo")
    quantita = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Quantità")
    descrizione = models.TextField(blank=True, verbose_name="Descrizione Aggiuntiva")
    ordine = models.PositiveIntegerField(default=0, verbose_name="Ordine")

    class Meta:
        verbose_name = "Riga DDT"
        verbose_name_plural = "Righe DDT"
        ordering = ['ordine']

    def __str__(self):
        return f"{self.articolo.nome} - {self.quantita} {self.articolo.um}"

    @property
    def valore_totale(self):
        """Calcola il valore totale della riga"""
        return self.quantita * self.articolo.prezzo_unitario


class Configurazione(models.Model):
    """Modello per le configurazioni dell'applicazione"""
    chiave = models.CharField(max_length=100, unique=True, verbose_name="Chiave")
    valore = models.TextField(verbose_name="Valore")
    descrizione = models.TextField(blank=True, verbose_name="Descrizione")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configurazione"
        verbose_name_plural = "Configurazioni"

    def __str__(self):
        return f"{self.chiave}: {self.valore}"


class CausaleTrasporto(models.Model):
    """Modello per le causali di trasporto"""
    codice = models.CharField(max_length=10, unique=True, verbose_name="Codice")
    descrizione = models.CharField(max_length=200, verbose_name="Descrizione")
    attiva = models.BooleanField(default=True, verbose_name="Attiva")
    note = models.TextField(blank=True, verbose_name="Note")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Causale di Trasporto"
        verbose_name_plural = "Causali di Trasporto"
        ordering = ['codice']

    def __str__(self):
        return f"{self.codice} - {self.descrizione}"


class FormatoNumerazioneDDT(models.Model):
    """Modello per la configurazione del formato di numerazione DDT"""
    FORMATO_CHOICES = [
        ('aaaa-num', 'AAAA-NUM (es: 2024-0001)'),
        ('num', 'NUM (es: 0001)'),
        ('mmaa-num', 'MMAA-NUM (es: 1224-0001)'),
        ('aa-num', 'AA-NUM (es: 24-0001)'),
        ('custom', 'Personalizzato'),
    ]
    
    formato = models.CharField(
        max_length=20, 
        choices=FORMATO_CHOICES, 
        default='aaaa-num',
        verbose_name="Formato Numerazione"
    )
    formato_personalizzato = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Formato Personalizzato",
        help_text="Usa {anno} per l'anno, {mese} per il mese, {numero} per il numero progressivo"
    )
    numero_iniziale = models.PositiveIntegerField(
        default=1, 
        verbose_name="Numero Iniziale"
    )
    lunghezza_numero = models.PositiveIntegerField(
        default=4, 
        verbose_name="Lunghezza Numero",
        help_text="Numero di cifre per il numero progressivo (es: 4 = 0001, 3 = 001)"
    )
    attivo = models.BooleanField(default=True, verbose_name="Attivo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Formato Numerazione DDT"
        verbose_name_plural = "Formati Numerazione DDT"

    def __str__(self):
        return f"{self.get_formato_display()} - {self.numero_iniziale}"

    def genera_numero(self, anno=None, mese=None):
        """Genera il prossimo numero DDT secondo il formato configurato"""
        from datetime import datetime
        
        if not anno:
            anno = datetime.now().year
        if not mese:
            mese = datetime.now().month
            
        # Trova l'ultimo numero utilizzato per questo formato
        ultimo_ddt = DDT.objects.filter(
            numero__startswith=self.get_prefisso(anno, mese)
        ).order_by('-numero').first()
        
        if ultimo_ddt:
            # Estrai il numero dall'ultimo DDT
            try:
                ultimo_numero = int(ultimo_ddt.numero.split('-')[-1])
                prossimo_numero = ultimo_numero + 1
            except (ValueError, IndexError):
                prossimo_numero = self.numero_iniziale
        else:
            prossimo_numero = self.numero_iniziale
            
        # Formatta il numero con la lunghezza richiesta
        numero_formattato = str(prossimo_numero).zfill(self.lunghezza_numero)
        
        if self.formato == 'custom' and self.formato_personalizzato:
            return self.formato_personalizzato.format(
                anno=anno,
                mese=mese,
                numero=numero_formattato
            )
        else:
            return f"{self.get_prefisso(anno, mese)}-{numero_formattato}"
    
    def get_prefisso(self, anno, mese):
        """Ottiene il prefisso per il formato selezionato"""
        if self.formato == 'aaaa-num':
            return str(anno)
        elif self.formato == 'num':
            return ""
        elif self.formato == 'mmaa-num':
            return f"{mese:02d}{str(anno)[-2:]}"
        elif self.formato == 'aa-num':
            return str(anno)[-2:]
        else:
            return ""

