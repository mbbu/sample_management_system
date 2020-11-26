import Vue from 'vue';
import Router from 'vue-router';
import Box from './pages/Box.vue';
import Sample from './pages/Sample/ListSampleView.vue';
import Chamber from './pages/Chamber.vue';
import Theme from './pages/Theme.vue';
import Login from './pages/Auth/Login.vue';
import AddSample from './pages/Sample/Add_and_Update_Sample.vue';
import Map from './pages/Map.vue';
import BioHazardLevel from "./pages/BioHazardLevel";
import QuantityType from "./pages/QuantityType";
import Lab from "./pages/Lab";
import Freezer from "./pages/Freezer";
import SignUp from "./pages/Auth/SignUp";
import ContactUs from "./pages/ContactUs";
import Rack from "./pages/Rack";
import Tray from "./pages/Tray";
import Publication from "./pages/Publication";
import DetailedSampleView from "./pages/Sample/DetailedSampleView";
import {isUpdate} from "./utils/util_functions";
import UserRole from "./pages/UserProfile/UserRole";
import UserCard from "./pages/UserProfile/UserCard";
import EditProfileForm from "./pages/UserProfile/EditProfileForm";
import ConfirmUser from "./pages/ConfirmUserAccount/ConfirmUser";
import ResendConfirmation from "./pages/ConfirmUserAccount/ResendConfirmation";
import PasswordResetRequest from "./pages/Auth/PasswordResetRequest";
import PasswordResetConfirmation from "./pages/Auth/PasswordResetConfirmation";
import Project from "./pages/Project";
import FetchSample from "./pages/REDCapPages/FetchSample";
import SampleRequestResponse from "./pages/SampleRequest/SampleRequestResponse";
import PageNotFound from "./pages/PageNotFound";
import StudyBlock from "@/pages/StudyBlock";


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
            path: '/confirm/*',
            name: 'user-confirm',
            component: ConfirmUser,
        },

        {
            path: '/requestConfirmation',
            name: 'email-request',
            component: ResendConfirmation,
        },

        {
            path: '/forgot',
            name: 'forgot-password',
            alias: ['/forgotPassword', '/forgot-password', '/forgot-pwd'],
            component: PasswordResetRequest,
        },

        {
            path: '/reset/*',
            name: 'pwd-reset',
            component: PasswordResetConfirmation,
        },

        {
            path: '/roles',
            name: 'role',
            alias: ['/role', '/user-roles'],
            component: UserRole,
        },

        {
            path: '/user',
            name: 'user',
            alias: ['/me'],
            component: UserCard,
        },

        {
            path: '/edit-user',
            name: 'update-user',
            alias: ['/update-user'],
            component: EditProfileForm,
        },

        {
            path: '/contact-us',
            name: 'contact',
            alias: ['/contact'],
            component: ContactUs,
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
            path: '/project',
            name: 'project',
            alias: ['/projects'],
            component: Project,
        },

        {
            path: '/bio-hazard-level',
            name: 'BioHazardLevel',
            alias: ['/biohazardlevel'],
            component: BioHazardLevel,
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

        {
            path: '/study-block',
            name: 'Study Block',
            alias: ['/study_block'],
            component: StudyBlock,
        },

        // redcap routes
        {
            path: '/redcap-samples',
            name: 'RedcapSamples',
            alias: ['/redcap-sample', '/redcapsample'],
            component: FetchSample,
        },

        {
            path: '/request-response/*',
            name: 'SampleRequestResponse',
            alias: ['/sample-request-response/*'],
            component: SampleRequestResponse,
        },

        {path: "*", component: PageNotFound}

    ],
});
