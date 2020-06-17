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
                    <tr :key="bio_hazard.id" v-for="(bio_hazard, index) in response.message">
                        <td> {{ index + 1 }}</td>
                        <td> {{ bio_hazard.name }}</td>
                        <td> {{ bio_hazard.code }}</td>
                        <td> {{ bio_hazard.description }}</td>

                        <td>
                            <b-icon
                                    :title="`Update ${ bio_hazard.name }`"
                                    @mouseover="fillFormForUpdate(bio_hazard.name, bio_hazard.code, bio_hazard.description)"
                                    class="border border-info rounded" font-scale="2.0"
                                    icon="pencil" v-b-modal.modal-bio-level-edit
                                    v-b-tooltip.hover
                                    variant="info"
                            ></b-icon>
                            &nbsp;
                            <b-icon
                                    :title="`Delete ${bio_hazard.name}!`" @click="deleteBioHazardLevel(bio_hazard.code)"
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
                        @ok="createBioHazardLevel"
                        @submit="showModal = false"
                        cancel-variant="danger"
                        id="modal-bio-level"
                        ok-title="Save"
                        title="Add Bio Hazard Level"
                >
                    <form @submit.prevent="createBioHazardLevel">

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
                        @ok="updateBioHazardLevel(old_code)"
                        @submit="showModal = false"
                        cancel-variant="danger"
                        id="modal-bio-level-edit"
                        ok-title="Update"
                        title="Edit Bio Hazard Level"
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
                      v-b-modal.modal-bio-level variant="primary"
            >Add Bio Hazard Level
            </b-button>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import {bio_hazard_level_resource} from '../utils/api_paths'
    import TopNav from "../components/TopNav";
    import {respondTo401, secureStoreGetString, showFlashMessage} from "../utils/util_functions";

    export default {
        name: 'BioHazardLevel',
        data() {
            return {
                page_title: "Bio Hazard Level",
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

            getBioHazardLevel() {
                axios.get(bio_hazard_level_resource)
                    .then((res) => {
                        this.$log.info("Response: " + res.status + " " + res.data['message']);
                        this.response = res.data;
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        this.$log.error(error);
                    });
            },

            createBioHazardLevel: function () {
                let self = this;
                axios.post(bio_hazard_level_resource, {
                    name: this.name,
                    code: this.code,
                    description: this.desc,
                }, {
                    headers: {
                        Authorization: secureStoreGetString()
                    }
                })
                    .then((response) => {
                        this.getBioHazardLevel();
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
                                showFlashMessage(self, 'error', "Error", error.response.data['message'])
                            }
                        }
                    });
                this.clearForm();
            },

            updateBioHazardLevel: function (code) {
                let self = this;

                axios.put(bio_hazard_level_resource, {
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
                        this.getBioHazardLevel();
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

            deleteBioHazardLevel: function (code) {
                let self = this;

                axios.delete(bio_hazard_level_resource, {
                    headers:
                        {
                            code: code,
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getBioHazardLevel();
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
            this.getBioHazardLevel();
        },
        components: {TopNav}
    };
</script>
