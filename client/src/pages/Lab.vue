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
            <th class="table-header-style" scope="col"> Room</th>
            <th v-if="isAuth" class="table-header-style" scope="col"> Actions</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(lab, index) in filteredList.arr" :key="lab.id">
            <td> {{ index + 1 }}</td>
            <td> {{ lab.name }}</td>
            <td> {{ lab.code }}</td>
            <td> {{ lab.room }}</td>

            <td v-if="isAuth">
              <b-icon
                  v-b-modal.modal-lab-edit
                  v-b-tooltip.hover
                  :font-scale="`${font_scale}`" :title="`Update ${ lab.name }`"
                  class="border border-info rounded" icon="pencil"
                  variant="info"
                  @mouseover="fillFormForUpdate(lab.name, lab.code, lab.room)"
              ></b-icon>
              &nbsp;
              <b-icon
                  v-b-tooltip.hover :font-scale="`${font_scale}`"
                  :title="`Delete ${lab.name}!`" class="border rounded bg-danger p-1"
                  icon="trash" variant="light"
                  @click="deleteLab(lab.code)"
              ></b-icon>
            </td>
          </tr>
          </tbody>
        </table>
        <!--TOP-PAGINATION-->
        <v-page v-model="current" :total-row="filteredList.pg_len" align="center"
                @page-change="pageInfo"></v-page>
        <br>
      </div>

      <div v-if="!isEditing">
        <b-modal
            id="modal-lab"
            cancel-variant="danger"
            ok-title="Save"
            title="Add Lab"
            @hidden="clearForm"
            @ok="onSubmit"
            @submit="showModal = false"
        >
          <form @submit.prevent="createLab">
            <!-- NAME -->
            <b-form-group id="form-name-group"
                          :class="{ 'form-group--error': $v.lab.name.$error }" label="Name:" label-for="form-name-input">
              <b-form-input
                  id="form-name-input"
                  v-model.trim="$v.lab.name.$model"
                  placeholder="Enter Name"
                  required
                  type="text"
              ></b-form-input>
              <div v-if="$v.lab.name.$dirty">
                <div v-if="!$v.lab.name.required" class="error">Field is
                  required
                </div>
              </div>
            </b-form-group>

            <b-form-group id="form-code-group"
                          :class="{ 'form-group--error': $v.lab.code.$error }" label="Code:" label-for="form-code-input">
              <b-form-input
                  id="form-code-input"
                  v-model.trim="$v.lab.code.$model"
                  placeholder="Enter Code"
                  required
                  type="text"></b-form-input>
              <div v-if="$v.lab.code.$dirty">
                <div v-if="!$v.lab.code.required" class="error">Field is
                  required
                </div>
              </div>
            </b-form-group>

            <b-form-group id="form-room-group"
                          :class="{ 'form-group--error': $v.lab.room.$error }" label="Room:" label-for="form-room-input">
              <b-form-input
                  id="form-room-input"
                  v-model.trim="$v.lab.room.$model"
                  placeholder="Enter Room Number"
                  required
                  type="text"
              ></b-form-input>
              <div v-if="$v.lab.room.$dirty">
                <div v-if="!$v.lab.room.required" class="error">Field is
                  required
                </div>
              </div>
            </b-form-group>
          </form>
        </b-modal>
      </div>

      <div v-else-if="isEditing">
        <b-modal
            id="modal-lab-edit"
            cancel-variant="danger"
            ok-title="Update"
            title="Edit Lab"
            @hidden="clearForm"
            @ok="updateLab"
            @submit="showModal = false"
        >
          <form @submit.prevent="updateLab">
            <!-- NAME -->
            <b-form-group id="form-name-group-edit"
                          :class="{ 'form-group--error': $v.lab.name.$error }" label="Name:" label-for="form-name-input">
              <b-form-input
                  id="form-name-input"
                  v-model.trim="$v.lab.name.$model"
                  placeholder="Enter Name"
                  required
                  type="text"
              ></b-form-input>
              <div v-if="$v.lab.name.$dirty">
                <div v-if="!$v.lab.name.required" class="error">Field is
                  required
                </div>
              </div>
            </b-form-group>

            <!--CODE-->
            <b-form-group id="form-code-group-edit"
                          :class="{ 'form-group--error': $v.lab.code.$error }" label="Code:" label-for="form-code-input">
              <b-form-input
                  id="form-code-input"
                  v-model.trim="$v.lab.code.$model"
                  placeholder="Enter Code"
                  required
                  type="text"></b-form-input>
              <div v-if="$v.lab.code.$dirty">
                <div v-if="!$v.lab.code.required" class="error">Field is
                  required
                </div>
              </div>
            </b-form-group>

            <!--ROOM-->
            <b-form-group id="form-room-group-edit"
                          :class="{ 'form-group--error': $v.lab.room.$error }" label="Room:" label-for="form-room-input">
              <b-form-input
                  id="form-room-input"
                  v-model.trim="$v.lab.room.$model"
                  placeholder="Enter Room Number"
                  required
                  type="text"
              ></b-form-input>
              <div v-if="$v.lab.room.$dirty">
                <div v-if="!$v.lab.room.required" class="error">Field is
                  required
                </div>
              </div>
            </b-form-group>
          </form>
        </b-modal>
      </div>
      <b-button v-if="isAuth" v-b-modal.modal-lab class="float_btn" style="border-radius: 50%" variant="primary">
        <span>Add Lab</span> <i class="fas fa-plus-circle menu_icon"></i>
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
import {lab_resource} from '@/utils/api_paths'
import TopNav from "../components/TopNav";
import {
  handleError,
  isThemeAdmin,
  pageStartLoader,
  paginate,
  secureStoreGetAuthString,
  showFlashMessage
} from "@/utils/util_functions";
import {font_scale} from '@/utils/constants';
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

      font_scale,

      // variable to check user status and role
      isAuth: null,

      search: '',
      labList: [],

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

    // stop&hide progressPath
    haltProgressPath(cont = false, path = 0, size = 0) {
      this.indeterminate = cont
      this.progressPath = path
      this.size = size
    },

    getLab() {
      this.isAuth = isThemeAdmin()

      axios.get(lab_resource)
          .then((res) => {
            setTimeout(() => {
              this.haltProgressPath()
              this.labList = this.response = res.data['message'];
            }, this.time)
          })
          .catch((error) => {
            // eslint-disable-next-line
            this.$log.error(error);
          });
    },

    createLab: function () {
      let loader = pageStartLoader(this)
      axios.post(lab_resource, {
        name: this.lab.name,
        code: this.lab.code,
        room: this.lab.room,
      }, {
        headers: {
          Authorization: secureStoreGetAuthString()
        }
      }).then((response) => {
        setTimeout(() => {
          loader.hide()
          this.getLab();
          this.clearForm();
          showFlashMessage(this, 'success', response.data['message'], '')
        }, this.time)
      }).catch((error) => {
        handleError(this, error, loader)
      });
      this.clearForm();
    },

    updateLab: function (evt) {
      this.$v.$touch();
      if (this.$v.$invalid) {
        evt.preventDefault()
      } else {
        let loader = pageStartLoader(this)

        axios.put(lab_resource, {
          name: this.lab.name,
          code: this.lab.code,
          room: this.lab.room,
        }, {
          headers:
              {
                code: this.old_code,
                Authorization: secureStoreGetAuthString()
              }
        }).then((response) => {
          setTimeout(() => {
            loader.hide()
            this.getLab();
            showFlashMessage(this, 'success', response.data['message'], '')
          }, this.time)
        }).catch((error) => {
          handleError(this, error, loader)
        });
        this.clearForm();
      }
    },

    deleteLab: function (code) {
      let loader = pageStartLoader(this)
      axios.delete(lab_resource, {
        headers:
            {
              code: code,
              Authorization: secureStoreGetAuthString()
            }
      }).then((response) => {
        setTimeout(() => {
          loader.hide()
          this.getLab();
          showFlashMessage(this, 'success', response.data['message'], '')
        }, this.time)
      }).catch((error) => {
        handleError(this, error, loader)
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
