from django.forms import BaseForm
from django.http import JsonResponse, HttpResponse


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form. Must be used with an object-based FormView (e.g. CreateView)
    """
    request = None

    def form_invalid(self, form: BaseForm) -> HttpResponse:
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form: BaseForm) -> HttpResponse:
        response = super().form_valid(form)
        if self.request.is_ajax():
            response = JsonResponse({})
        return response
