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
                                    icon="pencil" font-scale="2.0"
                                    class="border border-info rounded" variant="info"
                                    v-b-tooltip.hover :title="`Update ${ sec_level.name }`"
                                    v-b-modal.modal-security-level-edit
                                    @mouseover="fillFormForUpdate(sec_level.name, sec_level.code, sec_level.description)"
                            ></b-icon>
                            &nbsp;
                            <b-icon
                                    icon="trash" font-scale="1.85"
                                    class="border rounded bg-danger p-1" variant="light"
                                    v-b-tooltip.hover :title="`Delete ${sec_level.name}!`"
                                    @click="deleteSecurityLevel(sec_level.code)"
                            ></b-icon>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>

            <div v-if="!isEditing">
                <b-modal
                        title="Add Security Level"
                        id="modal-security-level"
                        ok-title="Save"
                        cancel-variant="danger"
                        @ok="createSecurityLevel"
                        @submit="showModal = false"
                        @hidden="clearForm"
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
                        title="Edit Security Level"
                        @ok="updateSecurityLevel(old_code)"
                        @submit="showModal = false"
                        id="modal-security-level-edit"
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
    import {security_level_resource} from '../../src/utils/api_paths'
    import TopNav from "@/components/TopNav";
    import {secureStoreGetString} from "../utils/util_functions";

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
                        this.flashMessage.show({
                            status: 'success',
                            title: response.data['message'], message: ""
                        });
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 409) {
                                this.flashMessage.show({
                                    status: 'error',
                                    title: "Error",
                                    message: error.response.data['message']
                                });
                            } else if (error.response.status === 401) {
                                this.flashMessage.show({
                                    status: 'error',
                                    title: "Session Expired",
                                    message: "You need to log in to perform this operation"
                                });
                            } else {
                                this.flashMessage.show({
                                    status: 'error',
                                    title: "Error",
                                    message: "Security Level already exists"
                                });
                            }
                        }
                    });
                this.clearForm();
            },

            updateSecurityLevel: function (code) {
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
                        this.flashMessage.show({
                            status: 'success',
                            title: response.data['message'], message: ""
                        });
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 304) {
                                this.flashMessage.show({
                                    status: 'info',
                                    title: "Info",
                                    message: "Record not modified"
                                });
                            } else if (error.response.status === 401) {
                                this.flashMessage.show({
                                    status: 'error',
                                    title: "Session Expired",
                                    message: "You need to log in to perform this operation"
                                });
                            } else {
                                this.flashMessage.show({
                                    status: 'error',
                                    title: "Error",
                                    message: error.response.data['message']
                                });
                            }
                        }
                    });
                this.clearForm();
            },

            deleteSecurityLevel: function (code) {
                axios.delete(security_level_resource, {
                    headers:
                        {
                            code: code,
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getSecurityLevel();
                        this.flashMessage.show({
                            status: 'success',
                            title: response.data['message'], message: ""
                        });
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 401) {
                                this.flashMessage.show({
                                    status: 'error',
                                    title: "Session Expired",
                                    message: "You need to log in to perform this operation"
                                });
                            } else {
                                this.flashMessage.show({
                                    status: 'error',
                                    title: error, message: ""
                                });
                            }
                        }
                    });
            },
        },
        created() {
            this.getSecurityLevel();
        },
        components: {TopNav}
    };
</script>
