import 'bootstrap/dist/css/bootstrap.css';
import {BootstrapVue, BootstrapVueIcons} from 'bootstrap-vue';
import 'bootstrap-vue/src/icons.scss'
import {DropDownListPlugin} from "@syncfusion/ej2-vue-dropdowns";
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import Page from 'v-page';
import Vuelidate from "vuelidate";
import VueLogger from 'vuejs-logger';
import FlashMessage from "@smartweb/vue-flash-message";
import axios from 'axios';
import VueAxios from 'vue-axios';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'
import Loading from 'vue-loading-overlay';


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

const pagination_config = {
    language: 'en'
}

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);
Vue.use(DropDownListPlugin);
Vue.use(VueAxios, axios);
Vue.use(Vuelidate);
Vue.use(VueLogger, options);
Vue.use(FlashMessage, flash_config);
Vue.use(Loading);
Vue.use(Page, pagination_config)

Vue.component('font-awesome-icon', FontAwesomeIcon);
Vue.config.productionTip = false;


new Vue({
    router,
    render: h => h(App),
}).$mount('#app');
