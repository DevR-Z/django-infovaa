"""
URL configuration for infovana project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from infovanaapp import views as v1
from infovanaDB import views as v2

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',v1.home,name='home'),
    path('signin/',v1.signin,name='signin'),
    path('signup/',v1.signup,name='signup'),
    path('logout/',v1.signout,name='logout'),
    path('buscar_titulo/',v1.buscarPelicula,name='buscar_titulo'),
    path('listado_peliculas/',v1.listarPeliculas,name='listado_peliculas'),
    path('listado_series/',v1.listarSeries,name='listado_series'),
    path('detalle_pelicula/<str:imdbID>',v1.detallePelicula, name='detalle_pelicula'),
    path('detalle_serie/<str:imdbID>',v1.detalleSerie, name='detalle_serie'),
    path('detalle_episodio/<str:imdbID>',v1.detalleEpisodio, name='detalle_episodio'),
    path('titulos_guardados',v2.titulosGuardados, name='titulos_guardados'),
    path('titulos_guardados/peliculas/<str:imdbID>',v2.detalle_peliculaGuardada, name='detalle_pelicula_guardada'),
    path('titulos_guardados/series/<str:imdbID>',v2.detalle_serieGuardada, name='detalle_serie_guardada'),
    path('titulos_guardados/series/episodio/<str:imdbID>',v2.detalle_episodioGuardado, name='detalle_episodio_guardado')
]
