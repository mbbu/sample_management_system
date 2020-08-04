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
                        <th scope="col"> Room</th>
                        <th scope="col" v-if="isAuth"> Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr :key="lab.id" v-for="(lab, index) in filteredList.arr">
                        <td> {{ index + 1 }}</td>
                        <td> {{ lab.name }}</td>
                        <td> {{ lab.code }}</td>
                        <td> {{ lab.room }}</td>

                      <td v-if="isAuth">
                        <b-icon
                            :title="`Update ${ lab.name }`"
                            @mouseover="fillFormForUpdate(lab.name, lab.code, lab.room)"
                            class="border border-info rounded" font-scale="2.0"
                            icon="pencil" v-b-modal.modal-lab-edit
                            v-b-tooltip.hover
                            variant="info"
                        ></b-icon>
                        &nbsp;
                        <b-icon
                                    :title="`Delete ${lab.name}!`" @click="deleteLab(lab.code)"
                                    class="border rounded bg-danger p-1" font-scale="1.85"
                                    icon="trash" v-b-tooltip.hover
                                    variant="light"
                            ></b-icon>
                        </td>
                    </tr>
                    </tbody>
                </table>
                <!--TOP-PAGINATION-->
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
                        id="modal-lab"
                        ok-title="Save"
                        title="Add Lab"
                >
                    <form @submit.prevent="createLab">
                        <!-- NAME -->
                        <b-form-group :class="{ 'form-group--error': $v.lab.name.$error }"
                                      id="form-name-group" label="Name:" label-for="form-name-input">
                            <b-form-input
                                    id="form-name-input"
                                    placeholder="Enter Name"
                                    required
                                    type="text"
                                    v-model.trim="$v.lab.name.$model"
                            ></b-form-input>
                            <div v-if="$v.lab.name.$dirty">
                                <div class="error" v-if="!$v.lab.name.required">Field is
                                    required
                                </div>
                            </div>
                        </b-form-group>

                        <b-form-group :class="{ 'form-group--error': $v.lab.code.$error }"
                                      id="form-code-group" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required
                                    type="text"
                                    v-model.trim="$v.lab.code.$model"></b-form-input>
                            <div v-if="$v.lab.code.$dirty">
                                <div class="error" v-if="!$v.lab.code.required">Field is
                                    required
                                </div>
                            </div>
                        </b-form-group>

                        <b-form-group :class="{ 'form-group--error': $v.lab.room.$error }"
                                      id="form-room-group" label="Room:" label-for="form-room-input">
                            <b-form-input
                                    id="form-room-input"
                                    placeholder="Enter Room Number"
                                    required
                                    type="text"
                                    v-model.trim="$v.lab.room.$model"
                            ></b-form-input>
                            <div v-if="$v.lab.room.$dirty">
                                <div class="error" v-if="!$v.lab.room.required">Field is
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
                        @ok="updateLab"
                        @submit="showModal = false"
                        cancel-variant="danger"
                        id="modal-lab-edit"
                        ok-title="Update"
                        title="Edit Lab"
                >
                    <form @submit.prevent="updateLab">
                        <!-- NAME -->
                        <b-form-group :class="{ 'form-group--error': $v.lab.name.$error }"
                                      id="form-name-group-edit" label="Name:" label-for="form-name-input">
                            <b-form-input
                                    id="form-name-input"
                                    placeholder="Enter Name"
                                    required
                                    type="text"
                                    v-model.trim="$v.lab.name.$model"
                            ></b-form-input>
                            <div v-if="$v.lab.name.$dirty">
                                <div class="error" v-if="!$v.lab.name.required">Field is
                                    required
                                </div>
                            </div>
                        </b-form-group>

                        <!--CODE-->
                        <b-form-group :class="{ 'form-group--error': $v.lab.code.$error }"
                                      id="form-code-group-edit" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required
                                    type="text"
                                    v-model.trim="$v.lab.code.$model"></b-form-input>
                            <div v-if="$v.lab.code.$dirty">
                                <div class="error" v-if="!$v.lab.code.required">Field is
                                    required
                                </div>
                            </div>
                        </b-form-group>

                        <!--ROOM-->
                        <b-form-group :class="{ 'form-group--error': $v.lab.room.$error }"
                                      id="form-room-group-edit" label="Room:" label-for="form-room-input">
                            <b-form-input
                                    id="form-room-input"
                                    placeholder="Enter Room Number"
                                    required
                                    type="text"
                                    v-model.trim="$v.lab.room.$model"
                            ></b-form-input>
                            <div v-if="$v.lab.room.$dirty">
                                <div class="error" v-if="!$v.lab.room.required">Field is
                                    required
                                </div>
                            </div>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>
          <b-button class="float_btn" style="border-radius: 50%" v-b-modal.modal-lab v-if="isAuth" variant="primary">
            <span>Add Lab</span> <i class="fas fa-plus-circle menu_icon"></i>
          </b-button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import {lab_resource} from '@/utils/api_paths'
