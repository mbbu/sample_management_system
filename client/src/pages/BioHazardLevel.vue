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
                      <th class="table-header-style" scope="col"> Id</th>
                      <th class="table-header-style" scope="col"> Name</th>
                      <th class="table-header-style" scope="col"> Code</th>
                      <th class="table-header-style" scope="col"> Description</th>
                      <th class="table-header-style" scope="col" v-if="isAuth"> Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr :key="bio_hazard.id" v-for="(bio_hazard, index) in filteredList.arr">
                        <td> {{ index + 1 }}</td>
                        <td> {{ bio_hazard.name }}</td>
                        <td> {{ bio_hazard.code }}</td>
                        <td> {{ bio_hazard.description }}</td>

                      <td v-if="isAuth">
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
                        id="modal-bio-level"
                        ok-title="Save"
                        title="Add Bio Hazard Level"
                >
                    <form @submit.prevent="createBioHazardLevel">


                        <!-- NAME -->
                        <b-form-group :class="{ 'form-group--error': $v.level.name.$error }"
                                      id="form-name-group" label="Name:" label-for="form-name-input">
                            <b-form-input
                                    id="form-name-input"
                                    placeholder="Enter Name"
                                    required
                                    type="text"
                                    v-model.trim="$v.level.name.$model"
                            ></b-form-input>
                            <div v-if="$v.level.name.$dirty">
                                <div class="error" v-if="!$v.level.name.required">Field is
                                    required
                                </div>
                            </div>
                        </b-form-group>

                        <!--CODE-->
                        <b-form-group :class="{ 'form-group--error': $v.level.code.$error }"
                                      id="form-code-group" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required
                                    type="text"
                                    v-model.trim="$v.level.code.$model"></b-form-input>
                            <div v-if="$v.level.code.$dirty">
                                <div class="error" v-if="!$v.level.code.required">Field is
                                    required
                                </div>
                            </div>
                        </b-form-group>

                        <!--DESCRIPTION-->
                        <b-form-group :class="{ 'form-group--error': $v.level.desc.$error }"
                                      id="form-desc-group" label="Description:" label-for="form-desc-input">
                            <b-form-textarea
                                    id="form-desc-input"
                                    placeholder="Enter Description"
                                    required
                                    type="text"
                                    v-model.trim="$v.level.desc.$model"
                            ></b-form-textarea>
                            <div v-if="$v.level.desc.$dirty">
                                <div class="error" v-if="!$v.level.desc.required">Field is
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
                        @ok="updateBioHazardLevel"
                        @submit="showModal = false"
                        cancel-variant="danger"
                        id="modal-bio-level-edit"
                        ok-title="Update"
                        title="Edit Bio Hazard Level"
                >
                    <form>

                        <b-form-group :class="{ 'form-group--error': $v.level.name.$error }"
                                      id="form-name-group-edit" label="Name:" label-for="form-name-input">
                            <b-form-input
                                    id="form-name-input"
                                    placeholder="Enter Name"
                                    required
                                    type="text"
                                    v-model.trim="$v.level.name.$model"
                            ></b-form-input>
                            <div v-if="$v.level.name.$dirty">
                                <div class="error" v-if="!$v.level.name.required">Field is
                                    required
                                </div>
                            </div>
                        </b-form-group>

                        <!--CODE-->
                        <b-form-group :class="{ 'form-group--error': $v.level.code.$error }"
                                      id="form-code-group-edit" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required
                                    type="text"
                                    v-model.trim="$v.level.code.$model"></b-form-input>
                            <div v-if="$v.level.code.$dirty">
                                <div class="error" v-if="!$v.level.code.required">Field is
                                    required
                                </div>
                            </div>
                        </b-form-group>

                        <!--DESCRIPTION-->
                        <b-form-group :class="{ 'form-group--error': $v.level.desc.$error }"
                                      id="form-desc-group-edit" label="Description:" label-for="form-desc-input">
                            <b-form-textarea
                                    id="form-desc-input"
                                    placeholder="Enter Description"
                                    required
                                    type="text"
                                    v-model.trim="$v.level.desc.$model"
                            ></b-form-textarea>
                            <div v-if="$v.level.desc.$dirty">
                                <div class="error" v-if="!$v.level.desc.required">Field is
                                    required
                                </div>
                            </div>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>
          <b-button class="float_btn" style="border-radius: 50%" v-b-modal.modal-bio-level v-if="isAuth"
                    variant="primary">
            <span>Add Bio Hazard Level</span> <i class="fas fa-plus-circle menu_icon"></i>
          </b-button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import TopNav from "../components/TopNav";
