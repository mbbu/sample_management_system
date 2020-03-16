<template>
  <div id="wrapper" :class="wrapperClass">
      <TopNav :page_title="page_title"></TopNav>
      <Nav></Nav>
      <ContentOverlay></ContentOverlay>
      <router-view/>
  </div>
</template>

<script>

    import Nav from '@/components/Nav.vue';
    import ContentOverlay from '@/components/ContentOverlay.vue';
    import TopNav from '@/components/TopNav.vue';

    export default {

        components: {
            ContentOverlay,
            Nav,
            TopNav,
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

