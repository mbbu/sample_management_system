<template>
  <div id="wrapper" :class="wrapperClass">
      <TopNav> </TopNav>
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

</style>