import EventBus from '../components/EventBus';
import {bio_hazard_level_resource} from '@/utils/api_paths'
import {isThemeAdmin, paginate, respondTo401, secureStoreGetAuthString, showFlashMessage} from "@/utils/util_functions";
import {required} from "vuelidate/lib/validators";

export default {
  name: 'BioHazardLevel',
  data() {
    return {
      page_title: "Bio Hazard Level",
      response: [],
      bioHazardList: [],
      search: '',
      level: {
        name: '',
        code: '',
        desc: '',
      },

      // variable to check user status and role
      isAuth: null,

      // values for data modification
      old_code: null,
      showModal: true,
      isEditing: false,

      // data for pagination
      current: 1,
    };
        },

        validations: {
            level: {
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
                return paginate(this.bioHazardList.filter(bioHazard => {
                    return bioHazard.name.toLowerCase().includes(this.search.toLowerCase())
                }))
            }
        },

        methods: {

            pageInfo(info) {
                EventBus.$emit('page-info', {'pgInfo': info, 'pgData': this.bioHazardList})
            },

            onSubmit(evt) {
                this.$v.$touch();
                if (this.$v.$invalid) {
                    // stop here if form is invalid
                    evt.preventDefault()
                    return;
                }
                this.createBioHazardLevel();
            },

            clearForm() {
                this.level.name = null;
                this.level.code = null;
                this.level.desc = null;
                this.isEditing = false;
                this.$v.$reset();
            },

            fillFormForUpdate(name, code, desc) {
                this.level.name = name;
                this.level.code = code;
                this.level.desc = desc;
                this.old_code = code;
                this.isEditing = true;
                this.showModal = true;
            },

            getBioHazardLevel() {
              this.isAuth = isThemeAdmin()
              axios.get(bio_hazard_level_resource)
                  .then((res) => {
                    this.$log.info("Response: " + res.status + " " + res.data['message']);
                    this.response = res.data;
                    this.bioHazardList = this.response.message
                  })
                  .catch((error) => {
                    // eslint-disable-next-line
                    this.$log.error(error);
                  });
            },

            createBioHazardLevel: function () {
                let self = this;
                axios.post(bio_hazard_level_resource, {
                    name: this.level.name,
                    code: this.level.code,
                    description: this.level.desc,
                }, {
                    headers: {
                      Authorization: secureStoreGetAuthString()
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

            updateBioHazardLevel: function (evt) {
                this.$v.$touch();
                if (this.$v.$invalid) {
                    evt.preventDefault()
                } else {
                    let self = this;

                    axios.put(bio_hazard_level_resource, {
                        name: this.level.name,
                        code: this.level.code,
                        description: this.level.desc,
                    }, {
                        headers:
                            {
                                code: this.old_code,
                              Authorization: secureStoreGetAuthString()
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
                }
            },

            deleteBioHazardLevel: function (code) {
                let self = this;

                axios.delete(bio_hazard_level_resource, {
                    headers:
                        {
                            code: code,
                          Authorization: secureStoreGetAuthString()
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
                this.clearForm();
            },

            searchData() {
                return this.bioHazardList.filter(bioHazard => {
                    return bioHazard.name.toLowerCase().includes(this.search.toLowerCase())
                })
            }
        },
        created() {
            this.getBioHazardLevel();
        },
        components: {TopNav}
    };
</script>
