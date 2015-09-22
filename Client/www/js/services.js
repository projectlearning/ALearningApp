angular.module('alearn.services', ['ionic'])

.factory('Chats', function() {
  // Might use a resource here that returns a JSON array

  // Some fake testing data
  var chats = [{
    id: 0,
    name: 'Ben Sparrow',
    lastText: 'You on your way?',
    face: 'https://pbs.twimg.com/profile_images/514549811765211136/9SgAuHeY.png'
  }, {
    id: 1,
    name: 'Max Lynx',
    lastText: 'Hey, it\'s me',
    face: 'https://avatars3.githubusercontent.com/u/11214?v=3&s=460'
  }, {
    id: 2,
    name: 'Adam Bradleyson',
    lastText: 'I should buy a boat',
    face: 'https://pbs.twimg.com/profile_images/479090794058379264/84TKj_qa.jpeg'
  }, {
    id: 3,
    name: 'Perry Governor',
    lastText: 'Look at my mukluks!',
    face: 'https://pbs.twimg.com/profile_images/598205061232103424/3j5HUXMY.png'
  }, {
    id: 4,
    name: 'Mike Harrington',
    lastText: 'This is wicked good ice cream.',
    face: 'https://pbs.twimg.com/profile_images/578237281384841216/R3ae1n61.png'
  }];

  return {
    all: function() {
      return chats;
    },
    remove: function(chat) {
      chats.splice(chats.indexOf(chat), 1);
    },
    get: function(chatId) {
      for (var i = 0; i < chats.length; i++) {
        if (chats[i].id === parseInt(chatId)) {
          return chats[i];
        }
      }
      return null;
    }
  };
})

.factory('BannerService',function(){
  // Might use a resource here that returns a JSON array

  // Some fake testing data
  var banners = [{
    id: 0,
    image: 'img/home-slider01.jpg',
    title: '',
    url: ''
  }, {
    id: 1,
    image: 'img/home-slider02.jpg',
    title: '',
    url: ''
  }];

  return {
    get: function() {
      /*

      */
      return banners;
    },
  };
})

.factory('CityPickerService',function(){
  var cities = {
    now_city: '广州',
    hot_city: [{
      id: 0,
      name_zh: '广州',
      name_en: 'Guang Zhou'
    },{
      id: 1,
      name_zh: '佛山',
      name_en: 'Fo Shan'
    },{
      id: 2,
      name_zh: '深圳',
      name_en: 'Shen Zhen'
    }],
  };

  return {
    getNowCity: function(){
      return cities.now_city;
    },
    setNowCity: function(name){
      cities.now_city = name;
    },
    getHotCities: function()
    {
      return cities.hot_city;
    },
    getAllCities: function()
    {
      return cities.all_city;
    }
  };
})

.factory('AccountService', function(){
  var account = {
    loginFlag: 1,
    username: 'Ant',
    tel: '12345678',
  };

  return {
    getAccount: function(){
      return account;
    },
    login: function(user){

    }
  };
})
