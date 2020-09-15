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
                      <th class="table-header-style" scope="col"> Id</th>
                      <th class="table-header-style" scope="col"> Type</th>
                      <th class="table-header-style" scope="col"> Code</th>
                      <th class="table-header-style" scope="col"> Freezer Room</th>
                      <th class="table-header-style" scope="col"> Freezer Number</th>
                      <th class="table-header-style" scope="col" v-if="isAuth"> Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr :key="chamber.id" v-for="(chamber, index) in matchFiltersAndSearch.arr">
                        <td> {{ index + 1 }}</td>
                        <td> {{chamber.type}}</td>
                        <td> {{chamber.code}}</td>
                        <td> {{chamber['freezer.room']}}</td>
                        <td> {{chamber['freezer.number']}}</td>

                      <td v-if="isAuth">
                        <b-icon
                            :title="`Update chamber ${ chamber.code }`"
                            @mouseover="fillFormForUpdate(chamber['freezer.number'], chamber.type, chamber.code)"
                            class="border border-info rounded" font-scale="2.0"
                            icon="pencil" v-b-modal.modal-chamber-edit
                            v-b-tooltip.hover
                            variant="info"
                        ></b-icon>
                        &nbsp;
                        <b-icon
                                    :title="`Delete chamber ${chamber.code}!`" @click="deleteChamber(chamber.code)"
                                    class="border rounded bg-danger p-1" font-scale="1.85"
                                    icon="trash" v-b-tooltip.hover
                                    variant="light"
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

            <div v-if="!isEditing">
                <b-modal
                        :title="`Add ${page_title}`"
                        @hidden="clearForm"
                        @ok="onSubmit"
                        @submit="showModal=false"
                        cancel-variant="danger"
                        id="modal-chamber"
                        ok-title="Save"
                >
                    <form @submit.prevent="createChamber">
                        <!--FREEZER-->
                        <b-form-group id="form-freezer-group" label="Freezer Number:" label-for="form-freezer-input">
                            <ejs-dropdownlist
                                    :dataSource='freezerDataList'
                                    :fields="fields"
                                    id='dropdownlist'
                                    placeholder='Select a freezer'
                                    v-model.trim="$v.chamber.freezer.$model"
                            ></ejs-dropdownlist>
                            <div v-if="$v.chamber.freezer.$dirty">
                                <div class="error" v-if="!$v.chamber.freezer.required">Field is required</div>
                            </div>
                        </b-form-group>

                        <!-- TYPE -->
                        <b-form-group :class="{ 'form-group--error': $v.chamber.type.$error }"
                                      id="form-type-group" label="Type:" label-for="form-type-input">
                            <b-form-input
                                    id="form-type-input"
                                    placeholder="Enter Freezer Type"
                                    required
                                    type="text"
                                    v-model.trim="$v.chamber.type.$model"
                            ></b-form-input>
                            <div v-if="$v.chamber.type.$dirty">
                                <div class="error" v-if="!$v.chamber.type.required">Field is required</div>
                            </div>
                        </b-form-group>

                        <!--CODE-->
                        <b-form-group :class="{ 'form-group--error': $v.chamber.code.$error }"
                                      id="form-code-group" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required
                                    type="text"
                                    v-model.trim="$v.chamber.code.$model">
                            </b-form-input>
                            <div v-if="$v.chamber.code.$dirty">
                                <div class="error" v-if="!$v.chamber.code.required">Field is required</div>
                            </div>
                        </b-form-group>

                    </form>
                </b-modal>
            </div>

            <div v-else-if="isEditing">
                <b-modal
                        :title="`Edit ${page_title}`"
                        @hidden="clearForm"
                        @ok="updateChamber"
                        @shown="selectItemForUpdate(chamber.freezer)"
                        @submit="showModal = false"
                        cancel-variant="danger"
                        id="modal-chamber-edit"
                        ok-title="Update"
                >
                    <form>
                        <!--FREEZER-->
                        <b-form-group id="form-freezer-group-edit" label="Freezer Number:"
                                      label-for="form-freezer-input">
                            <ejs-dropdownlist
                                    :dataSource='freezerDataList'
                                    :fields="fields"
                                    id='dropdownlist'
                                    placeholder='Select a freezer'
                                    v-model.trim="$v.chamber.freezer.$model"
                            ></ejs-dropdownlist>
                            <div v-if="$v.chamber.freezer.$dirty">
                                <div class="error" v-if="!$v.chamber.freezer.required">Field is required</div>
                            </div>
                        </b-form-group>

                        <!-- TYPE -->
                        <b-form-group :class="{ 'form-group--error': $v.chamber.type.$error }"
                                      id="form-type-group-edit" label="Type:" label-for="form-type-input">
                            <b-form-input
                                    id="form-type-input"
                                    placeholder="Enter Freezer Type"
                                    required
                                    type="text"
                                    v-model.trim="$v.chamber.type.$model"
                            ></b-form-input>
                            <div v-if="$v.chamber.type.$dirty">
                                <div class="error" v-if="!$v.chamber.type.required">Field is required</div>
                            </div>
                        </b-form-group>

                        <!--CODE-->
                        <b-form-group :class="{ 'form-group--error': $v.chamber.code.$error }"
                                      id="form-code-group-edit" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required
                                    type="text"
                                    v-model.trim="$v.chamber.code.$model">
                            </b-form-input>
                            <div v-if="$v.chamber.code.$dirty">
                                <div class="error" v-if="!$v.chamber.code.required">Field is required</div>
                            </div>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>
          <b-button class="float_btn" style="border-radius: 50%" v-b-modal.modal-chamber v-if="isAuth"
                    variant="primary">
            <span>Add Chamber</span> <i class="fas fa-plus-circle menu_icon"></i>
          </b-button>
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
import {chamber_resource, freezer_resource} from '@/utils/api_paths'
import TopNav from "../components/TopNav";
import {
  extractFreezerData,
  getItemDataList,
  isThemeAdmin, pageStartLoader,
  paginate,
  respondTo401,
  secureStoreGetAuthString,
  selectItemForUpdate,
  showFlashMessage
} from "@/utils/util_functions";
import EventBus from '@/components/EventBus';
import FilterCard from "@/components/FilterCard";
import {required} from "vuelidate/lib/validators";

