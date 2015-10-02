from django.db import models
import api.models as api_models

class Contest(models.Model):
	begin = models.DateTimeField(null=True)
	end = models.DateTimeField(null=True)
	name = models.CharField(max_length=300)
	best_girl = models.BooleanField(default=False)
	best_card = models.BooleanField(default=False)
	query = models.CharField(max_length=4092, null=True)

	def set_query(self, queryset):
		from django.db import connection
		sql, formatters = queryset._as_sql(connection)
		self.query = sql % formatters

	def get_query(self):
		return api_models.Card.objects.raw(self.query)

class Vote(models.Model):
	contest = models.ForeignKey(Contest, related_name='votes')
	card = models.ForeignKey(api_models.Card, related_name='votes')
	idolized = models.BooleanField(default=False)
	counter = models.PositiveIntegerField(default=0)

class Session(models.Model):
	right = models.ForeignKey(Vote, related_name='right')
	left = models.ForeignKey(Vote, related_name='left')
	fingerprint = models.CharField(max_length=300)
	contest = models.ForeignKey(Contest, related_name='sessions')
	token = models.CharField(max_length=36)
	date = models.DateTimeField()
