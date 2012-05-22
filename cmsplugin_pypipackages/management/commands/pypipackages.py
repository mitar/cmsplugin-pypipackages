import xmlrpclib

from django.core.management import base
from django.db import transaction

import slumber

from cmsplugin_pypipackages import models

class Command(base.NoArgsCommand):
    help = 'Updates cache for all PyPiPackages plugins from PyPi.'

    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity'))

        client = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
        readthedocs = slumber.API(base_url='http://readthedocs.org/api/v1/')

        models.PyPiPackage.objects.all().update(updated=False)

        for plugin in models.PyPiPackagesPlugin.objects.all():
            if verbosity > 1:
                self.stdout.write("%s.\n" % (plugin,))

            for package in client.search({'keywords': plugin.keyword}):
                if verbosity > 1:
                    self.stdout.write("Processing '%s' (%s).\n" % (package['name'], package['version']))

                data = client.release_data(package['name'], package['version'])

                try:
                    docs = readthedocs.project.get(slug=package['name'].lower())['objects'][0]
                except IndexError:
                    docs = {}

                models.PyPiPackage.objects.filter(plugin=plugin, name=data['name']).delete()
                models.PyPiPackage.objects.create(
                    plugin=plugin,
                    name=data['name'],
                    version=data['version'],
                    summary=data.get('summary', ''),
                    description=data.get('description', ''),
                    home_page=data.get('home_page', ''),
                    download_url=data.get('download_url', ''),
                    docs_url=data.get('docs_url', '') or docs.get('subdomain', ''),
                    repo_url=docs.get('repo', ''),
                )

        models.PyPiPackage.objects.filter(updated=False).delete()

        transaction.commit_unless_managed()
