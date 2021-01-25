<template>
	<checkbox-svg-map v-model="selectedLocations" :map="World" />
</template>

<script>
import { CheckboxSvgMap } from "vue-svg-map";
import World from "@svg-maps/world";

export default {
	name: "MyCheckboxMap",
	components: {
		CheckboxSvgMap
	},
	data() {
		return {
			World,
			selectedLocations: []
		};
	}
};
</script>

<style src="vue-svg-map/dist/index.css"></style>