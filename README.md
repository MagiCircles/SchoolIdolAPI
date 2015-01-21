![LoveLive! School Idol API Logo](http://i.imgur.com/iICRSYZ.png)

# LoveLive! School Idol API

REST API to get cards from the mobile game Love Live! School Idol Festival.

## API Documentation

### Get the list of cards

```json
GET /cards/

{
    count: 525,
    next: "http://localhost:8000/cards/?page=2",
    previous: null,
    results: [
	{
	    id: 1,
	    name: "Ousaka Shizuku",
	    rarity: "N",
	    attribute: "Smile",
	    is_promo: false,
	    is_special: false,
	    hp: 2,
	    minimum_statistics_smile: 960,
	    minimum_statistics_pure: 450,
	    minimum_statistics_cool: 308,
	    non_idolized_maximum_statistics_smile: 0,
	    non_idolized_maximum_statistics_pure: 0,
	    non_idolized_maximum_statistics_cool: 0,
	    idolized_maximum_statistics_smile: 1340,
	    idolized_maximum_statistics_pure: 690,
	    idolized_maximum_statistics_cool: 500,
	    skill: "",
	    skill_details: "",
	    center_skill: "",
	    card_url: "http://vignette3.wikia.nocookie.net/love-live/images/6/6b/N_1_Shizuku_Osaka.jpg/revision/latest?cb=20140717040003",
	    card_idolized_url: "http://vignette1.wikia.nocookie.net/love-live/images/b/b1/N_1_Transformed_Shizuku_Osaka.jpg/revision/latest?cb=20140717040004"
	},
	...
    ]
}
```

### Get a single card

```
GET /cards/{id}/

See output above.
```

### Navigate, Search & Filter

* Navigate through pages using the `page` parameter:
  * `GET /cards/?page=6`
* You can search through name, skill and center skill using the GET parameter `search`:
  * `GET /cards/?search=Eli`
* You can filter results using the exact values of: `name`, `rarity`, `attribute`, `is_promo`, `is_special`, `hp`, `skill`, `center_skill`:
  * `GET /cards/?rarity=UR&attribute=Smile`

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

##### Update the cards from the internet

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
