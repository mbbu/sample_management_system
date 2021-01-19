<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <top-nav :page_title="page_title" v-bind:search_query="search"></top-nav>

                <!-- FLASH MESSAGES -->
                <FlashMessage :position="'right bottom'"></FlashMessage>
                <br>
                <!-- FILTER CARD SECTION -->
                <filter-card :all-filters="allFilters"></filter-card>
                <br>

                <!--TOP-PAGINATION-->
                <v-page :total-row="matchFiltersAndSearch.pg_len" @page-change="pageInfo" align="center"
                        v-model="current"></v-page>
                <br>
                <table class="table table-hover">
                    <thead>
                    <tr>
                      <th class="table-header-style" scope="col"> Id</th>
                      <th class="table-header-style" scope="col"> Theme</th>
                      <th class="table-header-style" scope="col"> Project</th>
                      <th class="table-header-style" scope="col"> (P.I)</th>
                      <th class="table-header-style" scope="col"> Location Collected</th>
                      <th class="table-header-style" scope="col"> Animal Species</th>
                      <th class="table-header-style" scope="col"> BarCode</th>
                      <th class="table-header-style" scope="col"> Actions</th>
                    </tr>
                    </thead>

                    <tbody>
                    <tr :key="sample.id" v-for="(sample, index) in matchFiltersAndSearch.arr">
                        <td> {{ index + 1 }}</td>
                        <td> {{ sample['theme.name'] }}</td>
                        <td> {{ sample['project.name'] }}</td>
                        <td> {{ sample['project.lead.first_name'] }} {{ sample['project.lead.last_name'] }}</td>
                        <td> {{ sample.location_collected }}</td>
                        <td> {{ sample.animal_species }}</td>
                        <td> {{ sample.barcode }}</td>


                        <td>
                            <b-icon
                                    @click="viewSample(sample.code)"
                                    class="border border-info rounded" font-scale="1.95"
                                    icon="eye-fill" title="View Sample"
                                    v-b-tooltip.hover variant="info"
                            ></b-icon>
                        </td>
                    </tr>
                    </tbody>
                </table>
              <!--BOTTOM-PAGINATION-->
              <v-page :total-row="matchFiltersAndSearch.pg_len" @page-change="pageInfo" align="center"
                      v-model="current"></v-page>
              <br>
            </div>

          <div v-if="isAuth">
            <a href="/addsample">
              <b-button class="float_btn" style="border-radius: 50%" variant="primary">
                <span>Add Sample</span> <i class="fas fa-plus-circle menu_icon"></i>
              </b-button>
            </a>
          </div>
        <div style="margin: auto;">
            <loading-progress
              :indeterminate="indeterminate"
              :hide-background="hideBackground"
              :progress="progressPath"
              :size="size"
              rotate
              fillDuration="2"
              rotationDuration="1"
            />
          </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import {sample_resource} from "@/utils/api_paths";
import TopNav from "@/components/TopNav";
import {getLoggedInUser, paginate, redirectAfterCountDown, setSampleCode} from "@/utils/util_functions";
import EventBus from "@/components/EventBus";
import FilterCard from "@/components/FilterCard";

