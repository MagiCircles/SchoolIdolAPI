from django.core.management.base import BaseCommand, CommandError
from api import models
from pprint import pprint
import urllib2, urllib
import json
import sys
import datetime

def imageURLToDatabase(URL):
    if URL:
        return URL.replace('http://i.schoolido.lu/', '')
    return None

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        if 'songs' in args:
            page_url = u'http://schoolido.lu/api/songs/?page_size=50&expand_event'
            while page_url is not None:
                response = urllib.urlopen(page_url)
                data = json.loads(response.read())
                page_url = data['next']
                for song in data['results']:
                    data = {
                        'romaji_name': song['romaji_name'],
                        'translated_name': song['translated_name'],
                        'attribute': song['attribute'],
                        'BPM': song['BPM'],
                        'time': song['time'],
                        'main_unit': song['main_unit'],
                        'event': models.Event.objects.get(japanese_name=song['event']['japanese_name']) if song['event'] else None,
                        'rank': song['rank'],
                        'daily_rotation': song['daily_rotation'],
                        'daily_rotation_position': song['daily_rotation_position'],
                        'image': imageURLToDatabase(song['image']),
                        'easy_difficulty': song['easy_difficulty'],
                        'easy_notes': song['easy_notes'],
                        'normal_difficulty': song['normal_difficulty'],
                        'normal_notes': song['normal_notes'],
                        'hard_difficulty': song['hard_difficulty'],
                        'hard_notes': song['hard_notes'],
                        'expert_difficulty': song['expert_difficulty'],
                        'expert_random_difficulty': song['expert_random_difficulty'],
                        'expert_notes': song['expert_notes'],
                        'master_difficulty': song['master_difficulty'],
                        'master_notes': song['master_notes'],
                        'available': song['available'],
                        'itunes_id': song['itunes_id'],
                    }
                    print u'======== Song {} ========'.format(song['name'])
                    pprint(data)
                    models.Song.objects.update_or_create(name=song['name'], defaults=data)
            return

        if 'idols' in args:
            page_url = u'http://schoolido.lu/api/idols/?page_size=50'
            while page_url is not None:
                response = urllib.urlopen(page_url)
                data = json.loads(response.read())
                page_url = data['next']
                for idol in data['results']:
                    data = {
                        'japanese_name': idol['japanese_name'],
                        'main': idol['main'],
                        'main_unit': idol['main_unit'],
                        'sub_unit': idol['sub_unit'],
                        'age': idol['age'],
                        'school': idol['school'],
                        'birthday': datetime.datetime.strptime(idol['birthday'], '%m-%d').date() if idol['birthday'] else None,
                        'astrological_sign': idol['astrological_sign'],
                        'blood': idol['blood'],
                        'height': idol['height'],
                        'measurements': idol['measurements'],
                        'favorite_food': idol['favorite_food'],
                        'least_favorite_food': idol['least_favorite_food'],
                        'hobbies': idol['hobbies'],
                        'attribute': idol['attribute'],
                        'year': idol['year'],
                        'cv': idol['cv']['name'] if idol['cv'] else None,
                        'cv_url': idol['cv']['url'] if idol['cv'] else None,
                        'cv_nickname': idol['cv']['nickname'] if idol['cv'] else None,
                        'cv_twitter': idol['cv']['twitter'] if idol['cv'] else None,
                        'cv_instagram': idol['cv']['instagram'] if idol['cv'] else None,
                        'official_url': idol['official_url'],
                        'summary': idol['summary'],
                    }
                    print u'======== Idol {} ========'.format(idol['name'])
                    pprint(data)
                    models.Idol.objects.update_or_create(name=idol['name'], defaults=data)
            return

        if 'events' in args:
            page_url = u'http://schoolido.lu/api/events/?page_size=50'
            while page_url is not None:
                response = urllib.urlopen(page_url)
                data = json.loads(response.read())
                page_url = data['next']
                for event in data['results']:
                    data = {
                        'romaji_name': event['romaji_name'],
                        'english_name': event['english_name'],
                        'english_t1_points': event['english_t1_points'],
                        'english_t1_rank': event['english_t1_rank'],
                        'english_t2_points': event['english_t2_points'],
                        'english_t2_rank': event['english_t2_rank'],
                        'japanese_t1_points': event['japanese_t1_points'],
                        'japanese_t1_rank': event['japanese_t1_rank'],
                        'japanese_t2_points': event['japanese_t2_points'],
                        'japanese_t2_rank': event['japanese_t2_rank'],
                        'note': event['note'],
                        'image': imageURLToDatabase(event['image']),
                        'english_image': imageURLToDatabase(event['english_image']),
                        'beginning': event['beginning'],
                        'end': event['end'],
                        'english_beginning': event['english_beginning'],
                        'english_end': event['english_end'],
                        'english_name': event['english_name'],
                    }
                    print u'======== Event {} ========'.format(event['japanese_name'])
                    pprint(data)
                    models.Event.objects.update_or_create(japanese_name=event['japanese_name'], defaults=data)
            return

        if 'cards' in args:
            page_url = u'http://schoolido.lu/api/cards/?page_size=50&ordering=-id'
            while page_url is not None:
                response = urllib.urlopen(page_url)
                data = json.loads(response.read())
                page_url = data['next']
                for card in data['results']:
                    data = {}
                    data['idol'] = models.Idol.objects.get(name=card['idol']['name'])
                    if card['event']:
                        data['event'] = models.Event.objects.get(japanese_name=card['event']['japanese_name'])
                    if card['event']:
                        data['event'] = models.Event.objects.get(japanese_name=card['event']['japanese_name'])
                    data['game_id'] = card['game_id']
                    data['japanese_collection'] = card['japanese_collection']
                    #data['english_collection'] = card['english_collection']
                    data['translated_collection'] = card['translated_collection']
                    data['rarity'] = card['rarity']
                    data['attribute'] = card['attribute']
                    data['is_promo'] = card['is_promo']
                    data['promo_item'] = card['promo_item']
                    data['promo_link'] = card['promo_link']
                    data['release_date'] = card['release_date']
                    data['is_special'] = card['is_special']
                    data['japan_only'] = card['japan_only']
                    #data['seal_shop'] = card['seal_shop']
                    data['hp'] = card['hp']
                    data['minimum_statistics_smile'] = card['minimum_statistics_smile']
                    data['minimum_statistics_pure'] = card['minimum_statistics_pure']
                    data['minimum_statistics_cool'] = card['minimum_statistics_cool']
                    data['non_idolized_maximum_statistics_smile'] = card['non_idolized_maximum_statistics_smile']
                    data['non_idolized_maximum_statistics_pure'] = card['non_idolized_maximum_statistics_pure']
                    data['non_idolized_maximum_statistics_cool'] = card['non_idolized_maximum_statistics_cool']
                    data['idolized_maximum_statistics_smile'] = card['idolized_maximum_statistics_smile']
                    data['idolized_maximum_statistics_pure'] = card['idolized_maximum_statistics_pure']
                    data['idolized_maximum_statistics_cool'] = card['idolized_maximum_statistics_cool']
                    data['skill'] = card['skill']
                    data['japanese_skill'] = card['japanese_skill']
                    data['skill_details'] = card['skill_details']
                    data['japanese_skill_details'] = card['japanese_skill_details']
                    data['center_skill'] = card['center_skill']
                    data['transparent_image'] = imageURLToDatabase(card['transparent_image'])
                    data['transparent_idolized_image'] = imageURLToDatabase(card['transparent_idolized_image'])
                    data['card_image'] = imageURLToDatabase(card['card_image'])
                    data['card_idolized_image'] = imageURLToDatabase(card['card_idolized_image'])
                    data['english_card_image'] = imageURLToDatabase(card['english_card_image'])
                    data['english_card_idolized_image'] = imageURLToDatabase(card['english_card_idolized_image'])
                    data['round_card_image'] = imageURLToDatabase(card['round_card_image'])
                    data['round_card_idolized_image'] = imageURLToDatabase(card['round_card_idolized_image'])
                    data['english_round_card_image'] = imageURLToDatabase(card['english_round_card_image'])
                    data['english_round_card_idolized_image'] = imageURLToDatabase(card['english_round_card_idolized_image'])
                    data['clean_ur'] = imageURLToDatabase(card['clean_ur'])
                    data['clean_ur_idolized'] = imageURLToDatabase(card['clean_ur_idolized'])
                    data['video_story'] = card['video_story']
                    data['japanese_video_story'] = card['japanese_video_story']
                    print '======== Card #{} ========'.format(card['id'])
                    pprint(data)
                    models.Card.objects.update_or_create(id=card['id'], defaults=data)
            return

        if 'ur_pairs' in args:
            page_url = u'http://schoolido.lu/api/cards/?page_size=50&rarity=UR'
            while page_url is not None:
                response = urllib.urlopen(page_url)
                data = json.loads(response.read())
                page_url = data['next']
                for card in data['results']:
                    data = {}
                    pprint(card)
                    data['ur_pair'] = models.Card.objects.get(pk=card['ur_pair']['card']['id']) if card['ur_pair'] else None
                    data['ur_pair_reverse'] = card['ur_pair']['reverse_display'] if card['ur_pair'] else False
                    data['ur_pair_idolized_reverse'] = card['ur_pair']['reverse_display_idolized'] if card['ur_pair'] else False
                    data['clean_ur'] = card['clean_ur']
                    data['clean_ur_idolized'] = imageURLToDatabase(card['clean_ur_idolized'])
                    print '======== Card #{} ========'.format(card['id'])
                    pprint(data)
                    models.Card.objects.update_or_create(id=card['id'], defaults=data)
            return

        if 'imageURLs' in args:
            cards = models.Card.objects.all()
            for card in cards:
                card.card_idolized_image = 'cards/' + str(card.id) + 'idolized' + card.name.split(' ')[-1] + '.png'
                card.transparent_idolized_image = 'cards/transparent/' + str(card.id) + 'idolizedTransparent.png'
                card.round_card_idolized_image = 'cards/' + str(card.id) + 'RoundIdolized' + card.name.split(' ')[-1] + '.png'
                if not card.is_special and not card.is_promo:
                    card.card_image = 'cards/' + str(card.id) + card.name.split(' ')[-1] + '.png'
                    card.transparent_image = 'cards/transparent/' + str(card.id) + 'Transparent.png'
                    card.round_card_image = 'cards/' + str(card.id) + 'Round' + card.name.split(' ')[-1] + '.png'
                else:
                    card.card_image = None
                    card.transparent_image = None
                    card.round_card_image = None
                card.save()
            return
