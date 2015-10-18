angular.module('alearn.controllers', ['alearn.config','ngCordova'])

.controller('HomeTabCtrl', ['$scope', '$location', '$state', '$ionicModal', '$ionicHistory', 'BannerService', 'CityPickerService',
  function ($scope, $location, $state, $ionicModal, $ionicHistory, BannerService, CityPickerService) {
    $scope.banners = BannerService.getBanners();
    $scope.currentCity = CityPickerService.getCurrentCity();

    $scope.homeLocationIconPressed = function () {
      $state.go("homeCitySelect");
    };

    $scope.homeSearchIconPressed = function () {
      $state.go("homeSearch");
   };
}])



.controller('CityPickerCtrl', ['$scope', '$state', 'CityPickerService', function ($scope, $state, CityService) {
  $scope.popularCities = CityService.getPopularCities();
  $scope.currentCity = CityService.getCurrentCity();
  $scope.cityClicked = $scope.currentCity;

  $scope.onClickCity = function (cityClicked) {
    $scope.cityClicked = cityClicked;
  };

  $scope.onClickConfirm = function () {
    CityService.setCurrentCity($scope.cityClicked);
    $state.go("tabs.homeTab");
  };
}])



.controller('HomeSearchCtrl', function ($scope, $state) {
  $scope.goBack = function () {
    $state.go("tabs.homeTab");
  };
})



.controller('ClassTabCtrl', ['$scope', '$http', function ($scope, $http) {
  var requirement = [];
  $scope.getRequire = function () {
  };
}])



.controller('ChatsTabCtrl', function ($scope, Chats) {
  // With the new view caching in Ionic, Controllers are only called
  // when they are recreated or on app start, instead of every page change.
  // To listen for when this page is active (for example, to refresh data),
  // listen for the $ionicView.enter event:
  //
  //$scope.$on('$ionicView.enter', function(e) {
  //});

  $scope.chats = Chats.all();
  $scope.remove = function (chat) {
    Chats.remove(chat);
  };
})



.controller('ChatDetailsCtrl', function ($scope, $stateParams, Chats) {
  $scope.chat = Chats.get($stateParams.chatId);

  $scope.btn_keypad = false;
  $scope.txt_txt = true;
  $scope.btn_send = true;
  $scope.btn_add = false;
  $scope.box_add = false;
})



.controller('AccountTabCtrl', ['$scope', 'AccountService', '$rootScope', 'cacheService', '$http', 'config',
  function ($scope, AccountService, $rootScope, cacheService, $http, config) {
    $rootScope.user.isSign = true;
    $scope.loginFlag = $rootScope.user.isSign;
    if($rootScope.user.isSign) {
      $http.get(config.url + cmd['user_info_get'] + '?userID=' + $rootScope.user.id).success(function (data) {
        if(data.responseStr == 'Success') {
          $scope.account = data.user;
          $scope.account.phone = $rootScope.user.phone;
        } else {
          $ionicLoading.show({template: responseCode[data.responseStr], duration: 1000});
          return false;
        }
      }).error(function (data) {
        $ionicLoading.show({template: responseCode['Network_Error'], duration: 1000});
        return false;
      });
    }
    $scope.account = AccountService.getAccount();
}])



.controller('AccountLoginFailedCtrl', function () {
})



