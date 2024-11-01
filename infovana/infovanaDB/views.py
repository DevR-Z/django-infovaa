from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import TituloxUser,Titulo,Movie,Serie,Episode

# Create your views here.
@login_required
def titulosGuardados(request):
	peliculas_guardadas=Movie.objects.filter(imdbID__tituloxuser__user=request.user,imdbID__type='movie')
	series_guardadas=Serie.objects.filter(imdbID__tituloxuser__user=request.user,imdbID__type='series')
	return render(request,'titulos_guardados.html',{
		'peliculas_guardadas':peliculas_guardadas,
		'series_guardadas':series_guardadas})

@login_required
def detalle_peliculaGuardada(request,imdbID):
	if request.method=='GET':
		cnt_as_favorite_movie = TituloxUser.objects.filter(imdbID=imdbID).count()
		detalle_pelicula = Movie.objects.filter(imdbID=imdbID)
		return render(request,'detalle_pelicula_guardada.html',{
			'detalle_pelicula':detalle_pelicula[0],
			'cnt_as_favorite_movie':cnt_as_favorite_movie})
	if request.method=='POST':
		first_time=TituloxUser.objects.filter(user=request.user,imdbID=imdbID).exists()
		if request.POST.get('remove',None):
			tituloxuser_instance = get_object_or_404(TituloxUser,imdbID=imdbID,user=request.user)
			tituloxuser_instance.delete()
			print(f'El usuario {request.user.username} ha borrado la pelicula {tituloxuser_instance.imdbID.title} de favoritos')
			return redirect('detalle_pelicula_guardada',imdbID=imdbID)
		if first_time:
			cnt_as_favorite_movie = TituloxUser.objects.filter(imdbID=imdbID).count()
			detalle_pelicula = Movie.objects.filter(imdbID=imdbID)
			return render(request,'detalle_pelicula_guardada.html',{
				'detalle_pelicula':detalle_pelicula[0],
				'añadido':True,
				'cnt_as_favorite_movie':cnt_as_favorite_movie})
		if request.POST.get('add',None):
			titulo_instance = Titulo.objects.get(imdbID=imdbID)
			tituloxuser_instance = TituloxUser.objects.create(imdbID=titulo_instance,user=request.user)
			detalle_pelicula=Movie.objects.filter(imdbID=imdbID)
			cnt_as_favorite_movie = TituloxUser.objects.filter(imdbID=imdbID).count()
			print(f"El usuario {request.user.username} ha añadido la pelicula {titulo_instance.title} en favoritos")
			return render(request,'detalle_pelicula_guardada.html',{
				'detalle_pelicula':detalle_pelicula[0],
				'añadido':True,
				'cnt_as_favorite_movie':cnt_as_favorite_movie})
get_object_or_404
@login_required
def detalle_serieGuardada(request,imdbID):
	if request.method=='GET':
		detalle_serie = Serie.objects.filter(imdbID=imdbID)
		list_temporadas = [i for i in range(1,int(detalle_serie[0].totalSeasons)+1)]
		temporada_seleccionada = int(request.GET.get('temporada',1))
		episodios_data = Episode.objects.filter(imdbID_serie=imdbID,season=temporada_seleccionada)
		cnt_as_favorite_serie = TituloxUser.objects.filter(imdbID=imdbID).count()
		serie_added = TituloxUser.objects.filter(imdbID=imdbID,user=request.user).exists()
		añadido=True if serie_added else False 
		return render(request,'detalle_serie_guardada.html',{
			'detalle_serie':detalle_serie[0],
			'list_temporadas':list_temporadas,
			'temporada_seleccionada':temporada_seleccionada,
			'episodios_data':episodios_data,
			'cnt_as_favorite_serie':cnt_as_favorite_serie,
			'añadido':añadido})
	if request.method=='POST':
		first_time=TituloxUser.objects.filter(user=request.user,imdbID=imdbID)
		if request.POST.get('remove',None):
			tituloxuser_instance = get_object_or_404(TituloxUser,imdbID=imdbID,user=request.user)
			tituloxuser_instance.delete()
			print(f'El usuario {request.user.username} ha borrado la serie {tituloxuser_instance.imdbID.title} de favoritos')
			return redirect('detalle_serie_guardada',imdbID=imdbID)
		if first_time:
			detalle_serie = Serie.objects.filter(imdbID=imdbID)
			list_temporadas = [i for i in range(1,int(detalle_serie[0].totalSeasons)+1)]
			temporada_seleccionada = int(request.GET.get('temporada',1))
			episodios_data = Episode.objects.filter(imdbID_serie=imdbID,season=temporada_seleccionada)
			cnt_as_favorite_serie = TituloxUser.objects.filter(imdbID=imdbID).count()
			return render(request,'detalle_serie_guardada.html',{
				'detalle_serie':detalle_serie[0],
				'list_temporadas':list_temporadas,
				'temporada_seleccionada':temporada_seleccionada,
				'episodios_data':episodios_data,
				'cnt_as_favorite_serie':cnt_as_favorite_serie,
				'añadido':True})
		if request.POST.get('add',None):
			titulo_instance = Titulo.objects.get(imdbID=imdbID)
			tituloxuser_instance = TituloxUser.objects.create(user=request.user,imdbID=titulo_instance)
			detalle_serie = Serie.objects.filter(imdbID=imdbID)
			list_temporadas = [i for i in range(1,int(detalle_serie[0].totalSeasons)+1)]
			temporada_seleccionada = int(request.GET.get('temporada',1))
			episodios_data = Episode.objects.filter(imdbID_serie=imdbID,season=temporada_seleccionada)
			cnt_as_favorite_serie = TituloxUser.objects.filter(imdbID=imdbID).count()
			return render(request,'detalle_serie_guardada.html',{
				'detalle_serie':detalle_serie[0],
				'list_temporadas':list_temporadas,
				'temporada_seleccionada':temporada_seleccionada,
				'episodios_data':episodios_data,
				'cnt_as_favorite_serie':cnt_as_favorite_serie,
				'añadido':True})

@login_required
def detalle_episodioGuardado(request,imdbID):
	detalle_episodio = Episode.objects.filter(imdbID=imdbID)
	return render(request,'detalle_episodio_guardado.html',{
		'detalle_episodio':detalle_episodio[0]})