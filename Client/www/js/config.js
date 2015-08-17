angular.module('alearn.config',[])

.constant('config',{
  /*time: 2015-08-16
  *author: ant
  *content: platform config
  */
  platFormConfig: {
    host: '',
    verision: '0.0.0.0',
  },

  /*time: 2015-08-16
  *author: ant
  *content: home banner config
  */
  banner: {
    width: 1300,
    height: 450,
    changeTime: 5000,
    speed: 500
  }
})
