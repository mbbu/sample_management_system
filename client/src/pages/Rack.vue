<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-sm-12">
        <top-nav :page_title="page_title" v-bind:search_query.sync="search"></top-nav>

        <!-- FLASH MESSAGES -->
        <FlashMessage :position="'right bottom'"></FlashMessage>
        <br>
        <!-- FILTER CARD SECTION -->
        <filter-card :all-filters="allFilters"></filter-card>
        <br>

        <!--TOP-PAGINATION-->
        <v-page v-model="current" :total-row="matchFiltersAndSearch.pg_len" align="center"
                @page-change="pageInfo"></v-page>
        <br>
        <table class=" table table-hover">
          <thead>
          <tr>
            <th class="table-header-style" scope="col"> Id</th>
            <th class="table-header-style" scope="col"> Number</th>
            <th class="table-header-style" scope="col"> Code</th>
            <th class="table-header-style" scope="col"> Chamber Type</th>
            <th v-if="isAuth" class="table-header-style" scope="col"> Actions</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(rack, index) in matchFiltersAndSearch.arr" :key="rack.id">
            <td> {{ index + 1 }}</td>
            <td> {{ rack.number }}</td>
            <td> {{ rack.code }}</td>
            <td> {{ rack['chamber.type'] }}</td>

            <td v-if="isAuth">
              <b-icon
                  v-b-modal.modal-rack-edit
                  v-b-tooltip.hover
                  :font-scale="`${font_scale}`" :title="`Update rack ${ rack.code }`"
                  class="border border-info rounded" icon="pencil"
                  variant="info"
                  @mouseover="fillFormForUpdate(rack['chamber.type'], rack.number, rack.code)"
              ></b-icon>
              &nbsp;
              <b-icon
                  v-b-tooltip.hover :font-scale="`${font_scale}`"
                  :title="`Delete rack ${rack.code}!`" class="border rounded bg-danger p-1"
                  icon="trash" variant="light"
                  @click="deleteRack(rack.code)"
              ></b-icon>
            </td>
          </tr>
          </tbody>
        </table>
        <!--TOP-PAGINATION-->
        <v-page v-model="current" :total-row="matchFiltersAndSearch.pg_len" align="center"
                @page-change="pageInfo"></v-page>
        <br>
      </div>

      <div v-if="!isEditing">
        <b-modal
            id="modal-rack"
            :title="`Add ${page_title}`"
            cancel-variant="danger"
            ok-title="Save"
            @hidden="clearForm"
            @ok="onSubmit"
            @submit="showModal=false"
        >
          <form @submit.prevent="createRack">
            <b-form-group id="form-chamber-group" label="Chamber Type:" label-for="form-chamber-input">
              <ejs-dropdownlist
                  id='dropdownlist'
                  v-model.trim="$v.rack.chamber.$model"
                  :dataSource='chamberDataList'
                  :fields="fields"
                  placeholder='Select a chamber'
              ></ejs-dropdownlist>
              <div v-if="$v.rack.chamber.$dirty">
                <div v-if="!$v.rack.chamber.required" class="error">Field is required</div>
              </div>
            </b-form-group>

            <!--NUMBER-->
            <b-form-group id="form-number-group"
                          :class="{ 'form-group--error': $v.rack.number.$error }" label="Number:" label-for="form-number-input">
              <b-form-input
                  id="form-number-input"
                  v-model.trim="$v.rack.number.$model"
                  placeholder="Enter Rack Number"
                  required
                  type="text"
              ></b-form-input>
              <div v-if="$v.rack.number.$dirty">
                <div v-if="!$v.rack.number.required" class="error">Field is required</div>
              </div>
            </b-form-group>

            <!--CODE-->
            <b-form-group id="form-code-group"
                          :class="{ 'form-group--error': $v.rack.code.$error }" label="Code:" label-for="form-code-input">
              <b-form-input
                  id="form-code-input"
                  v-model.trim="$v.rack.code.$model"
                  placeholder="Enter Code"
                  required
                  type="text">
              </b-form-input>
              <div v-if="$v.rack.code.$dirty">
                <div v-if="!$v.rack.code.required" class="error">Field is required</div>
              </div>
            </b-form-group>
          </form>
        </b-modal>
      </div>

      <div v-else-if="isEditing">
        <b-modal
            id="modal-rack-edit"
            :title="`Edit ${page_title}`"
            cancel-variant="danger"
            ok-title="Update"
            @hidden="clearForm"
            @ok="updateRack"
            @shown="selectItemForUpdate(rack.chamber)"
            @submit="showModal = false"
        >
          <form>
            <b-form-group id="form-chamber-group-edit" label="Chamber Type:" label-for="form-chamber-input">
              <ejs-dropdownlist
                  id='dropdownlist'
                  v-model.trim="$v.rack.chamber.$model"
                  :dataSource='chamberDataList'
                  :fields="fields"
                  placeholder='Select a chamber'
              ></ejs-dropdownlist>
              <div v-if="$v.rack.chamber.$dirty">
                <div v-if="!$v.rack.chamber.required" class="error">Field is required</div>
              </div>
            </b-form-group>

            <!--NUMBER-->
            <b-form-group id="form-number-group-edit"
                          :class="{ 'form-group--error': $v.rack.number.$error }" label="Number:" label-for="form-number-input">
              <b-form-input
                  id="form-number-input"
                  v-model.trim="$v.rack.number.$model"
                  placeholder="Enter Rack Number"
                  required
                  type="text"
              ></b-form-input>
              <div v-if="$v.rack.number.$dirty">
                <div v-if="!$v.rack.number.required" class="error">Field is required</div>
              </div>
            </b-form-group>

            <!--CODE-->
            <b-form-group id="form-code-group-edit"
                          :class="{ 'form-group--error': $v.rack.code.$error }" label="Code:" label-for="form-code-input">
              <b-form-input
                  id="form-code-input"
                  v-model.trim="$v.rack.code.$model"
                  placeholder="Enter Code"
                  required
                  type="text">
              </b-form-input>
              <div v-if="$v.rack.code.$dirty">
                <div v-if="!$v.rack.code.required" class="error">Field is required</div>
              </div>
            </b-form-group>
          </form>
        </b-modal>
      </div>
      <b-button v-if="isAuth" v-b-modal.modal-rack class="float_btn" style="border-radius: 50%" variant="primary">
        <span>Add Rack</span> <i class="fas fa-plus-circle menu_icon"></i>
      </b-button>
      <div style="margin: auto;">
        <loading-progress
            :hide-background="hideBackground"
            :indeterminate="indeterminate"
            :progress="progressPath"
            :size="size"
            fillDuration="2"
            rotate
            rotationDuration="1"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import {chamber_resource, rack_resource} from '@/utils/api_paths'
