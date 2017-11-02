from magi import forms

class AccountForm(forms.AccountForm):
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        #if 'starter' in self.fields:
        #    self.fields['starter'].queryset = models.Card.objects.filter(pk__in=STARTERS)
        if 'fake' in self.fields:
            del(self.fields['fake'])
        if 'transfer_code' in self.fields:
            del(self.fields['transfer_code'])
        if 'nickname' in self.fields and self.request.user.is_authenticated():
            self.fields['nickname'].initial = self.request.user.username

    class Meta(forms.AccountForm.Meta):
        optional_fields = ('rank', 'friend_id', 'accept_friend_requests', 'device', 'start_date',
                           'loveca', 'friend_points', 'g', 'tickets', 'vouchers', 'bought_loveca',
                           'i_play_with', 'i_os')
