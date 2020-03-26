import 'bootstrap/dist/css/bootstrap.css';
import {BootstrapVue, BootstrapVueIcons} from 'bootstrap-vue';
import 'bootstrap-vue/src/icons.scss'
import {DropDownListPlugin} from "@syncfusion/ej2-vue-dropdowns";
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import Vuelidate from "vuelidate";
import VueLogger from 'vuejs-logger';
import FlashMessage from "@smartweb/vue-flash-message";
import axios from 'axios';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'

// logging options
const isProduction = process.env.NODE_ENV === 'production';
const options = {
    isEnabled: true,
    logLevel: isProduction ? 'error' : 'debug',
    stringifyArguments: false,
    showLogLevel: true,
    showMethodName: true,
    separator: '|',
    showConsoleColors: true
};

const flash_config = {
    time: 5000,
    icon: true
};

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);
Vue.use(DropDownListPlugin);
Vue.use(axios);
Vue.use(Vuelidate);
Vue.use(VueLogger, options);
Vue.use(FlashMessage, flash_config);
Vue.component('font-awesome-icon', FontAwesomeIcon);
Vue.config.productionTip = false;

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
