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
                        <th class="table-header-style" scope="col"> Id</th>
                        <th class="table-header-style" scope="col"> Lab Located</th>
                        <th class="table-header-style" scope="col"> Room</th>
                        <th class="table-header-style" scope="col"> Freezer Number</th>
                        <th class="table-header-style" scope="col"> Code</th>
                        <th class="table-header-style" scope="col"> Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr :key="freezer.id" v-for="(freezer, index) in matchFiltersAndSearch">
                        <td> {{ index + 1 }}</td>
                        <td> {{ freezer['lab.name'] }}</td>
                        <td> {{ freezer.room }}</td>
                        <td> {{ freezer.number }}</td>
                        <td> {{ freezer.code }}</td>

                        <td>
                            <b-icon
                                    :title="`Update freezer ${ freezer.number }`"
                                    @mouseover="fillFormForUpdate(freezer.number, freezer.code, freezer.room, freezer['lab.name'])"
                                    class="border border-info rounded" font-scale="2.0"
                                    icon="pencil" v-b-modal.modal-freezer-edit
                                    v-b-tooltip.hover
                                    variant="info"
                            ></b-icon>
                            &nbsp;
                            <b-icon
                                    :title="`Delete freezer ${freezer.number}!`" @click="deleteFreezer(freezer.code)"
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
                        @hidden="clearForm"
                        @ok="createFreezer"
                        @submit="clearForm"
                        cancel-variant="danger"
                        id="modal-freezer"
                        ok-title="Save"
                        title="Add Freezer"
                >
                    <form @submit.prevent="createFreezer">
                        <b-form-group id="form-lab-group" label="Lab:" label-for="form-lab-input">
                            <ejs-dropdownlist
                                    :dataSource='labDataList'
                                    :fields="fields"
                                    :v-model="laboratory"
                                    id='dropdownlist'
                                    placeholder='Select a lab'
                            ></ejs-dropdownlist>
                        </b-form-group>

                        <b-form-group id="form-room-group" label="Room:" label-for="form-room-input">
                            <b-form-input
                                    id="form-room-input"
                                    placeholder="Enter Room Number"
                                    required="true"
                                    type="text"
                                    v-model="room"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-num-group" label="Num:" label-for="form-num-input">
                            <b-form-input
                                    id="form-num-input"
                                    placeholder="Enter Freezer Number"
                                    required="true"
                                    type="text"
                                    v-model="number">
                            </b-form-input>
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
                        @hidden="clearForm"
                        @ok="updateFreezer(old_code)"
                        @shown="selectLabItemForUpdate(laboratory)"
                        @submit="showModal = false"
                        cancel-variant="danger"
                        id="modal-freezer-edit"
                        ok-title="Update"
                        title="Edit Freezer"
                >
                    <form>
                        <b-form-group id="form-lab-group-edit" label="Lab:" label-for="form-lab-input">
                            <ejs-dropdownlist
                                    :dataSource='labDataList'
                                    :fields="fields"
                                    :v-model="laboratory"
                                    id='dropdownlist'
                                    placeholder='Select a lab'
                            ></ejs-dropdownlist>
                        </b-form-group>

                        <b-form-group id="form-room-group-edit" label="Room:" label-for="form-room-input">
                            <b-form-input
                                    id="form-room-input"
                                    placeholder="Enter Room Number"
                                    required="true"
                                    type="text"
                                    v-model="room"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-num-group-edit" label="Num:" label-for="form-num-input">
                            <b-form-input
                                    id="form-num-input"
                                    placeholder="Enter Freezer Number"
                                    required="true"
                                    type="text"
                                    v-model="number">
                            </b-form-input>
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
            <b-button class="float_btn" style="border-radius: 50%" v-b-modal.modal-freezer variant="primary">
                <span>Add Freezer</span> <i class="fas fa-plus-circle menu_icon"></i>
            </b-button>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import {freezer_resource, lab_resource} from '../utils/api_paths'
    import TopNav from "../components/TopNav";
    import {
        extractApiData,
        getItemDataList,
        getSelectedItem,
        respondTo401,
        secureStoreGetString,
        showFlashMessage
    } from "../utils/util_functions";
    import EventBus from '../components/EventBus';
    import FilterCard from "../components/FilterCard";

    export default {
        name: 'Freezer',
        components: {TopNav, FilterCard},

        data() {
            return {
                page_title: "Freezer",
                filters: [],
                response: [],
                freezerList: [],
                labDataList: [],
                code: null,
                search: '',
                room: null,
                number: null,
                laboratory: null,
                fields: {text: '', value: ''},

                // values for data modification
                old_code: null,
                showModal: true,
                isEditing: false,
            };
        },

        created() {
            this.getFreezer();
        },

        mounted() {
            EventBus.$on('searchQuery', (payload) => {
                this.search = payload
                this.searchData()
            })

            EventBus.$on('filters', (payload) => {
                this.filters = payload
                if (this.filters.length === 0) {
                    this.freezerList = this.response
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
                        'By Lab': this.response
                            .map(({['lab.name']: lab}) => lab)
                            .filter((value, index, self) => self.indexOf(value) === index),
                    },
                    {
                        'By Room': this.response
                            .map(({room}) => room)
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
                /* freezerList,which is a copy of response, is passed as the data here instead of response to avoid
                mutating response data.*/
                let filteredData = this.filterData(this.freezerList)

                let filterByLab = filteredData.lab
                let filterByRoom = filteredData.room


                if (searchList !== null) {
                    return searchList
                } else if (this.filters.length > 1) {
                    // Possibly, multiple filters have been applied. Return the array with the least elements
                    return filterByLab.length < filterByRoom.length ?
                        filterByLab : filterByRoom
                } else if (filterByLab !== null && filterByLab.length > 0) {
                    this.freezerList = filterByLab // eslint-disable-line
                    this.filterData(filterByLab)
                    return filterByLab
                } else if (filterByRoom !== null && filterByRoom.length > 0) {
                    this.freezerList = filterByRoom // eslint-disable-line
                    this.filterData(filterByRoom)
                    return filterByRoom
                }
                return this.freezerList
            },
        },

        methods: {
            // Util Functions
            clearForm() {
                this.laboratory = null;
                this.number = null;
                this.code = null;
                this.room = null;
                this.isEditing = false;
                this.labDataList = [];
                this.onLoadPage();
            },

            fillFormForUpdate(number, code, room, laboratory) {
                this.laboratory = laboratory;
                this.number = number;
                this.code = code;
                this.room = room;
                this.old_code = code;
                this.isEditing = true;
                this.showModal = true;
            },

            onLoadPage() {
                getItemDataList(lab_resource).then(data => {
                    let labList = extractApiData(data);

                    // update local variables with data from API
                    this.fields = labList['fields'];
                    for (let i = 0; i < labList.items.length; i++) {
                        this.labDataList.push({
                            'Code': labList.items[i].Code,
                            'Name': labList.items[i].Name,
                        });
                    }
                })
            },

            selectLabItemForUpdate(laboratory) {
                // set dropdownitem to the selected item
                var element = document.getElementById("dropdownlist");
                element.value = laboratory;
            },
            // end of Util functions

            // Functions to interact with api
            getFreezer() {
                this.clearForm();
                axios.get(freezer_resource)
                    .then((res) => {
                        this.response = res.data['message'];
                        this.freezerList = this.response
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        this.$log.error(error);
                    });
            },

            createFreezer: function () {
                let self = this;
                this.laboratory = getSelectedItem(this.labDataList, this.laboratory);

                axios.post(freezer_resource, {
                    laboratory: this.laboratory,
                    number: this.number,
                    code: this.code,
                    room: this.room,
                }, {
                    headers:
                        {
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getFreezer();
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
                                respondTo401(self);
                            } else if (error.response.status === 403) {
                                showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
                            } else {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            }
                        }
                    });
            },

            updateFreezer: function (code) {
                let self = this;
                this.laboratory = getSelectedItem(this.labDataList, this.laboratory);

                axios.put(freezer_resource, {
                    laboratory: this.laboratory,
                    number: this.number,
                    code: this.code,
                    room: this.room,
                }, {
                    headers:
                        {
                            code: code,
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getFreezer();
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
                                respondTo401(self);
                            } else if (error.response.status === 403) {
                                showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
                            } else {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            }
                        }
                    });
            },

            deleteFreezer: function (code) {
                let self = this;
                axios.delete(freezer_resource, {
                    headers:
                        {
                            code: code,
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getFreezer();
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
                let filterByRoom = this.filters.length
                    ? data.filter(freezer => this.filters.some(filter => freezer.room.match(filter)))
                    : null

                let filterByLab = this.filters.length
                    ? data.filter(freezer => this.filters.some(filter => freezer['lab.name'].match(filter)))
                    : null

                return {'lab': filterByLab, 'room': filterByRoom}
            },

            searchData() {
                return this.response.filter(freezer => {
                    for (let count = 0; count <= this.response.length; count++) {
                        let byRoom = freezer.room.toString().toLowerCase().includes(this.search.toLowerCase())
                        let byCode = freezer.code.toString().toLowerCase().includes(this.search.toLowerCase())
                        let byNumber = freezer.number.toString().toLowerCase().includes(this.search.toLowerCase())
                        let byLabName = freezer['lab.name'].toString().toLowerCase().includes(this.search.toLowerCase())

                        if (byNumber === true) {
                            return byNumber
                        } else if (byRoom) {
                            return byRoom
                        } else if (byCode) {
                            return byCode
                        } else if (byLabName) {
                            return byLabName
                        }
                    }
                })
            },
            // end-of methods for search and filter
        },
    };
</script>
