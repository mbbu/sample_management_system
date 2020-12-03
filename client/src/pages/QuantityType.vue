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
          <tr v-for="(qt, index) in filteredList.arr" :key="qt.id">
            <td> {{ index + 1 }}</td>
            <td> {{ qt.name }}</td>
            <td> {{ qt.id }}</td>
            <td> {{ qt.description }}</td>

            <td v-if="isAuth">
              <b-icon
                  v-b-modal.modal-quantity-type-edit
                  v-b-tooltip.hover
                  :font-scale="`${font_scale}`" :title="`Update ${ qt.name }`"
                  class="border border-info rounded" icon="pencil"
                  variant="info"
                  @mouseover="fillFormForUpdate(qt.name, qt.id, qt.description)"
              ></b-icon>
              &nbsp;
              <b-icon
                  v-b-tooltip.hover :font-scale="`${font_scale}`"
                  :title="`Delete ${qt.name}!`" class="border rounded bg-danger p-1"
                  icon="trash" variant="light"
                  @click="deleteQuantityType(qt.id)"
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
            id="modal-quantity-type"
            cancel-variant="danger"
            ok-title="Save"
            title="Add Quantity Type"
            @hidden="clearForm"
            @ok="onSubmit"
            @submit="showModal = false"
        >
          <form @submit.prevent="createQuantityType">

            <!-- NAME -->
            <b-form-group id="form-name-group"
                          :class="{ 'form-group--error': $v.qt.name.$error }" label="Name:" label-for="form-name-input">
              <b-form-input
                  id="form-name-input"
                  v-model.trim="$v.qt.name.$model"
                  placeholder="Enter Name"
                  required
                  type="text"
              ></b-form-input>
              <div v-if="$v.qt.name.$dirty">
                <div v-if="!$v.qt.name.required" class="error">Field is
                  required
                </div>
              </div>
            </b-form-group>

            <!--CODE-->
            <b-form-group id="form-code-group"
                          :class="{ 'form-group--error': $v.qt.code.$error }" label="Code:" label-for="form-code-input">
              <b-form-input
                  id="form-code-input"
                  v-model.trim="$v.qt.code.$model"
                  placeholder="Enter Code"
                  required
                  type="text"></b-form-input>
              <div v-if="$v.qt.code.$dirty">
                <div v-if="!$v.qt.code.required" class="error">Field is
                  required
                </div>
              </div>
            </b-form-group>

            <!--DESC-->
            <b-form-group id="form-desc-group"
                          :class="{ 'form-group--error': $v.qt.desc.$error }" label="Description:" label-for="form-desc-input">
              <b-form-textarea
                  id="form-desc-input"
                  v-model.trim="$v.qt.desc.$model"
                  placeholder="Enter Description"
                  required
                  type="text"
              ></b-form-textarea>
              <div v-if="$v.qt.desc.$dirty">
                <div v-if="!$v.qt.desc.required" class="error">Field is
                  required
                </div>
              </div>
            </b-form-group>
          </form>
        </b-modal>
      </div>

      <div v-else-if="isEditing">
        <b-modal
            id="modal-quantity-type-edit"
            cancel-variant="danger"
            ok-title="Update"
            title="Edit Quantity Type"
            @hidden="clearForm"
            @ok="updateQuantityType"
            @submit="showModal = false"
        >
          <form>

            <!-- NAME -->
            <b-form-group id="form-name-group-edit"
                          :class="{ 'form-group--error': $v.qt.name.$error }" label="Name:" label-for="form-name-input">
              <b-form-input
                  id="form-name-input"
                  v-model.trim="$v.qt.name.$model"
                  placeholder="Enter Name"
                  required
                  type="text"
              ></b-form-input>
              <div v-if="$v.qt.name.$dirty">
                <div v-if="!$v.qt.name.required" class="error">Field is
                  required
                </div>
              </div>
            </b-form-group>

            <!--CODE-->
            <b-form-group id="form-code-group-edit"
                          :class="{ 'form-group--error': $v.qt.code.$error }" label="Code:" label-for="form-code-input">
              <b-form-input
                  id="form-code-input"
                  v-model.trim="$v.qt.code.$model"
                  placeholder="Enter Code"
                  required
                  type="text"></b-form-input>
              <div v-if="$v.qt.code.$dirty">
                <div v-if="!$v.qt.code.required" class="error">Field is
                  required
                </div>
              </div>
            </b-form-group>

            <!--DESC-->
            <b-form-group id="form-desc-group-edit"
                          :class="{ 'form-group--error': $v.qt.desc.$error }" label="Description:" label-for="form-desc-input">
              <b-form-textarea
                  id="form-desc-input"
                  v-model.trim="$v.qt.desc.$model"
                  placeholder="Enter Description"
                  required
                  type="text"
              ></b-form-textarea>
              <div v-if="$v.qt.desc.$dirty">
                <div v-if="!$v.qt.desc.required" class="error">Field is
                  required
                </div>
              </div>
            </b-form-group>
          </form>
        </b-modal>
      </div>
      <b-button v-if="isAuth" v-b-modal.modal-quantity-type class="float_btn" style="border-radius: 50%"
                variant="primary">
        <span>Add Quantity Type</span> <i class="fas fa-plus-circle menu_icon"></i>
      </b-button>
      <div style="margin: auto;">
        <loading-progress
            :hide-background="hideBackground"
            :indeterminate="indeterminate"
            :progress="progressPath"
            :size="size"
            fillDuration="2"
            rotate
            rotationDuration="1"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import {quantity_type_resource} from '@/utils/api_paths'
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

      font_scale,

      // variable to check user status and role
      isAuth: null,


      // loader-time
      time: 2000,

      // progressPath
      indeterminate: true,
      hideBackground: true,
      progressPath: 5,
      size: 180,

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

    // stop&hide progressPath
    haltProgressPath(cont = false, path = 0, size = 0) {
      this.indeterminate = cont
      this.progressPath = path
      this.size = size
    },

    getQuantityType() {
      this.isAuth = isThemeAdmin()

      axios.get(quantity_type_resource)
          .then((res) => {
            setTimeout(() => {
              this.haltProgressPath()
              this.QTList = this.response = res.data['message'];
            }, this.time)
          })
          .catch((error) => {
            // eslint-disable-next-line
            this.$log.error(error);
          });
    },

    createQuantityType: function () {
      let loader = pageStartLoader(this)

      axios.post(quantity_type_resource, {
        name: this.qt.name,
        code: this.qt.code,
        description: this.qt.desc,
      }, {
        headers: {
          Authorization: secureStoreGetAuthString()
        }
      }).then((response) => {
        setTimeout(() => {
          loader.hide()
          this.getQuantityType();
          showFlashMessage(this, 'success', response.data['message'], '')
        }, this.time)
      }).catch((error) => {
        handleError(this, error, loader)
      });
      this.clearForm();
    },

    updateQuantityType: function (evt) {
      this.$v.$touch();
      if (this.$v.$invalid) {
        evt.preventDefault()
      } else {
        let loader = pageStartLoader(this)
        axios.put(quantity_type_resource, {
          name: this.qt.name,
          code: this.qt.code,
          description: this.qt.desc,
        }, {
          headers:
              {
                code: this.old_code,
                Authorization: secureStoreGetAuthString()
              }
        }).then((response) => {
              setTimeout(() => {
                loader.hide()
                this.getQuantityType();
                showFlashMessage(this, 'success', response.data['message'], '')
              }, this.time)
            }).catch((error) => {
          handleError(this, error, loader)
        });
        this.clearForm();
      }
    },

    deleteQuantityType: function (code) {
      let loader = pageStartLoader(this)
      axios.delete(quantity_type_resource, {
        headers:
            {
              code: code,
              Authorization: secureStoreGetAuthString()
            }
      }).then((response) => {
        setTimeout(() => {
          loader.hide()
          this.getQuantityType();
          showFlashMessage(this, 'success', response.data['message'], '')
        }, this.time)
      }).catch((error) => {
        handleError(this, error, loader)
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