import TopNav from "@/components/TopNav";
import {
  extractChamberData,
  getItemDataList,
  handleError,
  isThemeAdmin,
  pageStartLoader,
  paginate,
  secureStoreGetAuthString,
  selectItemForUpdate,
  showFlashMessage
} from "@/utils/util_functions";
import {font_scale} from '@/utils/constants';
import EventBus from '@/components/EventBus';
import FilterCard from "@/components/FilterCard";
import {required} from "vuelidate/lib/validators";

export default {
  name: 'Rack',
  components: {TopNav, FilterCard},

  data() {
    return {
      page_title: "Rack",
      filters: [],
      response: [],
      rackList: [],
      search: '',
      rack: {
        code: '',
        number: '',
        chamber: '',
      },

      font_scale,

      // variable to check user status and role
      isAuth: null,

      // loader-time
      time: 2000,

      // progressPath
      indeterminate: true,
      hideBackground: true,
      progressPath: 5,
      size: 180,

      chamberDataList: [],
      fields: {text: '', value: ''},

      // values for data modification
      old_code: null,
      showModal: true,
      isEditing: false,

      // data for pagination
      current: 1,
    };
  },
  validations: {
    rack: {
      chamber: {required},
      code: {required},
      number: {required},
    }
  },

  created() {
    this.onLoadPage();
  },

  mounted() {
    EventBus.$on('searchQuery', (payload) => {
      this.search = payload
      this.searchData()
    })

    EventBus.$on('filters', (payload) => {
      this.filters = payload
      if (this.filters.length === 0) {
        this.rackList = this.response
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
          'By Chamber': this.response
              .map(({['chamber.type']: chamber}) => chamber)
              .filter((value, index, self) => self.indexOf(value) === index),
        },
        {
          'By Number': this.response
              .map(({number}) => number)
              .filter((value, index, self) => self.indexOf(value) === index)
        },
      ]
    },

    /**
     * function checks for any filters or searches applied to the data and returns filtered/searched list.
     * @returns {null|[]|*}
     */
    matchFiltersAndSearch: function () {
      let searchList = this.search ? this.searchData() : null
      /* rackList,which is a copy of response, is passed as the data here instead of response to avoid
      mutating response data.*/
      let filteredData = this.filterData(this.rackList)

      let filterByNumber = filteredData.number
      let filterByChamber = filteredData.chamber


      if (searchList !== null) {
        this.rackList = searchList // eslint-disable-line
        return paginate(searchList)
      } else if (this.filters.length > 1) {
        // Possibly, multiple filters have been applied. Return the array with the least elements
        return filterByNumber.length < filterByChamber.length ?
            paginate(filterByNumber) : paginate(filterByChamber)
      } else if (filterByNumber !== null && filterByNumber.length > 0) {
        this.rackList = filterByNumber // eslint-disable-line
        this.filterData(filterByNumber)
        return paginate(filterByNumber)
      } else if (filterByChamber !== null && filterByChamber.length > 0) {
        this.rackList = filterByChamber // eslint-disable-line
        this.filterData(filterByChamber)
        return paginate(filterByChamber)
      }
      return paginate(this.rackList)
    },
  },

  methods: {
    // Util Functions
    selectItemForUpdate,

    pageInfo(info) {
      EventBus.$emit('page-info', {'pgInfo': info, 'pgData': this.rackList})
    },

    onSubmit(evt) {
      this.$v.$touch();
      if (this.$v.$invalid) {
        // stop here if form is invalid
        evt.preventDefault()
        return;
      }
      this.createRack();
    },

    clearForm() {
      this.rack.chamber = null;
      this.rack.code = null;
      this.rack.number = null;
      this.isEditing = false;
      this.$v.$reset();
    },

    fillFormForUpdate(chamber, number, code) {
      this.rack.chamber = chamber;
      this.rack.code = code;
      this.rack.number = number;
      this.old_code = code;
      this.isEditing = true;
      this.showModal = true;
    },

    onLoadPage() {
      getItemDataList(chamber_resource).then(data => {
        let chamberList = extractChamberData(data);

        // update local variables with data from API
        this.fields = chamberList['fields'];
        for (let i = 0; i < chamberList.items.length; i++) {
          this.chamberDataList.push({
            'Code': chamberList.items[i].Code,
            'Name': chamberList.items[i].Name,
          });
        }
      })
      this.getRack()
    },
    // stop&hide progressPath
    haltProgressPath(cont = false, path = 0, size = 0) {
      this.indeterminate = cont
      this.progressPath = path
      this.size = size
    },
    // end of Util functions

    // Functions to interact with api
    getRack() {
      this.isAuth = isThemeAdmin()

      axios.get(rack_resource)
          .then((res) => {
            setTimeout(() => {
              this.haltProgressPath()
              this.rackList = this.response = res.data['message'];
            }, this.time)
          })
          .catch((error) => {
            // eslint-disable-next-line
            this.$log.error(error);
          });
    },

    createRack: function () {
      let loader = pageStartLoader(this)

      axios.post(rack_resource, {
        chamber: this.rack.chamber,
        number: this.rack.number,
        code: this.rack.code,
      }, {
        headers:
            {
              Authorization: secureStoreGetAuthString()
            }
      }).then((response) => {
        setTimeout(() => {
          this.getRack();
          loader.hide()
          showFlashMessage(this, 'success', response.data['message'], '');
        }, this.time)
      }).catch((error) => {
        handleError(this, error, loader)
      });
      this.clearForm();
    },

    updateRack: function (evt) {
      this.$v.$touch();
      if (this.$v.$invalid) {
        evt.preventDefault()
      } else {
        let loader = pageStartLoader(this)

        axios.put(rack_resource, {
          chamber: this.rack.chamber,
          number: this.rack.number,
          code: this.rack.code,
        }, {
          headers:
              {
                code: this.old_code,
                Authorization: secureStoreGetAuthString()
              }
        }).then((response) => {
          setTimeout(() => {
            this.getRack();
            loader.hide()
            showFlashMessage(this, 'success', response.data['message'], '');
          }, this.time)
        }).catch((error) => {
          handleError(this, error, loader)
        });
        this.clearForm();
      }
    },

    deleteRack: function (code) {
      let loader = pageStartLoader(this)

      axios.delete(rack_resource, {
        headers:
            {
              code: code,
              Authorization: secureStoreGetAuthString()
            }
      }).then((response) => {
        setTimeout(() => {
          this.getRack();
          loader.hide()
          showFlashMessage(this, 'success', response.data['message'], '');
        }, this.time)
      }).catch((error) => {
        handleError(this, error, loader)
      });
      this.clearForm();
    },
    //end of methods for api interaction

    /* Methods associated with searching and filtering of data in the page */
    filterData(data) {
      let filterByNumber = this.filters.length
          ? data.filter(rack => this.filters.some(filter => rack.number.toString().match(filter)))
          : null

      let filterByChamber = this.filters.length
          ? data.filter(rack => this.filters.some(filter => rack['chamber.type'].match(filter)))
          : null

      return {'number': filterByNumber, 'chamber': filterByChamber}
    },

    searchData() {
      return this.response.filter(rack => {
        for (let count = 0; count <= this.response.length; count++) {
          let byCode = rack.code.toString().toLowerCase().includes(this.search.toLowerCase())
          let byNumber = rack.number.toString().toLowerCase().includes(this.search.toLowerCase())
          let byChamber = rack['chamber.type'].toString().toLowerCase().includes(this.search.toLowerCase())

          if (byNumber) {
            return byNumber
          } else if (byCode) {
            return byCode
          } else if (byChamber) {
            return byChamber
          }
        }
      })
    },
    // end-of methods for search and filter

  },
};
</script>
