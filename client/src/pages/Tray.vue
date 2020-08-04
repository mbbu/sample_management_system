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
                <v-page :total-row="matchFiltersAndSearch.pg_len" @page-change="pageInfo" align="center"
                        v-model="current"></v-page>
                <br>
                <table class=" table table-hover">
                    <thead>
                    <tr>
                        <th scope="col"> Id</th>
                        <th scope="col"> Number</th>
                        <th scope="col"> Code</th>
                        <th scope="col"> Rack Number</th>
                        <th scope="col" v-if="isAuth"> Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr :key="tray.id" v-for="(tray, index) in matchFiltersAndSearch.arr">
                        <td> {{ index + 1 }}</td>
                        <td> {{tray.number}}</td>
                        <td> {{tray.code}}</td>
                        <td> {{tray['rack.number']}}</td>

                      <td v-if="isAuth">
                        <b-icon
                            :title="`Update tray ${ tray.code }`"
                            @mouseover="fillFormForUpdate(tray['rack.number'], tray.number, tray.code)"
                            class="border border-info rounded" font-scale="2.0"
                            icon="pencil" v-b-modal.modal-tray-edit
                            v-b-tooltip.hover
                            variant="info"
                        ></b-icon>
                        &nbsp;
                        <b-icon
                                    :title="`Delete tray ${tray.code}!`" @click="deleteTray(tray.code)"
                                    class="border rounded bg-danger p-1" font-scale="1.85"
                                    icon="trash" v-b-tooltip.hover
                                    variant="light"
                            ></b-icon>
                        </td>
                    </tr>
                    </tbody>
                </table>
                <!--TOP-PAGINATION-->
                <v-page :total-row="matchFiltersAndSearch.pg_len" @page-change="pageInfo" align="center"
                        v-model="current"></v-page>
            </div>

            <div v-if="!isEditing">
                <b-modal
                        :title="`Add ${page_title}`"
                        @hidden="clearForm"
                        @ok="onSubmit"
                        @submit="showModal=false"
                        cancel-variant="danger"
                        id="modal-tray"
                        ok-title="Save"
                >
                    <form @submit.prevent="createTray">
                        <!--RACK-->
                        <b-form-group id="form-lab-group" label="Rack Number:" label-for="form-lab-input">
                            <ejs-dropdownlist
                                    :dataSource='rackDataList'
                                    :fields="fields"
                                    id='dropdownlist'
                                    placeholder='Select a rack'
                                    v-model.trim="$v.tray.rack.$model"
                            ></ejs-dropdownlist>
                            <div v-if="$v.tray.rack.$dirty">
                                <div class="error" v-if="!$v.tray.rack.required">Field is required</div>
                            </div>
                        </b-form-group>

                        <!-- NUMBER -->
                        <b-form-group :class="{ 'form-group--error': $v.tray.number.$error }"
                                      id="form-number-group" label="Number:" label-for="form-number-input">
                            <b-form-input
                                    id="form-number-input"
                                    placeholder="Enter Tray Number"
                                    required
                                    type="text"
                                    v-model.trim="$v.tray.number.$model"
                            ></b-form-input>
                            <div v-if="$v.tray.number.$dirty">
                                <div class="error" v-if="!$v.tray.number.required">Field is required</div>
                            </div>
                        </b-form-group>

                        <!--CODE-->
                        <b-form-group :class="{ 'form-group--error': $v.tray.code.$error }"
                                      id="form-code-group" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required
                                    type="text"
                                    v-model.trim="$v.tray.code.$model">
                            </b-form-input>
                            <div v-if="$v.tray.code.$dirty">
                                <div class="error" v-if="!$v.tray.code.required">Field is required</div>
                            </div>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>

            <div v-else-if="isEditing">
                <b-modal
                        :title="`Edit ${page_title}`"
                        @hidden="clearForm"
                        @ok="updateTray"
                        @shown="selectItemForUpdate(tray.rack)"
                        @submit="showModal = false"
                        cancel-variant="danger"
                        id="modal-tray-edit"
                        ok-title="Update"
                >
                    <form>
                        <!--RACK-->
                        <b-form-group id="form-lab-group-edit" label="Rack Number:" label-for="form-lab-input">
                            <ejs-dropdownlist
                                    :dataSource='rackDataList'
                                    :fields="fields"
                                    id='dropdownlist'
                                    placeholder='Select a rack'
                                    v-model.trim="$v.tray.rack.$model"
                            ></ejs-dropdownlist>
                            <div v-if="$v.tray.rack.$dirty">
                                <div class="error" v-if="!$v.tray.rack.required">Field is required</div>
                            </div>
                        </b-form-group>

                        <!-- NUMBER -->
                        <b-form-group :class="{ 'form-group--error': $v.tray.number.$error }"
                                      id="form-number-group-edit" label="Number:" label-for="form-number-input">
                            <b-form-input
                                    id="form-number-input"
                                    placeholder="Enter Tray Number"
                                    required
                                    type="text"
                                    v-model.trim="$v.tray.number.$model"
                            ></b-form-input>
                            <div v-if="$v.tray.number.$dirty">
                                <div class="error" v-if="!$v.tray.number.required">Field is required</div>
                            </div>
                        </b-form-group>

                        <!--CODE-->
                        <b-form-group :class="{ 'form-group--error': $v.tray.code.$error }"
                                      id="form-code-group-edit" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required
                                    type="text"
                                    v-model.trim="$v.tray.code.$model">
                            </b-form-input>
                            <div v-if="$v.tray.code.$dirty">
                                <div class="error" v-if="!$v.tray.code.required">Field is required</div>
                            </div>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>
          <b-button class="float_btn" style="border-radius: 50%" v-b-modal.modal-tray v-if="isAuth" variant="primary">
            <span>Add Tray</span> <i class="fas fa-plus-circle menu_icon"></i>
          </b-button>
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
  isThemeAdmin,
  paginate,
  respondTo401,
  secureStoreGetString,
  selectItemForUpdate,
  showFlashMessage
} from "@/utils/util_functions";
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

      // variable to check user status and role
      isAuth: null,

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
            // end of util functions

            // Functions to interact with api
            getTray() {
              this.isAuth = isThemeAdmin()

              this.clearForm();
              axios.get(tray_resource)
                  .then((res) => {
                    this.$log.info("Response: " + res.status + " ", res.data['message']);
                    this.trayList = this.response = res.data['message'];
                  })
                  .catch((error) => {
                    // eslint-disable-next-line
                    this.$log.error(error);
                    });
            },

            createTray: function () {
                let self = this;

                axios.post(tray_resource, {
                    rack: this.tray.rack,
                    number: this.tray.number,
                    code: this.tray.code,
                }, {
                    headers:
                        {
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getTray();
                        showFlashMessage(self, 'success', response.data['message'], '');
                        this.clearForm();
                    })
                    .catch((error) => {
                        this.clearForm();
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 409) {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            } else if (error.response.status === 400) {
                                showFlashMessage(self, 'error', error.response.data['message'], 'Kindly refill the form');
                            } else if (error.response.status === 401) {
                                respondTo401(self)
                            } else if (error.response.status === 403) {
                                showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
                            } else {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            }
                        }
                    });
                this.clearForm();
            },

            updateTray: function (evt) {
                this.$v.$touch();
                if (this.$v.$invalid) {
                    evt.preventDefault()
                } else {
                    let self = this;

                    axios.put(tray_resource, {
                        rack: this.tray.rack,
                        number: this.tray.number,
                        code: this.tray.code,
                    }, {
                        headers:
                            {
                                code: this.old_code,
                                Authorization: secureStoreGetString()
                            }
                    })
                        .then((response) => {
                            this.getTray();
                            showFlashMessage(self, 'success', response.data['message'], '');
                            this.clearForm();
                        })
                        .catch((error) => {
                            this.clearForm();
                            this.$log.error(error);
                            if (error.response) {
                                if (error.response.status === 304) {
                                    showFlashMessage(self, 'info', 'Record not modified!', '');
                                } else if (error.response.status === 401) {
                                    respondTo401(self)
                                } else if (error.response.status === 403) {
                                    showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
                                } else {
                                    showFlashMessage(self, 'error', error.response.data['message'], '');
                                }
                            }
                        });
                    this.clearForm();
                }
            },

            deleteTray: function (code) {
                let self = this;
                axios.delete(tray_resource, {
                    headers:
                        {
                            code: code,
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getTray();
                        showFlashMessage(self, 'success', response.data['message'], '');
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 401) {
                                respondTo401(self);
                            } else if (error.response.status === 403) {
                                showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
                            } else {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            }
                        }
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
