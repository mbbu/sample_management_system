<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <top-nav :page_title="page_title" v-bind:search_query.sync="search"></top-nav>

                <!-- FLASH MESSAGES -->
                <FlashMessage :position="'right bottom'"></FlashMessage>
                <br> <br>

                <!--TOP-PAGINATION-->
                <v-page :total-row="filteredList.pg_len" @page-change="pageInfo" align="center"
                        v-model="current"></v-page>
                <br>
                <table class=" table table-hover">
                    <thead>
                    <tr>
                        <th scope="col"> Id</th>
                        <th scope="col"> Name</th>
                        <th scope="col"> Code</th>
                        <th scope="col"> Description</th>
                        <th scope="col" v-if="isAuth"> Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr :key="qt.id" v-for="(qt, index) in filteredList.arr">
                      <td> {{ index + 1 }}</td>
                      <td> {{ qt.name }}</td>
                      <td> {{ qt.id }}</td>
                      <td> {{ qt.description }}</td>

                      <td v-if="isAuth">
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
                <!--BOTTOM-PAGINATION-->
                <v-page :total-row="filteredList.pg_len" @page-change="pageInfo" align="center"
                        v-model="current"></v-page>
                <br>
            </div>

            <div v-if="!isEditing">
                <b-modal
                        @hidden="clearForm"
                        @ok="onSubmit"
                        @submit="showModal = false"
                        cancel-variant="danger"
                        id="modal-quantity-type"
                        ok-title="Save"
                        title="Add Quantity Type"
                >
                    <form @submit.prevent="createQuantityType">

                        <!-- NAME -->
                        <b-form-group :class="{ 'form-group--error': $v.qt.name.$error }"
                                      id="form-name-group" label="Name:" label-for="form-name-input">
                            <b-form-input
                                    id="form-name-input"
                                    placeholder="Enter Name"
                                    required
                                    type="text"
                                    v-model.trim="$v.qt.name.$model"
                            ></b-form-input>
                            <div v-if="$v.qt.name.$dirty">
                                <div class="error" v-if="!$v.qt.name.required">Field is
                                    required
                                </div>
                            </div>
                        </b-form-group>

                        <!--CODE-->
                        <b-form-group :class="{ 'form-group--error': $v.qt.code.$error }"
                                      id="form-code-group" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required
                                    type="text"
                                    v-model.trim="$v.qt.code.$model"></b-form-input>
                            <div v-if="$v.qt.code.$dirty">
                                <div class="error" v-if="!$v.qt.code.required">Field is
                                    required
                                </div>
                            </div>
                        </b-form-group>

                        <!--DESC-->
                        <b-form-group :class="{ 'form-group--error': $v.qt.desc.$error }"
                                      id="form-desc-group" label="Description:" label-for="form-desc-input">
                            <b-form-textarea
                                    id="form-desc-input"
                                    placeholder="Enter Description"
                                    required
                                    type="text"
                                    v-model.trim="$v.qt.desc.$model"
                            ></b-form-textarea>
                            <div v-if="$v.qt.desc.$dirty">
                                <div class="error" v-if="!$v.qt.desc.required">Field is
                                    required
                                </div>
                            </div>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>

            <div v-else-if="isEditing">
                <b-modal
                        @hidden="clearForm"
                        @ok="updateQuantityType"
                        @submit="showModal = false"
                        cancel-variant="danger"
                        id="modal-quantity-type-edit"
                        ok-title="Update"
                        title="Edit Quantity Type"
                >
                    <form>

                        <!-- NAME -->
                        <b-form-group :class="{ 'form-group--error': $v.qt.name.$error }"
                                      id="form-name-group-edit" label="Name:" label-for="form-name-input">
                            <b-form-input
                                    id="form-name-input"
                                    placeholder="Enter Name"
                                    required
                                    type="text"
                                    v-model.trim="$v.qt.name.$model"
                            ></b-form-input>
                            <div v-if="$v.qt.name.$dirty">
                                <div class="error" v-if="!$v.qt.name.required">Field is
                                    required
                                </div>
                            </div>
                        </b-form-group>

                        <!--CODE-->
                        <b-form-group :class="{ 'form-group--error': $v.qt.code.$error }"
                                      id="form-code-group-edit" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required
                                    type="text"
                                    v-model.trim="$v.qt.code.$model"></b-form-input>
                            <div v-if="$v.qt.code.$dirty">
                                <div class="error" v-if="!$v.qt.code.required">Field is
                                    required
                                </div>
                            </div>
                        </b-form-group>

                        <!--DESC-->
                        <b-form-group :class="{ 'form-group--error': $v.qt.desc.$error }"
                                      id="form-desc-group-edit" label="Description:" label-for="form-desc-input">
                            <b-form-textarea
                                    id="form-desc-input"
                                    placeholder="Enter Description"
                                    required
                                    type="text"
                                    v-model.trim="$v.qt.desc.$model"
                            ></b-form-textarea>
                          <div v-if="$v.qt.desc.$dirty">
                            <div class="error" v-if="!$v.qt.desc.required">Field is
                              required
                            </div>
                          </div>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>
          <b-button class="float_btn" style="border-radius: 50%" v-b-modal.modal-quantity-type v-if="isAuth"
                    variant="primary">
            <span>Add Quantity Type</span> <i class="fas fa-plus-circle menu_icon"></i>
          </b-button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import {quantity_type_resource} from '@/utils/api_paths'
