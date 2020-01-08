import Vue from 'vue';
import Router from 'vue-router';
import Box from './components/Box.vue';
import Sample from './components/Sample.vue';

Vue.use(Router);

export default new Router({
     mode: 'history',
     base: process.env.BASE_URL,
     routes: [
     {
        path: '/box',
        name: 'Box',
        component: Box,
         },

     {
        path: '/sample',
        name: 'Sample',
        component: Sample,
     },
     ],
});
