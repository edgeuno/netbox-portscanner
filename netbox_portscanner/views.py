from django.shortcuts import render
from django.views import View


class HomeView(View):
    """Homepage"""
    template_name = 'netbox_portscanner/home.html'

    # service incoming GET HTTP requests
    def get(self, request):
        """Get request."""
        return render(request, self.template_name)
