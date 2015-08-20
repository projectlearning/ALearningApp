angular.module('alearn.controllers', ['alearn.config'])

.controller('HomeTabCtrl', ['$scope','$location','$state','$ionicModal','$ionicHistory','HomeBanner','config','CityService',
  function($scope, $location, $state, $ionicModal, $ionicHistory,HomeBanner,config,CityService) {
    $scope.banner = HomeBanner.all();
    $scope.city = CityService.getNowCity();
    $scope.homeLocationIconPressed = function() {
      $state.go("homeCitySelect");
    };

    $scope.homeSearchIconPressed = function() {
      $state.go("homeSearch");
   };
}])

.controller('HomeCitySelectCtrl',['$scope','$state','CityService',function($scope, $state, CityService) {
  $scope.nowCity = CityService.getNowCity();
  $scope.hotCity = CityService.getHotCities();
  $scope.allCity = CityService.getAllCities();
  $scope.goBack = function() {
    $state.go("tabs.homeTab");
  };
}])

.controller('HomeSearchCtrl', function($scope,$state) {
  $scope.goBack = function() {
    $state.go("tabs.homeTab");
  };
})

.controller('ClassTabCtrl', function($scope) {})

.controller('ChatsTabCtrl', function($scope, Chats) {
  // With the new view caching in Ionic, Controllers are only called
  // when they are recreated or on app start, instead of every page change.
  // To listen for when this page is active (for example, to refresh data),
  // listen for the $ionicView.enter event:
  //
  //$scope.$on('$ionicView.enter', function(e) {
  //});

  $scope.chats = Chats.all();
  $scope.remove = function(chat) {
    Chats.remove(chat);
  };
})

.controller('ChatDetailsCtrl', function($scope, $stateParams, Chats) {
  $scope.chat = Chats.get($stateParams.chatId);
})



.controller('AccountTabCtrl', function($scope) {

})

.controller('AccountLoginFailedCtrl', function() {

})

.controller('AccountRegisterCtrl', function($scope) {

})

.controller('AccountMoneyCtrl', function($scope) {

})

.controller('AccountOrdersCtrl', function($scope) {

})

.controller('AccountCommentsCtrl', function($scope) {

})

.controller('AccountInvitationCtrl', function($scope) {

})

.controller('AccountSettingsCtrl', function($scope) {

});
