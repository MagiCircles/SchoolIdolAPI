angular.module('cardStrength', ['ui.bootstrap'])
  .controller('FormController', function($scope) {

    // idol name typeahead
    $scope.selected_idol = undefined;
    $scope.idols = [{% for idol,str in filters.idols %} "{{str}}" {% if not forloop.last %},{% endif %} {% endfor %}]

    // collections typeahead
    $scope.selected_collection = undefined;
    $scope.collections = [{% for japanese_collection in filters.japanese_collection %} "{{japanese_collection}}", {% endfor %} 
    {% for translated_collection in filters.translated_collection %} "{{japanese_collection}}"{% if not forloop.last %},{% endif %} {% endfor %}]
  })
  .config(function($interpolateProvider) {
      
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');
      
    });