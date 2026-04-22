import time

from django.core.management.base import BaseCommand
from django.utils import timezone

from ...scanner.vm_port_scanner_queue import VMPortScannerQueue


class Command(BaseCommand):
    help = "Run the port scanner"

    def add_arguments(self, parser):
        parser.add_argument('tenants', nargs='+', help="Tenants for the machines to get the ports")
        pass

    def handle(self, *args, **options):
        tenants = options.get('tenants')
        scanner = VMPortScannerQueue(tenants=tenants)
        scanner.run()
        self.stdout.write(
            "[{:%H:%M:%S}] Finished".format(timezone.now())
        )
