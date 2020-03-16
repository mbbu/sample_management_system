import 'bootstrap/dist/css/bootstrap.css';
import {BootstrapVue, IconsPlugin} from 'bootstrap-vue';
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import Vuelidate from "vuelidate";
import axios from 'axios';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);
Vue.use(axios);
Vue.use(Vuelidate);
Vue.component('font-awesome-icon', FontAwesomeIcon);
Vue.config.productionTip = false;

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
