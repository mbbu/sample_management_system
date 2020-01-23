import Vue from 'vue';
import Router from 'vue-router';
import Box from './components/Box.vue';
import Sample from './components/Sample.vue';
import Index from './components/Index.vue';
import Chamber from './components/Chamber.vue'
import Theme from './components/Theme.vue'

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
