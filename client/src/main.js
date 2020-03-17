import 'bootstrap/dist/css/bootstrap.css';
import {BootstrapVue, BootstrapVueIcons} from 'bootstrap-vue';
import 'bootstrap-vue/src/icons.scss'
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import Vuelidate from "vuelidate";
import FlashMessage from "@smartweb/vue-flash-message";
import axios from 'axios';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);
Vue.use(axios);
Vue.use(Vuelidate);
Vue.use(FlashMessage);
Vue.component('font-awesome-icon', FontAwesomeIcon);
Vue.config.productionTip = false;

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
