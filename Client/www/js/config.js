angular.module('alearn.config',['ionic'])

.constant('api_host',{
  url: ''
})
.constant('patterns',{
  mobile: /^1\d{10}$/,
  email: /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/,
})
