import Vue from 'vue'
import App from './App.vue'
import { Row, Col, Divider,Input,Button,Tag,Message,Dialog,Image } from 'element-ui';

Vue.config.productionTip = false
Vue.use(Row)
Vue.use(Col)
Vue.use(Divider)
Vue.use(Input)
Vue.use(Button)
Vue.use(Tag)
Vue.use(Dialog)
Vue.use(Image)

Vue.prototype.$message = Message;

new Vue({
  render: h => h(App),
}).$mount('#app')
