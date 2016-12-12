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
angular.module('CardStrength',[])
  // .factory('resourceCards', function($resource) {
  //   return $resource('/api/cards')
  // })
  .factory('buildAPIQuery', function(filters){
    // if 

  })
  .controller('SkillController', function($scope) {
    $scope.song = {
      perfects: .85,
      notes: 550,
      seconds: 125,
      stars: 60
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