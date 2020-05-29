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
                        <th scope="col"> Description</th>
                        <th scope="col"> Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr :key="sec_level.id" v-for="(sec_level, index) in response.message">
                        <td> {{ index + 1 }}</td>
                        <td> {{ sec_level.name }}</td>
                        <td> {{ sec_level.code }}</td>
                        <td> {{ sec_level.description }}</td>

                        <td>
                            <b-icon
                                    :title="`Update ${ sec_level.name }`"
                                    @mouseover="fillFormForUpdate(sec_level.name, sec_level.code, sec_level.description)"
                                    class="border border-info rounded" font-scale="2.0"
                                    icon="pencil" v-b-modal.modal-security-level-edit
                                    v-b-tooltip.hover
                                    variant="info"
                            ></b-icon>
                            &nbsp;
                            <b-icon
                                    :title="`Delete ${sec_level.name}!`" @click="deleteSecurityLevel(sec_level.code)"
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
                        @ok="createSecurityLevel"
                        @submit="showModal = false"
                        cancel-variant="danger"
                        id="modal-security-level"
                        ok-title="Save"
                        title="Add Security Level"
                >
                    <form @submit.prevent="createSecurityLevel">

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

                        <b-form-group id="form-desc-group" label="Description:" label-for="form-desc-input">
                            <b-form-textarea
                                    id="form-desc-input"
                                    placeholder="Enter Description"
                                    required="true"
                                    type="text"
                                    v-model="desc"
                            ></b-form-textarea>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>

            <div v-else-if="isEditing">
                <b-modal
                        @hidden="clearForm"
                        @ok="updateSecurityLevel(old_code)"
                        @submit="showModal = false"
                        cancel-variant="danger"
                        id="modal-security-level-edit"
                        ok-title="Update"
                        title="Edit Security Level"
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

                        <b-form-group id="form-desc-group-edit" label="Description:" label-for="form-desc-input">
                            <b-form-textarea
                                    id="form-desc-input"
                                    placeholder="Enter Description"
                                    required="true"
                                    type="text"
                                    v-model="desc"
                            ></b-form-textarea>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>
            <b-button class="float_btn"
                      v-b-modal.modal-security-level variant="primary"
            >Add Security Level
            </b-button>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import {security_level_resource} from '../utils/api_paths'
    import TopNav from "@/components/TopNav";
    import {respondTo401, secureStoreGetString, showFlashMessage} from "../utils/util_functions";

    export default {
        name: 'SecurityLevel',
        data() {
            return {
                page_title: "Security Level",
                response: [],
                name: null,
                code: null,
                desc: null,

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
                this.desc = null;
                this.isEditing = false;
            },

            fillFormForUpdate(name, code, desc) {
                this.name = name;
                this.code = code;
                this.desc = desc;
                this.old_code = code;
                this.isEditing = true;
                this.showModal = true;
            },

            getSecurityLevel() {
                axios.get(security_level_resource)
                    .then((res) => {
                        this.$log.info("Response: " + res.status + " " + res.data['message']);
                        this.response = res.data;
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        this.$log.error(error);
                    });
            },

            createSecurityLevel: function () {
                let self = this;
                axios.post(security_level_resource, {
                    name: this.name,
                    code: this.code,
                    description: this.desc,
                }, {
                    headers: {
                        Authorization: secureStoreGetString()
                    }
                })
                    .then((response) => {
                        this.getSecurityLevel();
                        this.clearForm();
                        showFlashMessage(self, 'success', response.data['message'], "")
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 409) {
                                showFlashMessage(self, 'error', "Error", error.response.data['message'])
                            } else if (error.response.status === 401) {
                                respondTo401(self)
                            } else if (error.response.status === 403) {
                                showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
                            } else {
                                showFlashMessage(self, 'error', "Error", "Security Level already exists")
                            }
                        }
                    });
                this.clearForm();
            },

            updateSecurityLevel: function (code) {
                let self = this;

                axios.put(security_level_resource, {
                    name: this.name,
                    code: this.code,
                    description: this.desc,
                }, {
                    headers:
                        {
                            code: code,
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getSecurityLevel();
                        showFlashMessage(self, 'success', response.data['message'], "")
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 304) {
                                showFlashMessage(self, 'info', "Record not modified!", "")
                            } else if (error.response.status === 401) {
                                respondTo401(self)
                            } else if (error.response.status === 403) {
                                showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
                            } else {
                                showFlashMessage(self, 'error', "Error", error.response.data['message'])
                            }
                        }
                    });
                this.clearForm();
            },

            deleteSecurityLevel: function (code) {
                let self = this;

                axios.delete(security_level_resource, {
                    headers:
                        {
                            code: code,
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getSecurityLevel();
                        showFlashMessage(self, 'success', response.data['message'], "")
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        if (error.response.status === 401) {
                            respondTo401(self)
                        } else if (error.response.status === 403) {
                            showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
                        } else {
                            showFlashMessage(self, 'error', "Error", error.response.data['message'])
                        }
                    })
            }
        },
        created() {
            this.getSecurityLevel();
        },
        components: {TopNav}
    };
</script>
