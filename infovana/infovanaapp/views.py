from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from infovanaDB.models import Titulo,Movie,Serie,Episode,TituloxUser

from decouple import config
import requests

# Create your views here.

def home(request):
	return render(request,'infovana_home.html')

def signin(request):
	if request.user.is_authenticated:
		return redirect('buscar_titulo')
	if request.method=='GET':
		return render(request,'signin.html',{
		    'form': AuthenticationForm
		})
	else:
	    user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
	    if user is None:
	        return render(request,'signin.html',{
	            'form': AuthenticationForm,
	            'error': 'Username or password is incorrect!'
	        })
	    else:
	        login(request,user)
	        return redirect('buscar_titulo')

def signup(request):
    if request.method=='GET':
        return render(request,'signup.html',{
            'form': UserCreationForm
        })
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('buscar_titulo')
            except IntegrityError:
                return render(request,'signup.html',{
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })
        return render(request,'signup.html',{
            'form': UserCreationForm,
            'error': 'Passwords do not match'
        })

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def request_api_by_name_and_type(type,nombre_pelicula):
	url="https://www.omdbapi.com/"
	apikey=config('APIKEY')
	all_titulos,n=[],1
	for i in range(1,4):
		params ={
			"apikey":apikey,
			"s":nombre_pelicula, 
			"type":type,
			"page":i
		}
		response = requests.get(url, params=params)
		data = response.json()
		if data.get("Response")=="True":
			rows_movies=data.get("Search")
			for row in rows_movies:
				row_movie={
					"id":n,
					"imdbID":row.get("imdbID"),
					"Title":row.get("Title"),
					"Year":row.get("Year")
				}
				n+=1
				all_titulos.append(row_movie)
	return all_titulos

def request_api_by_id(imdbID):
	url="https://www.omdbapi.com/"
	apikey=config('APIKEY')
	params={
		"apikey":apikey,
		"i":imdbID
	}
	response=requests.get(url,params=params)
	data=response.json()
	all_details=[{
		"imdbID":data.get("imdbID"),
		"title":data.get("Title"),
		"plot":data.get("Plot"),
		"year":data.get("Year"),
		"released":data.get("Released"),
		"genre":data.get("Genre"),
		"language":data.get("Language"),
		"type":data.get("Type"),
		"imdbRating":data.get("imdbRating"),
		"poster":data.get("Poster"),
		"runtime":data.get("Runtime") if data.get("Type")!="series" else "N/A",
		"totalSeasons":data.get("totalSeasons") if data.get("Type")=="series" else "N/A",
		"season":data.get("Season") if data.get("Type")=="episode" else "N/A",
		"episode":data.get("Episode") if data.get("Type")=="episode" else "N/A"
	}]
	return all_details

def request_api_by_season(title_serie,season):
	url="https://www.omdbapi.com/"
	apikey=config('APIKEY')
	params={
		"apikey":apikey,
		"t":title_serie,
		"Season":season
	}
	response=requests.get(url,params=params)
	data=response.json()
	return data

@login_required
def buscarPelicula(request):
    return render(request,'search.html')

@login_required
def listarPeliculas(request):
    if request.method=='POST':
        lista_peliculas=request_api_by_name_and_type('movie',request.POST['movie']) #genera [{},{}]
        return render(request,'listado_titulos.html',{
        	'lista_peliculas':lista_peliculas,
        	'type':'peliculas'})

@login_required
def listarSeries(request):
	if request.method=='POST':
	    lista_series=request_api_by_name_and_type('series',request.POST['serie'])
	    return render(request,'listado_titulos.html',{
	    	'lista_series':lista_series,
	    	'type':'series'})

