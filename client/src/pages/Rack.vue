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
                        <th scope="col"> Chamber Type</th>
                        <th scope="col"> Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr :key="rack.id" v-for="(rack, index) in matchFiltersAndSearch">
                        <td> {{ index + 1 }}</td>
                        <td> {{rack.number}}</td>
                        <td> {{rack.code}}</td>
                        <td> {{rack['chamber.type']}}</td>

                        <td>
                            <b-icon
                                    :title="`Update rack ${ rack.code }`"
                                    @mouseover="fillFormForUpdate(rack['chamber.type'], rack.number, rack.code)"
                                    class="border border-info rounded" font-scale="2.0"
                                    icon="pencil" v-b-modal.modal-rack-edit
                                    v-b-tooltip.hover
                                    variant="info"
                            ></b-icon>
                            &nbsp;
                            <b-icon
                                    :title="`Delete rack ${rack.code}!`" @click="deleteRack(rack.code)"
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
                        @ok="createRack"
                        @submit="clearForm"
                        cancel-variant="danger"
                        id="modal-rack"
                        ok-title="Save"
                >
                    <form @submit.prevent="createRack">
                        <b-form-group id="form-chamber-group" label="Chamber Type:" label-for="form-chamber-input">
                            <ejs-dropdownlist
                                    :dataSource='chamberDataList'
                                    :fields="fields"
                                    :v-model="chamber"
                                    id='dropdownlist'
                                    placeholder='Select a chamber'
                            ></ejs-dropdownlist>
                        </b-form-group>

                        <b-form-group id="form-number-group" label="Number:" label-for="form-number-input">
                            <b-form-input
                                    id="form-number-input"
                                    placeholder="Enter Rack Number"
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
                        @ok="updateRack(old_code)"
                        @shown="selectItemForUpdate(chamber)"
                        @submit="showModal = false"
                        cancel-variant="danger"
                        id="modal-rack-edit"
                        ok-title="Update"
                >
                    <form>
                        <b-form-group id="form-chamber-group-edit" label="Freezer Number:"
                                      label-for="form-chamber-input">
                            <ejs-dropdownlist
                                    :dataSource='chamberDataList'
                                    :fields="fields"
                                    :v-model="chamber"
                                    id='dropdownlist'
                                    placeholder='Select a chamber'
                            ></ejs-dropdownlist>
                        </b-form-group>

                        <b-form-group id="form-type-group-edit" label="Number:" label-for="form-type-input">
                            <b-form-input
                                    id="form-type-input"
                                    placeholder="Enter Rack Number"
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
            <b-button class="float_btn" style="border-radius: 50%" v-b-modal.modal-rack variant="primary">
                <span>Add Rack</span> <i class="fas fa-plus-circle menu_icon"></i>
            </b-button>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import {chamber_resource, rack_resource} from '../utils/api_paths'
    import TopNav from "../components/TopNav";
    import {
        extractChamberData,
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
        name: 'Rack',
        components: {TopNav, FilterCard},

        data() {
            return {
                page_title: "Rack",
                filters: [],
                response: [],
                rackList: [],
                search: '',
                code: null,
                number: null,
                chamber: null,

                chamberDataList: [],
                fields: {text: '', value: ''},

                // values for data modification
                old_code: null,
                showModal: true,
                isEditing: false,
            };
        },

        created() {
            this.getRack();
        },

        mounted() {
            EventBus.$on('searchQuery', (payload) => {
                this.search = payload
                this.filteredList()
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
                    return searchList
                } else if (this.filters.length > 1) {
                    // Possibly, multiple filters have been applied. Return the array with the least elements
                    return filterByNumber.length < filterByChamber.length ?
                        filterByNumber : filterByChamber
                } else if (filterByNumber !== null && filterByNumber.length > 0) {
                    this.rackList = filterByNumber // eslint-disable-line
                    this.filterData(filterByNumber)
                    return filterByNumber
                } else if (filterByChamber !== null && filterByChamber.length > 0) {
                    this.rackList = filterByChamber // eslint-disable-line
                    this.filterData(filterByChamber)
                    return filterByChamber
                }
                return this.rackList
            },
        },

        methods: {
            selectItemForUpdate,
            // Util Functions
            clearForm() {
                this.chamber = null;
                this.code = null;
                this.number = null;
                this.isEditing = false;
                this.chamberDataList = [];
                this.onLoadPage();
            },

            fillFormForUpdate(chamber, number, code) {
                this.chamber = chamber;
                this.code = code;
                this.number = number;
                this.old_code = code;
                this.isEditing = true;
                this.showModal = true;
            },

            onLoadPage() {
                getItemDataList(chamber_resource).then(data => {
                    let chamberList = extractChamberData(data);
                    this.$log.info("Chamber list json: ", JSON.stringify(chamberList));

                    // update local variables with data from API
                    this.fields = chamberList['fields'];
                    for (let i = 0; i < chamberList.items.length; i++) {
                        this.chamberDataList.push({
                            'Code': chamberList.items[i].Code,
                            'Name': chamberList.items[i].Name,
                        });
                    }
                })
            },
            // end of Util functions

            // Functions to interact with api
            getRack() {
                this.clearForm();
                axios.get(rack_resource)
                    .then((res) => {
                        this.$log.info("Response: " + res.status + " ", res.data['message']);
                        this.rackList = this.response = res.data['message'];
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        this.$log.error(error);
                    });
            },

            createRack: function () {
                let self = this;
                this.chamber = getSelectedItem(this.chamberDataList, this.chamber);

                axios.post(rack_resource, {
                    chamber: this.chamber,
                    number: this.number,
                    code: this.code,
                }, {
                    headers:
                        {
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getRack();
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

            updateRack: function (code) {
                let self = this;
                this.chamber = getSelectedItem(this.chamberDataList, this.chamber);

                axios.put(rack_resource, {
                    chamber: this.chamber,
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
                        this.getRack();
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

            deleteRack: function (code) {
                let self = this;
                axios.delete(rack_resource, {
                    headers:
                        {
                            code: code,
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getRack();
                        showFlashMessage(self, 'success', response.data['message'], '');
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 401) {
                                respondTo401(self)
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
