from magi.magicollections import MagiCollection, AccountCollection as _AccountCollection
from magi.utils import CuteFormType, CuteFormTransform
from sukutomo import forms, models

class AccountCollection(_AccountCollection):
    form_class = forms.AccountForm

    filter_cuteform = {
        'accept_friend_requests': {
            'type': CuteFormType.YesNo,
        },
        # 'i_version': {
        #     'to_cuteform': lambda k, v: models.Account.PLAY_WITH_ICONS[k]],
        #     'transform': CuteFormTransform.Flaticon,
        # },
        # 'i_play_with'
        # 'i_os'
    }
