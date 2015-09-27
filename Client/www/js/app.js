// Ionic ALearn App
// angular.module is a global place for creating, registering and retrieving Angular modules
// 'alearn' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
// 'alearn.controllers' is found in controllers.js
// 'alearn.services' is found in services.js
var app = angular.module('alearn', ['ionic', 'alearn.controllers', 'alearn.services','alearn.directives','alearn.config','ngCordova'])

app.run(['$ionicPlatform','$cordovaAppVersion','config','$rootScope','$http','cacheService', '$cordovaAppVersion','versionService','$cordovaDevice'
  function($ionicPlatform,$cordovaAppVersion,config,$rootScope,$http,cacheService,$cordovaAppVersion,versionService,$cordovaDevice) {
  
  $rootScope.user || $rootScope.user = {};
  $ionicPlatform.ready(function() {
    console.log('platform ready');
    config.platform = ionic.Platform.platform();
    config.os_version = ionic.Platform.version();
    $rootScope.user.platform = ionic.Platform.platform();
    $rootScope.user.os_version = ionic.Platform.version();
    $http.defaults.cache = cacheService.product;

    /*检测版本*/
    $cordovaAppVersion.getVersionNumber().then(function(version){
      config.version = version;
      if(config.version !== cacheService.system.get('version'))
        cacheService.system.put('version',config.version);
      var r = versionService.check(config.platform);
      r.success(function(data){
        if(data.version !== config.version)
        {

        }
      })
    });

    config.uuid = $cordovaDevice.getUUID();
    config.model = $cordovaDevice.getModel();
    // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
    // for form inputs)
    if (window.cordova && window.cordova.plugins && window.cordova.plugins.Keyboard) {
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
      cordova.plugins.Keyboard.disableScroll(true);

    }
    if (window.StatusBar) {
      // org.apache.cordova.statusbar required
      StatusBar.styleLightContent();
    }
  });
}])

