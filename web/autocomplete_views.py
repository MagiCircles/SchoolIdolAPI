from dal import autocomplete
from api import models

class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = models.User.objects.all()
        if self.q and len(self.q) >= 3:
            qs = qs.filter(username__istartswith=self.q)
        else:
            return qs.none()
        return qs
