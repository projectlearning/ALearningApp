angular.module('alearn.config',['ionic'])

.constant('config',{
  url: "",
  host: "",
  api: "",
  version: "",
  uuid: "",
  model: "",
  platform: "",
  os_version: "",
  latitude: 0,
  longitude: 0,
  signature: '',
  address_city: "",
  user_status: ""
})
.constant('patterns',{
  mobile: /^1\d{10}$/,
  email: /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/,
})
