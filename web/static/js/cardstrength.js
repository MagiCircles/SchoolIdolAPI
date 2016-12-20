var calcActivations = function (song, skill) {
    if (skill.type == "notes" || skill.type == "hit" || skill.type == "combo") {
        return Math.floor(song.notes / skill.interval)
    }
    else if (skill.type == "perfects") {
        return Math.floor(song.notes * song.perfects / skill.interval)
    }
    else if (skill.type == "seconds") {
        return Math.floor(song.seconds / skill.interval)
    }
    else {
        //TODO: handle Snow Maiden Umi
        return 0
    }
}

angular.module('CardStrength', ['ngResource'])
    .factory('Cards', function ($resource) {
        return $resource('/api/cards')
    })
    .directive('formGroup', function () {
        return {
            restrict: 'C',
            scope: {
                filters: '='
            },
            controller: function ($scope) {
                // console.debug($scope.$parent.filter)
            }
        }
    })
    .directive('cuteformSelect', function () {
        return {
            restrict: 'C',
            require: '^formGroup',
            link: function ($scope, $elem, $attrs, formGroupCtrl) {
                if ($attrs['ngModel']) $scope.filter = $attrs['name']
                // console.log(formGroupCtrl.$scope.filter)
                // console.debug($scope.filters)
            }
        }
    })
    .directive('cuteformElt', function ($compile) {
        return {
            restrict: 'C',
            require: ['^formGroup', '^?cuteformSelect'],//'^?cuteform',
            link: function (scope, elem, attrs) {
                // console.debug(scope.filter)
                // if (!attrs['ngClick']) {
                //     var filter = ""
                //     var value = attrs['cuteformVal']
                //     elem.attr('ng-click', "setCFFilter('" + scope.filter + "','" + value + "')")
                //     console.debug(elem.val())
                //     $compile(elem.contents())(scope); 
                // }
                // elem.onClick(function(){
                //     scope.$parent.$parent.setCFFilter(scope.filter,attrs['cuteformVal'])
                // })
            }
        }
    })
    .factory('BuildAPIQuery', function (filters) {
        // if 

    })
    .controller('FiltersController', function ($scope) {
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
            }
        }
        var setAll = function(group) {
            angular.forEach($scope.filters[group], function(value,key) {
                if (key != 'All') $scope.filters[group][key] = false
            })
            $scope.filters[group].All = true;
        }
        $scope.setGroup = function(group, filter) {
            // var group = $scope.filters[group];

            if (filter == 'All') setAll(group);
            $scope.filters[group].All = false
            $scope.filters[group][filter] = !$scope.filters[group][filter] 

            var tempOtherFilters = $scope.filters[group]
            delete tempOtherFilters.All
            var allOtherFiltersOn = allOtherFiltersOff = true;
            angular.forEach(tempOtherFilters, function(value,key) {
                // console.debug(tempOtherFilters.key + ": " + value)
                allOtherFiltersOn &= value
                allOtherFiltersOff &= !value
            })

            if (allOtherFiltersOn || allOtherFiltersOff) setAll(group);
        }
    })
    .controller('SkillController', function ($scope, Cards) {
        var init = function () {
            $scope.song = {
                perfects: .85,
                notes: 550,
                seconds: 125,
                stars: 60
            }
            $scope.cards = {}
        }
        init();

        $scope.getCards = function () {
            Cards.query($scope.filters)
        }
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
    });