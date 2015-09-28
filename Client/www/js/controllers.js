angular.module('alearn.controllers', ['alearn.config','ngCordova'])

.controller('HomeTabCtrl', ['$scope', '$location', '$state', '$ionicModal', '$ionicHistory', 'BannerService', 'CityPickerService',
  function($scope, $location, $state, $ionicModal, $ionicHistory, BannerService, CityPickerService) {
    $scope.banner = BannerService.get();
    $scope.currentCity = CityPickerService.getCurrentCity();

    $scope.homeLocationIconPressed = function() {
      $state.go("homeCitySelect");
    };

    $scope.homeSearchIconPressed = function() {
      $state.go("homeSearch");
   };
}])

/*.controller('HomeCitySelectCtrl',['$scope','$state','CityService',function($scope, $state, CityService) {
  $scope.nowCity = CityService.getNowCity();
  $scope.hotCity = CityService.getHotCities();
  $scope.allCity = CityService.getAllCities();
  $scope.goBack = function() {
    $state.go("tabs.homeTab");
  };
}])*/

.controller('CityPickerCtrl', ['$scope', '$state', 'CityPickerService', function($scope, $state, CityService) {
  $scope.popularCities = CityService.getPopularCities();
  $scope.currentCity = CityService.getCurrentCity();
  $scope.cityClicked = $scope.currentCity;

  $scope.onClickCity = function(cityClicked){
    $scope.cityClicked = cityClicked;
  }

  $scope.onClickConfirm = function(){
    CityService.setCurrentCity($scope.cityClicked);
    $state.go("tabs.homeTab");
  }
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

  $scope.btn_keypad = false;
  $scope.txt_txt = true;
  $scope.btn_send = true;
  $scope.btn_add = false;
  $scope.box_add = false;
})



.controller('AccountTabCtrl',['$scope','AccountService',function($scope,AccountService) {
  $scope.account = AccountService.getAccount();
}])

.controller('AccountLoginFailedCtrl', function() {

})

.controller('AccountRegisterCtrl', ['$scope','$timeout','$cordovaToast',
  function($scope,$timeout,$cordovaToast) {
    $scope.verifyFlag = 0;
    $scope.sendSMS = function(){
      if(!$scope.register.username){
        $cordovaToast.show.show('用户名不能为空', 'short', 'center')
          .then(function(success) {
        // success
        }, function (error) {
        // error
        });
        return false;
      }
      $scope.verifyFlag = 1;

    };

    function checkSMSCode()
    {
      return true;
    }

    $scope.register = function(){

    }
}])

.controller('AccountLoginCtrl', ['$scope','$timeout','$ionicLoading','$state','$cordovaToast',
  function($scope,$timeout,$ionicLoading,$state,$cordovaToast) {

  $scope.login = function() {
    if (!$scope.login.username) {
      $cordovaToast.show('用户名不能为空', 'short', 'center')
        .then(function(success) {
      // success
      }, function (error) {
      // error
      });
      return false;
    };
    if (!$scope.login.password) {
      $cordovaToast.show('密码不能为空', 'short', 'center')
        .then(function(success) {
      // success
      }, function (error) {
      // error
      });
      return false;
    };
    $ionicLoading.show({
      template: "正在登录..."
    });
    $timeout(function() {
      $ionicLoading.hide();
    }, 1400);

    $state.go("tabs.homeTab");
    /*$http.post(ApiEndpoint.url + '/User/Login?_ajax_=1', {
      user: $scope.loginData.username,
      password: $scope.loginData.password
    }).success(function(data) {
      $ionicLoading.hide();
      if (data.error != 0) {
        $scope.showMsg(data.info);
      } else {
        Userinfo.save(data.user_info);
        Userinfo.add('flag', 1);
        $scope.sign = Userinfo.l.today_signed;
        $scope.avaImg = Userinfo.l.avatar_url ? Userinfo.l.avatar_url : 'img/default-ava.png';
        $scope.flag = 1;
        $scope.closeLogin();
      }
    });*/
  }
}])

.controller('AccountMoneyCtrl', function($scope,$ionicScrollDelegate) {
  $scope.isActive = 'a', $scope.isb = true, $scope.isTab = false;
  $scope.changeTab = function(evt) {
    if ($scope.isTab) {
      return;
    }
    var elem = evt.currentTarget;
    $scope.isActive = elem.getAttributeNode('data-active').value;
    $ionicScrollDelegate.scrollTop(false);
    if ($scope.isActive == 'b' && $scope.isb) {
      // $scope.loadMore_b();
      $scope.isb = false;
    }
  };

})
  .controller('moneyAccountDetailCtrl', function($scope) {

  })
    .controller('moneyAccountEntryDetailCtrl', function($scope) {

    })
  .controller('moneyAccountTopUpCtrl', function($scope) {

  })
  .controller('moneyWithdrawalCtrl', function($scope) {

  })
  .controller('couponRedeemCtrl', function($scope) {

  })
.controller('AccountOrdersCtrl', function($scope) {

})
.controller('AccountVerificationCtrl', function($scope) {

})

.controller('AccountCommentsCtrl', function($scope) {

})

.controller('AccountInfoCtrl', ['$scope','NoticeService','$ionicActionSheet','$cordovaCamera',
  function($scope,NoticeService,$ionicActionSheet,$cordovaCamera) {

  $scope.changeAvatger = function(){
    var options = {
      title: '更换头像',
      buttonLabels: ['拍照', '从相册中选取'],
      addCancelButtonWithLabel: '取消',
      androidEnableCancelButton: true,
      winphoneEnableCancelButton: true
    };
    $cordovaActionSheet.show(options)
      .then(function(btnIndex) {
        switch (btnIndex) {
          case 1:
            getPictureFromStorage();
            break;
          case 2:
            getPictureFromCamera();
            break;
          default:
            break;
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

})

.controller('PublicCatagoryCtrl', function($rootScope,$scope) {

})

.controller('ClassDetailCtrl', function($scope) {

})

.controller('OrderClassCtrl', function($scope) {

})

.controller('IdentityVerificationCtrl', function($scope) {

})

.controller('RequirementPostCtrl', function($scope) {

});
