import Vue from 'vue';
import Router from 'vue-router';
import Box from './pages/Box.vue';
import Sample from './pages/Sample.vue';
import Index from './pages/Index.vue';
import Chamber from './pages/Chamber.vue'
import Theme from './pages/Theme.vue'

Vue.use(Router);

export default new Router({
     mode: 'history',
     base: process.env.BASE_URL,
     routes: [
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
             path: '/',
             name: 'home',
             alias: ['/index', '/welcome'],
             component: Index,
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

     ],
});
