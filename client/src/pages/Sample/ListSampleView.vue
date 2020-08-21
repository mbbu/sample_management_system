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
                      <th class="table-header-style" scope="col"> Owner (P.I)</th>
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
                        <td> {{ sample.project }}</td>
                        <td> {{ sample.project_owner }}</td>
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
          'By Type': this.response
              .map(({sample_type}) => sample_type)
              .filter((value, index, self) => self.indexOf(value) === index),
        },
        {
          'By Status': this.response
              .map(({status}) => status)
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
      let filterByType = filteredData.type
      let filterByTheme = filteredData.theme
      let filterByStatus = filteredData.status
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
          console.log("Item  " + i + " ", filteredData[i])
          if ((filteredData[i] < filteredData[lowest]) && filteredData[i].length > 0) lowest = i;
        }
        return paginate(filteredData[lowest]);

      } else if (filterByPI !== null && filterByPI.length > 0) {
        this.sampleList = filterByPI // eslint-disable-line
        this.filterData(filterByPI)
        return paginate(filterByPI)
      } else if (filterByType !== null && filterByType.length > 0) {
        this.sampleList = filterByType // eslint-disable-line
        this.filterData(filterByType)
        return paginate(filterByType)
      } else if (filterByTheme !== null && filterByTheme.length > 0) {
        this.sampleList = filterByTheme // eslint-disable-line
        this.filterData(filterByTheme)
        return paginate(filterByTheme)
      } else if (filterByStatus !== null && filterByStatus.length > 0) {
        this.sampleList = filterByStatus // eslint-disable-line
        this.filterData(filterByStatus)
        return paginate(filterByStatus)
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

    // methods to interact with api
    getSamples() {
      this.isAuth = getLoggedInUser()
      axios.get(sample_resource)
          .then((res) => {
            this.$log.info("Response: " + res.status + " ", res.data.message);
            this.sampleList = this.response = res.data.message;
            for (const [key, value] of this.response.entries()) {
              console.log(key, value);
              for (let item in key) {
                console.log(item + typeof item)
              }
            }

            // this.sampleList = this.response.message
            // this.$log.info(this.sampleList)
          })
          .catch((error) => {
            // eslint-disable-next-line
            this.$log.error(error);
          });
    },

    viewSample(code) {
      let self = this;
      // 1st call the setter function to set the code
      setSampleCode(code)
      // redirect to sample view page
      redirectAfterCountDown(self, '/view-sample', 1)
    },
    //end of methods for api interaction

    /* Methods associated with searching and filtering of data in the page */
    filterData(data) {
      // box.label: (...)
      // retention_date: (...)
      console.log("FilterData called")
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

      let filterByType = this.filters.length
          ? data.filter(sample =>
              this.filters.some(filter => sample.sample_type ? sample.sample_type.toString().match(filter) : null))
          : null

      let filterByStatus = this.filters.length
          ? data.filter(sample =>
              this.filters.some(filter => sample.status ? sample.status.toString().match(filter) : null))
          : null

      let filterByRetention = this.filters.length
          ? data.filter(sample =>
              this.filters.some(filter => sample.retention ? sample.retention.toString().match(filter) : null))
          : null


      return {
        'pi': filterByPI,
        'type': filterByType,
        'theme': filterByTheme,
        'status': filterByStatus,
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
            console.log("byTheme", byTheme)
            return byTheme
          } else if (byProject) {
            console.log("byProject", byProject)
            return byProject
          } else if (byPI) {
            console.log("byPI", byPI)
            return byPI
          } else if (byLocCollected) {
            console.log("byLocCollected", byLocCollected)
            return byLocCollected
          } else if (byLocInLab) {
            console.log("byLocInLab", byLocInLab)
            return byLocInLab
          } else if (bySpecies) {
            console.log("bySpecies", bySpecies)
            return bySpecies
          } else if (byType) {
            console.log("byType", byType)
            return byType
          } else if (byStatus) {
            console.log("byStatus", byStatus)
            return byStatus
          } else if (byRetention) {
            console.log("byRetention", byRetention)
            return byRetention
          }
        }
      })
    },
    // end-of methods for search and filter
  },
};
</script>
