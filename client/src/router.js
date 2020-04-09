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
import Lab from "./pages/Lab";
import Freezer from "./pages/Freezer";
import SignUp from "./pages/SignUp";
import ContactUs from "./pages/ContactUs";
import Rack from "./pages/Rack";
import Tray from "./pages/Tray";
import Publication from "./pages/Publication";


Vue.use(Router);

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/login',
            name: 'login',
            alias: ['/auth', '/auth/login'],
            component: Login,
        },

        {
            path: '/register',
            name: 'register',
            alias: ['/signup'],
            component: SignUp,
        },

        {
            path: '/contact-us',
            name: 'contact',
            alias: ['/contact'],
            component: ContactUs,
        },

        {
            path: '/updateprofile',
            name: 'updateprofile',
            component: UpdateProfile,
        },

        {
            path: '/home',
            name: 'Map',
            alias: ['/', '/index', '/welcome'],
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

        {
            path: '/lab',
            name: 'Lab',
            alias: ['/laboratory'],
            component: Lab,
        },

        {
            path: '/freezer',
            name: 'Freezer',
            alias: ['/freezer'],
            component: Freezer,
        },

        {
            path: '/rack',
            name: 'Rack',
            alias: ['/racks'],
            component: Rack,
        },

        {
            path: '/tray',
            name: 'Tray',
            alias: ['/trays'],
            component: Tray,
        },

        {
            path: '/publication',
            name: 'Publication',
            alias: ['/publications'],
            component: Publication,
        },


    ],
});
