from django.utils.translation import ugettext as _

from cms import plugin_base
from cms.plugin_pool import plugin_pool

from cmsplugin_pypipackages import models

class PyPiPackagesPlugin(plugin_base.CMSPluginBase):
    model = models.PyPiPackagesPlugin
    name = _("PyPi Packages")
    render_template = 'cmsplugin_pypipackages/packages.html'

    def render(self, context, instance, placeholder):
        context.update({
            'packages': instance.packages.all(),
        })
        return context

plugin_pool.register_plugin(PyPiPackagesPlugin)
