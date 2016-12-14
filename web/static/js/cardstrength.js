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
  .directive('cuteform', function () {
    // text-based cuteforms
    return {
      restrict: 'A',
      scope: { returnModel: '&model'},
      transclude: true,
      controller: function ($scope, $attrs) {
        this.returnModel = function() { 
          var val = $attrs.ngModel ? $attrs.ngModel : false
          return {value: val}
        }
      }
    }
  })
  // .directive('cuteformSelect', function () {
  //   // image-based cuteforms
  //   return {
  //     restrict: 'C',
  //     scope: {},
  //     transclude: true,
  //     controller: function ($scope, $attrs) {
  //       this.returnModel = function() { return $attrs.ngModel ? $attrs.ngModel : false}
  //     }
  //   }
  // })
  .directive('cuteformElt', function () {
    function link($scope, element, attrs, controllers) {
      var textCtrl = controllers[0],
          imageCtrl = controllers[1];

      // figure out which type of cuteform this elt belongs to
      var model = textCtrl.returnModel(); 
      if (model) {
        attrs.set("ngClick", model)
      }
      // else $attrs.set("ngClick", imageCtrl.returnModel())
    }
    return {
      restrict: 'C',
      scope: { 
        model: '@'
      },
      require: ['^?cuteform'],//, '^?cuteformSelect'],
      link: link,
    }
  })
  .factory('BuildAPIQuery', function (filters) {
    // if 

  })
  .controller('FiltersController', function ($scope) {
    $scope.filters = {}

    $scope.setCFFilter = function (filter, newValue) {
      // var found_key = false;
      // angular.forEach($scope.filters, function(value,key){
      //   if (key == filter) {
      //     $scope.filters[key] = newValue; 
      //     found_key = true;
      //     return;
      //     }
      // })
      // if (!found_key) {
      //   $scope.filters[filter] = newValue
      // };
      $scope.filters[filter] = newValue

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