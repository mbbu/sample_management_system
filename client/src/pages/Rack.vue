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
                        <th scope="col"> Chamber Type</th>
                        <th scope="col"> Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr :key="rack.id" v-for="(rack, index) in response.message">
                        <td> {{ index + 1 }}</td>
                        <td> {{rack.number}}</td>
                        <td> {{rack.code}}</td>
                        <td> {{rack['chamber.type']}}</td>

                        <td>
                            <b-icon
                                    icon="pencil" font-scale="2.0"
                                    class="border border-info rounded" variant="info"
                                    v-b-tooltip.hover :title="`Update rack ${ rack.code }`"
                                    v-b-modal.modal-freezer-edit
                                    @mouseover="fillFormForUpdate(rack['chamber.type'], rack.number, rack.code)"
                            ></b-icon>
                            &nbsp;
                            <b-icon
                                    icon="trash" font-scale="1.85"
                                    class="border rounded bg-danger p-1" variant="light"
                                    v-b-tooltip.hover :title="`Delete rack ${rack.code}!`"
                                    @click="deleteRack(rack.code)"
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
                        @ok="createRack"
                        @submit="clearForm"
                        @hidden="clearForm"
                >
                    <form @submit.prevent="createRack">
                        <b-form-group id="form-lab-group" label="Chamber Type:" label-for="form-lab-input">
                            <ejs-dropdownlist
                                    id='dropdownlist'
                                    :dataSource='chamberDataList'
                                    :fields="fields"
                                    placeholder='Select a chamber'
                                    :v-model="freezer"
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
                        @ok="updateRack(old_code)"
                        @submit="showModal = false"
                        id="modal-freezer-edit"
                        ok-title="Update"
                        cancel-variant="danger"
                        @shown="selectItemForUpdate(chamber)"
                        @hidden="clearForm"
                >
                    <form>
                        <b-form-group id="form-freezer-group-edit" label="Freezer Number:"
                                      label-for="form-freezer-input">
                            <ejs-dropdownlist
                                    id='dropdownlist'
                                    :dataSource='chamberDataList'
                                    :fields="fields"
                                    placeholder='Select a chamber'
                                    :v-model="freezer"
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
            <b-button class="float_btn"
                      v-b-modal.modal-freezer variant="primary"
            >Add Rack
            </b-button>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import {chamber_resource, rack_resource} from '../../src/utils/api_paths'
    import TopNav from "@/components/TopNav";
    import {
        extractChamberData,
        getItemDataList,
        getSelectedItem,
        respondTo401,
        secureStoreGetString,
        selectItemForUpdate,
        showFlashMessage
    } from "../utils/util_functions";

    export default {
        name: 'Rack',
        data() {
            return {
                page_title: "Rack",
                response: [],
                chamber: null,
                code: null,
                number: null,
                chamberDataList: [],
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

            // Functions to interact with api
            getRack() {
                this.clearForm();
                axios.get(rack_resource)
                    .then((res) => {
                        this.$log.info("Response: " + res.status + " " + res.data['message']);
                        this.response = res.data;
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
        },
        created() {
            this.getRack();
        },
        components: {TopNav}
    };
</script>
