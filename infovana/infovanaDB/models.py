from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Titulo(models.Model):
	imdbID = models.CharField(max_length=255, primary_key=True)
	title = models.CharField(max_length=255)
	year = models.CharField(max_length=20)
	released = models.CharField(max_length=255)
	genre = models.CharField(max_length=255)
	language = models.CharField(max_length=255)
	type = models.CharField(max_length=255)
	imdbRating = models.CharField(max_length=10) #o FloatField() en caso no haya valores N/A
	poster = models.CharField(max_length=255)
	plot = models.CharField(max_length=255)

	def __str__(self):
		return f"Titulo: {self.imdbID}: {self.title}"

class Movie(models.Model):
	imdbID = models.OneToOneField(Titulo,on_delete=models.CASCADE,primary_key=True)
	runtime = models.CharField(max_length=255,null=True)

	def __str__(self):
		return f"Movie: {self.imdbID.imdbID}: {self.imdbID.title}"

class Serie(models.Model):
	imdbID = models.OneToOneField(Titulo,on_delete=models.CASCADE,primary_key=True)
	totalSeasons = models.IntegerField()

	def __str__(self):
		return f"Serie: {self.imdbID.imdbID}: {self.imdbID.title}"

class Episode(models.Model):
	imdbID = models.OneToOneField(Titulo,on_delete=models.CASCADE,primary_key=True)
	imdbID_serie = models.ForeignKey(Serie,on_delete=models.CASCADE)
	season = models.IntegerField()
	episode = models.IntegerField()
	runtime = models.CharField(max_length=255)

	def __str__(self):
		return f"Episode: {self.imdbID.imdbID},Serie {self.imdbID_serie.imdbID.title} {self.season}x{self.episode}"

class TituloxUser(models.Model):
	imdbID = models.ForeignKey(Titulo,on_delete=models.CASCADE)
	user = models.ForeignKey(User,on_delete=models.CASCADE)

	class Meta:
		constraints = [models.UniqueConstraint(fields=['imdbID','user'],name='unique_tituloxuser')]

	def __str__(self):
		return f"{self.user.username}-{self.imdbID.title} : {self.imdbID.imdbID}"