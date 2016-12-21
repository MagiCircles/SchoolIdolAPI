angular.module('CardStrength', ['ngResource'])
    .factory('API', function ($resource, $http) {
        return $resource("/api/cards/", {})
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
            rarity: {
                All: true,
                R: false,
                SR: false,
                SSR: false,
                UR: false,
            },
            attr: {
                All: true,
                Smile: false,
                Pure: false,
                Cool: false,
            },
            promo: "",
            main_unit: "",
            sub_unit: "",
            year: "",
        }
        var setAll = function (group) {
            angular.forEach($scope.filters[group], function (value, key) {
                if (key != 'All') $scope.filters[group][key] = false
            })
            $scope.filters[group].All = true;
        }
        $scope.setGroup = function (group, filter) {
            if (filter == 'All') setAll(group);
            $scope.filters[group].All = false
            $scope.filters[group][filter] = !$scope.filters[group][filter]

            var otherFilters = $scope.filters[group]
            delete otherFilters.All
            var allOtherFiltersOn = allOtherFiltersOff = true;
            angular.forEach(otherFilters, function (value, key) {
                allOtherFiltersOn &= value
                allOtherFiltersOff &= !value
            })

            if (allOtherFiltersOn || allOtherFiltersOff) setAll(group);
        }
        $scope.setString = function (filter, string) {
            $scope.filters[filter] = string
        }

        $rootScope.cards = []
        var nextUrl = "";
        var getNextUrlSuccess = function (response) {
            if (response.data.next) nextUrl = response.data.next;
            else nextUrl = null;
            console.log(nextUrl)

            angular.forEach(response.data.results, function (value) {
                $rootScope.cards.push(value)
            })

            if (nextUrl) HTTP.getUrl(nextUrl).then(getNextUrlSuccess);
        }
        $scope.getCards = function () {
            var cards = API.get(function () {
                angular.forEach(cards.results, function (value) {
                    $rootScope.cards.push(value)
                })

                if (cards.next) {
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