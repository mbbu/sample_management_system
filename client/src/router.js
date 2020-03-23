import Vue from 'vue';
import Router from 'vue-router';
import Box from './pages/Box.vue';
import Sample from './pages/Sample.vue';
import Chamber from './pages/Chamber.vue';
import Theme from './pages/Theme.vue';
import Login from './pages/Login.vue';
import AddSample from './pages/AddSample.vue';
import Map from './pages/Map.vue';
import UpdateProfile from './pages/UpdateProfile.vue';
import SecurityLevel from "./pages/SecurityLevel";
import QuantityType from "./pages/QuantityType";


Vue.use(Router);

export default new Router({
     mode: 'history',
     base: process.env.BASE_URL,
     routes: [
         {
             path: '/login',
             name: 'login',
             alias: ['/signin'],
             component: Login,
         },

         {
             path: '/updateprofile',
             name: 'updateprofile',
             component: UpdateProfile,
         },

         {
             path: '/home',
             name: 'Map',
             alias: ['/welcome'],
             component: Map,
         },

         {
             path: '/box',
             name: 'Box',
             alias: ['/boxes'],
             component: Box,
         },

         {
             path: '/sample',
             name: 'Sample',
             alias: ['/samples'],
             component: Sample,
         },

         {
             path: '/addsample',
             name: 'AddSample',
             alias: ['/addsamples'],
             component: AddSample,
         },

         {
             path: '/chamber',
             name: 'chamber',
             alias: ['/chambers'],
             component: Chamber,
         },

         {
             path: '/theme',
             name: 'theme',
             alias: ['/themes'],
             component: Theme,
         },

         {
             path: '/security-level',
             name: 'SecurityLevel',
             alias: ['/securitylevel'],
             component: SecurityLevel,
         },

         {
             path: '/quantity-type',
             name: 'QuantityType',
             alias: ['/qt'],
             component: QuantityType,
         },


     ],
});
