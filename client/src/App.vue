<template>
  <div id="wrapper" :class="wrapperClass">
      <TopNav> </TopNav>
      <Nav></Nav>
      <NavToggleBtn></NavToggleBtn>
      <ContentOverlay></ContentOverlay>
      <router-view/>
  </div>
</template>

<script>

import NavToggleBtn from '@/components/NavToggleBtn.vue'
import Nav from '@/components/Nav.vue';
import ContentOverlay from '@/components/ContentOverlay.vue';
import TopNav from '@/components/TopNav.vue';

export default {

    components: {
    NavToggleBtn,
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



