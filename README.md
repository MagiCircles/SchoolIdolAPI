![LoveLive! School Idol API Logo](http://i.imgur.com/iICRSYZ.png)

# LoveLive! School Idol API

REST API to get cards from the mobile game Love Live! School Idol Festival.

## API Documentation

### Get the list of cards

```json
GET /api/cards/

{
    "count": 533,
    "next": "http://schoolido.lu/api/cards/?page=2",
    "previous": null,
    "results": [
        {
            "id": 509,
            "name": "Minami Kotori",
            "japanese_name": "南ことり",
            "japanese_collection": "おせち編",
            "rarity": "SR",
            "attribute": "Cool",
            "japanese_attribute": "クール",
            "is_promo": false,
            "promo_item": null,
            "release_date": "2015-01-05",
            "japan_only": true,
            "event": {
                "japanese_name": "Score Match Round 15",
                "english_name": "Score Match Round 15",
                "beginning": "2015-01-05",
                "end": "2015-01-15",
                "japan_current": false,
                "world_current": false,
                "cards": [
                    508,
                    509
                ]
            },
            "is_special": false,
            "hp": 3,
            "minimum_statistics_smile": 2760,
            "minimum_statistics_pure": 2420,
            "minimum_statistics_cool": 3610,
            "non_idolized_maximum_statistics_smile": 3590,
            "non_idolized_maximum_statistics_pure": 3250,
            "non_idolized_maximum_statistics_cool": 4440,
            "idolized_maximum_statistics_smile": 3870,
            "idolized_maximum_statistics_pure": 3530,
            "idolized_maximum_statistics_cool": 4720,
            "skill": "Perfect Lock",
            "japanese_skill": "幸せの香り",
            "skill_details": null,
            "japanese_skill_details": "",
            "center_skill": "Cool Heart",
            "japanese_center_skill": "クールハート",
            "japanese_center_skill_details": "",
            "card_image": "http://schoolido.lu/static/cards/509.jpg",
            "card_idolized_image": "http://schoolido.lu/static/cards/509idolized.jpg",
            "round_card_image": "http://schoolido.lu/static/cards/509round.jpg",
            "website_url": "http://schoolido.lu/cards/509/",
            "owned_cards": null
        },
        ...
    ]
}

```

#### Navigate, Search, Filter & Order

* Navigate through pages using the `page` parameter:
  * `GET /api/cards/?page=6`
* Search using `search`:
  * `GET /api/cards/?search=Eli`
  * _Will search through 'name', 'japanese_name', 'skill', 'japanese_skill', 'skill_details', 'japanese_skill_details', 'center_skill', 'japanese_center_skill','japanese_center_skill_details','japanese_collection','promo_item','event__english_name','event__japanese_name'_
* Filter results using the exact values of `name`, `rarity`, `attribute`, `japanese_collection`, `hp`, `skill`, `center_skill`:
  * `GET /api/cards/?rarity=UR&attribute=Smile`
* Filter results using `True` or `False` for `is_promo`, `is_special` or `is_event`:
  * `GET /api/cards/?is_event=True`
* Sort results by any field using `ordering`:
  * `GET /api/cards/?ordering=name`
* To get default images instead of empty fields, use `imagedefault` with `True` or `False`:
```json
GET /api/cards/?ordering=name

...
            "card_image": "http://localhost:9000/static/default-Cool.png",
	    "card_idolized_image": "http://localhost:9000/static/default-Cool.png",
	    "round_card_image": "http://localhost:9000/static/circle-Cool.png",
...
```
* To fill information about the cards owned by a user, use `account` (otherwise the field is null):
```json
GET /api/cards/?account=1

...
            owned_cards: [
                {
                    "idolized": false,
                    "stored": "Deck",
                    "expiration": null,
                    "max_level": false,
                    "max_bond": false
                }
            ]
...
```

### Get a single card

```json
GET /api/cards/{id}/

See output above.
```

### Get only card ids

```json
GET /api/cardids/

[
    1,
    2,
    3,
    ...
]
```
This endpoint allows you to get only the card ids instead of the whole card objects
and is not paginated, so you get all the results at once.
All search, filter and order parameters of the regular card endpoint work here as well.

### Get the list of events

```json
GET /api/events/

{
    "count": 43,
    "next": "http://schoolido.lu/api/events/?page=2",
    "previous": null,
    "results": [
        {
            "japanese_name": "みんな集まれ! Sweet Holiday ことりのおやつ",
            "english_name": "Sweet Holiday",
            "beginning": "2013-05-03",
            "end": "2013-05-16",
            "japan_current": false,
            "world_current": false,
            "cards": [
                74,
                75
            ]
        }, ...
    ]
}
```

#### Navitate, Search

* Navigate through pages using the `page` parameter:
  * `GET /api/events/?page=2`
* Search through english or japanese names using the `search` parameter:
  * `GET /api/events/?search=medley`
* Sort results by any field using `ordering`:
  * `GET /api/events/?ordering=english_name`

---

## Contribute

Browse issues to find something to do: [![Stories in Ready](https://badge.waffle.io/db0company/SchoolIdolAPI.png?label=ready&title=Ready)](https://waffle.io/db0company/SchoolIdolAPI)

_Note: To contribute to [School Idol Contest](http://schoolido.lu/contest/), go to [the other repo](https://github.com/Engil/SchoolIdolContest)._

#### Install the 1st time

```shell
# Install pre-requirements
apt-get install libpython-dev libffi-dev python-virtualenv libmysqlclient-dev

# Create a virtualenv to isolate the package dependencies locally
virtualenv env
source env/bin/activate

# Clone the repo
git clone git@github.com:db0company/SchoolIdolAPI.git
cd SchoolIdolAPI

# Install packages, no need to be root
pip install -r requirements.txt

# Create tables, initialize database
python manage.py migrate

# Fill database with cards
python manage.py importcards
```

#### Anytime

##### Reactivate the environment
```shell
source env/bin/activate
```

##### Launch the server

```shell
python manage.py runserver
```
If you want it to be externally visible, add an extra argument `0.0.0.0:8000`.

No need to restart it to see your modifications, the server reloads itself automatically.

##### Whenever you change the models

```shell
python manage.py makemigrations
python manage.py migrate
```

##### Update the cards & events from the internet

```shell
python manage.py importcards
```

Extra command line arguments:
- `redownload` will download the images for the cards, even when they already have been downloaded
- `delete` will remove all information about `cards` and `events` in the database
- `local` will consider you already have the `*.html` files with information at the root of the repo and will not download them from the internet (good for testing & development)

## Credits & Thanks

Informations about the cards come from:
* [LoveLive! School Idol Wiki decaf.kouhi.me](http://decaf.kouhi.me/lovelive/)
* [LoveLive! Wikia](http://love-live.wikia.com/wiki/Main_Page)

## Copyright/License

    Copyright 2015 Deby Barbara Lepage <db0company@gmail.com>
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.    


## Up to date

Latest version is on GitHub :
* https://github.com/db0company/SchoolIdolAPI