export default {
  name: 'Chamber',
  components: {TopNav, FilterCard},

  data() {
    return {
      page_title: "Chambers",
      filters: [],
      response: [],
      chamberList: [],
      freezerDataList: [],
      chamber: {
        code: '',
        type: '',
        freezer: '',
      },

      // variable to check user status and role
      isAuth: null,

            // loader-time
      time: 2000,

           // progressPath
      indeterminate: true,
      hideBackground: true,
      progressPath: 5,
      size: 180,

      search: '',
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
            chamber: {
                freezer: {required},
                code: {required},
                type: {required},
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
                    this.chamberList = this.response
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
                        'By Type': this.chamberList
                            .map(({type}) => type)
                            .filter((value, index, self) => self.indexOf(value) === index)
                    },
                    {
                        'By Freezer Number': this.chamberList
                            .map(({['freezer.number']: lab}) => lab)
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

                /* freezerList,which is a copy of response, is passed as the data here instead of response to avoid
                mutating response data.*/
                let filteredData = this.filterData(this.chamberList)

                let filterByType = filteredData.type
                let filterByFreezer = filteredData.freezer

                if (searchList !== null) {
                    return paginate(searchList)
                } else if (this.filters.length > 1) {
                    // Possibly, multiple filters have been applied. Return the array with the least elements
                    return filterByType.length < filterByFreezer.length ?
                        paginate(filterByType) : paginate(filterByFreezer)
                } else if (filterByType !== null && filterByType.length > 0) {
                    this.freezerList = filterByType // eslint-disable-line
                    this.filterData(filterByType)
                    return paginate(filterByType)
                } else if (filterByFreezer !== null && filterByFreezer.length > 0) {
                    this.freezerList = filterByFreezer // eslint-disable-line
                    this.filterData(filterByFreezer)
                    return paginate(filterByFreezer)
                }
                return paginate(this.chamberList)
            },
        },

        methods: {
            //Util Functions

            pageInfo(info) {
                EventBus.$emit('page-info', {'pgInfo': info, 'pgData': this.chamberList})
            },

            onSubmit(evt) {
                this.$v.$touch();
                if (this.$v.$invalid) {
                    // stop here if form is invalid
                    evt.preventDefault()
                    return;
                }
                this.createChamber();
            },
            selectItemForUpdate,
            // Util Functions
            clearForm() {
                this.chamber.freezer = null;
                this.chamber.code = null;
                this.chamber.type = null;
                this.isEditing = false;
                this.$v.$reset();
            },

            fillFormForUpdate(freezer, type, code) {
                this.chamber.freezer = freezer;
                this.chamber.code = code;
                this.chamber.type = type;
                this.old_code = code;
                this.isEditing = true;
                this.showModal = true;
            },

            onLoadPage() {
                getItemDataList(freezer_resource).then(data => {
                    let freezerList = extractFreezerData(data);

                    // update local variables with data from API
                    this.fields = freezerList['fields'];
                    for (let i = 0; i < freezerList.items.length; i++) {
                        this.freezerDataList.push({
                            'Code': freezerList.items[i].Code,
                            'Name': freezerList.items[i].Name,
                        });
                    }
                    console.log(this.freezerDataList)
                })
                this.getChamber()
            },
                    // stop&hide progressPath
haltProgressPath(cont=false, path=0, size=0){
  this.indeterminate = cont
this.progressPath = path
this.size = size
},
            // end of Util functions

            // Functions to interact with api
            getChamber() {
              this.isAuth = isThemeAdmin()

              this.clearForm();
              axios.get(chamber_resource)
                  .then((res) => {
                    setTimeout(()=> {
                    this.haltProgressPath()
                    this.chamberList = this.response = res.data['message'];
                  }, this.time)
                    })
                  .catch((error) => {
                    // eslint-disable-next-line
                    this.$log.error(error);
                  });
            },

            createChamber: function () {
                let self = this;
                // this.freezer = getSelectedItem(this.freezerDataList, this.freezer);
                let loader = pageStartLoader(this)

                axios.post(chamber_resource, {
                    freezer: this.chamber.freezer,
                    type: this.chamber.type,
                    code: this.chamber.code,
                }, {
                    headers:
                        {
                          Authorization: secureStoreGetAuthString()
                        }
                })
                    .then((response) => {
                      setTimeout(()=> {
                        loader.hide()
                        this.getChamber();
                        showFlashMessage(self, 'success', response.data['message'], '');
                        this.clearForm();
                        },this.time)
                    })
                    .catch((error) => {
                        this.clearForm();
                        this.$log.error(error);
                        loader.hide()
                        if (error.response) {
                            if (error.response.status === 409) {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            } else if (error.response.status === 400) {
                                showFlashMessage(self, 'error', error.response.data['message'], 'Kindly refill the form');
                            } else if (error.response.status === 401) {
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

            updateChamber: function (evt) {
                this.$v.$touch();
                if (this.$v.$invalid) {
                    evt.preventDefault()
                } else {
                    let self = this;
                    // this.freezer = getSelectedItem(this.freezerDataList, this.freezer);
                  let loader = pageStartLoader(this)
                    axios.put(chamber_resource, {
                        freezer: this.chamber.freezer,
                        type: this.chamber.type,
                        code: this.chamber.code,
                    }, {
                        headers:
                            {
                                code: this.old_code,
                              Authorization: secureStoreGetAuthString()
                            }
                    })
                        .then((response) => {
                          setTimeout( () => {
                            loader.hide()
                            this.getChamber();
                            showFlashMessage(self, 'success', response.data['message'], '');
                            this.clearForm();
                            }, this.time)
                        })
                        .catch((error) => {
                            this.clearForm();
                            this.$log.error(error);
                            loader.hide()
                            if (error.response) {
                                if (error.response.status === 304) {
                                    showFlashMessage(self, 'info', 'Record not modified!', '');
                                } else if (error.response.status === 401) {
                                    respondTo401(self);
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

            deleteChamber: function (code) {
                let self = this;
                let loader = pageStartLoader(this)

                axios.delete(chamber_resource, {
                    headers:
                        {
                            code: code,
                          Authorization: secureStoreGetAuthString()
                        }
                })
                    .then((response) => {
                      setTimeout(() => {
                        loader.hide()
                        this.getChamber();
                        showFlashMessage(self, 'success', response.data['message'], '');
                    }, this.time)
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        loader.hide()
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
            // todo: issue with data filtration
            filterData(data) {
                let filterByType = this.filters.length
                    ? data.filter(chamber => this.filters.some(filter => chamber.type.match(filter)))
                    : null

                let filterByFreezerNum = this.filters.length
                    ? data.filter(chamber => this.filters.some(filter => chamber['freezer.number'].match(filter)))
                    : null

                return {'type': filterByType, 'freezer': filterByFreezerNum}
            },

            searchData() {
                return this.chamberList.filter(chamber => {
                    for (let count = 0; count <= this.chamberList.length; count++) {
                        let byType = chamber.type.toString().toLowerCase().includes(this.search.toLowerCase())
                        let byCode = chamber.code.toString().toLowerCase().includes(this.search.toLowerCase())
                        let byFreezerNum = chamber['freezer.number'].toString().toLowerCase().includes(this.search.toLowerCase())

                        if (byType) {
                            return byType
                        } else if (byCode) {
                            return byCode
                        } else if (byFreezerNum) {
                            return byFreezerNum
                        }
                    }
                })
            },
            // end of search methods
        },
    };
</script>
