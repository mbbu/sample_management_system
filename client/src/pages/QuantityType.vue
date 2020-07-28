<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <top-nav :page_title="page_title" v-bind:search_query.sync="search"></top-nav>

                <!-- FLASH MESSAGES -->
                <FlashMessage :position="'right bottom'"></FlashMessage>
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
                    <tr :key="qt.id" v-for="(qt, index) in filteredList">
                        <td> {{ index + 1 }}</td>
                        <td> {{ qt.name }}</td>
                        <td> {{ qt.id }}</td>
                        <td> {{ qt.description }}</td>

                        <td>
                            <b-icon
                                    :title="`Update ${ qt.name }`"
                                    @mouseover="fillFormForUpdate(qt.name, qt.id, qt.description)"
                                    class="border border-info rounded" font-scale="2.0"
                                    icon="pencil" v-b-modal.modal-quantity-type-edit
                                    v-b-tooltip.hover
                                    variant="info"
                            ></b-icon>
                            &nbsp;
                            <b-icon
                                    :title="`Delete ${qt.name}!`" @click="deleteQuantityType(qt.id)"
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
                        @ok="createQuantityType"
                        @submit="showModal = false"
                        cancel-variant="danger"
                        id="modal-quantity-type"
                        ok-title="Save"
                        title="Add Quantity Type"
                >
                    <form @submit.prevent="createQuantityType">

                        <b-form-group id="form-name-group" label="Name:" label-for="form-name-input">
                            <b-form-input
                                    id="form-name-input"
                                    placeholder="Enter Name"
                                    required
                                    type="text"
                                    v-model="name"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-code-group" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required
                                    type="text"
                                    v-model="code"></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-desc-group" label="Description:" label-for="form-desc-input">
                            <b-form-textarea
                                    id="form-desc-input"
                                    placeholder="Enter Description"
                                    required
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
                        @ok="updateQuantityType(old_code)"
                        @submit="showModal = false"
                        cancel-variant="danger"
                        id="modal-quantity-type-edit"
                        ok-title="Update"
                        title="Edit Quantity Type"
                >
                    <form>

                        <b-form-group id="form-name-group-edit" label="Name:" label-for="form-name-input">
                            <b-form-input
                                    id="form-name-input"
                                    placeholder="Enter Name"
                                    required
                                    type="text"
                                    v-model="name"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-code-group-edit" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required
                                    type="text"
                                    v-model="code"></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-desc-group-edit" label="Description:" label-for="form-desc-input">
                            <b-form-textarea
                                    id="form-desc-input"
                                    placeholder="Enter Description"
                                    required
                                    type="text"
                                    v-model="desc"
                            ></b-form-textarea>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>
            <b-button class="float_btn" style="border-radius: 50%" v-b-modal.modal-quantity-type variant="primary">
                <span>Add Quantity Type</span> <i class="fas fa-plus-circle menu_icon"></i>
            </b-button>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import {quantity_type_resource} from '../utils/api_paths'
    import TopNav from "../components/TopNav";
    import {respondTo401, secureStoreGetString, showFlashMessage} from "../utils/util_functions";
    import EventBus from '../components/EventBus';

    export default {
        name: 'QuantityType',
        data() {
            return {
                page_title: "Quantity Type",
                response: [],
                name: null,
                code: null,
                desc: null,
                search: '',
                QTList: [],

                // values for data modification
                old_code: null,
                showModal: true,
                isEditing: false,
            };
        },

        mounted() {
            EventBus.$on('searchQuery', (payload) => {
                this.search = payload
                this.filteredList()
            })
        },

        computed: {
            filteredList() {
                return this.QTList.filter(qt => {
                    return qt.name.toLowerCase().includes(this.search.toLowerCase())
                })
            }
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

            getQuantityType() {
                axios.get(quantity_type_resource)
                    .then((res) => {
                        this.$log.info("Response: " + res.status + " " + res.data['message']);
                        this.response = res.data;
                        this.QTList = this.response.message
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        this.$log.error(error);
                    });
            },

            createQuantityType: function () {
                let self = this;
                axios.post(quantity_type_resource, {
                    name: this.name,
                    code: this.code,
                    description: this.desc,
                }, {
                    headers: {
                        Authorization: secureStoreGetString()
                    }
                })
                    .then((response) => {
                        this.getQuantityType();
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

            updateQuantityType: function (code) {
                let self = this;
                axios.put(quantity_type_resource, {
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
                        this.getQuantityType();
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

            deleteQuantityType: function (code) {
                let self = this;
                axios.delete(quantity_type_resource, {
                    headers:
                        {
                            code: code,
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getQuantityType();
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
                this.clearForm();
            },
        },
        created() {
            this.getQuantityType();
        },
        components: {TopNav}
    };
</script>
