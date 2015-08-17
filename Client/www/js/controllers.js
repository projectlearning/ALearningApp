angular.module('starter.controllers', ['alearn.config'])

.controller('HomeCtrl',['$scope','$state','config','HomeBanner',
  function($scope,$state,config,HomeBanner) {
  var homeData = {
    banner: [],
    bannerConfig: config['banner'],
  };
  $scope.homeData = homeData;
  homeData.banner = HomeBanner.all();
  $scope.openLocation = function()
  {
     $state.go("citychange");
  }
}])
.controller('ClassCtrl', function($scope) {})

.controller('ChatsCtrl', function($scope, Chats) {
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

.controller('ChatDetailCtrl', function($scope, $stateParams, Chats) {
  $scope.chat = Chats.get($stateParams.chatId);
})

.controller('AccountCtrl', function($scope) {
  $scope.settings = {
    enableFriends: true
  };
})

.controller('CityCtrl',function($scope){})
