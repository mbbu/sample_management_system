<template>
  <div id="wrapper" :class="wrapperClass">

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

export default {

    components: {
    NavToggleBtn,
    ContentOverlay,
    Nav,
},
};
</script>

<style lang="scss" >
@import 'styles/layout.scss';
@import 'styles/nav.scss';
@import 'styles/media-queries.scss';
@import 'styles/nav-toggle-btn.scss';

</style>