app.config(function($stateProvider, $urlRouterProvider, $ionicConfigProvider) {
  // ====================================================
  // ionic config
  // ====================================================
  $ionicConfigProvider.backButton.text('返回').icon('ion-ios-arrow-left'); // set icon of back button and the text after the back button
  $ionicConfigProvider.backButton.previousTitleText(false); // whether to display title text of previous view after the back button
  $ionicConfigProvider.tabs.style('standard'); // tab样式
  $ionicConfigProvider.tabs.position('bottom');
  $ionicConfigProvider.navBar.alignTitle('center'); // title位置

  // Ionic uses AngularUI Router which uses the concept of states
  // Learn more here: https://github.com/angular-ui/ui-router
  // Set up the various states which the app can be in.
  // Each state's controller can be found in controllers.js
  $stateProvider

  // setup an abstract state for the tabs directive
  .state('tabs', {
    url: '/tabs',
    abstract: true,
    templateUrl: 'templates/tabs.html'
  })

  // Each tab has its own nav history stack:

  .state('tabs.homeTab', {
    url: '/home',
    views: {
      'homeTab': {
        templateUrl: 'templates/homeTab.html',
        controller: 'HomeTabCtrl'
      }
    }
  })
    .state('tabs.citypicker', {
      url: '/citypicker',
      views: {
        'homeTab': {
          templateUrl: 'templates/public/citypicker.html',
          controller: 'CityPickerCtrl'
        }
      }
    })

    .state('homeSearch', {
      url: '/homeSearch',
      templateUrl: 'templates/homeSearch.html',
      controller: 'HomeSearchCtrl'
    })

  .state('tabs.classTab', {
    url: '/class',
    views: {
      'classTab': {
        templateUrl: 'templates/classTab.html',
        controller: 'ClassTabCtrl'
      }
    }
  })

  .state('tabs.chatsTab', {
      url: '/chats',
      views: {
        'chatsTab': {
          templateUrl: 'templates/chatsTab.html',
          controller: 'ChatsTabCtrl'
        }
      }
    })
    .state('tabs.chatDetails', {
      url: '/chats/:chatId',
      views: {
        'chatsTab': {
          templateUrl: 'templates/chatDetails.html',
          controller: 'ChatDetailsCtrl'
        }
      }
    })

  .state('tabs.accountTab', {
    url: '/account',
    views: {
      'accountTab': {
        templateUrl: 'templates/accountTab.html',
        controller: 'AccountTabCtrl'
      }
    }
  })
  .state('tabs.accountLoginFailed', {
    url: '/account/loginFailed',
    views: {
      'accountTab': {
        templateUrl: 'templates/account/accountLoginFailed.html',
        controller: 'AccountLoginFailedCtrl'
      }
    }
  })
  .state('tabs.accountRegister', {
    url: '/account/register',
    views: {
      'accountTab': {
        templateUrl: 'templates/account/accountRegister.html',
        controller: 'AccountRegisterCtrl'
      }
    }
  })
  .state('tabs.accountLogin', {
    url: '/account/login',
    views: {
      'accountTab': {
        templateUrl: 'templates/account/accountLogin.html',
        controller: 'AccountLoginCtrl'
      }
    }
  })
  .state('tabs.accountMoney', {
    url: '/account/money',
    views: {
      'accountTab': {
        templateUrl: 'templates/account/accountMoney.html',
        controller: 'AccountMoneyCtrl'
      }
    }
  })
    .state('tabs.moneyAccountDetail', {
      url: '/account/money/moneyAccountDetail',
      views: {
        'accountTab': {
          templateUrl: 'templates/account/moneyAccount/moneyAccountDetail.html',
          controller: 'moneyAccountDetailCtrl'
        }
      }
    })
    .state('tabs.moneyAccountTopUp', {
      url: '/account/money/topUp',
      views: {
        'accountTab': {
          templateUrl: 'templates/account/moneyAccount/topUp.html',
          controller: 'moneyAccountTopUpCtrl'
        }
      }
    })
    .state('tabs.moneyWithdrawal', {
      url: '/account/money/moneyWithdrawal',
      views: {
        'accountTab': {
          templateUrl: 'templates/account/moneyAccount/moneyWithdrawal.html',
          controller: 'moneyWithdrawalCtrl'
        }
      }
    })
    .state('tabs.couponRedeem', {
      url: '/account/money/couponRedeem',
      views: {
        'accountTab': {
          templateUrl: 'templates/account/moneyAccount/couponRedeem.html',
          controller: 'couponRedeemCtrl'
        }
      }
    })
  .state('tabs.accountOrders', {
    url: '/account/orders',
    views: {
      'accountTab': {
        templateUrl: 'templates/account/accountOrders.html',
        controller: 'AccountOrdersCtrl'
      }
    }
  })
  .state('tabs.accountVerification', {
    url: '/account/verification',
    views: {
      'accountTab': {
        templateUrl: 'templates/account/accountVerification.html',
        controller: 'AccountVerificationCtrl'
      }
    }
  })
  .state('tabs.accountComments', {
    url: '/account/comments',
    views: {
      'accountTab': {
        templateUrl: 'templates/account/accountComments.html',
        controller: 'AccountCommentsCtrl'
      }
    }
  })
  .state('tabs.accountInfo', {
    url: '/account/info',
    views: {
      'accountTab': {
        templateUrl: 'templates/account/accountInfo.html',
        controller: 'AccountInfoCtrl'
      }
    }
  })
  .state('tabs.accountInvitation', {
    url: '/account/invitation',
    views: {
      'accountTab': {
        templateUrl: 'templates/account/accountInvitation.html',
        controller: 'AccountInvitationCtrl'
      }
    }
  })
  .state('tabs.accountSettings', {
    url: '/account/settings',
    views: {
      'accountTab': {
        templateUrl: 'templates/account/accountSettings.html',
        controller: 'AccountSettingsCtrl'
      }
    }
  })
  .state('tabs.publicCatagory', {
    url: '/public/catagory',
    views: {
      'homeTab': {
        templateUrl: 'templates/public/catagory.html',
        controller: 'PublicCatagoryCtrl'
      }
    }
  })
  .state('tabs.classDetail', {
    url: '/public/detail',
    views: {
      'homeTab': {
        templateUrl: 'templates/public/classDetail.html',
        controller: 'ClassDetailCtrl'
      }
    }
  })
  .state('tabs.orderClass', {
    url: '/public/order-class',
    views: {
      'homeTab': {
        templateUrl: 'templates/public/orderClass.html',
        controller: 'OrderClassCtrl'
      }
    }
  })

  .state('tabs.identityVerification', {
    url: '/verification/identity',
    views: {
      'accountTab': {
        templateUrl: 'templates/verification/identityVerification.html',
        controller: 'IdentityVerificationCtrl'
      }
    }
  })

  .state('tabs.requirementPost', {
    url: '/requirement/post',
    views: {
      'classTab': {
        templateUrl: 'templates/requirement/post.html',
        controller: 'RequirementPostCtrl'
      }
    }
  });

  // if none of the above states are matched, use this as the fallback
  $urlRouterProvider.otherwise('/tabs/home');
});
