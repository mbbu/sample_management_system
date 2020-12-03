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
            <th class="table-header-style" scope="col"> Rack Number</th>
            <th v-if="isAuth" class="table-header-style" scope="col"> Actions</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(tray, index) in matchFiltersAndSearch.arr" :key="tray.id">
            <td> {{ index + 1 }}</td>
            <td> {{ tray.number }}</td>
            <td> {{ tray.code }}</td>
            <td> {{ tray['rack.number'] }}</td>

            <td v-if="isAuth">
              <b-icon
                  v-b-modal.modal-tray-edit
                  v-b-tooltip.hover
                  :font-scale="`${font_scale}`" :title="`Update tray ${ tray.code }`"
                  class="border border-info rounded" icon="pencil"
                  variant="info"
                  @mouseover="fillFormForUpdate(tray['rack.number'], tray.number, tray.code)"
              ></b-icon>
              &nbsp;
              <b-icon
                  v-b-tooltip.hover :font-scale="`${font_scale}`"
                  :title="`Delete tray ${tray.code}!`" class="border rounded bg-danger p-1"
                  icon="trash" variant="light"
                  @click="deleteTray(tray.code)"
              ></b-icon>
            </td>
          </tr>
          </tbody>
        </table>
        <!--TOP-PAGINATION-->
        <v-page v-model="current" :total-row="matchFiltersAndSearch.pg_len" align="center"
                @page-change="pageInfo"></v-page>
      </div>

      <div v-if="!isEditing">
        <b-modal
            id="modal-tray"
            :title="`Add ${page_title}`"
            cancel-variant="danger"
            ok-title="Save"
            @hidden="clearForm"
            @ok="onSubmit"
            @submit="showModal=false"
        >
          <form @submit.prevent="createTray">
            <!--RACK-->
            <b-form-group id="form-lab-group" label="Rack Number:" label-for="form-lab-input">
              <ejs-dropdownlist
                  id='dropdownlist'
                  v-model.trim="$v.tray.rack.$model"
                  :dataSource='rackDataList'
                  :fields="fields"
                  placeholder='Select a rack'
              ></ejs-dropdownlist>
              <div v-if="$v.tray.rack.$dirty">
                <div v-if="!$v.tray.rack.required" class="error">Field is required</div>
              </div>
            </b-form-group>

            <!-- NUMBER -->
            <b-form-group id="form-number-group"
                          :class="{ 'form-group--error': $v.tray.number.$error }" label="Number:" label-for="form-number-input">
              <b-form-input
                  id="form-number-input"
                  v-model.trim="$v.tray.number.$model"
                  placeholder="Enter Tray Number"
                  required
                  type="text"
              ></b-form-input>
              <div v-if="$v.tray.number.$dirty">
                <div v-if="!$v.tray.number.required" class="error">Field is required</div>
              </div>
            </b-form-group>

            <!--CODE-->
            <b-form-group id="form-code-group"
                          :class="{ 'form-group--error': $v.tray.code.$error }" label="Code:" label-for="form-code-input">
              <b-form-input
                  id="form-code-input"
                  v-model.trim="$v.tray.code.$model"
                  placeholder="Enter Code"
                  required
                  type="text">
              </b-form-input>
              <div v-if="$v.tray.code.$dirty">
                <div v-if="!$v.tray.code.required" class="error">Field is required</div>
              </div>
            </b-form-group>
          </form>
        </b-modal>
      </div>

      <div v-else-if="isEditing">
        <b-modal
            id="modal-tray-edit"
            :title="`Edit ${page_title}`"
            cancel-variant="danger"
            ok-title="Update"
            @hidden="clearForm"
            @ok="updateTray"
            @shown="selectItemForUpdate(tray.rack)"
            @submit="showModal = false"
        >
          <form>
            <!--RACK-->
            <b-form-group id="form-lab-group-edit" label="Rack Number:" label-for="form-lab-input">
              <ejs-dropdownlist
                  id='dropdownlist'
                  v-model.trim="$v.tray.rack.$model"
                  :dataSource='rackDataList'
                  :fields="fields"
                  placeholder='Select a rack'
              ></ejs-dropdownlist>
              <div v-if="$v.tray.rack.$dirty">
                <div v-if="!$v.tray.rack.required" class="error">Field is required</div>
              </div>
            </b-form-group>

            <!-- NUMBER -->
            <b-form-group id="form-number-group-edit"
                          :class="{ 'form-group--error': $v.tray.number.$error }" label="Number:" label-for="form-number-input">
              <b-form-input
                  id="form-number-input"
                  v-model.trim="$v.tray.number.$model"
                  placeholder="Enter Tray Number"
                  required
                  type="text"
              ></b-form-input>
              <div v-if="$v.tray.number.$dirty">
                <div v-if="!$v.tray.number.required" class="error">Field is required</div>
              </div>
            </b-form-group>

            <!--CODE-->
            <b-form-group id="form-code-group-edit"
                          :class="{ 'form-group--error': $v.tray.code.$error }" label="Code:" label-for="form-code-input">
              <b-form-input
                  id="form-code-input"
                  v-model.trim="$v.tray.code.$model"
                  placeholder="Enter Code"
                  required
                  type="text">
              </b-form-input>
              <div v-if="$v.tray.code.$dirty">
                <div v-if="!$v.tray.code.required" class="error">Field is required</div>
              </div>
            </b-form-group>
          </form>
        </b-modal>
      </div>
      <b-button v-if="isAuth" v-b-modal.modal-tray class="float_btn" style="border-radius: 50%" variant="primary">
        <span>Add Tray</span> <i class="fas fa-plus-circle menu_icon"></i>
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
import {rack_resource, tray_resource} from '@/utils/api_paths'
import TopNav from "@/components/TopNav";
import {
  extractRackData,
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
  name: 'Tray',
  components: {TopNav, FilterCard},

  data() {
    return {
      page_title: "Tray",
      filters: [],
      response: [],
      trayList: [],
      search: '',
      tray: {
        rack: '',
        code: '',
        number: '',
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

      rackDataList: [],
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
    tray: {
      rack: {required},
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
        this.trayList = this.response
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
          'By Rack': this.response
              .map(({['rack.number']: chamber}) => chamber)
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
      /* trayList,which is a copy of response, is passed as the data here instead of response to avoid
      mutating response data.*/
      let filteredData = this.filterData(this.trayList)

      let filterByNumber = filteredData.number
      let filterByRack = filteredData.rack


      if (searchList !== null) {
        return paginate(searchList)
      } else if (this.filters.length > 1) {
        // Possibly, multiple filters have been applied. Return the array with the least elements
        return filterByNumber.length < filterByRack.length ?
            paginate(filterByNumber) : paginate(filterByRack)
      } else if (filterByNumber !== null && filterByNumber.length > 0) {
        this.trayList = filterByNumber // eslint-disable-line
        this.filterData(filterByNumber)
        return paginate(filterByNumber)
      } else if (filterByRack !== null && filterByRack.length > 0) {
        this.trayList = filterByRack // eslint-disable-line
        this.filterData(filterByRack)
        return paginate(filterByRack)
      }
      return paginate(this.trayList)
    },
  },

  methods: {
    // Util Functions
    selectItemForUpdate,

    pageInfo(info) {
      EventBus.$emit('page-info', {'pgInfo': info, 'pgData': this.trayList})
    },

    onSubmit(evt) {
      this.$v.$touch();
      if (this.$v.$invalid) {
        // stop here if form is invalid
        evt.preventDefault()
        return;
      }
      this.createTray();
    },

    clearForm() {
      this.tray.rack = null;
      this.tray.code = null;
      this.tray.number = null;
      this.isEditing = false;
      this.$v.$reset();
    },

    fillFormForUpdate(rack, number, code) {
      this.tray.rack = rack;
      this.tray.code = code;
      this.tray.number = number;
      this.old_code = code;
      this.isEditing = true;
      this.showModal = true;
    },

    onLoadPage() {
      getItemDataList(rack_resource).then(data => {
        let rackList = extractRackData(data);

        // update local variables with data from API
        this.fields = rackList['fields'];
        for (let i = 0; i < rackList.items.length; i++) {
          this.rackDataList.push({
            'Code': rackList.items[i].Code,
            'Name': rackList.items[i].Name,
          });
        }
      })
      this.getTray()
    },
    // stop&hide progressPath
    haltProgressPath(cont = false, path = 0, size = 0) {
      this.indeterminate = cont
      this.progressPath = path
      this.size = size
    },
    // end of util functions

    // Functions to interact with api
    getTray() {
      this.isAuth = isThemeAdmin()

      this.clearForm();
      axios.get(tray_resource)
          .then((res) => {
            setTimeout(() => {
              this.haltProgressPath()
              this.trayList = this.response = res.data['message'];
            }, this.time)
          })
          .catch((error) => {
            // eslint-disable-next-line
            this.$log.error(error);
          });
    },

    createTray: function () {
      let loader = pageStartLoader(this)

      axios.post(tray_resource, {
        rack: this.tray.rack,
        number: this.tray.number,
        code: this.tray.code,
      }, {
        headers:
            {
              Authorization: secureStoreGetAuthString()
            }
      }).then((response) => {
        setTimeout(() => {
          loader.hide()
          this.getTray();
          showFlashMessage(this, 'success', response.data['message'], '');
        }, this.time)
      })
          .catch((error) => {
            handleError(this, error, loader)
          });
      this.clearForm();
    },

    updateTray: function (evt) {
      this.$v.$touch();
      if (this.$v.$invalid) {
        evt.preventDefault()
      } else {
        let loader = pageStartLoader(this)
        axios.put(tray_resource, {
          rack: this.tray.rack,
          number: this.tray.number,
          code: this.tray.code,
        }, {
          headers:
              {
                code: this.old_code,
                Authorization: secureStoreGetAuthString()
              }
        })
            .then((response) => {
              setTimeout(() => {
                loader.hide()
                this.getTray();
                showFlashMessage(this, 'success', response.data['message'], '');
              }, this.time)
            })
            .catch((error) => {
              handleError(this, error, loader)
            });
        this.clearForm();
      }
    },

    deleteTray: function (code) {
      let loader = pageStartLoader(this)

      axios.delete(tray_resource, {
        headers:
            {
              code: code,
              Authorization: secureStoreGetAuthString()
            }
      })
          .then((response) => {
            setTimeout(() => {
              loader.hide()
              this.getTray();
              showFlashMessage(this, 'success', response.data['message'], '');
            }, this.time)
          })
          .catch((error) => {
            handleError(this, error, loader)
          });
      this.clearForm();
    },
    //end of methods for api interaction

    /* Methods associated with searching and filtering of data in the page */
    filterData(data) {
      let filterByNumber = this.filters.length
          ? data.filter(tray => this.filters.some(filter => tray.number.toString().match(filter)))
          : null

      let filterByChamber = this.filters.length
          ? data.filter(tray => this.filters.some(filter => tray['rack.number'].toString().match(filter)))
          : null

      return {'number': filterByNumber, 'rack': filterByChamber}
    },

    searchData() {
      return this.response.filter(tray => {
        for (let count = 0; count <= this.response.length; count++) {
          let byCode = tray.code.toString().toLowerCase().includes(this.search.toLowerCase())
          let byNumber = tray.number.toString().toLowerCase().includes(this.search.toLowerCase())
          let byChamber = tray['rack.number'].toString().toLowerCase().includes(this.search.toLowerCase())

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
