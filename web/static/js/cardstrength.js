angular.module('CardStrength', ['ngResource', 'ngStorage'])
    .factory('API', function ($resource, $http) {
        return $resource("/api/cards/?page_size=100&is_special=False&attribute=:attr&is_promo=:promo&is_event=:event&main_unit=:main_unit&sub_unit=:sub_unit&year=:idol_year&idol_school=:idol_school&translated_collection=:translated_collection&japanese_collection=:japanese_collection&japan_only=:japan_only", {
            attr: "@attr",
            promo: "@promo",
            event: "@event",
            main_unit: "@main_unit",
            sub_unit: "@sub_unit",
            idol_year: "@idol_year",
            idol_school: "@idol_school",
            translated_collection: "@translated_collection",
            japanese_collection: "@japanese_collection",
            japan_only: "@japan_only"
        })
    })
    .factory('HTTP', function ($resource, $http) {
        var ret = {};
        ret.getUrl = function (url) {
            return $http.get(url)
        }
        return ret
    })

    .factory('Calculations', function () {
        var ret = {};

        ret.activations = function (song, skill) {
            if (skill.type == "notes" || skill.type == "hit" || skill.type == "combo") {
                return Math.floor(song.notes / skill.interval)
            }
            else if (skill.type == "perfects") {
                return Math.floor(Math.floor(song.notes * song.perfects) / skill.interval)
            }
            else if (skill.type == "seconds") {
                return Math.floor(song.seconds / skill.interval)
            }
            else {
                //TODO: handle Snow Maiden Umi and point-based score up
                return 0
            }
        };

        // score = floor(stat * 0.0125 * accuracy * combo_position * note_type * attribute_bool * group_bool)
        ret.scoreUpMod = function (song, scoreUp) {
            // given a score that a card has generated, return stat corresponding to that score
            return Math.floor(scoreUp / song.notes / 0.0125);
        };

        ret.plScoreBonus = function (on_attr, song, pl_time, type) {
            // calculate exactly how many notes are estimated to go great -> perfect
            var pl_proportion_of_song = pl_time < song.seconds ? pl_time / song.seconds : 1
            var notes_during_pl = Math.floor(song.notes * pl_proportion_of_song)
            var transformed_greats_proportion_of_song = notes_during_pl * (1 - song.perfects) / song.notes

            // how much the score changed due to greats -> perfects
            var score_difference = Math.floor(on_attr * 0.0125 * .22 * Math.floor(song.notes / 2) * 1 * 1.1 * 1.1) * transformed_greats_proportion_of_song

            return ret.scoreUpMod(song, score_difference)
        }

        ret.trickStatBonus = function (on_attr, song, pl_time) {
            // calculate exactly how many notes are estimated to go great -> perfect
            var pl_proportion_of_song = pl_time < song.seconds ? pl_time / song.seconds : 1
            var notes_during_pl = Math.floor(song.notes * pl_proportion_of_song)
            var greats_during_pl = notes_during_pl * (1 - song.perfects) / song.notes
            var perfects_during_pl = notes_during_pl * song.perfects / song.notes

            var bonus = Math.floor(on_attr * 0.33)
            // how many more points greats give
            var trick_greats_bonus = Math.floor(bonus * 0.0125 * .22 * Math.floor(song.notes / 2) * 1 * 1.1 * 1.1) * greats_during_pl
            // how many more points perfects give 
            var trick_perfects_bonus = Math.floor(bonus * 0.0125 * 1 * Math.floor(song.notes / 2) * 1 * 1.1 * 1.1) * perfects_during_pl

            return ret.scoreUpMod(song, trick_greats_bonus + trick_perfects_bonus)
        }


        return ret;
    })

    .controller('FiltersController', function ($rootScope, $scope, API, HTTP, $localStorage) {
        $scope.$storage = $localStorage
        if ($scope.$storage.filters) $scope.filters = $scope.$storage.filters
        else {
            $scope.filters = {
                rarity: 'R,SR,SSR,UR',
                attr: "",
                promo: "",
                event: "",
                main_unit: "",
                sub_unit: "",
                year: "",
            }
            $scope.$storage.filters = $scope.filters
        }
        if ($scope.$storage.cards) $rootScope.cards = $scope.$storage.cards
        /// filter creation functions
        $scope.setRarity = function (rarity) {
            if (rarity == 'R,SR,SSR,UR') {
                $scope.filters.rarity = rarity;
                return
            }
            // console.log($scope.filters.rarity)
            if ($scope.filters.rarity == "R,SR,SSR,UR") {

                $scope.filters.rarity = rarity
                $scope.single_rarity_selected = true
                // console.log($scope.filters.rarity)
                return
            }
            else {
                var split = $scope.filters.rarity.split(",")
                var index = split.indexOf(rarity)
                console.debug(split)
                console.debug("indexOf(" + rarity + "): " + index)

                if (index < 0) {
                    console.debug("not in filter")

                    split.push(rarity)
                    split = split.filter(function (n) { return n != undefined });
                    $scope.filters.rarity = split.join(",")
                }
                else {
                    // split.push(rarity)
                    // split = split.filter(function (n) { return n != undefined });
                    // if (split.length >= 5) {
                    //     $scope.filters.rarity = 'R,SR,SSR,UR'
                    // }
                    // else $scope.filters.rarity = split.join(",")
                    if ($scope.filters.rarity == "R,SR,SSR,UR") {
                        $scope.filters.rarity = rarity
                    }
                    else {
                        delete split[index]
                        split = split.filter(function (n) { return n != undefined });
                        if (split.length >= 4 || split.length <= 0) {
                            $scope.filters.rarity = 'R,SR,SSR,UR'
                        }
                        else $scope.filters.rarity = split.join(",")
                    }
                }
            }
            // $scope.single_rarity_selected = 
            
            $scope.$storage.filters.rarity = $scope.filters.rarity
        }
        $scope.setString = function (filter, string) {
            $scope.filters[filter] = string
        }

        var nextUrl = "";
        var calcOnAttr = function (card) {
            card.on_attr = {}
            if (card.attribute == "Smile") {
                card.on_attr.base = card.non_idolized_maximum_statistics_smile
                card.on_attr.idlz = card.idolized_maximum_statistics_smile
            }
            else if (card.attribute == "Pure") {
                card.on_attr.base = card.non_idolized_maximum_statistics_pure
                card.on_attr.idlz = card.idolized_maximum_statistics_pure
            }
            else if (card.attribute == "Cool") {
                card.on_attr.base = card.non_idolized_maximum_statistics_cool
                card.on_attr.idlz = card.idolized_maximum_statistics_cool
            }
            if (card.rarity == 'R') {
                card.on_attr.base += 100
                card.on_attr.idlz += 200
            }
            else if (card.rarity == "SR") {
                card.on_attr.base += 250
                card.on_attr.idlz += 500
            }
            else if (card.rarity == "SSR") {
                card.on_attr.base += 375
                card.on_attr.idlz += 750
            }
            else if (card.rarity == "UR") {
                card.on_attr.base += 500
                card.on_attr.idlz += 1000
            }
            if (card.is_promo) card.on_attr.base = card.on_attr.idlz
        }
        var parseSkill = function (card) {
            var skilltype = card.skill
            card.skill = {
                category: skilltype,
                interval: 0,
                type: "",
                amount: 0,
                percent: 0
            }
            card.sis = {}

            var parsedNumbers = 0, i = 0;
            var skill_words = card.skill_details.split(" ")
            var length = skill_words.length
            var word;
            for (var i = 0; i < length; i++) {
                word = skill_words[i]
                var num = parseInt(word)

                if (num && (parsedNumbers == 0)) {
                    card.skill.interval = word
                    card.skill.type = skill_words[i + 1].replace(',', '')
                    ++parsedNumbers
                }
                else if (num && parsedNumbers == 1) {
                    card.skill.percent = num / 100
                    ++parsedNumbers
                }
                else if (num && parsedNumbers == 2) {
                    card.skill.amount = word
                    ++parsedNumbers
                    break
                }
            }
        }
        var getNextUrlSuccess = function (response) {
            if (response.data.next) nextUrl = response.data.next;
            else nextUrl = null;
            angular.forEach(response.data.results, function (value) {
                $rootScope.cards.push(value)
            })

            if (nextUrl) HTTP.getUrl(nextUrl).then(getNextUrlSuccess);
        }
        $scope.getCards = function () {
            var cards = API.get($scope.filters, function () {
                $rootScope.cards = []
                angular.forEach(cards.results, function (value) {
                    $rootScope.cards.push(value)
                })

                if (cards.next) {
                    HTTP.getUrl(cards.next).then(getNextUrlSuccess);
                }
                var length = $rootScope.cards.length
                for (var i = 0; i < length; i++) {
                    calcOnAttr($rootScope.cards[i])
                    parseSkill($rootScope.cards[i])

                }
            });
            // $scope.$broadcast("cardsUpdate", { cards: $rootScope.cards })
        }
    })
    .controller('SkillController', function ($rootScope, $scope, Calculations, $localStorage) {
        $scope.$storage = $localStorage
        $scope.song = {
            perfects: .85,
            notes: 550,
            seconds: 125,
            stars: 60
        }
        // calcs
        var activations;

        var calcSkill = function (card) {
            card.skill.avg = card.skill.best = "Loading..."
            // console.log(card.rarity)

            if (!card.skill) return;

            card.skill.activations = Calculations.activations($scope.song, card.skill);
            card.skill.avg = Math.floor(card.skill.activations * card.skill.percent) * card.skill.amount
            card.skill.best = card.skill.activations * card.skill.amount

            if (card.skill.category == "Perfect Lock" || card.skill.category.includes("Trick")) {
                card.skill.stat_bonus_avg = Calculations.plScoreBonus(card.on_attr.base, $scope.song, card.skill.avg)
                card.skill.stat_bonus_best = Calculations.plScoreBonus(card.on_attr.base, $scope.song, card.skill.best)
            }
            else if ((card.skill.category == "Healer" || card.skill.category.includes("Yell")) && !card.equippedSIS) {
                card.skill.stat_bonus_avg = card.skill.stat_bonus_best = 0;
            }
            else { // scorer
                card.skill.stat_bonus_avg = Calculations.scoreUpMod($scope.song, card.skill.avg)
                card.skill.stat_bonus_best = Calculations.scoreUpMod($scope.song, card.skill.best)
            }
        }

        // sis calculations 
        var calcTrickStatBonus = function (card) {
            var stat;
            // console.log(card.on_attr)
            if (card.idlz) stat = card.on_attr.idlz
            else stat = card.on_attr.base

            var bonus = Math.floor(stat * 0.33)

            card.sis.avg = Math.floor(card.skill.avg / $scope.song.seconds * bonus)
            card.sis.best = Math.floor(card.skill.best / $scope.song.seconds * bonus)

            card.sis.stat_bonus_avg = Calculations.trickStatBonus(stat, $scope.song, card.skill.avg)
            card.sis.stat_bonus_best = Calculations.trickStatBonus(stat, $scope.song, card.skill.best)
        }
        var calcSIS = function (card) {
            if (card.rarity == 'R' || card.is_promo) {
                card.sis = card.skill
                return;
            }

            // score up: SU skill power x2.5
            if (card.skill.category == "Score Up") {
                card.sis.avg = card.skill.avg * 2.5
                card.sis.best = card.skill.best * 2.5
                card.sis.stat_bonus_avg = Calculations.scoreUpMod($scope.song, card.sis.avg)
                card.sis.stat_bonus_best = Calculations.scoreUpMod($scope.song, card.sis.best)
            }
            // healer: convert to SU with x480 multiplier
            else if (card.skill.category == "Healer") {
                card.sis.avg = card.skill.avg * 480
                card.sis.best = card.skill.best * 480
                card.sis.stat_bonus_avg = Calculations.scoreUpMod($scope.song, card.sis.avg)
                card.sis.stat_bonus_best = Calculations.scoreUpMod($scope.song, card.sis.best)
            }
            // PLer: + x0.33 on-attribute stat when PL is active
            else if (card.skill.category == "Perfect Lock") {
                calcTrickStatBonus(card);
            } else return;
        }

        var calcStatBonus = function (card) {
            var base, bonus = {};
            if (!card.idlz) {
                base = card.on_attr.base
            } else base = card.on_attr.idlz

            if (!card.equippedSIS) {
                bonus.avg = card.skill.stat_bonus_avg
                bonus.best = card.skill.stat_bonus_best
            }
            else {
                bonus.avg = card.sis.stat_bonus_avg
                bonus.best = card.sis.stat_bonus_best
            }

            card.on_attr.avg = base + bonus.avg
            card.on_attr.best = base + bonus.best

        }
        $rootScope.$watch('cards', function (event, args) {
            var length = $rootScope.cards.length
            console.log("cardsUpdate")
            // console.log($rootScope.cards)
            for (var i = 0; i < length; i++) {
                // card = $rootScope.cards[i]
                // console.log($rootScope.cards[i])
                calcSkill($rootScope.cards[i]);
                calcSIS($rootScope.cards[i]);
                calcStatBonus($rootScope.cards[i])
                $rootScope.cards[i].equippedSIS = $rootScope.cards[i].idlz = false
                $rootScope.cards[i].on_attr.display = $rootScope.cards[i].on_attr.base
                $rootScope.cards[i].skill_display = {
                    avg: $rootScope.cards[i].skill.avg,
                    best: $rootScope.cards[i].skill.best
                }
            }
            $scope.$storage.cards = $rootScope.cards
            // console.log($scope.$storage.cards)
        })

        $scope.toggleEquipSIS = function (card) {
            card.equippedSIS = !card.equippedSIS
            calcSIS(card)
            if (card.equippedSIS) {
                card.skill_display.avg = card.sis.avg;
                card.skill_display.best = card.sis.best
            } else {
                card.skill_display.avg = card.skill.avg;
                card.skill_display.best = card.skill.best
            }
            calcStatBonus(card)
            $scope.$storage.cards = $rootScope.cards
        }

        $scope.toggleIdlz = function (card) {
            if (card.idlz) {
                if (card.skill.category == "Perfect Lock") calcTrickStatBonus(card);
                calcStatBonus(card)

                card.on_attr.display = card.on_attr.idlz
            }
            else card.on_attr.display = card.on_attr.base

            $scope.$storage.cards = $rootScope.cards
        }

        $scope.sort = { type: "id", desc: false }
        $scope.sortBy = function (sorter) {
            $scope.sort.desc = ($scope.sort.type == sorter) ? !$scope.sort.desc : true

            // if (sorter == "on_attr") {

            // }
            $scope.sort.type = sorter;

            if ($scope.sort.desc) $scope.sort.chevron = "down"
            else $scope.sort.chevron = "up"
        }


    })
    .filter('skillToSIS', function () {
        return function (input) {
            if (input) var split = input.split(" ")
            if (input == "Score Up" || (split && split.indexOf("Charm") > 0)) {
                return "Charm"
            }
            else if (input == "Healer" || (split && split.indexOf("Yell") > 0)) {
                return "Heal"
            }
            else if (input == "Perfect Lock" || (split && split.indexOf("Trick") > 0)) {
                return "Trick"
            }
        }
    })
    .filter('skillToFlaticon', function () {
        return function (input) {
            if (input) var split = input.split(" ")
            if (input == "Score Up" || (split && split.indexOf("Charm") > 0)) {
                return "scoreup"
            }
            else if (input == "Healer" || (split && split.indexOf("Yell") > 0)) {
                return "healer"
            }
            else if (input == "Perfect Lock" || (split && split.indexOf("Trick") > 0)) {
                return "perfectlock"
            }
        }
    })
    .filter('skillToEffect', function () {
        return function (input, equipped_sis) {
            if (input) var split = input.split(" ")
            if (input == "Score Up" || (split && split.indexOf("Charm") > 0) || (input == "Healer" && equipped_sis)) {
                return "points"
            }
            else if (input == "Healer" || (split && split.indexOf("Yell") > 0)) {
                return "stamina"
            }
            else if (input == "Perfect Lock" || (split && split.indexOf("Trick") > 0)) {
                return "seconds"
            }
            else if (input == "Perfect Lock" && equipped_sis) {
                return ""
            }
        }
    })
    .config(function ($interpolateProvider) {
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');
    })
    .config(function ($qProvider) {
        $qProvider.errorOnUnhandledRejections(false);
    })