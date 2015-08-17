/*create at 2015-08-16
*anthor: ant
*content: alearn directive
*/
var dire = angular.module('alearn.directives',['Ionic','alearn.config']);

/*time: 2015-08-16
*author: ant
*content: home banner directive
*/
dire.directive('alearnBanner',['config', '$window', function(config, $window){
  return {
    require: '?^ionSildeBox',
    restrict: 'A',
    template: '',
    replace: true,
    link: function($scope, element, attrs, controllers){
      $scope.check = function(){
        return element.find('img').size();
      }

      var watcher = $scope.$watch('check()',function(data){
        if(data){
          var radio = config['banner'].width / config['banner'].height,
              height = $window.innerWidth / radio;
          element.css('height', height);
          element.animate({'opacity' : 1}, config['banner'].speed);
          watcher();
        }
      })
    }
  }
}]);
