var calcActivations = function(song,skill) {
  if (skill.type == "notes" || skill.type == "hit" || skill.type == "combo") {
    return Math.floor(song.notes / skill.interval)
  }
  else if (skill.type == "perfects") {
    return Math.floor(song.notes * song.perfects / skill.interval)
  }
  else if (skill.type == "seconds") {
    return Math.floor(song.seconds / skill.interval)
  }
  else  {
    //TODO: handle Snow Maiden Umi
    return 0
  }
}

angular.module('CardStrength',['ngResource'])
  .factory('Cards', function($resource) {
    return $resource('/api/cards')
  })
  .factory('BuildAPIQuery', function(filters){
    // if 

  })
  .controller('FiltersController', function($scope){
    $scope.filters = {}

    $scope.setCFFilter = function(filter, newValue) {
      var found_key = false;
      angular.forEach($scope.filters, function(value,key){
        if (key == filter) {
          $scope.filters[key] = newValue; 
          found_key = true;
          return;
          }
      })
      if (!found_key) {
        $scope.filters[filter] = newValue
      };
      
    }
  })
  .controller('SkillController', function($scope, Cards) {
    var init = function() {
      $scope.song = {
        perfects: .85,
        notes: 550,
        seconds: 125,
        stars: 60
      }
      $scope.cards = {}
    }
    init();

    $scope.getCards = function() {
      Cards.query($scope.filters)
    }
    $scope.calcAvg = function(song,skill) {
      return calcActivations(song,skill) * skill.percent * skill.amount;      
    }

    $scope.calcBest = function(song,skill) {
      return calcActivations(song,skill) * skill.amount
    }

      
  })
  .config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
  });