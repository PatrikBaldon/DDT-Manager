#!/usr/bin/env python3
"""
Comando per configurare il formato di numerazione DDT predefinito
"""

from django.core.management.base import BaseCommand
from ddt_app.models import FormatoNumerazioneDDT


class Command(BaseCommand):
    help = 'Configura il formato di numerazione DDT predefinito'

    def add_arguments(self, parser):
        parser.add_argument(
            '--formato',
            type=str,
            default='aaaa-num',
            choices=['aaaa-num', 'num', 'mmaa-num', 'aa-num'],
            help='Formato di numerazione da impostare (default: aaaa-num)'
        )
        parser.add_argument(
            '--numero-iniziale',
            type=int,
            default=1,
            help='Numero iniziale per la numerazione (default: 1)'
        )
        parser.add_argument(
            '--lunghezza',
            type=int,
            default=4,
            help='Lunghezza del numero progressivo (default: 4)'
        )

    def handle(self, *args, **options):
        formato = options['formato']
        numero_iniziale = options['numero_iniziale']
        lunghezza = options['lunghezza']

        # Disattiva tutti i formati esistenti
        FormatoNumerazioneDDT.objects.update(attivo=False)

        # Crea o aggiorna il formato predefinito
        formato_obj, created = FormatoNumerazioneDDT.objects.get_or_create(
            formato=formato,
            defaults={
                'numero_iniziale': numero_iniziale,
                'lunghezza_numero': lunghezza,
                'attivo': True
            }
        )

        if not created:
            formato_obj.numero_iniziale = numero_iniziale
            formato_obj.lunghezza_numero = lunghezza
            formato_obj.attivo = True
            formato_obj.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Formato di numerazione "{formato_obj.get_formato_display()}" '
                f'configurato con successo!'
            )
        )
        self.stdout.write(f'Numero iniziale: {formato_obj.numero_iniziale}')
        self.stdout.write(f'Lunghezza numero: {formato_obj.lunghezza_numero}')
        self.stdout.write(f'Attivo: {formato_obj.attivo}')
