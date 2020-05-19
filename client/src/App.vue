<template>
  <div id="wrapper" :class="wrapperClass">
      <side-menu></side-menu>
<!--      <ContentOverlay></ContentOverlay>-->
      <router-view/>
  </div>
</template>

<script>

    // import ContentOverlay from '@/components/ContentOverlay.vue';
    import SideMenu from "./components/SideNav";
    // import FooterScript from "./components/Footer";

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
    @import "../node_modules/@syncfusion/ej2-base/styles/material.css";
    @import "../node_modules/@syncfusion/ej2-inputs/styles/material.css";
    @import "../node_modules/@syncfusion/ej2-vue-dropdowns/styles/material.css";
    @import "../node_modules/@fortawesome/fontawesome-free/css/all.min.css";
    @import "../node_modules/mdbootstrap/css/bootstrap.min.css";
    @import "../node_modules/mdbvue/lib/css/mdb.min.css";
    @import '../node_modules/vue-loading-overlay/dist/vue-loading.css';
</style>

