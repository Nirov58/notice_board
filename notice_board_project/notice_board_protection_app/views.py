from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from guardian.decorators import permission_required

from notice_board_main_app.models import Response
from notice_board_main_app.filters import ResponseFilter


class Responses(LoginRequiredMixin, ListView):
    model = Response
    ordering = "-date"
    template_name = 'protection/responses.html'
    context_object_name = 'responses'
    filterset = None
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(target__author=self.request.user)
        self.filterset = ResponseFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


@permission_required('notice_board_main_app.change_response', (Response, 'pk', 'pk'), return_403=True)
def accept(request, pk):
    response = Response.objects.get(pk=pk)
    response.is_accepted = True
    response.save()
    response.delete()
    return redirect('../')


@permission_required('notice_board_main_app.delete_response', (Response, 'pk', 'pk'), return_403=True)
def reject(request, pk):
    response = Response.objects.get(pk=pk)
    response.delete()
    return redirect('../')
