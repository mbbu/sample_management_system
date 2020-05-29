<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <top-nav :page_title="page_title"></top-nav>

                <FlashMessage :position="'center bottom'"></FlashMessage>
                <br> <br>
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
                    <tr :key="tray.id" v-for="(tray, index) in response.message">
                        <td> {{ index + 1 }}</td>
                        <td> {{tray.number}}</td>
                        <td> {{tray.code}}</td>
                        <td> {{tray['rack.number']}}</td>

                        <td>
                            <b-icon
                                    icon="pencil" font-scale="2.0"
                                    class="border border-info rounded" variant="info"
                                    v-b-tooltip.hover :title="`Update tray ${ tray.code }`"
                                    v-b-modal.modal-freezer-edit
                                    @mouseover="fillFormForUpdate(tray['rack.number'], tray.number, tray.code)"
                            ></b-icon>
                            &nbsp;
                            <b-icon
                                    icon="trash" font-scale="1.85"
                                    class="border rounded bg-danger p-1" variant="light"
                                    v-b-tooltip.hover :title="`Delete tray ${tray.code}!`"
                                    @click="deleteTray(tray.code)"
                            ></b-icon>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>

            <div v-if="!isEditing">
                <b-modal
                        :title="`Add ${page_title}`"
                        id="modal-freezer"
                        ok-title="Save"
                        cancel-variant="danger"
                        @ok="createTray"
                        @submit="clearForm"
                        @hidden="clearForm"
                >
                    <form @submit.prevent="createTray">
                        <b-form-group id="form-lab-group" label="Rack Number:" label-for="form-lab-input">
                            <ejs-dropdownlist
                                    id='dropdownlist'
                                    :dataSource='rackDataList'
                                    :fields="fields"
                                    placeholder='Select a rack'
                                    :v-model="freezer"
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
                        @ok="updateTray(old_code)"
                        @submit="showModal = false"
                        id="modal-freezer-edit"
                        ok-title="Update"
                        cancel-variant="danger"
                        @shown="selectItemForUpdate(rack)"
                        @hidden="clearForm"
                >
                    <form>
                        <b-form-group id="form-freezer-group-edit" label="Rack Number:"
                                      label-for="form-freezer-input">
                            <ejs-dropdownlist
                                    id='dropdownlist'
                                    :dataSource='rackDataList'
                                    :fields="fields"
                                    placeholder='Select a rack'
                                    :v-model="freezer"
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
            <b-button class="float_btn"
                      v-b-modal.modal-freezer variant="primary"
            >Add Tray
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

    export default {
        name: 'Tray',
        data() {
            return {
                page_title: "Tray",
                response: [],
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

            // Functions to interact with api
            getTray() {
                this.clearForm();
                axios.get(tray_resource)
                    .then((res) => {
                        this.$log.info("Response: " + res.status + " " + res.data['message']);
                        this.response = res.data;
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
        },
        created() {
            this.getTray();
        },
        components: {TopNav}
    };
</script>
