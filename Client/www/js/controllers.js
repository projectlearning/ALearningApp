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



.controller('AccountTabCtrl', ['$scope', 'AccountService', '$rootScope', 'cacheService', '$http', 'config','$ionicLoading',
  function ($scope, AccountService, $rootScope, cacheService, $http, config, $ionicLoading) {
    $rootScope.user.isSign = true;
    //$rootScope.user.id = 1001;
    console.log(config.url + cmd['user_info_get'] + '?userID=' + $rootScope.user.id);
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



.controller('AccountRegisterCtrl', ['$scope', '$timeout', '$ionicLoading', 'cacheService', 'config','$http',
  function ($scope, $timeout,$ionicLoading, cacheService, config,$http) {
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
        password: $scope.register.password
        }).success(function (data) {
          $ionicLoading.hide();
          if(data.responseStr == "Success") {
              $http.post(config.url + cmd['user_login'],{
                phone: $scope.register.phone,
                password: $scope.register.phone
              }).success(function(data) {
                $rootScope.user.isSign = true;
                $rootScope.user.id = data.userID;
                $rootScope.user.token = data.token;
                $rootScope.user.phone = $scope.register.phone;
                cacheService.system.put('USERID', $rootScope.user.token);
                cacheService.system.put('TOKEN', $rootScope.user.token);
                cacheService.system.put('USERPHONE', $rootScope.user.phone);
              })
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
      password: $scope.login.password
    }).success(function (data) {
      $ionicLoading.hide();

      if(data.responseStr == "Success") {
          $rootScope.user.isSign = true;
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
  '$ionicActionSheet','$ionicListDelegate',
  function ($scope, $ionicActionSheet, config, $http, $rootScope, $ionicModal, $ionicPopup,
    cameraService, $ionicLoading, AccountInfoService, debugService,$ionicActionSheet,$ionicListDelegate) {

    //debugService.popupDebugMsg(AccountInfoService.getCurrentProfilePhotoURI());

    $scope.update = {};
    $scope.account = {};
    $scope.account.teaching_record = {};
    $scope.user_type_list = userType;
    $scope.user_academic_list = academic;
    //console.log(angular.isArray($scope.user_type_list));
    //console.log(userType['1']);

    if (null !== AccountInfoService.getCurrentProfilePhotoURI()) {
      $scope.ProfilePhotoURI = AccountInfoService.getCurrentProfilePhotoURI();
    }

    $http.get(config.url + cmd['user_info_get'] + '?userID=' + $rootScope.user.id).success(
      function (data) {
        if(data.responseStr == 'Success') {
          $scope.account = data.user;
          $scope.account.phone = $rootScope.user.phone;
          $scope.account.status = userType[$scope.account.UserType];
          $scope.account.academic = academic[$scope.account.AcademicQualification];
        } else {
          $ionicLoading.show({template: responseCode[data.responseStr], duration: 1000});
          return false;
        }
      }).error(function (data) {
          $ionicLoading.show({template: responseCode['Network_Error'], duration: 1000});
          return false;
      });

    $scope.update.user_type = $scope.account.UserType;
    $scope.update.user_academic = $scope.account.AcademicQualification;


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

        $ionicLoading.show({
          template: responseCode['Updateing']
        });
        $http.post(config.url + cmd['user_info_update'] + '?userId=' + $rootScope.user.id,{
          //firstname: $scope.update.FirstName,
          //lastname: $scope.update.LastName
          username: $scope.update.UserName
        }).success(function (data) {
          if(data.responseStr == "Success") {
            $ionicLoading.hide();
            $scope.account.FirstName = $scope.update.FirstName;
            $scope.account.LastName = $scope.update.LastName;
            $ionicLoading.show({template: responseCode["Update_Success"], duration: 1000});
            $scope.updateNameModal.hide();
          } else {
            $ionicLoading.hide();
            $ionicLoading.show({template: responseCode[data.responseStr], duration: 1000});
            return false;
          }
        }).error(function (data) {
          $ionicLoading.hide();
          $ionicLoading.show({template: responseCode['Network_Error'], duration: 1000});
          return false;
        });
      }

    $ionicModal.fromTemplateUrl('update_type_modal.html', {
        scope: $scope,
        animation: 'slide-in-up'
      }).then(function(modal) {
        $scope.updateTypeModal = modal;
      });

    $scope.openUpdateTypeModal = function () {
        $scope.updateTypeModal.show();
      };

    $scope.closeUpdateTypeModal = function () {
        $scope.updateTypeModal.hide();
      };

    $scope.updateUserType = function () {
      //console.log($scope.update.user_type);
      $ionicLoading.show({
        template: responseCode['Updateing']
      });
      $http.post(config.url + cmd['user_info_update'] + '?userId=' + $rootScope.user.id,{
        usertype: $scope.update.user_type
      }).success(function (data) {
        if(data.responseStr == "Success") {
          $ionicLoading.hide();
          $scope.account.UserType = $scope.update.user_type;
          $ionicLoading.show({template: responseCode["Update_Success"], duration: 1000});
          $scope.updateTypeModal.hide();
        } else {
          $ionicLoading.hide();
          $ionicLoading.show({template: responseCode[data.responseStr], duration: 1000});
          return false;
        }
      }).error(function (data) {
        $ionicLoading.hide();
        $ionicLoading.show({template: responseCode['Network_Error'], duration: 1000});
        return false;
      });
    }

    $ionicModal.fromTemplateUrl('update_academic_model.html', {
        scope: $scope,
        animation: 'slide-in-up'
      }).then(function(modal) {
        $scope.updateAcademicModal = modal;
      });

    $scope.openUpdateAcademicModal = function () {
        $scope.updateAcademicModal.show();
      };

    $scope.closeUpdateAcademicModal = function () {
        $scope.updateAcademicModal.hide();
      };

    $scope.updateUserAcademic = function () {
      console.log($scope.update.user_academic);
      $ionicLoading.show({
        template: responseCode['Updateing']
      });
      $http.post(config.url + cmd['user_info_update'] + '?userId=' + $rootScope.user.id,{
        academicqualification: $scope.update.user_academic
      }).success(function (data) {
        if(data.responseStr == "Success") {
          $ionicLoading.hide();
          $scope.account.AcademicQualification = $scope.update.user_academic;
          $ionicLoading.show({template: responseCode["Update_Success"], duration: 1000});
          $scope.updateAcademicModal.hide();
        } else {
          $ionicLoading.hide();
          $ionicLoading.show({template: responseCode[data.responseStr], duration: 1000});
          return false;
        }
      }).error(function (data) {
        $ionicLoading.hide();
        $ionicLoading.show({template: responseCode['Network_Error'], duration: 1000});
        return false;
      });
    }

  /*设置USER学校*/
  $ionicModal.fromTemplateUrl('update_school_modal.html', {
        scope: $scope,
        animation: 'slide-in-up'
      }).then(function(modal) {
        $scope.updateSchoolModal = modal;
      });

    $scope.openUpdateSchoolModal = function () {
        $scope.updateSchoolModal.show();
      };

    $scope.closeUpdateSchoolModal = function () {
        $scope.updateSchoolModal.hide();
      };

    $scope.updateUserSchool = function () {
      console.log($scope.update.user_school);
      $ionicLoading.show({
        template: responseCode['Updateing']
      });
      $http.post(config.url + cmd['user_info_update'] + '?userId=' + $rootScope.user.id,{
        graduatefrom: $scope.update.user_school
      }).success(function (data) {
        if(data.responseStr == "Success") {
          $ionicLoading.hide();
          $scope.account.GraduateFrom = $scope.update.user_school;
          $ionicLoading.show({template: responseCode["Update_Success"], duration: 1000});
          $scope.updateAcademicModal.hide();
        } else {
          $ionicLoading.hide();
          $ionicLoading.show({template: responseCode[data.responseStr], duration: 1000});
          return false;
        }
      }).error(function (data) {
        $ionicLoading.hide();
        $ionicLoading.show({template: responseCode['Network_Error'], duration: 1000});
        return false;
      });
    }

  /*设置USER地址*/
  $ionicModal.fromTemplateUrl('update_address_modal.html', {
        scope: $scope,
        animation: 'slide-in-up'
      }).then(function(modal) {
        $scope.updateAddressModal = modal;
      });

    $scope.openUpdateAddressModal = function () {
        $scope.updateAddressModal.show();
      };

    $scope.closeUpdateAddressModal = function () {
        $scope.updateAddressModal.hide();
      };

    $scope.updateUserAddress = function () {
      console.log($scope.update.user_address);
      $ionicLoading.show({
        template: responseCode['Updateing']
      });
      $http.post(config.url + cmd['user_info_update'] + '?userId=' + $rootScope.user.id,{
        addressforclass: $scope.update.user_address
      }).success(function (data) {
        if(data.responseStr == "Success") {
          $ionicLoading.hide();
          $scope.account.AddressForClass = $scope.update.user_address;
          $ionicLoading.show({template: responseCode["Update_Success"], duration: 1000});
          $scope.updateAcademicModal.hide();
        } else {
          $ionicLoading.hide();
          $ionicLoading.show({template: responseCode[data.responseStr], duration: 1000});
          return false;
        }
      }).error(function (data) {
        $ionicLoading.hide();
        $ionicLoading.show({template: responseCode['Network_Error'], duration: 1000});
        return false;
      });
    }

  $ionicModal.fromTemplateUrl('get_teaching_record.html', {
    scope: $scope,
    animation: 'slide-in-up'
  }).then(function(modal) {
    $scope.getTeachingRecordModal = modal;
  });

  $scope.openGetTeachingRecordModal = function () {
    $http.get(config.url + cmd['teaching_record_get'] + '?userID=' + $rootScope.user.id).success(
      function (data) {
        if(data.responseStr == 'Success') {
          $scope.account.teaching_record = data.record;
        }
        else {
          $ionicLoading.show({template: responseCode[data.responseStr], duration: 1000});
          return false;
        }
      }).error(function (data) {
        $ionicLoading.show({template: responseCode['Network_Error'], duration: 1000});
         return false;
      });
    $scope.getTeachingRecordModal.show();
  };
  $scope.closeGetTeachingRecordModal = function () {
    $scope.getTeachingRecordModal.hide();
  };
  $scope.deleteTeachingRecord = function (id, index) {
    var deleteRecord = $ionicActionSheet.show({
      titleText: '确认删除?',
      cancelText: '确认',
      destructiveText: '删除',
      cancel: function () {
      // 如果用户选择cancel, 则会隐藏删除按钮
        $ionicListDelegate.closeOptionButtons();
      },
      destructiveButtonClicked: function () {
        // 通过id删除开支记录
        $http.post(config.url + cmd['teaching_record_delete'] + '?userId=' + $rootScope.user.id,{}).success(
          function(data) {
            if(data.responseStr == 'Success') {
              $ionicLoading.show({template: responseCode["Delete_Success"], duration: 1000});
              //删除数组中的元素
              $scope.account.teaching_record.splice(index , 1);
            }
            else {
              $ionicLoading.show({template: responseCode[data.responseStr], duration: 1000});
              return false;
            }
          }).error(function (data) {
            $ionicLoading.show({template: responseCode['Network_Error'], duration: 1000});
            return false;
          })

        // 隐藏对话框
        deleteTeachingRecord();
      }
    });
  };

  $ionicModal.fromTemplateUrl('teaching_record_detail.html', {
    scope: $scope,
    animation: 'slide-in-up'
  }).then(function(modal) {
    $scope.teachingRecordDetailModal = modal;
  });

  $scope.teachRecordStartDate = {};
  var startDatePickerCallback = function (val) {
    if (typeof(val) === 'undefined') {
      console.log('No date selected');
    } else {
      $scope.teachRecordStartDate.inputDate = val;
    }
  };

  $scope.teachRecordEndDate = {};
  var endDatePickerCallback = function (val) {
    if (typeof(val) === 'undefined') {
      console.log('No date selected');
    } else {
      $scope.teachRecordEndDate.inputDate = val;
    }
  };
  $scope.openTeachingRecordDetailModal = function () {
    $scope.teachingRecordDetailModal.show();
    $scope.teachRecordStartDate = {
      titleLabel: '开始日期',  //Optional
      todayLabel: '今天',  //Optional
      closeLabel: '关闭',  //Optional
      setLabel: '确定',  //Optional
      setButtonType : 'button-assertive',  //Optional
      todayButtonType : 'button-assertive',  //Optional
      closeButtonType : 'button-assertive',  //Optional
      inputDate: new Date(),    //Optional
      mondayFirst: true,    //Optional
      templateType: 'popup', //Optional
      showTodayButton: 'true', //Optional
      modalHeaderColor: 'bar-positive', //Optional
      modalFooterColor: 'bar-positive', //Optional
      from: new Date(2010, 1, 1),   //Optional
      to: new Date(2018, 12, 31),    //Optional
      callback: function (val) {    //Mandatory
        startDatePickerCallback(val);
      }
    };

    $scope.teachRecordEndDate = {
      titleLabel: '结束日期',  //Optional
      todayLabel: '今天',  //Optional
      closeLabel: '关闭',  //Optional
      setLabel: '确定',  //Optional
      setButtonType : 'button-assertive',  //Optional
      todayButtonType : 'button-assertive',  //Optional
      closeButtonType : 'button-assertive',  //Optional
      inputDate: new Date(),    //Optional
      mondayFirst: true,    //Optional
      templateType: 'popup', //Optional
      showTodayButton: 'true', //Optional
      modalHeaderColor: 'bar-positive', //Optional
      modalFooterColor: 'bar-positive', //Optional
      from: new Date(2010, 1, 1),   //Optional
      to: new Date(2018, 12, 31),    //Optional
      callback: function (val) {    //Mandatory
        endDatePickerCallback(val);
      }
    };
  };

  $scope.closeTeachingRecordDetailModal = function () {
    $scope.teachingRecordDetailModal.hide();
  };

  $scope.teaching_record_description = "";
  $scope.insertTeachingRecord = function () {
    $http.post(config.url + cmd['teaching_record_add'] + '?userId=' + $rootScope.user.id,{
      starttime: $scope.teachRecordStartDate.inputDate,
      endtime: $scope.teachRecordEndDate.inputDate,
      description: $scope.teaching_record_description,
    }).success(function (data) {
      if(data.responseStr == "Success")
      {
        $ionicLoading.show({template: responseCode["Save_Success"], duration: 1000});
      } else {
        $ionicLoading.show({template: responseCode[data.responseStr], duration: 1000});
        return false;
      }
    }).error(function (data) {
      $ionicLoading.show({template: responseCode['Network_Error'], duration: 1000});
      return false;
    })
  }

  $scope.updateTeachingRecord = function (id) {
    $http.post(config.url + cmd['teaching_record_update'] + '?userId=' + $rootScope.user.id + '&teachingRecordId=' + id,{
      starttime: $scope.teachRecordStartDate.inputDate,
      endtime: $scope.teachRecordEndDate.inputDate,
      description: $scope.teaching_record_description
    }).success(function (data) {
      if(data.responseStr == "Success")
      {
        $ionicLoading.show({template: responseCode["Save_Success"], duration: 1000});
      } else {
        $ionicLoading.show({template: responseCode[data.responseStr], duration: 1000});
        return false;
      }
    }).error(function (data) {
      $ionicLoading.show({template: responseCode['Network_Error'], duration: 1000});
      return false;
    })
  }

  $ionicModal.fromTemplateUrl('get_successful_cases.html', {
    scope: $scope,
    animation: 'slide-in-up'
  }).then(function(modal) {
    $scope.getSuccessfulCasesModal = modal;
  });

  $scope.openGetSuccessfulCasesModal = function () {
    $http.get(config.url + cmd['successful_cases_get'] + '?userID=' + $rootScope.user.id).success(
      function (data) {
        if(data.responseStr == 'Success') {
          $scope.account.successful_cases = data.record;
        }
        else {
          $ionicLoading.show({template: responseCode[data.responseStr], duration: 1000});
          return false;
        }
      }).error(function (data) {
        $ionicLoading.show({template: responseCode['Network_Error'], duration: 1000});
         return false;
      });
    $scope.getSuccessfulCasesModal.show();
  };
  $scope.closeGetSuccessfulCasesModal = function () {
    $scope.getSuccessfulCasesModal.hide();
  };
  $scope.deleteSuccessfulCases = function (id, index) {
    var deleteRecord = $ionicActionSheet.show({
      titleText: '确认删除?',
      cancelText: '确认',
      destructiveText: '删除',
      cancel: function () {
      // 如果用户选择cancel, 则会隐藏删除按钮
        $ionicListDelegate.closeOptionButtons();
      },
      destructiveButtonClicked: function () {
        // 通过id删除开支记录
        $http.post(config.url + cmd['successful_cases_delete'] + '?userId=' + $rootScope.user.id,{}).success(
          function(data) {
            if(data.responseStr == 'Success') {
              $ionicLoading.show({template: responseCode["Delete_Success"], duration: 1000});
              //删除数组中的元素
              $scope.account.successful_cases.splice(index , 1);
            }
            else {
              $ionicLoading.show({template: responseCode[data.responseStr], duration: 1000});
              return false;
            }
          }).error(function (data) {
            $ionicLoading.show({template: responseCode['Network_Error'], duration: 1000});
            return false;
          })

        // 隐藏对话框
        deleteTeachingRecord();
      }
    });
  };

  $ionicModal.fromTemplateUrl('successful_cases_detail.html', {
    scope: $scope,
    animation: 'slide-in-up'
  }).then(function(modal) {
    $scope.successfulCasesDetailModal = modal;
  });
  $scope.successfulCasesStartDate = {};
  var successfulCasesStartDatePickerCallback = function (val) {
    if (typeof(val) === 'undefined') {
      console.log('No date selected');
    } else {
      $scope.successfulCasesStartDate.inputDate = val;
    }
  };

  $scope.successfulCasesEndDate = {};
  var successfulCasesEndDatePickerCallback = function (val) {
    if (typeof(val) === 'undefined') {
      console.log('No date selected');
    } else {
      $scope.successfulCasesEndDate.inputDate = val;
    }
  };
  $scope.openSuccessfulCasesDetailModal = function () {
    $scope.successfulCasesDetailModal.show();
    $scope.successfulCasesStartDate = {
      titleLabel: '开始日期',  //Optional
      todayLabel: '今天',  //Optional
      closeLabel: '关闭',  //Optional
      setLabel: '确定',  //Optional
      setButtonType : 'button-assertive',  //Optional
      todayButtonType : 'button-assertive',  //Optional
      closeButtonType : 'button-assertive',  //Optional
      inputDate: new Date(),    //Optional
      mondayFirst: true,    //Optional
      templateType: 'popup', //Optional
      showTodayButton: 'true', //Optional
      modalHeaderColor: 'bar-positive', //Optional
      modalFooterColor: 'bar-positive', //Optional
      from: new Date(2010, 1, 1),   //Optional
      to: new Date(2018, 12, 31),    //Optional
      callback: function (val) {    //Mandatory
        successfulCasesStartDatePickerCallback(val);
      }
    };

    $scope.successfulCasesEndDate = {
      titleLabel: '结束日期',  //Optional
      todayLabel: '今天',  //Optional
      closeLabel: '关闭',  //Optional
      setLabel: '确定',  //Optional
      setButtonType : 'button-assertive',  //Optional
      todayButtonType : 'button-assertive',  //Optional
      closeButtonType : 'button-assertive',  //Optional
      inputDate: new Date(),    //Optional
      mondayFirst: true,    //Optional
      templateType: 'popup', //Optional
      showTodayButton: 'true', //Optional
      modalHeaderColor: 'bar-positive', //Optional
      modalFooterColor: 'bar-positive', //Optional
      from: new Date(2010, 1, 1),   //Optional
      to: new Date(2018, 12, 31),    //Optional
      callback: function (val) {    //Mandatory
        successfulCasesEndDatePickerCallback(val);
      }
    };
  };

  $scope.closeSuccessfulCasesDetailModal = function () {
    $scope.successfulCasesDetailModal.hide();
  };

  $scope.successful_cases_description = "";
  $scope.insertSuccessfulCases = function () {
    $http.post(config.url + cmd['successful_cases_add'] + '?userId=' + $rootScope.user.id,{
      starttime: $scope.successfulCasesStartDate.inputDate,
      endtime: $scope.successfulCasesEndDate.inputDate,
      description: $scope.successful_cases_description,
    }).success(function (data) {
      if(data.responseStr == "Success")
      {
        $ionicLoading.show({template: responseCode["Save_Success"], duration: 1000});
      } else {
        $ionicLoading.show({template: responseCode[data.responseStr], duration: 1000});
        return false;
      }
    }).error(function (data) {
      $ionicLoading.show({template: responseCode['Network_Error'], duration: 1000});
      return false;
    })
  }

  $scope.updateSuccessfulCases = function (id) {
    $http.post(config.url + cmd['successful_cases_update'] + '?userId=' + $rootScope.user.id + '&successfulCasesId=' + id,{
      starttime: $scope.successfulCasesStartDate.inputDate,
      endtime: $scope.successfulCasesEndDate.inputDate,
      description: $scope.teaching_record_description
    }).success(function (data) {
      if(data.responseStr == "Success")
      {
        $ionicLoading.show({template: responseCode["Save_Success"], duration: 1000});
      } else {
        $ionicLoading.show({template: responseCode[data.responseStr], duration: 1000});
        return false;
      }
    }).error(function (data) {
      $ionicLoading.show({template: responseCode['Network_Error'], duration: 1000});
      return false;
    })
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