@login_required
def detallePelicula(request,imdbID):
	if request.method=='GET':
		cnt_as_favorite_movie = TituloxUser.objects.filter(imdbID=imdbID).count()
		detalle_pelicula=request_api_by_id(imdbID)
		return render(request,'detalle_pelicula.html',{
			'detalle_pelicula':detalle_pelicula[0],
			'cnt_as_favorite_movie':cnt_as_favorite_movie})
	if request.method=='POST':
		not_first_time=request.POST.get('imdbID',None) #verifica si entró por primera vez, ya que al dar "ver detalle" no se envia el imdbID al post
		if not not_first_time: #si es primera vez, no hay imdbID, por lo que not_first_time=None(False), entonces el if es True
			cnt_as_favorite_movie = TituloxUser.objects.filter(imdbID=imdbID).count()
			detalle_pelicula=request_api_by_id(imdbID)
			pelicula_added = TituloxUser.objects.filter(imdbID=imdbID,user=request.user).exists()
			añadido=True if pelicula_added else False
			return render(request,'detalle_pelicula.html',{
				'detalle_pelicula':detalle_pelicula[0],
				'añadido':añadido,
				'cnt_as_favorite_movie':cnt_as_favorite_movie})
		if request.POST.get('remove',None):
			tituloxuser_instance=get_object_or_404(TituloxUser,imdbID=imdbID,user=request.user)
			tituloxuser_instance.delete()
			print(f'El usuario {request.user.username} ha borrado la pelicula {tituloxuser_instance.imdbID.title} de favoritos')
			return redirect('detalle_pelicula',imdbID=imdbID) #redirige a la url con su imdbID correspondiente con el metodo GET
		if request.POST.get('add',None):	
			pelicula_added = TituloxUser.objects.filter(imdbID=imdbID,user=request.user).exists()
			detalle_pelicula={key: request.POST.get(key,None) for key in request.POST if key!='add' or key!='remove'}
			if not pelicula_added:
				titulo_exists = Titulo.objects.filter(imdbID=imdbID).exists()
				if not titulo_exists:
					titulo_instance=Titulo.objects.create(imdbID=detalle_pelicula['imdbID'],title=detalle_pelicula['title'],
							year=detalle_pelicula['year'],released=detalle_pelicula['released'],genre=detalle_pelicula['genre'],
							language=detalle_pelicula['language'],type=detalle_pelicula['type'],
							imdbRating=detalle_pelicula['imdbRating'],poster=detalle_pelicula['poster'],
							plot=detalle_pelicula['plot'])
					Movie.objects.create(imdbID=titulo_instance,runtime=detalle_pelicula['runtime'])
				else:
					titulo_instance=Titulo.objects.get(imdbID=imdbID)
				TituloxUser.objects.create(imdbID=titulo_instance,user=request.user)
				añadido=True
				print(f"El usuario {request.user.username} ha añadido la pelicula {titulo_instance.title} en favoritos")
			else:
				añadido=False
			cnt_as_favorite_movie = TituloxUser.objects.filter(imdbID=imdbID).count()
			return render(request,'detalle_pelicula.html',{
				'detalle_pelicula':detalle_pelicula,
				'añadido':añadido,
				'cnt_as_favorite_movie':cnt_as_favorite_movie})

