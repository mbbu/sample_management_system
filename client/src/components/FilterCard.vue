<template>
  <mdb-card>
    <details>
      <summary class="pt-3 blue-gradient d-flex justify-content-center white-text"><h5>Filters</h5>
      </summary>
      <mdb-card-body>
        <mdb-row>
          <div :key="idx" v-for="(possibleFilter, idx) in allFilters">
            <mdb-col :md="` ${(12 / allFilters.length) }`" class="d-flex align-items-start">
              <ul :key="title" v-for="(values, title) in possibleFilter">
                <li><em>{{ title }}</em>
                  <hr>
                </li>
                <li :key="filter" v-for="filter in values">
                  <label>
                    <input :checked="filters.includes(filter)"
                           @change="toggleFilter(filter)"
                           type="checkbox">
                    <span> {{ filter }}</span>
                  </label>
                </li>
              </ul>
            </mdb-col>
          </div>
        </mdb-row>
        <div class="d-flex justify-content-end">
          <button @click="clearFilters" class="btn btn-outline-info btn-rounded">clear filters</button>
        </div>
      </mdb-card-body>
    </details>
  </mdb-card>
</template>

<script>
import {mdbCard, mdbCardBody, mdbCol, mdbRow} from "mdbvue";
import EventBus from "./EventBus";

export default {
  name: "FilterCard",
  components: {mdbCard, mdbCardBody, mdbRow, mdbCol},

  data() {
    return {
      filters: []
    }
  },

  props: {
    allFilters: {
      required: true,
    },
  },

  methods: {
    toggleFilter: function (newFilter) {
      this.filters = !this.filters.includes(newFilter)
          ? [...this.filters, newFilter]
          : this.filters.filter(filter => filter !== newFilter)

      EventBus.$emit('filters', this.filters);
    },

    clearFilters() {
      this.filters = []
      EventBus.$emit('filters', this.filters);
    }
  }
}
</script>
