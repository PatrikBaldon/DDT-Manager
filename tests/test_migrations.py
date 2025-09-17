"""
Test migrations for DDT Application.
"""
import pytest
from django.test import TestCase
from django.core.management import call_command
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.db import models
from io import StringIO


class MigrationTest(TestCase):
    """Test migrations."""
    
    def test_migrations_apply_correctly(self):
        """Test that migrations apply correctly."""
        # Check that all migrations can be applied
        executor = MigrationExecutor(connection)
        executor.migrate([])
        
        # Check that all tables exist
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            # Check for DDT app tables
            self.assertIn('ddt_app_mittente', tables)
            self.assertIn('ddt_app_sedemittente', tables)
            self.assertIn('ddt_app_destinatario', tables)
            self.assertIn('ddt_app_destinazione', tables)
            self.assertIn('ddt_app_vettore', tables)
            self.assertIn('ddt_app_targavettore', tables)
            self.assertIn('ddt_app_articolo', tables)
            self.assertIn('ddt_app_ddt', tables)
            self.assertIn('ddt_app_ddtriga', tables)
            self.assertIn('ddt_app_configurazione', tables)
            self.assertIn('ddt_app_causaletrasporto', tables)
            self.assertIn('ddt_app_formatonumerazioneddt', tables)
    
    def test_migrations_rollback_correctly(self):
        """Test that migrations can be rolled back."""
        # Apply all migrations
        executor = MigrationExecutor(connection)
        executor.migrate([])
        
        # Rollback to initial state
        executor.migrate([('ddt_app', None)])
        
        # Check that DDT app tables don't exist
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            # Check that DDT app tables don't exist
            self.assertNotIn('ddt_app_mittente', tables)
            self.assertNotIn('ddt_app_sedemittente', tables)
            self.assertNotIn('ddt_app_destinatario', tables)
            self.assertNotIn('ddt_app_destinazione', tables)
            self.assertNotIn('ddt_app_vettore', tables)
            self.assertNotIn('ddt_app_targavettore', tables)
            self.assertNotIn('ddt_app_articolo', tables)
            self.assertNotIn('ddt_app_ddt', tables)
            self.assertNotIn('ddt_app_ddtriga', tables)
            self.assertNotIn('ddt_app_configurazione', tables)
            self.assertNotIn('ddt_app_causaletrasporto', tables)
            self.assertNotIn('ddt_app_formatonumerazioneddt', tables)
    
    def test_migrate_command(self):
        """Test migrate command."""
        # Run migrate command
        out = StringIO()
        call_command('migrate', stdout=out)
        
        # Check output
        output = out.getvalue()
        self.assertIn('No migrations to apply', output)
    
    def test_makemigrations_command(self):
        """Test makemigrations command."""
        # Run makemigrations command
        out = StringIO()
        call_command('makemigrations', '--dry-run', stdout=out)
        
        # Check output
        output = out.getvalue()
        self.assertIn('No changes detected', output)
    
    def test_showmigrations_command(self):
        """Test showmigrations command."""
        # Run showmigrations command
        out = StringIO()
        call_command('showmigrations', 'ddt_app', stdout=out)
        
        # Check output
        output = out.getvalue()
        self.assertIn('ddt_app', output)
        self.assertIn('0001_initial', output)
        self.assertIn('0002_formatonumerazioneddt_ddt_note_centrali_and_more', output)
        self.assertIn('0003_remove_mittente_cap_remove_mittente_citta_and_more', output)
        self.assertIn('0004_alter_ddt_trasporto_mezzo', output)
        self.assertIn('0005_causaletrasporto_alter_ddt_causale_trasporto', output)


@pytest.mark.django_db
def test_migrations_integration():
    """Test migrations integration."""
    # Apply all migrations
    executor = MigrationExecutor(connection)
    executor.migrate([])
    
    # Check that all tables exist
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Check for DDT app tables
        assert 'ddt_app_mittente' in tables
        assert 'ddt_app_sedemittente' in tables
        assert 'ddt_app_destinatario' in tables
        assert 'ddt_app_destinazione' in tables
        assert 'ddt_app_vettore' in tables
        assert 'ddt_app_targavettore' in tables
        assert 'ddt_app_articolo' in tables
        assert 'ddt_app_ddt' in tables
        assert 'ddt_app_ddtriga' in tables
        assert 'ddt_app_configurazione' in tables
        assert 'ddt_app_causaletrasporto' in tables
        assert 'ddt_app_formatonumerazioneddt' in tables


@pytest.mark.django_db
def test_migrations_rollback_integration():
    """Test migrations rollback integration."""
    # Apply all migrations
    executor = MigrationExecutor(connection)
    executor.migrate([])
    
    # Rollback to initial state
    executor.migrate([('ddt_app', None)])
    
    # Check that DDT app tables don't exist
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Check that DDT app tables don't exist
        assert 'ddt_app_mittente' not in tables
        assert 'ddt_app_sedemittente' not in tables
        assert 'ddt_app_destinatario' not in tables
        assert 'ddt_app_destinazione' not in tables
        assert 'ddt_app_vettore' not in tables
        assert 'ddt_app_targavettore' not in tables
        assert 'ddt_app_articolo' not in tables
        assert 'ddt_app_ddt' not in tables
        assert 'ddt_app_ddtriga' not in tables
        assert 'ddt_app_configurazione' not in tables
        assert 'ddt_app_causaletrasporto' not in tables
        assert 'ddt_app_formatonumerazioneddt' not in tables


@pytest.mark.django_db
def test_migrate_command_integration():
    """Test migrate command integration."""
    # Run migrate command
    out = StringIO()
    call_command('migrate', stdout=out)
    
    # Check output
    output = out.getvalue()
    assert 'No migrations to apply' in output or 'Applying' in output


@pytest.mark.django_db
def test_makemigrations_command_integration():
    """Test makemigrations command integration."""
    # Run makemigrations command
    out = StringIO()
    call_command('makemigrations', '--dry-run', stdout=out)
    
    # Check output
    output = out.getvalue()
    assert 'No changes detected' in output or 'Migrations for' in output


@pytest.mark.django_db
def test_showmigrations_command_integration():
    """Test showmigrations command integration."""
    # Run showmigrations command
    out = StringIO()
    call_command('showmigrations', 'ddt_app', stdout=out)
    
    # Check output
    output = out.getvalue()
    assert 'ddt_app' in output
    assert '0001_initial' in output
    assert '0002_formatonumerazioneddt_ddt_note_centrali_and_more' in output
    assert '0003_remove_mittente_cap_remove_mittente_citta_and_more' in output
    assert '0004_alter_ddt_trasporto_mezzo' in output
    assert '0005_causaletrasporto_alter_ddt_causale_trasporto' in output
