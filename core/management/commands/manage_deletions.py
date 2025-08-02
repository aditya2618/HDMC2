from django.core.management.base import BaseCommand
from django.apps import apps
from core.models import DeletionLog
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Manage deletion logs and restore deleted items'

    def add_arguments(self, parser):
        parser.add_argument(
            '--list-logs',
            action='store_true',
            help='List all deletion logs',
        )
        parser.add_argument(
            '--restore',
            type=int,
            help='Restore item by deletion log ID',
        )
        parser.add_argument(
            '--model',
            type=str,
            help='Filter logs by model name',
        )
        parser.add_argument(
            '--user',
            type=str,
            help='Filter logs by username',
        )

    def handle(self, *args, **options):
        if options['list_logs']:
            self.list_deletion_logs(options)
        elif options['restore']:
            self.restore_item(options['restore'])
        else:
            self.stdout.write(
                self.style.ERROR('Please specify --list-logs or --restore <id>')
            )

    def list_deletion_logs(self, options):
        logs = DeletionLog.objects.all()
        
        if options['model']:
            logs = logs.filter(model_name__icontains=options['model'])
        
        if options['user']:
            logs = logs.filter(deleted_by__username__icontains=options['user'])
        
        logs = logs.order_by('-deleted_at')[:50]  # Last 50 logs
        
        if not logs:
            self.stdout.write(self.style.WARNING('No deletion logs found.'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Found {logs.count()} deletion logs:'))
        self.stdout.write('-' * 80)
        
        for log in logs:
            self.stdout.write(
                f'ID: {log.id} | '
                f'Model: {log.model_name} | '
                f'Object ID: {log.object_id} | '
                f'Deleted by: {log.deleted_by} | '
                f'Date: {log.deleted_at.strftime("%Y-%m-%d %H:%M:%S")}'
            )

    def restore_item(self, log_id):
        try:
            log = DeletionLog.objects.get(id=log_id)
        except DeletionLog.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Deletion log with ID {log_id} not found.')
            )
            return
        
        # Get the model class
        try:
            model_class = apps.get_model(app_label='students', model_name=log.model_name)
        except LookupError:
            try:
                model_class = apps.get_model(app_label='gallery', model_name=log.model_name)
            except LookupError:
                try:
                    model_class = apps.get_model(app_label='performances', model_name=log.model_name)
                except LookupError:
                    try:
                        model_class = apps.get_model(app_label='core', model_name=log.model_name)
                    except LookupError:
                        self.stdout.write(
                            self.style.ERROR(f'Model {log.model_name} not found.')
                        )
                        return
        
        # Try to find the soft-deleted item
        try:
            obj = model_class.objects.get(id=log.object_id, is_deleted=True)
            obj.restore()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully restored {log.model_name} with ID {log.object_id}'
                )
            )
        except model_class.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f'Item {log.model_name} with ID {log.object_id} not found or not deleted.'
                )
            )
