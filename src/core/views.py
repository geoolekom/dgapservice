from django.contrib import auth
from django.views.generic import CreateView, View
from core.forms import RegistrationForm
from core.models import User
from django.http import HttpResponse, JsonResponse
import shutil
from dgapservice.settings import MEDIA_ROOT, MEDIA_URL
import json


class RegisterView(CreateView):
	template_name = "core/register.html"
	model = User
	form_class = RegistrationForm
	success_url = '/feed'

	def form_valid(self, form):
		ref = super(RegisterView, self).form_valid(form)
		user = form.save()
		if user is not None and user.is_active:
			auth.login(self.request, user)
		return ref


class UploadView(View):

	def get(self, request):
		return HttpResponse("OK")

	def post(self, request):
		file = request.FILES['file']
		server_name = MEDIA_ROOT + "posts/" + str(request.user) + "_" + file.name
		simple_server_name = MEDIA_URL + "posts/" + str(request.user) + "_" + file.name

		destination = open(server_name, "wb+")
		shutil.copyfileobj(file, destination)
		response = {
			'filelink': simple_server_name,
			'filename': file.name,
		}
		return HttpResponse(json.dumps(response), content_type='application/json')

