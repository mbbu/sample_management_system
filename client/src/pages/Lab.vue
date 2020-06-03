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
                        <th scope="col"> Name</th>
                        <th scope="col"> Code</th>
                        <th scope="col"> Room</th>
                        <th scope="col"> Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr :key="lab.id" v-for="(lab, index) in response.message">
                        <td> {{ index + 1 }}</td>
                        <td> {{ lab.name }}</td>
                        <td> {{ lab.code }}</td>
                        <td> {{ lab.room }}</td>

                        <td>
                            <b-icon
                                    icon="pencil" font-scale="2.0"
                                    class="border border-info rounded" variant="info"
                                    v-b-tooltip.hover :title="`Update ${ lab.name }`"
                                    v-b-modal.modal-lab-edit
                                    @mouseover="fillFormForUpdate(lab.name, lab.code, lab.room)"
                            ></b-icon>
                            &nbsp;
                            <b-icon
                                    icon="trash" font-scale="1.85"
                                    class="border rounded bg-danger p-1" variant="light"
                                    v-b-tooltip.hover :title="`Delete ${lab.name}!`"
                                    @click="deleteLab(lab.code)"
                            ></b-icon>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>

            <div v-if="!isEditing">
                <b-modal
                        title="Add Lab"
                        id="modal-lab"
                        ok-title="Save"
                        cancel-variant="danger"
                        @ok="createLab"
                        @submit="showModal = false"
                        @hidden="clearForm"
                >
                    <form @submit.prevent="createLab">

                        <b-form-group id="form-name-group" label="Name:" label-for="form-name-input">
                            <b-form-input
                                    id="form-name-input"
                                    placeholder="Enter Name"
                                    required="true"
                                    type="text"
                                    v-model="name"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-code-group" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required="true"
                                    type="text"
                                    v-model="code"></b-form-input>
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
                    </form>
                </b-modal>
            </div>

            <div v-else-if="isEditing">
                <b-modal
                        title="Edit Lab"
                        @ok="updateLab(old_code)"
                        @submit="showModal = false"
                        id="modal-lab-edit"
                        ok-title="Update"
                        cancel-variant="danger"
                        @hidden="clearForm"
                >
                    <form>

                        <b-form-group id="form-name-group-edit" label="Name:" label-for="form-name-input">
                            <b-form-input
                                    id="form-name-input"
                                    placeholder="Enter Name"
                                    required="true"
                                    type="text"
                                    v-model="name"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-code-group-edit" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required="true"
                                    type="text"
                                    v-model="code"></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-room-group-edit" label="Room:" label-for="form-room-input">
                            <b-form-input
                                    id="form-room-input"
                                    placeholder="Enter Room"
                                    required="true"
                                    type="text"
                                    v-model="room"
                            ></b-form-input>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>
            <b-button class="float_btn"
                      v-b-modal.modal-lab variant="primary"
            >Add Lab
            </b-button>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import {lab_resource} from '../utils/api_paths'
    import TopNav from "../components/TopNav";
    import {respondTo401, secureStoreGetString, showFlashMessage} from "../utils/util_functions";

    export default {
        name: 'Lab',
        data() {
            return {
                page_title: "Labs",
                response: [],
                name: null,
                code: null,
                room: null,

                // values for data modification
                old_code: null,
                showModal: true,
                isEditing: false,
            };
        },
        methods: {
            clearForm() {
                this.name = null;
                this.code = null;
                this.room = null;
                this.isEditing = false;
            },

            fillFormForUpdate(name, code, room) {
                this.name = name;
                this.code = code;
                this.room = room;
                this.old_code = code;
                this.isEditing = true;
                this.showModal = true;
            },

            getLab() {
                axios.get(lab_resource)
                    .then((res) => {
                        this.$log.info("Response: " + res.status + " " + res.data['message']);
                        this.response = res.data;
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        this.$log.error(error);
                    });
            },

            createLab: function () {
                let self = this;
                axios.post(lab_resource, {
                    name: this.name,
                    code: this.code,
                    room: this.room,
                }, {
                    headers: {
                        Authorization: secureStoreGetString()
                    }
                })
                    .then((response) => {
                        this.getLab();
                        this.clearForm();
                        showFlashMessage(self, 'success', response.data['message'], '')
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 409) {
                                showFlashMessage(self, 'error', 'Error', error.response.data['message'])
                            } else if (error.response.status === 401) {
                                respondTo401(self)
                            } else if (error.response.status === 403) {
                                showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
                            } else {
                                showFlashMessage(self, 'error', 'Error', error.response.data['message'])
                            }
                        }
                    });
                this.clearForm();
            },

            updateLab: function (code) {
                let self = this;
                axios.put(lab_resource, {
                    name: this.name,
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
                        this.getLab();
                        showFlashMessage(self, 'success', response.data['message'], '')
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 304) {
                                showFlashMessage(self, 'info', 'Info', 'Record not modified!')
                            } else if (error.response.status === 401) {
                                respondTo401(self)
                            } else if (error.response.status === 403) {
                                showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
                            } else {
                                showFlashMessage(self, 'error', 'Error', error.response.data['message'])
                            }
                        }
                    });
                this.clearForm();
            },

            deleteLab: function (code) {
                let self = this;
                axios.delete(lab_resource, {
                    headers:
                        {
                            code: code,
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getLab();
                        showFlashMessage(self, 'success', response.data['message'], '')
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 401) {
                                respondTo401(self)
                            } else if (error.response.status === 403) {
                                showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
                            } else {
                                showFlashMessage(self, 'error', 'Error', error.response.data['message'])
                            }
                        }
                    });
            },
        },
        created() {
            this.getLab();
        },
        components: {TopNav}
    };
</script>
