angular.module('CardStrength', ['ngResource'])
    .factory('API', function ($resource, $http) {
        return $resource("/api/cards/?page_size=100&attribute=:attr&is_promo=:promo&is_event=:event&main_unit=:main&sub_unit=:sub&year=:year", {
            attr: "@attr",
            promo: "@promo",
            event: "@event",
            main: "@main",
            sub: "@sub",
            year: "@year",
        })
    })
    .factory('HTTP', function ($resource, $http) {
        var ret = {};
        ret.getUrl = function (url) {
            return $http.get(url)
        }
        return ret
    })
    .controller('FiltersController', function ($rootScope, $scope, API, HTTP) {
        $scope.filters = {
            rarity: "",
            attr: "",
            promo: "",
            event: "",
            main_unit: "",
            sub_unit: "",
            year: "",
        }
        $scope.setRarity = function (rarity) {
            if (rarity == '') {
                $scope.filters.rarity = '';
                return
            }
            var split = $scope.filters.rarity.split(",")
            var index = split.indexOf(rarity)
            
            if (index<0) {
                split.push(rarity)
                split = split.filter(function(n){ return n != undefined }); 
                if (split.length >= 5) {
                    $scope.filters.rarity = ""
                }
                else $scope.filters.rarity = split.join(",")
            }
            else {
                console.log(split)
                delete split[index]
                split = split.filter(function(n){ return n != undefined }); 
                $scope.filters.rarity = split.join(",")
            }
        }
        $scope.setString = function (filter, string) {
            $scope.filters[filter] = string
        }

        var nextUrl = "";
        var getNextUrlSuccess = function (response) {
            if (response.data.next) nextUrl = response.data.next;
            else nextUrl = null;
            angular.forEach(response.data.results, function (value) {
                $rootScope.cards.push(value)
            })

            if (nextUrl) HTTP.getUrl(nextUrl).then(getNextUrlSuccess);
        }
        var parameterStr = function (group) {
            if ($scope.filters[group].All) return "";

            var str = ""
            angular.forEach($scope.filters[group], function (value, key) {
                if (value) str += key + ","
            })
            return str
        }
        $scope.getCards = function () {
            var cards = API.get($scope.filters, function () {
                $rootScope.cards = []
                angular.forEach(cards.results, function (value) {
                    $rootScope.cards.push(value)
                })

                if (cards.next) {
                    console.log(cards.next)
                    HTTP.getUrl(cards.next).then(getNextUrlSuccess);
                }
            });
        }
    })
    .controller('SkillController', function ($rootScope, $scope) {
        var init = function () {
            $scope.song = {
                perfects: .85,
                notes: 550,
                seconds: 125,
                stars: 60
            }
        }
        init();

        $scope.calcAvg = function (song, skill) {
            return calcActivations(song, skill) * skill.percent * skill.amount;
        }

        $scope.calcBest = function (song, skill) {
            return calcActivations(song, skill) * skill.amount
        }


    })
    .config(function ($interpolateProvider) {
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');
    })
    .config(function ($qProvider) {
        $qProvider.errorOnUnhandledRejections(false);
    })