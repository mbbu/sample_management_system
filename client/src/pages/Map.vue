<template>
<div class="container-fluid">
  <div class="row">
    <div class="col-sm-12">
      <top-nav :page_title="page_title"></top-nav>

      <!-- FLASH MESSAGES -->
      <FlashMessage :position="'right bottom'"></FlashMessage>

      <!-- MAP COMPONENT -->
      <Map/>
    </div>
  </div>
</div>
</template>

<script>
  import Map from '@/components/MapView';
  import TopNav from "@/components/TopNav";

  export default {
    components: {Map, TopNav},
    data() {
      return {
        page_title: "Home",
      };
    },
};
</script>
