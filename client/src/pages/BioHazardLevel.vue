<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-sm-12">
        <top-nav :page_title="page_title" v-bind:search_query.sync="search"></top-nav>

        <!-- FLASH MESSAGES -->
        <FlashMessage :position="'right bottom'"></FlashMessage>
        <br> <br>
        <!--TOP-PAGINATION-->
        <v-page v-model="current" :total-row="filteredList.pg_len" align="center"
                @page-change="pageInfo"></v-page>
        <br>
        <table class=" table table-hover">
          <thead>
          <tr>
            <th class="table-header-style" scope="col"> Id</th>
            <th class="table-header-style" scope="col"> Name</th>
            <th class="table-header-style" scope="col"> Code</th>
            <th class="table-header-style" scope="col"> Description</th>
            <th v-if="isAuth" class="table-header-style" scope="col"> Actions</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(bio_hazard, index) in filteredList.arr" :key="bio_hazard.id">
            <td> {{ index + 1 }}</td>
            <td> {{ bio_hazard.name }}</td>
            <td> {{ bio_hazard.code }}</td>
            <td> {{ bio_hazard.description }}</td>

            <td v-if="isAuth">
              <b-icon
                  v-b-modal.modal-bio-level-edit
                  v-b-tooltip.hover
                  :font-scale="`${font_scale}`" :title="`Update ${ bio_hazard.name }`"
                  class="border border-info rounded" icon="pencil"
                  variant="info"
                  @mouseover="fillFormForUpdate(bio_hazard.name, bio_hazard.code, bio_hazard.description)"
              ></b-icon>
              &nbsp;
              <b-icon
                  v-b-tooltip.hover :font-scale="`${font_scale}`"
                  :title="`Delete ${bio_hazard.name}!`" class="border rounded bg-danger p-1"
                  icon="trash" variant="light"
                  @click="deleteBioHazardLevel(bio_hazard.code)"
              ></b-icon>
            </td>
          </tr>
          </tbody>
        </table>
        <!--BOTTOM-PAGINATION-->
        <v-page v-model="current" :total-row="filteredList.pg_len" align="center"
                @page-change="pageInfo"></v-page>
        <br>
      </div>

      <div v-if="!isEditing">
        <b-modal
            id="modal-bio-level"
            cancel-variant="danger"
            ok-title="Save"
            title="Add Bio Hazard Level"
            @hidden="clearForm"
            @ok="onSubmit"
            @submit="showModal = false"
        >
          <form @submit.prevent="createBioHazardLevel">


            <!-- NAME -->
            <b-form-group id="form-name-group"
                          :class="{ 'form-group--error': $v.level.name.$error }" label="Name:" label-for="form-name-input">
              <b-form-input
                  id="form-name-input"
                  v-model.trim="$v.level.name.$model"
                  placeholder="Enter Name"
                  required
                  type="text"
              ></b-form-input>
              <div v-if="$v.level.name.$dirty">
                <div v-if="!$v.level.name.required" class="error">Field is
                  required
                </div>
              </div>
            </b-form-group>

            <!--CODE-->
            <b-form-group id="form-code-group"
                          :class="{ 'form-group--error': $v.level.code.$error }" label="Code:" label-for="form-code-input">
              <b-form-input
                  id="form-code-input"
                  v-model.trim="$v.level.code.$model"
                  placeholder="Enter Code"
                  required
                  type="text"></b-form-input>
              <div v-if="$v.level.code.$dirty">
                <div v-if="!$v.level.code.required" class="error">Field is
                  required
                </div>
              </div>
            </b-form-group>

            <!--DESCRIPTION-->
            <b-form-group id="form-desc-group"
                          :class="{ 'form-group--error': $v.level.desc.$error }" label="Description:" label-for="form-desc-input">
              <b-form-textarea
                  id="form-desc-input"
                  v-model.trim="$v.level.desc.$model"
                  placeholder="Enter Description"
                  required
                  type="text"
              ></b-form-textarea>
              <div v-if="$v.level.desc.$dirty">
                <div v-if="!$v.level.desc.required" class="error">Field is
                  required
                </div>
              </div>
            </b-form-group>
          </form>
        </b-modal>
      </div>

      <div v-else-if="isEditing">
        <b-modal
            id="modal-bio-level-edit"
            cancel-variant="danger"
            ok-title="Update"
            title="Edit Bio Hazard Level"
            @hidden="clearForm"
            @ok="updateBioHazardLevel"
            @submit="showModal = false"
        >
          <form>

            <b-form-group id="form-name-group-edit"
                          :class="{ 'form-group--error': $v.level.name.$error }" label="Name:" label-for="form-name-input">
              <b-form-input
                  id="form-name-input"
                  v-model.trim="$v.level.name.$model"
                  placeholder="Enter Name"
                  required
                  type="text"
              ></b-form-input>
              <div v-if="$v.level.name.$dirty">
                <div v-if="!$v.level.name.required" class="error">Field is
                  required
                </div>
              </div>
            </b-form-group>

            <!--CODE-->
            <b-form-group id="form-code-group-edit"
                          :class="{ 'form-group--error': $v.level.code.$error }" label="Code:" label-for="form-code-input">
              <b-form-input
                  id="form-code-input"
                  v-model.trim="$v.level.code.$model"
                  placeholder="Enter Code"
                  required
                  type="text"></b-form-input>
              <div v-if="$v.level.code.$dirty">
                <div v-if="!$v.level.code.required" class="error">Field is
                  required
                </div>
              </div>
            </b-form-group>

            <!--DESCRIPTION-->
            <b-form-group id="form-desc-group-edit"
                          :class="{ 'form-group--error': $v.level.desc.$error }" label="Description:" label-for="form-desc-input">
              <b-form-textarea
                  id="form-desc-input"
                  v-model.trim="$v.level.desc.$model"
                  placeholder="Enter Description"
                  required
                  type="text"
              ></b-form-textarea>
              <div v-if="$v.level.desc.$dirty">
                <div v-if="!$v.level.desc.required" class="error">Field is
                  required
                </div>
              </div>
            </b-form-group>
          </form>
        </b-modal>
      </div>
      <b-button v-if="isAuth" v-b-modal.modal-bio-level class="float_btn" style="border-radius: 50%"
                variant="primary">
        <span>Add Bio Hazard Level</span> <i class="fas fa-plus-circle menu_icon"></i>
      </b-button>
      <div style="margin: auto;">
        <loading-progress :hide-background="hideBackground" :indeterminate="indeterminate" :progress="progressPath"
            :size="size" fillDuration="2" rotate rotationDuration="1"/>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import TopNav from "../components/TopNav";