.controller('AccountRegisterCtrl', ['$scope', '$timeout', '$ionicLoading', 'cacheService', 'config',
  function ($scope, $timeout,$ionicLoading, cacheService, config) {
    $scope.register = {};
    $scope.verifyFlag = 0;
    $scope.SMSTime = 0;
    $scope.sendSMS = function () {
      if(!$scope.register.phone) {
        $ionicLoading.show({template: responseCode['Phone_Not_Empty'], duration: 1000});
        return false;
      }

      if(!pattern['mobile'].test($scope.register.phone)) {
        $ionicLoading.show({template: responseCode['Phone_Not_Right'], duration: 1000});
        return false;
      }

      var code = "";
      for(var i=0; i < 6; ++i) {
        code += Math.floor(Math.random() * 10);
      }

      $scope.SMSCode = code;
      cacheService.system.put('SMSCODE', $scope.SMSCode);
      $ionicLoading.show({template: $scope.SMSCode, duration: 1000});
      keepTime();
      $scope.verifyFlag = 1;
    };

    function keepTime(time) {
      if(time <= 0) {
        return $scope.SMSTime = 0;
      }
      time = time || config.sms_maxtime;

      $timeout(function() {
        $scope.SMSTime = time - 1;
        keepTime(time - 1);
      }, 1000);
    }

    function checkSMSCode(code) {
      $scope.SMSCode = cacheService.system.get('SMSCODE');
      
      if(code == $scope.SMSCode) {
        return true;
      }

      return false;
    }

    $scope.register = function() {
      if(!$scope.register.phone) {
        $ionicLoading.show({template: responseCode['Phone_Not_Empty'], duration: 1000});
        return false;
      }

      if(!pattern['mobile'].test($scope.register.phone)) {
        $ionicLoading.show({template: responseCode['Phone_Not_Right'], duration: 1000});
        return false;
      }

      if (!$scope.register.password) {
        $ionicLoading.show({template:responseCode['Password_Not_Empty'], duration: 1000});
        return false;
      }

      if(!$scope.register.veriSMSCode) {
        $ionicLoading.show({template: responseCode['Verification_Code_Not_Empty'], duration: 1000});
        return false;
      }

      if(!checkSMSCode($scope.register.veriSMSCode)) {
        $ionicLoading.show({template: responseCode['Register_Wrong_Verification_Code'], duration: 1000});
        return false;
      }

      $ionicLoading.show({
        template: responseCode['Registering']
      });

      $http.post(config.url + cmd['user_register'], {
        phone: $scope.register.phone,
        password: $scope.register.phone
        }).success(function (data) {
          $ionicLoading.hide();

          if(data.responseStr == "Success") {
              $rootScope.user.isSign = true;
              $rootScope.user.id = data.userID;
              $rootScope.user.token = data.token;
              $rootScope.user.phone = $scope.register.phone;
              cacheService.system.put('USERID', $rootScope.user.token);
              cacheService.system.put('TOKEN', $rootScope.user.token);
              cacheService.system.put('USERPHONE', $rootScope.user.phone);
          }
          else {
            $ionicLoading.show({template: responseCode[data.responseStr], duration: 1000});
            return false;
          }
      }).error(function (data) {
        $ionicLoading.hide();
        $ionicLoading.show({template: responseCode['Register_Fail'], duration: 1000});
        return false;
      });

      $state.go("tabs.homeTab");
    }
}])



.controller('AccountLoginCtrl', function ($scope, $timeout, $ionicLoading, $state, $cordovaToast, $http,config, $rootScope, cacheService) {
  $scope.login = {};
  $scope.doLogin = function () {
    if (!$scope.login.phone) {
      $ionicLoading.show({template: responseCode['Phone_Not_Empty'], duration: 1000});
      return false;
    }

    if (!$scope.login.password) {
      $ionicLoading.show({template: responseCode['Password_Not_Empty'], duration: 1000});
      return false;
    }

    if(!pattern['mobile'].test($scope.login.phone)) {
      $ionicLoading.show({template: responseCode['Phone_Not_Right'], duration: 1000});
      return false;
    }

    $ionicLoading.show({
      template: responseCode['Logining']
    });
    /*$timeout(function() {
      $ionicLoading.hide();
    }, 1400);*/
    $http.post(config.url + cmd['user_login'], {
      phone: $scope.login.phone,
      password: $scope.login.phone
    }).success(function (data) {
      $ionicLoading.hide();

      if(data.responseStr == "Success") {
          $rootScope.user.isSign = 1;
          $rootScope.user.id = data.userID;
          $rootScope.user.token = data.token;
          $rootScope.user.phone = $scope.login.phone;
            cacheService.system.put('USERID', $rootScope.user.token);
            cacheService.system.put('TOKEN', $rootScope.user.token);
            cacheService.system.put('USERPHONE', $rootScope.user.phone);
      } else {
        $ionicLoading.show({template: responseCode[data.responseStr], duration: 1000});
        return false;
      }
    }).error(function (data) {
      $ionicLoading.hide();
      $ionicLoading.show({template: responseCode['Login_Fail'], duration: 1000});
      return false;
    });

    $state.go("tabs.homeTab");
  };
})