export default {
  name: "Sample",
  components: {TopNav, FilterCard},

  data() {
    return {
      page_title: "Samples",

      filters: [],
      response: [],
      sampleList: [],
      search: '',

      // data for pagination
      current: 1,

      // progressPath
      indeterminate: true,
      hideBackground: true,
      progressPath: 5,
      size: 180,

      isAuth: null,
    };
  },

  created() {
    this.getSamples();
  },

  mounted() {
    EventBus.$on('searchQuery', (payload) => {
      this.search = payload
      this.searchData()
    })

    EventBus.$on('filters', (payload) => {
      this.filters = payload
      if (this.filters.length === 0) {
        this.sampleList = this.response
      }
    })
  },

  computed: {
    /**
     * return a list of dictionaries containing the filters required
     */
    allFilters: function () {
      return [
        {
          'By Theme': this.response
              .map(({theme}) => theme)
              .filter((value, index, self) => self.indexOf(value) === index)
        },
        {
          'By Project': this.response
              .map(({project}) => project)
              .filter((value, index, self) => self.indexOf(value) === index),
        },
        {
          'By PI': this.response
              .map(({project_owner}) => project_owner)
              .filter((value, index, self) => self.indexOf(value) === index),
        },
        {
          'By Location Collected': this.response
              .map(({location_collected}) => location_collected)
              .filter((value, index, self) => self.indexOf(value) === index),
        },
        {
          'By Location In Lab': this.response
              .map(({['box.tray.rack.chamber.freezer.lab.name']: lab}) => lab)
              .filter((value, index, self) => self.indexOf(value) === index),
        },
        {
          'By Species': this.response
              .map(({animal_species}) => animal_species)
              .filter((value, index, self) => self.indexOf(value) === index),
        },
        {
          'By Retention': this.response
              .map(({retention_date}) => retention_date)
              .filter((value, index, self) => self.indexOf(value) === index),
        },
      ]
    },

    /**
     * function checks for any filters or searches applied to the data and returns filtered/searched list.
     * @returns {null|[]|*}
     */
    matchFiltersAndSearch: function () {
      let searchList = this.search ? this.searchData() : null
      /* sampleList,which is a copy of response, is passed as the data here instead of response to avoid
      mutating response data.*/
      let filteredData = this.filterData(this.sampleList)

      let filterByPI = filteredData.pi
      let filterByTheme = filteredData.theme
      let filterByProject = filteredData.project
      let filterBySpecies = filteredData.species
      let filterByRetention = filteredData.retention
      let filterByLocInLab = filteredData.loc_in_lab
      let filterByLocCollected = filteredData.loc_collected

      if (searchList !== null) {
        return paginate(searchList)
      } else if (this.filters.length > 1) {

        let lowest = 0;
        for (let i = 1; i < filteredData.length; i++) {
          if ((filteredData[i] < filteredData[lowest]) && filteredData[i].length > 0) lowest = i;
        }
        return paginate(filteredData[lowest]);

      } else if (filterByPI !== null && filterByPI.length > 0) {
        this.sampleList = filterByPI // eslint-disable-line
        this.filterData(filterByPI)
        return paginate(filterByPI)
      } else if (filterByTheme !== null && filterByTheme.length > 0) {
        this.sampleList = filterByTheme // eslint-disable-line
        this.filterData(filterByTheme)
        return paginate(filterByTheme)
      } else if (filterByProject !== null && filterByProject.length > 0) {
        this.sampleList = filterByProject // eslint-disable-line
        this.filterData(filterByProject)
        return paginate(filterByProject)
      } else if (filterBySpecies !== null && filterBySpecies.length > 0) {
        this.sampleList = filterBySpecies // eslint-disable-line
        this.filterData(filterBySpecies)
        return paginate(filterBySpecies)
      } else if (filterByRetention !== null && filterByRetention.length > 0) {
        this.sampleList = filterByRetention // eslint-disable-line
        this.filterData(filterByRetention)
        return paginate(filterByRetention)
      } else if (filterByLocInLab !== null && filterByLocInLab.length > 0) {
        this.sampleList = filterByLocInLab // eslint-disable-line
        this.filterData(filterByLocInLab)
        return paginate(filterByLocInLab)
      } else if (filterByLocCollected !== null && filterByLocCollected.length > 0) {
        this.sampleList = filterByLocCollected // eslint-disable-line
        this.filterData(filterByLocCollected)
        return paginate(filterByLocCollected)
      }
      return paginate(this.sampleList)
    },
  },

  methods: {
    pageInfo(info) {
      EventBus.$emit('page-info', {'pgInfo': info, 'pgData': this.sampleList})
    },

    // stop&hide progressPath
    haltProgressPath(cont=false, path=0, size=0){
      this.indeterminate = cont
      this.progressPath = path
      this.size = size
    },

    // methods to interact with api
    getSamples() {
      this.isAuth = getLoggedInUser()

      axios.get(sample_resource)
          .then((res) => {
            setTimeout(() => {
              this.haltProgressPath()
              this.sampleList = this.response = res.data.message;
              // eslint-disable-next-line no-unused-vars
              for (const [key, value] of this.response.entries()) {
                // eslint-disable-next-line no-unused-vars,no-empty
                for (let item in key) {}
            }
            }, 2000)
          })
          .catch((error) => {
            // eslint-disable-next-line
            this.$log.error(error);
          });
    },

    viewSample(code) {
      // 1st call the setter function to set the code
      setSampleCode(code)
      // redirect to sample view page
      redirectAfterCountDown(this, '/view-sample', 1)
    },
    //end of methods for api interaction

    /* Methods associated with searching and filtering of data in the page */
    filterData(data) {
      let filterByTheme = this.filters.length
          ? data.filter(sample =>
              this.filters.some(filter => sample['theme.name'] ? sample['theme.name'].toString().match(filter) : null))
          : null

      let filterByProject = this.filters.length
          ? data.filter(sample =>
              this.filters.some(filter => sample.project ? sample.project.toString().match(filter) : null))
          : null

      let filterByPI = this.filters.length
          ? data.filter(sample =>
              this.filters.some(filter => sample.project_owner ? sample.project_owner.toString().match(filter) : null))
          : null

      let filterByLocCollected = this.filters.length
          ? data.filter(sample =>
              this.filters.some(filter => sample.location_collected ? sample.location_collected.toString().match(filter) : null))
          : null

      let filterByLocInLab = this.filters.length
          ? data.filter(sample =>
              this.filters.some(filter => sample['box.tray.rack.chamber.freezer.lab.name'] ?
                  sample['box.tray.rack.chamber.freezer.lab.name'].toString().match(filter) : null))
          : null

      let filterBySpecies = this.filters.length
          ? data.filter(sample =>
              this.filters.some(filter => sample.animal_species ? sample.animal_species.toString().match(filter) : null))
          : null

      let filterByRetention = this.filters.length
          ? data.filter(sample =>
              this.filters.some(filter => sample.retention ? sample.retention.toString().match(filter) : null))
          : null


      return {
        'pi': filterByPI,
        'theme': filterByTheme,
        'project': filterByProject,
        'species': filterBySpecies,
        'retention': filterByRetention,
        'loc_in_lab': filterByLocInLab,
        'loc_collected': filterByLocCollected,
      }
    },

    searchData() {
      return this.sampleList.filter(sample => {
        for (let count = 0; count <= this.sampleList.length; count++) {
          let byTheme = sample['theme.name'] != null
              ? sample['theme.name'].includes(this.search.toLowerCase())
              : null

          let byProject = sample.project != null
              ? sample.project.includes(this.search.toLowerCase())
              : null

          let byPI = sample.project_owner != null
              ? sample.project_owner.includes(this.search.toLowerCase())
              : null

          let byLocCollected = sample.location_collected != null
              ? sample.location_collected.includes(this.search.toLowerCase())
              : null

          let byLocInLab = sample['box.tray.rack.chamber.freezer.lab.name'] != null
              ? sample['box.tray.rack.chamber.freezer.lab.name'].includes(this.search.toLowerCase())
              : null

          let bySpecies = sample.animal_species != null
              ? sample.animal_species.includes(this.search.toLowerCase())
              : null

          let byType = sample.sample_type != null
              ? sample.sample_type.includes(this.search.toLowerCase())
              : null

          let byStatus = sample.status != null
              ? sample.status.includes(this.search.toLowerCase())
              : null

          let byRetention = sample.retention != null
              ? sample.retention.includes(this.search.toLowerCase())
              : null

          if (byTheme) {
            return byTheme
          } else if (byProject) {
            return byProject
          } else if (byPI) {
            return byPI
          } else if (byLocCollected) {
            return byLocCollected
          } else if (byLocInLab) {
            return byLocInLab
          } else if (bySpecies) {
            return bySpecies
          } else if (byType) {
            return byType
          } else if (byStatus) {
            return byStatus
          } else if (byRetention) {
            return byRetention
          }
        }
      })
    },
    // end-of methods for search and filter
  },
};
</script>
