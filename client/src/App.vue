<template>
  <div id="wrapper">
      <side-menu></side-menu>
      <router-view/>
  </div>
</template>

<script>
    import SideMenu from "./components/SideNav";

    export default {
        components: {
            SideMenu,
        },
    };
</script>

<style lang="scss" >
    @import 'styles/layout.scss';
    @import 'styles/nav.scss';
    @import 'styles/media-queries.scss';
    @import 'styles/nav-toggle-btn.scss';
    @import "../node_modules/@syncfusion/ej2-base/styles/material.css";
    @import "../node_modules/@syncfusion/ej2-inputs/styles/material.css";
    @import "../node_modules/@syncfusion/ej2-vue-dropdowns/styles/material.css";
    @import "../node_modules/@fortawesome/fontawesome-free/css/all.min.css";
    @import "../node_modules/mdbootstrap/css/bootstrap.min.css";
    @import "../node_modules/mdbvue/lib/css/mdb.min.css";
    @import '../node_modules/vue-loading-overlay/dist/vue-loading.css';
    @import '../node_modules/vue-progress-path/dist/vue-progress-path.css';
</style>