@login_required
def detalleSerie(request,imdbID):
	if request.method=='GET':
		cnt_as_favorite_serie = TituloxUser.objects.filter(imdbID=imdbID).count()
		detalle_serie=request_api_by_id(imdbID)
		temporada_seleccionada=int(request.GET.get("temporada",1))
		temporadas=[i for i in range(1,int(detalle_serie[0]['totalSeasons'])+1)]
		episodios=request_api_by_season(detalle_serie[0]["title"],temporada_seleccionada)
		episodios_data=[episodio for episodio in episodios['Episodes']]
		return render(request,'detalle_serie.html',{
			'temporadas':temporadas,
			'detalle_serie':detalle_serie[0],
			'episodios_data':episodios_data,
			'temporada_seleccionada':temporada_seleccionada,
			'cnt_as_favorite_serie':cnt_as_favorite_serie})
	if request.method=='POST':
		not_first_time = request.POST.get('imdbID',None)
		if not not_first_time:
			cnt_as_favorite_serie = TituloxUser.objects.filter(imdbID=imdbID).count()
			detalle_serie=request_api_by_id(imdbID)
			temporada_seleccionada=int(request.GET.get("temporada",1))
			temporadas=[i for i in range(1,int(detalle_serie[0]['totalSeasons'])+1)]
			episodios=request_api_by_season(detalle_serie[0]["title"],temporada_seleccionada)
			episodios_data=[episodio for episodio in episodios['Episodes']]
			serie_exists = TituloxUser.objects.filter(imdbID=imdbID,user=request.user).exists()
			añadido=True if serie_exists else False
			return render(request,'detalle_serie.html',{
				'temporadas':temporadas,
				'detalle_serie':detalle_serie[0],
				'episodios_data':episodios_data,
				'temporada_seleccionada':temporada_seleccionada,
				'añadido':añadido,
				'cnt_as_favorite_serie':cnt_as_favorite_serie})
		if request.POST.get('remove',None):
			tituloxuser_instance=get_object_or_404(TituloxUser,imdbID=imdbID,user=request.user)
			tituloxuser_instance.delete()
			print(f'El usuario {request.user.username} ha borrado la serie {tituloxuser_instance.imdbID.title} de favoritos')
			return redirect('detalle_serie',imdbID=imdbID)
		if request.POST.get('add',None):
			serie_exists = TituloxUser.objects.filter(imdbID=imdbID,user=request.user).exists()
			detalle_serie={key: request.POST.get(key,None) for key in request.POST if key!='add' or key!='remove'}
			if not serie_exists:
				titulo_exists = Titulo.objects.filter(imdbID=imdbID).exists()
				if not titulo_exists:
					titulo_serie_instance = Titulo.objects.create(imdbID=detalle_serie['imdbID'],title=detalle_serie['title'],
							year=detalle_serie['year'],released=detalle_serie['released'],genre=detalle_serie['genre'],
							language=detalle_serie['language'],type=detalle_serie['type'],
							imdbRating=detalle_serie['imdbRating'],poster=detalle_serie['poster'],
							plot=detalle_serie['plot'])
					print("titulo_serie_instance añadido")
					serie_instance = Serie.objects.create(imdbID=titulo_serie_instance,totalSeasons=detalle_serie['totalSeasons'])
					print("serie_instance añadido")
					for i in range(1,int(detalle_serie['totalSeasons'])+1):
						episodios=request_api_by_season(detalle_serie['title'],i)
						titulo_episode_bulk_insert,episode_bulk_insert=[],[]
						for episodio in episodios['Episodes']:
							detalle_episodio=request_api_by_id(episodio['imdbID'])[0]
							varTitulo=Titulo(imdbID=detalle_episodio['imdbID'],title=detalle_episodio['title'],
								year=detalle_episodio['year'],released=detalle_episodio['released'],genre=detalle_episodio['genre'],
								language=detalle_episodio['language'],type=detalle_episodio['type'],
								imdbRating=detalle_episodio['imdbRating'],poster=detalle_episodio['poster'],
								plot=detalle_episodio['plot'])
							titulo_episode_bulk_insert.append(varTitulo)
							varEpisode=Episode(imdbID=varTitulo,
								imdbID_serie=serie_instance, season=detalle_episodio['season'],
								episode=detalle_episodio['episode'],runtime=detalle_episodio['runtime'])
							episode_bulk_insert.append(varEpisode)
							print(f"{serie_instance.imdbID.title}-{varEpisode.season}x{varEpisode.episode} añadido")
						Titulo.objects.bulk_create(titulo_episode_bulk_insert)
						Episode.objects.bulk_create(episode_bulk_insert)
						print(f"{serie_instance.imdbID.title}-Season {i} añadido")
				else:
					titulo_serie_instance = Titulo.objects.get(imdbID=imdbID)
				TituloxUser.objects.create(imdbID=titulo_serie_instance,user=request.user)
				añadido=True
				print(f"El usuario {request.user.username} ha añadido la serie {titulo_serie_instance.title} en favoritos")
			else:
				añadido=False
			cnt_as_favorite_serie = TituloxUser.objects.filter(imdbID=imdbID).count()
			temporada_seleccionada=int(request.GET.get("temporada",1))
			temporadas=[i for i in range(1,int(detalle_serie.get('totalSeasons'),0)+1)]
			episodios=request_api_by_season(detalle_serie.get('title',None),temporada_seleccionada)
			episodios_data=[episodio for episodio in episodios['Episodes']]
			return render(request,'detalle_serie.html',{
				'detalle_serie':detalle_serie,
				'temporada_seleccionada':temporada_seleccionada,
				'temporadas':temporadas,
				'episodios_data':episodios_data,
				'añadido':añadido,
				'cnt_as_favorite_serie':cnt_as_favorite_serie})

@login_required
def detalleEpisodio(request,imdbID):
	detalle_episodio=request_api_by_id(imdbID)
	return render(request,'detalle_episodio.html',{
		'detalle_episodio':detalle_episodio[0],
		'titulo_serie':request.POST.get('titulo_serie')})
