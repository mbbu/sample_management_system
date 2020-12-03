<template>
  <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <top-nav :page_title="page_title" v-bind:search_query.sync="search"></top-nav>

                <FlashMessage :position="'right bottom'"></FlashMessage>
                <br>

                <!--TOP-PAGINATION-->
                <v-page :total-row="page_length" @page-change="pageInfo" align="center"
                        v-model="current"></v-page>
                <br>
                <table class=" table table-hover">
                    <thead>
                    <tr>
                      <th class="table-header-style" scope="col"> Id</th>
                      <th class="table-header-style" scope="col"> Site</th>
                      <th class="table-header-style" scope="col"> Area</th>
                      <th class="table-header-style" scope="col"> Code</th>
                      <th class="table-header-style" scope="col" v-if="isAuth"> Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr :key="study_block.id" v-for="(study_block, index) in filteredList">
                        <td> {{ index + 1 }}</td>
                        <td> {{ study_block.area }}</td>
                        <td> {{ study_block.name }}</td>
                        <td> {{ study_block.code }}</td>

                      <td v-if="isAuth">
                        <b-icon
                            :title="`Update ${ study_block.name }`"
                            @mouseover="fillFormForUpdate(study_block.area, study_block.name, study_block.code)"
                            class="border border-info rounded" :font-scale="`${font_scale}`"
                            icon="pencil" v-b-modal.modal-study_block-edit
                            v-b-tooltip.hover
                            variant="info"
                        ></b-icon>
                        &nbsp;
                        <b-icon
                                    :title="`Delete ${study_block.name}!`" @click="deleteStudyBlock(study_block.code)"
                                    class="border rounded bg-danger p-1" :font-scale="`${font_scale}`"
                                    icon="trash" v-b-tooltip.hover
                                    variant="light"
                            ></b-icon>
                        </td>
                    </tr>
                    </tbody>
                </table>
                <!--BOTTOM-PAGINATION-->
                <v-page :total-row="page_length" @page-change="pageInfo" align="center"
                        v-model="current"></v-page>
                <br>
            </div>

            <div v-if="!isEditing">
                <b-modal
                        @hidden="clearForm"
                        @ok="onSubmit"
                        @submit="showModal = false"
                        cancel-variant="danger"
                        id="modal-study_block"
                        ok-title="Save"
                        title="Add StudyBlock"
                >
                    <form @submit.prevent="createStudyBlock">

                        <!-- AREA -->
                        <b-form-group :class="{ 'form-group--error': $v.study_block.area.$error }"
                                      id="form-area-group" label="Area:" label-for="form-area-input">
                            <b-form-input
                                    id="form-area-input" placeholder="Enter Area"
                                    required type="text" v-model.trim="$v.study_block.area.$model"
                            ></b-form-input>
                            <div v-if="$v.study_block.area.$dirty">
                                <div class="error" v-if="!$v.study_block.area.required">Field is required</div>
                            </div>
                        </b-form-group>

                        <!-- NAME -->
                        <b-form-group :class="{ 'form-group--error': $v.study_block.name.$error }"
                                      id="form-name-group" label="Name:" label-for="form-name-input">
                            <b-form-input
                                    id="form-name-input"
                                    placeholder="Enter Name"
                                    required
                                    type="text"
                                    v-model.trim="$v.study_block.name.$model"
                            ></b-form-input>
                            <div v-if="$v.study_block.name.$dirty">
                                <div class="error" v-if="!$v.study_block.name.required">Field is
                                    required
                                </div>
                            </div>
                        </b-form-group>

                        <!-- CODE -->
                        <b-form-group :class="{ 'form-group--error': $v.study_block.code.$error }"
                                      id="form-code-group" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required
                                    type="text"
                                    v-model.trim="$v.study_block.code.$model"></b-form-input>
                            <div v-if="$v.study_block.code.$dirty">
                                <div class="error" v-if="!$v.study_block.code.required">Field is
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
                        @ok="updateStudyBlock"
                        @submit="showModal = false"
                        cancel-variant="danger"
                        id="modal-study_block-edit"
                        ok-title="Update"
                        title="Edit StudyBlock"
                >
                    <form @submit.prevent="updateStudyBlock">

                      <!-- AREA -->
                        <b-form-group :class="{ 'form-group--error': $v.study_block.area.$error }"
                                      id="form-area-group-edit" label="Name:" label-for="form-area-input">
                            <b-form-input
                                    id="form-area-input" placeholder="Enter Area"
                                    required type="text" v-model.trim="$v.study_block.area.$model"
                            ></b-form-input>
                            <div v-if="$v.study_block.area.$dirty">
                                <div class="error" v-if="!$v.study_block.area.required">Field is required</div>
                            </div>
                        </b-form-group>

                        <!-- NAME -->
                        <b-form-group :class="{ 'form-group--error': $v.study_block.name.$error }"
                                      id="form-name-group-edit" label="Name:" label-for="form-name-input">
                            <b-form-input
                                    id="form-name-input"
                                    placeholder="Enter Name"
                                    required
                                    type="text"
                                    v-model.trim="$v.study_block.name.$model"
                            ></b-form-input>
                            <div v-if="$v.study_block.name.$dirty">
                                <div class="error" v-if="!$v.study_block.name.required">Field is
                                    required
                                </div>
                            </div>
                        </b-form-group>

                        <!-- CODE -->
                        <b-form-group :class="{ 'form-group--error': $v.study_block.code.$error }"
                                      id="form-code-group-edit" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required
                                    type="text"
                                    v-model.trim="$v.study_block.code.$model"></b-form-input>
                            <div v-if="$v.study_block.code.$dirty">
                                <div class="error" v-if="!$v.study_block.code.required">Field is
                                    required
                                </div>
                            </div>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>
          <div v-if="isAuth">
            <b-button class="float_btn" style="border-radius: 50%" v-b-modal.modal-study_block variant="primary">
              <span>Add StudyBlock</span> <i class="fas fa-plus-circle menu_icon"></i>
            </b-button>
          </div>

          <div style="margin: auto;">
            <loading-progress :indeterminate="indeterminate" :hide-background="hideBackground" :progress="progressPath"
              :size="size" rotate fillDuration="2" rotationDuration="1"/>
          </div>
        </div>
    </div>
