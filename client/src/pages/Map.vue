<template>
<div class="vue-world-map">
  <Map />
</div>
</template>

<script>
import chroma from 'chroma-js';
import Map from '../components/MapView';
import {
  getDynamicMapCss,
  getBaseCss,
  getCombinedCssString,
} from '../styles/dynamic-map-css.js';
export default {
  components: { Map },
  watch: {
    countryData() {
      this.renderMapCSS();
    },
  },
  props: {
    lowColor: {
      type: String,
      default: 'red',
    },
    highColor: {
      type: String,
      default: '#d83737',
    },
    countryData: {
      type: Object,
      required: true,
    },
    defaultCountryFillColor: {
      type: String,
      default: '#dadada',
    },
    countryStrokeColor: {
      type: String,
      default: '#ffffff',
    },
  },
  data() {
    return {
      node: document.createElement('style'),
      chromaScale: chroma.scale([this.$props.lowColor, this.$props.highColor]),
    };
  },
  methods: {
    renderMapCSS() {
      const baseCss = getBaseCss(this.$props);
      const dynamicMapCss = getDynamicMapCss(this.$props.countryData, this.chromaScale);
      this.$data.node.innerHTML = getCombinedCssString(baseCss, dynamicMapCss);
    },
  },
  mounted() {
    document.body.appendChild(this.$data.node);
    this.renderMapCSS();
  },
};
</script>

<style>
.vue-world-map {
  height: 100%;
}
#map-svg {
  height: 100%;
}
</style>