import EventBus from '../components/EventBus';
import {bio_hazard_level_resource} from '@/utils/api_paths'
import {
  handleError, isThemeAdmin,
  pageStartLoader, paginate,
  secureStoreGetAuthString, showFlashMessage
} from "@/utils/util_functions";
import {font_scale} from '@/utils/constants';
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

      font_scale: font_scale,

      // variable to check user status and role
      isAuth: null,

      // loader-time
      time: 2000,

      // progressPath
      indeterminate: true,
      hideBackground: true,
      progressPath: 5,
      size: 180,

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

    // stop&hide progressPath
    haltProgressPath(cont = false, path = 0, size = 0) {
      this.indeterminate = cont
      this.progressPath = path
      this.size = size
    },

    getBioHazardLevel() {
      this.isAuth = isThemeAdmin()
      axios.get(bio_hazard_level_resource)
          .then((res) => {
            setTimeout(() => {
              this.haltProgressPath()
              this.$log.info("Response: " + res.status + " " + res.data['message']);
              this.response = res.data;
              this.bioHazardList = this.response.message
            }, this.time)
          }).catch((error) => {
        // eslint-disable-next-line
        this.$log.error(error);
      });
    },

    createBioHazardLevel: function () {
      let loader = pageStartLoader(this);

      axios.post(bio_hazard_level_resource, {
        name: this.level.name,
        code: this.level.code,
        description: this.level.desc,
      }, {
        headers: {
          Authorization: secureStoreGetAuthString()
        }
      }).then((response) => {
        setTimeout(() => {
          loader.hide()
          this.getBioHazardLevel();
          this.clearForm();
          showFlashMessage(this, 'success', response.data['message'], "")
        }, this.time)
      }).catch((error) => {
        handleError(this, error, loader)
      });
      this.clearForm();
    },

    updateBioHazardLevel: function (evt) {
      this.$v.$touch();
      if (this.$v.$invalid) {
        evt.preventDefault()
      } else {
        let loader = pageStartLoader(this)
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
              setTimeout(() => {
                loader.hide()
                this.getBioHazardLevel();
                showFlashMessage(this, 'success', response.data['message'], "")
              }, this.time)
            }).catch((error) => {
          handleError(this, error, loader)
        });
        this.clearForm();
      }
    },

    deleteBioHazardLevel: function (code) {
      let loader = pageStartLoader(this)

      axios.delete(bio_hazard_level_resource, {
        headers:
            {
              code: code,
              Authorization: secureStoreGetAuthString()
            }
      }).then((response) => {
            setTimeout(() => {
              loader.hide()
              this.getBioHazardLevel();
              showFlashMessage(this, 'success', response.data['message'], "")
            }, this.time)
          }).catch((error) => {
        handleError(this, error, loader)
      })
      this.clearForm();
    },

    searchData() {
      return this.bioHazardList.filter(bioHazard => {
        return bioHazard.name.toLowerCase().includes(this.search.toLowerCase())
      })
    }
  },

  created() { this.getBioHazardLevel(); },

  components: {TopNav}
};
</script>
