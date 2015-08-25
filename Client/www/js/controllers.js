angular.module('alearn.controllers', ['alearn.config','ngCordova'])

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



.controller('AccountTabCtrl',['$scope','AccountService',function($scope,AccountService) {
  $scope.account = AccountService.getAccount();
}])

.controller('AccountLoginFailedCtrl', function() {

})

.controller('AccountRegisterCtrl', function($scope) {

})

.controller('AccountLoginCtrl', function($scope) {

})

.controller('AccountMoneyCtrl', function($scope) {

})

.controller('AccountOrdersCtrl', function($scope) {

})

.controller('AccountCommentsCtrl', function($scope) {

})

.controller('AccountInfoCtrl', ['$scope','NoticeService','$ionicActionSheet','$cordovaCamera',
  function($scope,NoticeService,$ionicActionSheet,$cordovaCamera) {

  $scope.changeAvatger = function(){
    $ionicActionSheet.show({
      titleText : '更换头像',
      cancelText: '取消',
      buttons   : [{text:'拍照'},{text:'从相册中选取'}],
      cancel    : function(){console.log('Change Avater Cancel');},
      buttonClicked : function(index){
        switch(index){
          case  1:
            getPictureFromStorage();
            break;
          case  0:
          default:
            getPictureFromCamera();
            break;
        }
        return true;
      }
    });
  };


  function getPictureFromCamera(){
    var options = {
        quality: 50,
        destinationType: Camera.DestinationType.DATA_URL,
        sourceType: Camera.PictureSourceType.CAMERA
      };
      $cordovaCamera.getPicture(options).then(onPictureSuccess, onPictureFailed);
  }
  function getPictureFromStorage(options){
    var options = {
        quality: 50,
        destinationType: Camera.DestinationType.DATA_URL,
        sourceType: Camera.PictureSourceType.CAMERA
      };
    $cordovaCamera.getPicture(options).then(onPictureSuccess, onPictureFailed);
  }
  function onPictureSuccess(imageData){
    $scope.cameraImg = "data:image/jpeg;base64," + imageData;
  }
  function onPictureFailed(err){
    NoticeService.loadingNotice('获取图像失败',1000);
    console.log('Get picture failed: ');
    console.log(err);
  }
  function uploadImage(imageData){

  }

}])

.controller('AccountInvitationCtrl', function($scope) {

})

.controller('AccountSettingsCtrl', function($scope) {

});
