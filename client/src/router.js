import Vue from 'vue';
import Router from 'vue-router';
import Box from './pages/Box.vue';
import Sample from './pages/Sample/ListSampleView.vue';
import Chamber from './pages/Chamber.vue';
import Theme from './pages/Theme.vue';
import Login from './pages/Login.vue';
import AddSample from './pages/Sample/Add_and_Update_Sample.vue';
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
import DetailedSampleView from "./pages/Sample/DetailedSampleView";
import {isUpdate} from "./utils/util_functions";


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
            path: '/add-sample',
            name: 'AddSample',
            alias: ['/addsample'],
            component: AddSample,
        },

        {
            path: '/view-sample',
            name: 'DetailedSampleView',
            alias: ['/viewsample'],
            component: DetailedSampleView,
        },

        {
            path: '/update-sample',
            name: 'UpdateSample',
            alias: ['/updatesample'],
            component: AddSample,
            condition: isUpdate()
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
            alias: ['/freezers'],
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