import TopNav from "../components/TopNav";
import {isThemeAdmin, paginate, respondTo401, secureStoreGetString, showFlashMessage} from "@/utils/util_functions";
import EventBus from '@/components/EventBus';
import {required} from "vuelidate/lib/validators";

export default {
  name: 'Lab',
  data() {
    return {
      page_title: "Labs",
      response: [],
      lab: {
        name: '',
        code: '',
        room: '',
      },

      // variable to check user status and role
      isAuth: null,

      search: '',
      labList: [],

      // values for data modification
      old_code: null,
      showModal: true,
      isEditing: false,

      // data for pagination
      current: 1,
    };
        },

        validations: {
            lab: {
                name: {required},
                code: {required},
                room: {required},
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
                    this.labList = searchList // eslint-disable-line
                    return paginate(searchList)
                }
                return paginate(this.labList)
            }
        },

        methods: {
            pageInfo(info) {
                EventBus.$emit('page-info', {'pgInfo': info, 'pgData': this.labList})
            },
            onSubmit(evt) {
                this.$v.$touch();
                if (this.$v.$invalid) {
                    // stop here if form is invalid
                    evt.preventDefault()
                    return;
                }
                this.createLab();
            },
            clearForm() {
                this.lab.name = null;
                this.lab.code = null;
                this.lab.room = null;
                this.isEditing = false;
                this.$v.$reset();
            },

            fillFormForUpdate(name, code, room) {
                this.lab.name = name;
                this.lab.code = code;
                this.lab.room = room;
                this.old_code = code;
                this.isEditing = true;
                this.showModal = true;
            },

            getLab() {
              this.isAuth = isThemeAdmin()

              axios.get(lab_resource)
                  .then((res) => {
                    this.$log.info("Response: " + res.status + " " + res.data['message']);
                    this.labList = this.response = res.data['message'];
                  })
                  .catch((error) => {
                    // eslint-disable-next-line
                    this.$log.error(error);
                  });
            },

            createLab: function () {
                let self = this;
                axios.post(lab_resource, {
                    name: this.lab.name,
                    code: this.lab.code,
                    room: this.lab.room,
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

            updateLab: function (evt) {
                this.$v.$touch();
                if (this.$v.$invalid) {
                    evt.preventDefault()
                } else {
                    let self = this;
                    axios.put(lab_resource, {
                        name: this.lab.name,
                        code: this.lab.code,
                        room: this.lab.room,
                    }, {
                        headers:
                            {
                                code: this.old_code,
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
                }
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
                this.clearForm();
            },

            searchData() {
                return this.response.filter(lab => {
                    for (let count = 0; count <= this.response.length; count++) {
                        let byName = lab.name.toString().toLowerCase().includes(this.search.toLowerCase())
                        let byCode = lab.code.toString().toLowerCase().includes(this.search.toLowerCase())
                        let byRoom = lab.room.toString().toLowerCase().includes(this.search.toLowerCase())

                        if (byName) {
                            return byName
                        } else if (byCode) {
                            return byCode
                        } else if (byRoom) {
                            return byRoom
                        }
                    }
                })
            }
        },
        created() {
            this.getLab();
        },
        components: {TopNav}
    };
</script>
