<template>
  <div id="wrapper" :class="wrapperClass">
      <side-menu></side-menu>
<!--      <ContentOverlay></ContentOverlay>-->
      <router-view/>
  </div>
</template>

<script>

    // import ContentOverlay from '@/components/ContentOverlay.vue';
    import SideMenu from "./components/Nav";

    export default {
        components: {
            SideMenu,
            // ContentOverlay,
        },
    };
</script>

<style lang="scss" >
    @import 'styles/layout.scss';
    @import 'styles/nav.scss';
    @import 'styles/media-queries.scss';
    @import 'styles/nav-toggle-btn.scss';
    @import 'node_modules/bootstrap/scss/bootstrap';
    @import 'node_modules/bootstrap-vue/src/index.scss';
</style>

