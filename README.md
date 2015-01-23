![LoveLive! School Idol API Logo](http://i.imgur.com/iICRSYZ.png)

# LoveLive! School Idol API

REST API to get cards from the mobile game Love Live! School Idol Festival.

## API Documentation

### Get the list of cards

```json
GET /api/cards/

{
    count: 525,
    next: "http://localhost:8000/api/cards/?page=2",
    previous: null,
    results: [
        {
            id: 64,
            name: "Koizumi Hanayo",
            rarity: "UR",
            attribute: "Pure",
            is_promo: false,
            promo_item: null,
            release_date: "2013-04-16",
            japan_only: false,
            is_event: false,
            event: null,
            is_special: false,
            hp: 5,
            minimum_statistics_smile: 3000,
            minimum_statistics_pure: 3740,
            minimum_statistics_cool: 2580,
            non_idolized_maximum_statistics_smile: 4190,
            non_idolized_maximum_statistics_pure: 4930,
            non_idolized_maximum_statistics_cool: 3770,
            idolized_maximum_statistics_smile: 4490,
            idolized_maximum_statistics_pure: 5230,
            idolized_maximum_statistics_cool: 4070,
            skill: "Healer",
            skill_details: "For every 20 notes, there is a 36% chance of recovering players HP by 3. (Level 1)",
            center_skill: "Pure Angel",
            card_url: "http://vignette3.wikia.nocookie.net/love-live/images/c/cf/UR_64_Hanayo_Initial_Ver..jpg/revision/latest?cb=20140717163233",
            card_idolized_url: "http://vignette4.wikia.nocookie.net/love-live/images/2/27/UR_64_Transformed_Hanayo_Initial_Ver..jpg/revision/latest?cb=20140717163233"
        },
	...
    ]
}

```

#### Navigate, Search, Filter & Order

* Navigate through pages using the `page` parameter:
  * `GET /api/cards/?page=6`
* Search through name, skill and center skill using `search`:
  * `GET /api/cards/?search=Eli`
* Filter results using the exact values of `name`, `rarity`, `attribute`, `hp`, `skill`, `center_skill`:
  * `GET /api/cards/?rarity=UR&attribute=Smile`
* Filter results using `True` or `False` for `is_promo`, `is_special` or `is_event`:
  * `GET /api/cards/?is_event=True`
* Sort results by any field using `ordering`:
  * `GET /api/cards/?ordering=name`

### Get a single card

```
GET /api/cards/{id}/

See output above.
```

### Get the list of events

```json
GET /api/events/

{
    count: 42,
    next: "http://localhost:8000/api/events/?page=2",
    previous: null,
    results: [
        {
            japanese_name: "みんな集まれ! Sweet Holiday ことりのおやつ",
            english_name: "Sweet Holiday",
            beginning: "2013-05-03",
            end: "2013-05-16",
            japan_current: false,
            world_current: false,
            cards: [
                    74,
                    75
                ]
        },
        ...
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

## Install

#### 1st time

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
python manage.py syncdb

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
python manage.py syncdb
```

##### Update the cards & events from the internet

```shell
python manage.py importcards
```

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
