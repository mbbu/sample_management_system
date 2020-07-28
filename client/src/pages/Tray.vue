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
                <table class=" table table-hover">
                    <thead>
                    <tr>
                        <th scope="col"> Id</th>
                        <th scope="col"> Number</th>
                        <th scope="col"> Code</th>
                        <th scope="col"> Rack Number</th>
                        <th scope="col"> Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr :key="tray.id" v-for="(tray, index) in matchFiltersAndSearch">
                        <td> {{ index + 1 }}</td>
                        <td> {{tray.number}}</td>
                        <td> {{tray.code}}</td>
                        <td> {{tray['rack.number']}}</td>

                        <td>
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
            </div>

            <div v-if="!isEditing">
                <b-modal
                        :title="`Add ${page_title}`"
                        @hidden="clearForm"
                        @ok="createTray"
                        @submit="clearForm"
                        cancel-variant="danger"
                        id="modal-tray"
                        ok-title="Save"
                >
                    <form @submit.prevent="createTray">
                        <b-form-group id="form-lab-group" label="Rack Number:" label-for="form-lab-input">
                            <ejs-dropdownlist
                                    :dataSource='rackDataList'
                                    :fields="fields"
                                    :v-model="rack"
                                    id='dropdownlist'
                                    placeholder='Select a rack'
                            ></ejs-dropdownlist>
                        </b-form-group>

                        <b-form-group id="form-number-group" label="Number:" label-for="form-number-input">
                            <b-form-input
                                    id="form-number-input"
                                    placeholder="Enter Tray Number"
                                    required="true"
                                    type="text"
                                    v-model="number"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-code-group" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required="true"
                                    type="text"
                                    v-model="code">
                            </b-form-input>
                        </b-form-group>

                    </form>
                </b-modal>
            </div>

            <div v-else-if="isEditing">
                <b-modal
                        :title="`Edit ${page_title}`"
                        @hidden="clearForm"
                        @ok="updateTray(old_code)"
                        @shown="selectItemForUpdate(rack)"
                        @submit="showModal = false"
                        cancel-variant="danger"
                        id="modal-tray-edit"
                        ok-title="Update"
                >
                    <form>
                        <b-form-group id="form-rack-group-edit" label="Rack Number:"
                                      label-for="form-rack-input">
                            <ejs-dropdownlist
                                    :dataSource='rackDataList'
                                    :fields="fields"
                                    :v-model="rack"
                                    id='dropdownlist'
                                    placeholder='Select a rack'
                            ></ejs-dropdownlist>
                        </b-form-group>

                        <b-form-group id="form-type-group-edit" label="Number:" label-for="form-type-input">
                            <b-form-input
                                    id="form-type-input"
                                    placeholder="Enter Tray Number"
                                    required="true"
                                    type="text"
                                    v-model="number"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-code-group-edit" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required="true"
                                    type="text"
                                    v-model="code">
                            </b-form-input>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>
            <b-button class="float_btn" style="border-radius: 50%" v-b-modal.modal-tray variant="primary">
                <span>Add Tray</span> <i class="fas fa-plus-circle menu_icon"></i>
            </b-button>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import {rack_resource, tray_resource} from '../utils/api_paths'
    import TopNav from "../components/TopNav";
    import {
        extractRackData,
        getItemDataList,
        getSelectedItem,
        respondTo401,
        secureStoreGetString,
        selectItemForUpdate,
        showFlashMessage
    } from "../utils/util_functions";
    import EventBus from '../components/EventBus';
    import FilterCard from "../components/FilterCard";

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
                rack: null,
                code: null,
                number: null,
                rackDataList: [],
                fields: {text: '', value: ''},

                // values for data modification
                old_code: null,
                showModal: true,
                isEditing: false,
            };
        },

        created() {
            this.getTray();
        },

        mounted() {
            EventBus.$on('searchQuery', (payload) => {
                this.search = payload
                this.filteredList()
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
                    return searchList
                } else if (this.filters.length > 1) {
                    // Possibly, multiple filters have been applied. Return the array with the least elements
                    return filterByNumber.length < filterByRack.length ?
                        filterByNumber : filterByRack
                } else if (filterByNumber !== null && filterByNumber.length > 0) {
                    this.trayList = filterByNumber // eslint-disable-line
                    this.filterData(filterByNumber)
                    return filterByNumber
                } else if (filterByRack !== null && filterByRack.length > 0) {
                    this.rackList = filterByRack // eslint-disable-line
                    this.filterData(filterByRack)
                    return filterByRack
                }
                return this.trayList
            },
        },

        methods: {
            selectItemForUpdate,
            // Util Functions
            clearForm() {
                this.rack = null;
                this.code = null;
                this.number = null;
                this.isEditing = false;
                this.rackDataList = [];
                this.onLoadPage();
            },

            fillFormForUpdate(rack, number, code) {
                this.rack = rack;
                this.code = code;
                this.number = number;
                this.old_code = code;
                this.isEditing = true;
                this.showModal = true;
            },

            onLoadPage() {
                getItemDataList(rack_resource).then(data => {
                    let rackList = extractRackData(data);
                    this.$log.info("Rack list json: ", JSON.stringify(rackList));

                    // update local variables with data from API
                    this.fields = rackList['fields'];
                    for (let i = 0; i < rackList.items.length; i++) {
                        this.rackDataList.push({
                            'Code': rackList.items[i].Code,
                            'Name': rackList.items[i].Name,
                        });
                    }
                })
            },
            // end of util functions

            // Functions to interact with api
            getTray() {
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
                this.rack = getSelectedItem(this.rackDataList, this.rack);

                axios.post(tray_resource, {
                    rack: this.rack,
                    number: this.number,
                    code: this.code,
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
            },

            updateTray: function (code) {
                let self = this;
                this.rack = getSelectedItem(this.rackDataList, this.rack);

                axios.put(tray_resource, {
                    rack: this.rack,
                    number: this.number,
                    code: this.code,
                }, {
                    headers:
                        {
                            code: code,
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