</template>

<script>
import {required} from "vuelidate/lib/validators";
import EventBus from "@/components/EventBus";
import {
  isAdmin,
  pageStartLoader,
  respondTo401,
  secureStoreGetAuthString,
  showFlashMessage
} from "@/utils/util_functions";
import {font_scale} from '@/utils/constants';
import axios from "axios";
import {study_block_resource} from "@/utils/api_paths";
import TopNav from "@/components/TopNav";

export default {
name: "StudyBlock",
  data() {
    return {
      page_title: "Study Blocks",
      response: [],
      search: '',
      study_blockList: [],

      study_block: { area: '', name: '', code: ''},

      font_scale,

      // variable to check user status and role
      isAuth: null,

      // loader-time
      time: 2000,

      // progressPath
      indeterminate: true, hideBackground: true, progressPath: 5, size: 180,

      // values for data modification
      old_code: null, showModal: true, isEditing: false,

      // data for pagination
      current: 1, page_length: null, page_array: [], page_info: {},
    };
  },

  validations: {study_block: {area: {required}, name: {required}, code: {required}}},

  mounted() {
      EventBus.$on('searchQuery', (payload) => {
          this.search = payload
          this.searchData()
      })
  },

  computed: {
      filteredList() {
          return this.study_blockList.filter(study_block => {
              return study_block.name.toLowerCase().includes(this.search.toLowerCase())
          })
      }
  },

  methods: {
    // util functions
      onSubmit(evt) {
          this.$v.$touch();
          if (this.$v.$invalid) {
              evt.preventDefault()
              return;
          }
          this.createStudyBlock();
      },

      clearForm() {
          this.study_block.area = null;
          this.study_block.name = null;
          this.study_block.code = null;
          this.isEditing = false;
          this.$v.$reset();
      },

      fillFormForUpdate(area, name, code) {
          this.study_block.area = area;
          this.study_block.name = name;
          this.study_block.name = name;
          this.study_block.code = code;
          this.old_code = code;
          this.isEditing = true;
          this.showModal = true;
      },

    // stop&hide progressPath
    haltProgressPath(cont=false, path=0, size=0){
      this.indeterminate = cont
      this.progressPath = path
      this.size = size
    },
    // pagination
    pageInfo(info) {
      this.page_info = info
    },

    paginate(data) {
      let start = 0, end = 0;

      start = this.page_info.pageSize * (this.page_info.pageNumber - 1)
      end = start + this.page_info.pageSize

      this.page_array.splice(0, this.page_array.length);

      if (end > data.length) end = data.length;

      for (let i = start; i < end; i++) {
          this.page_array.push(data[i])
      }

      this.page_length = data.length
      return this.page_array
    },

    // api interaction functions
    getStudyBlock() {
      this.isAuth = isAdmin()

      axios.get(study_block_resource)
          .then((res) => {
            setTimeout(()=> {
            this.haltProgressPath()
              this.study_blockList = this.response = res.data['message'];
            }, this.time)
          })
          .catch((error) => {
            // eslint-disable-next-line
            this.$log.error(error);
          });
    },

    createStudyBlock: function () {
        let self = this;
        let loader = pageStartLoader(this)

        axios.post(study_block_resource, {
            area: this.study_block.area,
            name: this.study_block.name,
            code: this.study_block.code,
        }, {
            headers: {
              Authorization: secureStoreGetAuthString()
            }
        })
            .then((response) => {
              setTimeout(()=> {
                loader.hide()
                this.getStudyBlock();
                this.clearForm();
                showFlashMessage(self, 'success', 'Success', response.data['message'])
              },this.time)
            })
            .catch((error) => {
                this.$log.error(error);
                loader.hide();
                if (error.response) {
                    if (error.response.status === 409) {
                        showFlashMessage(self, 'error', 'Error', error.response.data['message'])
                    } else if (error.response.status === 401) {
                        respondTo401(self);
                    } else if (error.response.status === 403) {
                        showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
                    } else {
                        showFlashMessage(self, 'error', 'Error', error.response.data['message'])
                    }
                }
            });
        this.clearForm();
    },

    updateStudyBlock: function (evt) {
        this.$v.$touch();
        if (this.$v.$invalid) {
            evt.preventDefault()
        } else {
            let self = this;
            let loader = pageStartLoader(this)
            axios.put(study_block_resource, {
                area: this.study_block.area,
                name: this.study_block.name,
                code: this.study_block.code,
            }, {
                headers:
                    {
                      code: this.old_code,
                      Authorization: secureStoreGetAuthString()
                    }
            })
                .then((response) => {
                  setTimeout( () => {
                    loader.hide()
                    this.getStudyBlock();
                    showFlashMessage(self, 'success', 'Success', response.data['message'])
                  }, this.time)
                })
                .catch((error) => {
                    this.$log.error(error);
                    loader.hide()
                    if (error.response) {
                        if (error.response.status === 304) {
                            showFlashMessage(self, 'info', 'Info', 'Record not modified!')
                        } else if (error.response.status === 401) {
                            respondTo401(self);
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

    deleteStudyBlock: function (code) {
        let self = this;
        let loader = pageStartLoader(this)

        axios.delete(study_block_resource, {
            headers: {
                code: code,
              Authorization: secureStoreGetAuthString()
            }
        })
            .then((response) => {
              setTimeout(() => {
                loader.hide()
                this.getStudyBlock();
                showFlashMessage(self, 'success', 'Success', response.data['message'])
              }, this.time)
            })
            .catch((error) => {
                this.$log.error(error);
                loader.hide()
                if (error.response) {
                    if (error.response.status === 401) {
                        respondTo401(self);
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
        return this.study_blockList.filter(study_block => {
            return study_block.name.toLowerCase().includes(this.search.toLowerCase())
        })
    }
  },
  created() { this.getStudyBlock();}, components: {TopNav}
}

</script>
