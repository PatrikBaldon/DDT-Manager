from django.core.management.base import BaseCommand
from django.db import transaction
import json
import os
from ddt_app.models import Mittente, Destinatario, Destinazione, Vettore, Articolo, Configurazione


class Command(BaseCommand):
    help = 'Carica i dati iniziali dal file JSON esistente'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='config/ddt_data.json',
            help='Percorso del file JSON da caricare'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        
        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.ERROR(f'File {file_path} non trovato')
            )
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            with transaction.atomic():
                # Carica mittenti
                self.load_mittenti(data.get('mittenti', []))
                
                # Carica destinatari e destinazioni
                self.load_destinatari(data.get('destinatari', []))
                
                # Carica vettori
                self.load_vettori(data.get('vettori', []))
                
                # Carica articoli
                self.load_articoli(data.get('articoli', []))
                
                # Carica configurazioni
                self.load_configurazioni(data)

            self.stdout.write(
                self.style.SUCCESS('Dati iniziali caricati con successo!')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Errore durante il caricamento: {str(e)}')
            )

    def load_mittenti(self, mittenti_data):
        """Carica i mittenti"""
        for mittente_data in mittenti_data:
            mittente, created = Mittente.objects.get_or_create(
                id=mittente_data['id'],
                defaults={
                    'nome': mittente_data['nome'],
                    'indirizzo': mittente_data['indirizzo'],
                    'cap': mittente_data['cap'],
                    'citta': mittente_data['citta'],
                    'provincia': mittente_data['provincia'],
                    'piva': mittente_data['piva'],
                    'cf': mittente_data['cf'],
                    'telefono': mittente_data['telefono'],
                    'email': mittente_data['email'],
                    'pec': mittente_data.get('pec', ''),
                    'sede_legale': mittente_data.get('sede_legale', True),
                    'note': mittente_data.get('note', ''),
                }
            )
            if created:
                self.stdout.write(f'  Creato mittente: {mittente.nome}')

    def load_destinatari(self, destinatari_data):
        """Carica destinatari e destinazioni"""
        for destinatario_data in destinatari_data:
            destinatario, created = Destinatario.objects.get_or_create(
                id=destinatario_data['id'],
                defaults={
                    'nome': destinatario_data['nome'],
                    'indirizzo': destinatario_data['indirizzo'],
                    'cap': destinatario_data['cap'],
                    'citta': destinatario_data['citta'],
                    'provincia': destinatario_data['provincia'],
                    'piva': destinatario_data['piva'],
                    'cf': destinatario_data['cf'],
                    'telefono': destinatario_data['telefono'],
                    'email': destinatario_data['email'],
                }
            )
            if created:
                self.stdout.write(f'  Creato destinatario: {destinatario.nome}')

            # Carica destinazioni
            for destinazione_data in destinatario_data.get('destinazioni', []):
                destinazione, created = Destinazione.objects.get_or_create(
                    destinatario=destinatario,
                    nome=destinazione_data['nome'],
                    defaults={
                        'indirizzo': destinazione_data['indirizzo'],
                        'note': destinazione_data.get('note', ''),
                    }
                )
                if created:
                    self.stdout.write(f'    Creato destinazione: {destinazione.nome}')

    def load_vettori(self, vettori_data):
        """Carica i vettori"""
        for vettore_data in vettori_data:
            vettore, created = Vettore.objects.get_or_create(
                id=vettore_data['id'],
                defaults={
                    'nome': vettore_data['nome'],
                    'indirizzo': vettore_data['indirizzo'],
                    'cap': vettore_data['cap'],
                    'citta': vettore_data['citta'],
                    'provincia': vettore_data['provincia'],
                    'piva': vettore_data['piva'],
                    'cf': vettore_data['cf'],
                    'telefono': vettore_data['telefono'],
                    'email': vettore_data['email'],
                    'autista': vettore_data['autista'],
                    'patente': vettore_data['patente'],
                    'targa': vettore_data['targa'],
                    'note': vettore_data.get('note', ''),
                }
            )
            if created:
                self.stdout.write(f'  Creato vettore: {vettore.nome}')

    def load_articoli(self, articoli_data):
        """Carica gli articoli"""
        for articolo_data in articoli_data:
            articolo, created = Articolo.objects.get_or_create(
                id=articolo_data['id'],
                defaults={
                    'nome': articolo_data['nome'],
                    'categoria': articolo_data['categoria'],
                    'um': articolo_data['um'],
                    'prezzo_unitario': articolo_data['prezzo_unitario'],
                    'note': articolo_data.get('note', ''),
                }
            )
            if created:
                self.stdout.write(f'  Creato articolo: {articolo.nome}')

    def load_configurazioni(self, data):
        """Carica le configurazioni"""
        configs = [
            ('causali_trasporto', json.dumps(data.get('causali_trasporto', [])), 'Lista causali di trasporto'),
            ('tipologie_trasporto', json.dumps(data.get('tipologie_trasporto', [])), 'Lista tipologie di trasporto'),
            ('unita_misura', json.dumps(data.get('unita_misura', [])), 'Lista unità di misura'),
        ]
        
        for chiave, valore, descrizione in configs:
            config, created = Configurazione.objects.get_or_create(
                chiave=chiave,
                defaults={
                    'valore': valore,
                    'descrizione': descrizione,
                }
            )
            if created:
                self.stdout.write(f'  Creata configurazione: {chiave}')