.controller('AccountMoneyCtrl', function ($scope, $ionicScrollDelegate) {
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


  .controller('moneyAccountDetailCtrl', function ($scope) {

  })


  .controller('moneyAccountEntryDetailCtrl', function ($scope) {

    })
  

  .controller('moneyAccountTopUpCtrl', function ($scope) {

  })
  

  .controller('moneyWithdrawalCtrl', function ($scope) {

  })
  

  .controller('couponRedeemCtrl', function ($scope) {

  })



.controller('AccountOrdersCtrl', function ($scope) {

})



.controller('AccountVerificationCtrl', function ($scope) {

})



.controller('AccountCommentsCtrl', function ($scope) {

})



.controller('AccountInfoCtrl', ['$scope', '$ionicActionSheet', 'config', '$http', '$rootScope',
  '$ionicModal', '$ionicPopup', 'cameraService', '$ionicLoading', 'AccountInfoService', 'debugService',
  function ($scope, $ionicActionSheet, config, $http, $rootScope, $ionicModal, $ionicPopup,
    cameraService, $ionicLoading, AccountInfoService, debugService) {

    //debugService.popupDebugMsg(AccountInfoService.getCurrentProfilePhotoURI());

    $scope.update = {};
    $scope.account = {};

    if (null !== AccountInfoService.getCurrentProfilePhotoURI()) {
      $scope.ProfilePhotoURI = AccountInfoService.getCurrentProfilePhotoURI();
    }

    $http.get(config.url + cmd['user_info_get'] + '?userID=' + $rootScope.user.id).success(
      function (data) {
        if(data.responseStr == 'Success') {
          $scope.account = data.user;
          $scope.account.phone = $rootScope.user.phone;
          $scope.account.status = userType[$scope.account.userType];
          $scope.account.academic = academic[$scope.account.userType];
        } else {
          $ionicLoading.show({template: responseCode[data.responseStr], duration: 1000});
          return false;
        }
      }).error(function (data) {
          $ionicLoading.show({template: responseCode['Network_Error'], duration: 1000});
          return false;
      });


      $ionicModal.fromTemplateUrl('update_name_modal.html', {
        scope: $scope,
        animation: 'slide-in-up'
      }).then(function(modal) {
        $scope.updateNameModal = modal;
      });

      $scope.openUpdateNameModal = function () {
        $scope.updateNameModal.show();
      };

      $scope.closeUpdateNameModal = function () {
        $scope.updateNameModal.hide();
      };

      $scope.updateUserName = function () {
        $scope.account.FirstName = $scope.update.FirstName;
        $scope.account.LastName = $scope.update.LastName;

        $http.post(config.url + cmd['user_info_update'],{
          user: $scope.account
        }).success(function (data) {
          if(data.responseStr == "Success") {
            $ionicLoading.show({template: responseCode["Update_Success"], duration: 1000});
            $scope.updateNameModal.hide();
          } else {
            $ionicLoading.show({template: responseCode[data.responseStr], duration: 1000});
            return false;
          }
        }).error(function (data) {
          $ionicLoading.show({template: responseCode['Network_Error'], duration: 1000});
          return false;
        });
      }

  var myPopup;

  $scope.showPopup = function () {
    // An elaborate, custom popup
    myPopup = $ionicPopup.show({
      scope: $scope,
      template: '<button class="button button-full button-positive" ng-click="takePhoto(\'fromCamera\')">拍照选取</button>'
              + '<button class="button button-full button-positive" ng-click="takePhoto(\'fromPhotoAlbum\')">从相册中选取</button>',
      buttons: [
        { text: '取消',
          type: 'button-positive'
        }
      ]
    });

    myPopup.then(function (res) {
      console.log('Tapped!', res);
    });
  };

  $scope.takePhoto = function (sourceFrom) {
    myPopup.close();

    var photoSource = sourceFrom === 'fromPhotoAlbum' ? 0 : 1;

    var options = {
      quality: 100,
      allowEdit: true,          // whether to allow editing after the photo is taken
      sourceType: photoSource  // PHOTOLIBRARY(0): Choose image from picture library (same as SAVEDPHOTOALBUM(2) for Android); CAMERA(1)

    };

    cameraService.getPicture(options).then(function (imageURI) {
      debugService.popupDebugMsg(imageURI);

      $scope.ProfilePhotoURI = imageURI;
      AccountInfoService.setCurrentProfilePhotoURI(imageURI);

    }, function (err) {}, {});
  };

}])



.controller('AccountInvitationCtrl', function ($scope) {

})



.controller('AccountSettingsCtrl', function ($scope) {

})



.controller('PublicCatagoryCtrl', function ($rootScope, $scope) {

})



.controller('ClassDetailCtrl', function ($scope) {

})



.controller('OrderClassCtrl', function ($scope) {

})



.controller('IdentityVerificationCtrl', function ($scope, $ionicPopup, cameraService) {
  var myPopup;

  $scope.showPopup = function () {
      // An elaborate, custom popup
      myPopup = $ionicPopup.show({
        scope: $scope,
        template: '<button class="button button-full button-positive" ng-click="takePhoto(\'fromCamera\')">拍照选取</button>'
                + '<button class="button button-full button-positive" ng-click="takePhoto(\'fromPhotoAlbum\')">从相册中选取</button>',
        buttons: [
          { text: '取消',
            type: 'button-positive'
          }
        ]
      });

      myPopup.then(function (res) {
        console.log('Tapped!', res);
      });
    };

  $scope.takePhoto = function (sourceFrom) {
    myPopup.close();

    var photoSource = sourceFrom === 'fromPhotoAlbum' ? 0 : 1;

    var options = {
      quality: 100,
      allowEdit: true,          // whether to allow editing after the photo is taken
      sourceType: photoSource,  // PHOTOLIBRARY(0): Choose image from picture library (same as SAVEDPHOTOALBUM(2) for Android); CAMERA(1)
    };

    cameraService.getPicture(options).then(function (imageURI) {
      $scope.lastPhoto = imageURI;
    }, function (err) {}, {});
  };
})



.controller('RequirementPostCtrl', function ($scope) {

});


