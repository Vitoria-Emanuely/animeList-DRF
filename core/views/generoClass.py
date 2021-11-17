from django.http import HttpResponse, JsonResponse
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from core.models import Genero


@method_decorator(csrf_exempt, name="dispatch")
class GeneroView(View):
    def get(self, request, id=None):
        if id:
            qs = Genero.objects.get(id=id)
            data = {}
            data['id'] = qs.id
            data['descricao'] = qs.descricao
            return JsonResponse(data)
        else:    
            data = list(Genero.objects.values())
            formatted_data = json.dumps(data, ensure_ascii=False)
            return HttpResponse(formatted_data, content_type="application/json")

    def post(self, request):
        json_data = json.loads(request.body)  
        novo_genero = Genero.objects.create(**json_data)
        data = {"id": novo_genero.id, "descricao": novo_genero.descricao}
        return JsonResponse(data)

    def patch(self, request, id):
        json_data = json.loads(request.body)
        qs = Genero.objects.get(id=id)
        qs.descricao = json_data['descricao'] # if "descricao" in json_data else qs.descricao
        qs.save()
        data = {}
        data['id'] = qs.id
        data['descricao'] = qs.descricao
        return JsonResponse(data)

    def delete(self, request, id):
        qs = Genero.objects.get(id=id)
        qs.delete()
        data = { "mensagem": "Item excluído com sucesso!" }
        return JsonResponse(data)    