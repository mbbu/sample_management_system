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
                        <th scope="col"> Type</th>
                        <th scope="col"> Code</th>
                        <th scope="col"> Freezer Room</th>
                        <th scope="col"> Freezer Number</th>
                        <th scope="col"> Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr :key="chamber.id" v-for="(chamber, index) in response.message">
                        <td> {{ index + 1 }}</td>
                        <td> {{chamber.type}}</td>
                        <td> {{chamber.code}}</td>
                        <td> {{chamber['freezer.room']}}</td>
                        <td> {{chamber['freezer.number']}}</td>

                        <td>
                            <b-icon
                                    icon="pencil" font-scale="2.0"
                                    class="border border-info rounded" variant="info"
                                    v-b-tooltip.hover :title="`Update chamber ${ chamber.code }`"
                                    v-b-modal.modal-freezer-edit
                                    @mouseover="fillFormForUpdate(chamber['freezer.number'], chamber.type, chamber.code)"
                            ></b-icon>
                            &nbsp;
                            <b-icon
                                    icon="trash" font-scale="1.85"
                                    class="border rounded bg-danger p-1" variant="light"
                                    v-b-tooltip.hover :title="`Delete chamber ${chamber.code}!`"
                                    @click="deleteChamber(chamber.code)"
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
                        @ok="createChamber"
                        @submit="clearForm"
                        @hidden="clearForm"
                >
                    <form @submit.prevent="createChamber">
                        <b-form-group id="form-lab-group" label="Freezer Number:" label-for="form-lab-input">
                            <ejs-dropdownlist
                                    id='dropdownlist'
                                    :dataSource='freezerDataList'
                                    :fields="fields"
                                    placeholder='Select a freezer'
                                    :v-model="freezer"
                            ></ejs-dropdownlist>
                        </b-form-group>

                        <b-form-group id="form-room-group" label="Type:" label-for="form-room-input">
                            <b-form-input
                                    id="form-room-input"
                                    placeholder="Enter Freezer Type"
                                    required="true"
                                    type="text"
                                    v-model="type"
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
                        @ok="updateChamber(old_code)"
                        @submit="showModal = false"
                        id="modal-freezer-edit"
                        ok-title="Update"
                        cancel-variant="danger"
                        @shown="selectItemForUpdate(freezer)"
                        @hidden="clearForm"
                >
                    <form>
                        <b-form-group id="form-freezer-group-edit" label="Freezer Number:"
                                      label-for="form-freezer-input">
                            <ejs-dropdownlist
                                    id='dropdownlist'
                                    :dataSource='freezerDataList'
                                    :fields="fields"
                                    placeholder='Select a freezer'
                                    :v-model="freezer"
                            ></ejs-dropdownlist>
                        </b-form-group>

                        <b-form-group id="form-type-group-edit" label="Type:" label-for="form-type-input">
                            <b-form-input
                                    id="form-type-input"
                                    placeholder="Enter chamber type"
                                    required="true"
                                    type="text"
                                    v-model="type"
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
            >Add Chamber
            </b-button>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import {chamber_resource, freezer_resource} from '../utils/api_paths'
    import TopNav from "../components/TopNav";
    import {
        extractFreezerData,
        getItemDataList,
        getSelectedItem,
        respondTo401,
        secureStoreGetString,
        selectItemForUpdate,
        showFlashMessage
    } from "../utils/util_functions";

    export default {
        name: 'Chamber',
        data() {
            return {
                page_title: "Chambers",
                response: [],
                freezer: null,
                code: null,
                type: null,
                freezerDataList: [],
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
                this.freezer = null;
                this.code = null;
                this.type = null;
                this.isEditing = false;
                this.freezerDataList = [];
                this.onLoadPage();
            },

            fillFormForUpdate(freezer, type, code) {
                this.freezer = freezer;
                this.code = code;
                this.type = type;
                this.old_code = code;
                this.isEditing = true;
                this.showModal = true;
            },

            onLoadPage() {
                getItemDataList(freezer_resource).then(data => {
                    let freezerList = extractFreezerData(data);
                    this.$log.info("Freezer list json: ", JSON.stringify(freezerList));

                    // update local variables with data from API
                    this.fields = freezerList['fields'];
                    for (let i = 0; i < freezerList.items.length; i++) {
                        this.freezerDataList.push({
                            'Code': freezerList.items[i].Code,
                            'Name': freezerList.items[i].Name,
                        });
                    }
                    this.$log.info("Extracted data as json fields: ", this.fields);
                    this.$log.info("Extracted freezerDataList items: ", this.freezerDataList)
                })
            },

            // Functions to interact with api
            getChamber() {
                this.clearForm();
                axios.get(chamber_resource)
                    .then((res) => {
                        this.$log.info("Response: " + res.status + " " + res.data['message']);
                        this.response = res.data;
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        this.$log.error(error);
                    });
            },

            createChamber: function () {
                let self = this;
                this.freezer = getSelectedItem(this.freezerDataList, this.freezer);

                axios.post(chamber_resource, {
                    freezer: this.freezer,
                    type: this.type,
                    code: this.code,
                }, {
                    headers:
                        {
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getChamber();
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

            updateChamber: function (code) {
                let self = this;
                this.freezer = getSelectedItem(this.freezerDataList, this.freezer);

                axios.put(chamber_resource, {
                    freezer: this.freezer,
                    type: this.type,
                    code: this.code,
                }, {
                    headers:
                        {
                            code: code,
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getChamber();
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

            deleteChamber: function (code) {
                let self = this;
                axios.delete(chamber_resource, {
                    headers:
                        {
                            code: code,
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getChamber();
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
            this.getChamber();
        },
        components: {TopNav}
    };
</script>
