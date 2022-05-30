# from django.http.response import HttpResponse
# from django.shortcuts import render
# from django.urls.base import reverse_lazy
# from django.views import View
# from boardgames.models import BoardGame
# import json


# class GetFormView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, "suggestion_app/suggestion_form.html")

#     def post(self, request, *args, **kwargs):
#         data_from_user = request.POST
#         queryset = BoardGame.objects.prefetch_related("themes").prefetch_related("game_mechanics")
#         for boardgame in queryset:
#             bg_rank = sum([
#                 self.process_is_party_game(boardgame, data_from_user.get("party_family")),
#                 self.process_game_themes(boardgame, data_from_user.get("themes")),
#                 self.process_game_mechanics(boardgame, data_from_user.get("mechanics")),
#                 self.process_duration(boardgame, data_from_user.get("duration")),
#                 self.process_is_allowed_for_one(boardgame, data_from_user.get("allow_one")),
#                 self.process_has_age_restriction(boardgame, data_from_user.get("age_restriction")),
#                 self.process_price(boardgame, data_from_user.get("price")),
#             ])
#             boardgame.rank = bg_rank
#         print([(bg.name, bg.rank) for bg in list(sorted(queryset, key=lambda x: x.rank))[::-1][:5]])
#         max_rank = max(bg.rank for bg in queryset)
#         filtered_bgs = list(filter(lambda x: x.rank and x.rank == max_rank, queryset))
#         request.session['ids_to_load'] = [bg.id for bg in filtered_bgs]
#         response = {
#             'status': 1,
#             'message': 'Всё хорошо',
#             'url': str(reverse_lazy('boardgames:search_for_bg'))
#         }
#         return HttpResponse(json.dumps(response), content_type='application/json')
        
#     def process_is_party_game(self, boardgame, party_or_family):
#         if party_or_family:
#             if party_or_family == "party":
#                 return 10 if boardgame.is_party_game else 0
#             else:
#                 return 10 if not boardgame.is_party_game else 0
#         return 0

#     def process_game_themes(self, boardgame, themes):
#         rank = 0
#         for theme in themes.split(','):
#             if theme in boardgame.themes.all():
#                 rank += 10 
#         return rank

#     def process_game_mechanics(self, boardgame, mechanics):
#         rank = 0
#         for mechanic in mechanics.split(','):
#             if mechanic in boardgame.game_mechanics.all():
#                 rank += 10 
#         return rank

#     def process_duration(self, boardgame, duration):
#         if duration:
#             if duration == "<1hour":
#                 return 10 if boardgame.game_avg_duration < 1 else 0
#             else:
#                 return 10 if boardgame.game_avg_duration > 1 else 0
#         return 0

#     def process_is_allowed_for_one(self, boardgame, is_allowed_for_one):
#         if is_allowed_for_one:
#             if is_allowed_for_one == "Yes":
#                 return 10 if boardgame.players_qty.split("-")[0] == "1" else 0
#             else:
#                 return 10 if boardgame.players_qty.split("-")[0] != "1" else 0
#         return 0

#     def process_has_age_restriction(self, boardgame, has_age_restriction):
#         if has_age_restriction:
#             if has_age_restriction == "Yes":
#                 return 10 if int(boardgame.age_restriction[:-1]) < 18 else 0
#             else:
#                 return 10 if int(boardgame.age_restriction[:-1]) >= 18 else 0
#         return 0

#     def process_price(self, boardgame, price_gap):
#         if price_gap:
#             if price_gap == "cheap":
#                 return 30 if boardgame.price < 50 else 0
#             elif price_gap == "middle":
#                 return 30 if boardgame.price >= 50 and boardgame.price < 100 else 0
#             elif price_gap == "expensive":
#                 return 30 if boardgame.price >= 100 and boardgame.price < 150 else 0
#             else:
#                 return 30 if boardgame.price >= 150 else 0
#         return 0