import TopNav from "../components/TopNav";
import {isThemeAdmin, paginate, respondTo401, secureStoreGetString, showFlashMessage} from "@/utils/util_functions";
import EventBus from '../components/EventBus';
import {required} from "vuelidate/lib/validators";

export default {
  name: 'QuantityType',
  data() {
    return {
      page_title: "Quantity Type",
      response: [],
      qt: {
        name: '',
        code: '',
        desc: '',
      },

      // variable to check user status and role
      isAuth: null,

      search: '',
      QTList: [],

      // values for data modification
      old_code: null,
      showModal: true,
      isEditing: false,

      // data for pagination
      current: 1,
    };
  },

        validations: {
            qt: {
                name: {required},
                code: {required},
                desc: {required},
            }
        },

        mounted() {
            EventBus.$on('searchQuery', (payload) => {
                this.search = payload
                this.searchData()
            })
        },

        computed: {
            filteredList() {
                let searchList = this.search ? this.searchData() : null

                if (searchList !== null) {
                    this.QTList = searchList // eslint-disable-line
                    return paginate(searchList)
                }
                return paginate(this.QTList)
            }
        },

        methods: {
            pageInfo(info) {
                EventBus.$emit('page-info', {'pgInfo': info, 'pgData': this.QTList})
            },

            onSubmit(evt) {
                this.$v.$touch();
                if (this.$v.$invalid) {
                    // stop here if form is invalid
                    evt.preventDefault()
                    return;
                }
                this.createQuantityType();
            },
            clearForm() {
                this.qt.name = null;
                this.qt.code = null;
                this.qt.desc = null;
                this.isEditing = false;
                this.$v.$reset();
            },

            fillFormForUpdate(name, code, desc) {
                this.qt.name = name;
                this.qt.code = code;
                this.qt.desc = desc;
                this.old_code = code;
                this.isEditing = true;
                this.showModal = true;
            },

            getQuantityType() {
              this.isAuth = isThemeAdmin()

              axios.get(quantity_type_resource)
                  .then((res) => {
                    this.$log.info("Response: " + res.status + " " + res.data['message']);
                    this.QTList = this.response = res.data['message'];
                  })
                  .catch((error) => {
                    // eslint-disable-next-line
                    this.$log.error(error);
                  });
            },

            createQuantityType: function () {
                let self = this;
                axios.post(quantity_type_resource, {
                    name: this.qt.name,
                    code: this.qt.code,
                    description: this.qt.desc,
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

            updateQuantityType: function (evt) {
                this.$v.$touch();
                if (this.$v.$invalid) {
                    evt.preventDefault()
                } else {
                    let self = this;
                    axios.put(quantity_type_resource, {
                        name: this.qt.name,
                        code: this.qt.code,
                        description: this.qt.desc,
                    }, {
                        headers:
                            {
                                code: this.old_code,
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
                }
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

            searchData() {
                return this.response.filter(qt => {
                    for (let count = 0; count <= this.response.length; count++) {
                        let byName = qt.name.toString().toLowerCase().includes(this.search.toLowerCase())
                        let byCode = qt.id.toString().toLowerCase().includes(this.search.toLowerCase())
                        let byDesc = qt.description.toString().toLowerCase().includes(this.search.toLowerCase())

                        if (byName === true) {
                            return byName
                        } else if (byCode) {
                            return byCode
                        } else if (byDesc) {
                            return byDesc
                        }
                    }
                })
            }
        },
        created() {
            this.getQuantityType();
        },
        components: {TopNav}
    };
</script>
