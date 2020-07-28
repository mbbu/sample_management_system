<template>

    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <top-nav :page_title="page_title" v-bind:search_query.sync="search"></top-nav>

                <FlashMessage :position="'center bottom'"></FlashMessage>
                <br>
                <!-- FILTER CARD SECTION -->
                <filter-card :all-filters="allFilters"></filter-card>
                <br>

                <table class=" table table-hover">
                    <thead>
                    <tr>
                        <th scope="col"> Id</th>
                        <th scope="col"> Label</th>
                        <th scope="col"> Tray</th>
                        <th scope="col"> Rack</th>
                        <th scope="col"> Chamber</th>
                        <th scope="col"> Freezer</th>
                        <th scope="col"> Lab Name</th>
                        <th scope="col"> Lab Room</th>
                        <th scope="col"> Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr :key="box.id" v-for="(box, index) in matchFiltersAndSearch">
                        <td> {{index + 1}}</td>
                        <td> {{box.label}}</td>
                        <td> {{box['tray.number']}}</td>
                        <td> {{box['tray.rack.number']}}</td>
                        <td> {{box['tray.rack.chamber.type']}}</td>
                        <td> {{box['tray.rack.chamber.freezer.number']}}</td>
                        <td> {{box['tray.rack.chamber.freezer.lab.name']}}</td>
                        <td> {{box['tray.rack.chamber.freezer.lab.room']}}</td>

                        <td>
                            <b-icon
                                    :title="`Update box ${ box.label }`"
                                    @mouseover="fillFormForUpdate(box['tray.number'], box.label, box.code)"
                                    class="border border-info rounded" font-scale="2.0"
                                    icon="pencil" v-b-modal.modal-box-edit
                                    v-b-tooltip.hover
                                    variant="info"
                            ></b-icon>
                            &nbsp;
                            <b-icon
                                    :title="`Delete box ${box.label}!`" @click="deleteBox(box.code)"
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
                        @ok="createBox"
                        @submit="clearForm"
                        cancel-variant="danger"
                        id="modal-box"
                        ok-title="Save"
                >
                    <form @submit.prevent="createBox">
                        <b-form-group id="form-tray-group" label="Tray Number:" label-for="form-tray-input">
                            <ejs-dropdownlist
                                    :dataSource='trayDataList'
                                    :fields="fields"
                                    :v-model="box.tray"
                                    id='dropdownlist'
                                    placeholder='Select a tray'
                            ></ejs-dropdownlist>
                        </b-form-group>

                        <b-form-group id="form-label-group" label="Box Label:" label-for="form-label-input">
                            <b-form-input
                                    id="form-label-input"
                                    placeholder="Enter box label"
                                    required="true"
                                    type="text"
                                    v-model="box.label"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-code-group" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required="true"
                                    type="text"
                                    v-model="box.code">
                            </b-form-input>
                        </b-form-group>

                    </form>
                </b-modal>
            </div>

            <div v-else-if="isEditing">
                <b-modal
                        :title="`Edit ${page_title}`"
                        @hidden="clearForm"
                        @ok="updateBox(old_code)"
                        @shown="selectItemForUpdate(box.tray)"
                        @submit="showModal = false"
                        cancel-variant="danger"
                        id="modal-box-edit"
                        ok-title="Update"
                >
                    <form>
                        <b-form-group id="form-tray-group-edit" label="Tray Number:" label-for="form-tray-input">
                            <ejs-dropdownlist
                                    :dataSource='trayDataList'
                                    :fields="fields"
                                    :v-model="box.tray"
                                    id='dropdownlist'
                                    placeholder='Select a tray'
                            ></ejs-dropdownlist>
                        </b-form-group>

                        <b-form-group id="form-label-group-edit" label="Box Label:" label-for="form-label-input">
                            <b-form-input
                                    id="form-label-input"
                                    placeholder="Enter box label"
                                    required="true"
                                    type="text"
                                    v-model="box.label"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-code-group-edit" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required="true"
                                    type="text"
                                    v-model="box.code">
                            </b-form-input>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>
            <b-button class="float_btn" style="border-radius: 50%" v-b-modal.modal-box variant="primary">
                <span>Add Box</span> <i class="fas fa-plus-circle menu_icon"></i>
            </b-button>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import TopNav from "../components/TopNav";
    import {
        extractTrayData,
        getItemDataList,
        getSelectedItem,
        respondTo401,
        secureStoreGetString,
        selectItemForUpdate,
        showFlashMessage
    } from "../utils/util_functions";
    import {box_resource, tray_resource} from "../utils/api_paths";
    import EventBus from '../components/EventBus';
    import FilterCard from "../components/FilterCard";

    export default {
        name: 'Box',
        components: {TopNav, FilterCard},

        data() {
            return {
                page_title: 'Boxes',

                filters: [],
                boxList: [],
                response: [],
                search: '',

                box: {
                    tray: null,
                    label: null,
                    code: null
                },

                trayDataList: [],
                fields: {text: '', value: ''},

                // values for data modification
                old_code: null,
                showModal: true,
                isEditing: false,

            };
        },

        created() {
            this.getBox();
        },

        mounted() {
            EventBus.$on('searchQuery', (payload) => {
                this.search = payload
                this.filteredList()
            })

            EventBus.$on('filters', (payload) => {
                this.filters = payload
                if (this.filters.length === 0) {
                    this.boxList = this.response
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
                        'By Label': this.response
                            .map(({label}) => label)
                            .filter((value, index, self) => self.indexOf(value) === index)
                    },
                    {
                        'By Tray': this.response
                            .map(({['tray.number']: tray}) => tray)
                            .filter((value, index, self) => self.indexOf(value) === index),
                    },
                    {
                        'By Rack': this.response
                            .map(({['tray.rack.number']: rack}) => rack)
                            .filter((value, index, self) => self.indexOf(value) === index),
                    },
                    {
                        'By chamber': this.response
                            .map(({['tray.rack.chamber.type']: chamber}) => chamber)
                            .filter((value, index, self) => self.indexOf(value) === index),
                    },
                    {
                        'By Freezer': this.response
                            .map(({['tray.rack.chamber.freezer.number']: freezer}) => freezer)
                            .filter((value, index, self) => self.indexOf(value) === index),
                    },
                    {
                        'By Lab': this.response
                            .map(({['tray.rack.chamber.freezer.lab.name']: lab}) => lab)
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
                /* boxList,which is a copy of response, is passed as the data here instead of response to avoid
                mutating response data.*/
                let filteredData = this.filterData(this.boxList)

                let filterByLabel = filteredData.label
                let filterByTray = filteredData.tray
                let filterByRack = filteredData.rack
                let filterByChamber = filteredData.chamber
                let filterByFreezer = filteredData.freezer
                let filterByLab = filteredData.lab


                if (searchList !== null) {
                    return searchList
                } else if (this.filters.length > 1) {
                    let freezerFiltered = filterByFreezer.length < filterByLab.length ?
                        filterByFreezer : filterByLab

                    let chamberFiltered = filterByChamber.length < filterByFreezer.length ?
                        filterByChamber : filterByFreezer

                    let rackFiltered = filterByRack.length < filterByChamber.length ?
                        filterByRack : null

                    let trayFiltered = filterByTray.length < filterByRack.length ?
                        filterByTray : null

                    let labelFiltered = filterByLabel.length < filterByTray.length ?
                        filterByLabel : null


                    this.boxList = labelFiltered != null && labelFiltered.length !== 0 && labelFiltered < trayFiltered ? labelFiltered // eslint-disable-line
                        : trayFiltered != null && trayFiltered.length !== 0 && trayFiltered < rackFiltered ? trayFiltered
                            : rackFiltered != null && rackFiltered.length !== 0 && rackFiltered < chamberFiltered ? rackFiltered
                                : chamberFiltered != null && chamberFiltered.length !== 0 && chamberFiltered < freezerFiltered ? chamberFiltered
                                    : freezerFiltered // eslint-disable-line

                    return this.boxList

                } else if (filterByLabel !== null && filterByLabel.length > 0) {
                    this.boxList = filterByLabel // eslint-disable-line
                    this.filterData(filterByLabel)
                    return filterByLabel
                } else if (filterByTray !== null && filterByTray.length > 0) {
                    this.rackList = filterByTray // eslint-disable-line
                    this.filterData(filterByTray)
                    return filterByTray
                } else if (filterByRack !== null && filterByRack.length > 0) {
                    this.rackList = filterByRack // eslint-disable-line
                    this.filterData(filterByRack)
                    return filterByRack
                } else if (filterByChamber !== null && filterByChamber.length > 0) {
                    this.rackList = filterByChamber // eslint-disable-line
                    this.filterData(filterByChamber)
                    return filterByChamber
                } else if (filterByFreezer !== null && filterByFreezer.length > 0) {
                    this.rackList = filterByFreezer // eslint-disable-line
                    this.filterData(filterByFreezer)
                    return filterByFreezer
                } else if (filterByLab !== null && filterByLab.length > 0) {
                    this.rackList = filterByLab // eslint-disable-line
                    this.filterData(filterByLab)
                    return filterByLab
                }

                return this.boxList
            },
        },

        methods: {
            // component util functions
            selectItemForUpdate,
            clearForm() {
                this.box.tray = null;
                this.box.code = null;
                this.box.label = null;
                this.isEditing = false;
                this.trayDataList = [];
                this.onLoadPage();
            },

            fillFormForUpdate(tray, label, code) {
                this.box.tray = tray;
                this.box.code = code;
                this.box.label = label;
                this.old_code = code;
                this.isEditing = true;
                this.showModal = true;
            },

            onLoadPage() {
                getItemDataList(tray_resource).then(data => {
                    let trayList = extractTrayData(data);
                    this.$log.info("Tray list json: ", JSON.stringify(trayList));

                    // update local variables with data from API
                    this.fields = trayList['fields'];
                    for (let i = 0; i < trayList.items.length; i++) {
                        this.trayDataList.push({
                            'Code': trayList.items[i].Code,
                            'Name': trayList.items[i].Name,
                        });
                    }
                    this.$log.info("FIELDS: ", this.fields);
                    this.$log.info("Data: ", this.fields);
                })
            },

            // functions to interact with API
            getBox() {
                this.clearForm();
                axios.get(box_resource)
                    .then((res) => {
                        this.boxList = this.response = res.data['message'];
                        console.log('box list: ', this.boxList)
                    })
                    .catch((error) => {
                        console.error(error);
                    });
            },

            createBox: function () {
                let self = this;
                this.box.tray = getSelectedItem(this.trayDataList, this.tray);

                axios.post(box_resource, {
                    tray: this.box.tray,
                    label: this.box.label,
                    code: this.box.code,
                }, {
                    headers:
                        {
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getBox();
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

            updateBox: function (code) {
                let self = this;
                this.box.tray = getSelectedItem(this.trayDataList, this.box.tray);

                axios.put(box_resource, {
                    tray: this.box.tray,
                    label: this.box.label,
                    code: this.box.code,
                }, {
                    headers:
                        {
                            code: code,
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getBox();
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

            deleteBox: function (code) {
                let self = this;
                axios.delete(box_resource, {
                    headers:
                        {
                            code: code,
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getBox();
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
                let filterByLab = this.filters.length
                    ? data.filter(box => this.filters.some(filter => box['tray.rack.chamber.freezer.lab.name'].toString().match(filter))) : null

                let filterByFreezer = this.filters.length
                    ? data.filter(box => this.filters.some(filter => box['tray.rack.chamber.freezer.number'].toString().match(filter))) : null

                let filterByChamber = this.filters.length
                    ? data.filter(box => this.filters.some(filter => box['tray.rack.chamber.type'].toString().match(filter))) : null

                let filterByRack = this.filters.length
                    ? data.filter(box => this.filters.some(filter => box['tray.rack.number'].toString().match(filter))) : null

                let filterByTray = this.filters.length
                    ? data.filter(box => this.filters.some(filter => box['tray.number'].toString().match(filter))) : null

                let filterByLabel = this.filters.length
                    ? data.filter(box => this.filters.some(filter => box.label.toString().match(filter)))
                    : null

                return {
                    'label': filterByLabel,
                    'tray': filterByTray,
                    'rack': filterByRack,
                    'chamber': filterByChamber,
                    'freezer': filterByFreezer,
                    'lab': filterByLab,
                }
            },

            searchData() {
                return this.boxList.filter(box => {
                    for (let count = 0; count <= this.boxList.length; count++) {
                        let byCode = box.code.toString().toLowerCase().includes(this.search.toLowerCase())
                        let byLabel = box.label.toString().toLowerCase().includes(this.search.toLowerCase())
                        let byTray = box['tray.number'].toString().toLowerCase().includes(this.search.toLowerCase())
                        let byRack = box['tray.rack.number'].toString().toLowerCase().includes(this.search.toLowerCase())
                        let byChamber = box['tray.rack.chamber.type'].toString().toLowerCase().includes(this.search.toLowerCase())
                        let byFreezer = box['tray.rack.chamber.freezer.number'].toString().toLowerCase().includes(this.search.toLowerCase())
                        let byLab = box['tray.rack.chamber.freezer.lab.name'].toString().toLowerCase().includes(this.search.toLowerCase())

                        if (byCode) {
                            return byCode
                        } else if (byLabel) {
                            return byLabel
                        } else if (byTray) {
                            return byTray
                        } else if (byRack) {
                            return byRack
                        } else if (byChamber) {
                            return byChamber
                        } else if (byFreezer) {
                            return byFreezer
                        } else if (byLab) {
                            return byLab
                        }
                    }
                })
            },
            // end-of methods for search and filter
        },
    };
</script>


