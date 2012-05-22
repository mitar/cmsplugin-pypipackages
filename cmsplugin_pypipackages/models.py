from django.db import models
from django.utils.translation import ugettext as _

from cms import models as cms_models

class PyPiPackagesPlugin(cms_models.CMSPlugin):
    keyword = models.CharField(_("Search keyword"), max_length=255)

    def __unicode__(self):
        return u"Keywords '%s'" % (self.keyword,)

class PyPiPackage(models.Model):
    plugin = models.ForeignKey(PyPiPackagesPlugin, related_name='packages')
    
    name = models.CharField(_("Name"), max_length=255)
    version = models.CharField(_("Version"), max_length=255)
    summary = models.TextField(_("Summary"), max_length=255, blank=True)
    description = models.TextField(_("Description"), blank=True)
    home_page = models.CharField(_("Homepage URL"), max_length=255, blank=True)
    download_url = models.CharField(_("Download URL"), max_length=255, blank=True)
    docs_url = models.CharField(_("Documentation URL"), max_length=255, blank=True)
    repo_url = models.CharField(_("Repository URL"), max_length=255, blank=True)

    updated = models.BooleanField(_("Updated flag"), default=True)

    class Meta:
        unique_together = (('plugin', 'name'),)
