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
                        <th scope="col"> Lab Located</th>
                        <th scope="col"> Room</th>
                        <th scope="col"> Freezer Number</th>
                        <th scope="col"> Code</th>
                        <th scope="col"> Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr :key="freezer.id" v-for="(freezer, index) in response.message">
                        <td> {{ index + 1 }}</td>
                        <td> {{ freezer['lab.name'] }}</td>
                        <td> {{ freezer.room }}</td>
                        <td> {{ freezer.number }}</td>
                        <td> {{ freezer.code }}</td>

                        <td>
                            <b-icon
                                    icon="pencil" font-scale="2.0"
                                    class="border border-info rounded" variant="info"
                                    v-b-tooltip.hover :title="`Update freezer ${ freezer.number }`"
                                    v-b-modal.modal-freezer-edit
                                    @mouseover="fillFormForUpdate(freezer.number, freezer.code, freezer.room, freezer['lab.name'])"
                            ></b-icon>
                            &nbsp;
                            <b-icon
                                    icon="trash" font-scale="1.85"
                                    class="border rounded bg-danger p-1" variant="light"
                                    v-b-tooltip.hover :title="`Delete freezer ${freezer.number}!`"
                                    @click="deleteFreezer(freezer.code)"
                            ></b-icon>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>

            <div v-if="!isEditing">
                <b-modal
                        title="Add Freezer"
                        id="modal-freezer"
                        ok-title="Save"
                        cancel-variant="danger"
                        @ok="createFreezer"
                        @submit="clearForm"
                        @hidden="clearForm"
                >
                    <form @submit.prevent="createFreezer">
                        <b-form-group id="form-lab-group" label="Lab:" label-for="form-lab-input">
                            <ejs-dropdownlist
                                    id='dropdownlist'
                                    :dataSource='labDataList'
                                    :fields="fields"
                                    placeholder='Select a lab'
                                    :v-model="laboratory"
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
                        title="Edit Freezer"
                        @ok="updateFreezer(old_code)"
                        @submit="showModal = false"
                        id="modal-freezer-edit"
                        ok-title="Update"
                        cancel-variant="danger"
                        @shown="selectLabItemForUpdate(laboratory)"
                        @hidden="clearForm"
                >
                    <form>
                        <b-form-group id="form-lab-group-edit" label="Lab:" label-for="form-lab-input">
                            <ejs-dropdownlist
                                    id='dropdownlist'
                                    :dataSource='labDataList'
                                    :fields="fields"
                                    placeholder='Select a lab'
                                    :v-model="laboratory"
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
            <b-button class="float_btn"
                      v-b-modal.modal-freezer variant="primary"
            >Add Freezer
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

    export default {
        name: 'Freezer',
        data() {
            return {
                page_title: "Freezer",
                response: [],
                laboratory: null,
                number: null,
                code: null,
                room: null,
                labDataList: [],
                fields: {text: '', value: ''},

                // values for data modification
                old_code: null,
                showModal: true,
                isEditing: false,
            };
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
                    this.$log.info("Role list json: ", JSON.stringify(labList));

                    // update local variables with data from API
                    this.fields = labList['fields'];
                    for (let i = 0; i < labList.items.length; i++) {
                        this.labDataList.push({
                            'Code': labList.items[i].Code,
                            'Name': labList.items[i].Name,
                        });
                    }
                    this.$log.info("Extracted data as json fields: ", this.fields);
                    this.$log.info("Extracted labDataList items: ", this.labDataList)
                })
            },

            selectLabItemForUpdate(laboratory) {
                // set dropdownitem to the selected item
                var element = document.getElementById("dropdownlist");
                element.value = laboratory;
            },

            // Functions to interact with api
            getFreezer() {
                this.clearForm();
                axios.get(freezer_resource)
                    .then((res) => {
                        this.$log.info("Response: " + res.status + " " + res.data['message']);
                        this.response = res.data;
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
        },
        created() {
            this.getFreezer();
        },
        components: {TopNav}
    };
</script>
