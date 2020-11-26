<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <top-nav :page_title="page_title" v-bind:search_query.sync="search"></top-nav>

                <FlashMessage :position="'right bottom'"></FlashMessage>
                <br>
                <table class=" table table-hover">
                    <thead>
                    <tr>
                      <th class="table-header-style" scope="col"> Id</th>
                      <th class="table-header-style" scope="col"> Name</th>
                      <th class="table-header-style" scope="col"> Code</th>
                      <th class="table-header-style" scope="col" v-if="isAuth"> Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr :key="theme.id" v-for="(theme, index) in filteredList">
                        <td> {{ index + 1 }}</td>
                        <td> {{ theme.name }}</td>
                        <td> {{ theme.code }}</td>

                      <td v-if="isAuth">
                        <b-icon
                            :title="`Update ${ theme.name }`"
                            @mouseover="fillFormForUpdate(theme.name, theme.code)"
                            class="border border-info rounded" font-scale="2.0"
                            icon="pencil" v-b-modal.modal-theme-edit
                            v-b-tooltip.hover
                            variant="info"
                        ></b-icon>
                        &nbsp;
                        <b-icon
                                    :title="`Delete ${theme.name}!`" @click="deleteTheme(theme.code)"
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
                <b-modal id="modal-theme" :title="`Add ${page_title}`"
                        @hidden="clearForm"  @ok="onSubmit" @submit="showModal = false"
                        cancel-variant="danger" ok-title="Save"
                >
                    <form @submit.prevent="createTheme">

                        <!-- NAME -->
                        <b-form-group :class="{ 'form-group--error': $v.theme.name.$error }"
                                      id="form-name-group" label="Name:" label-for="form-name-input">
                            <b-form-input id="form-name-input"
                                    placeholder="Enter Name" required type="text"
                                    v-model.trim="$v.theme.name.$model"></b-form-input>
                            <div v-if="$v.theme.name.$dirty">
                                <div class="error" v-if="!$v.theme.name.required">Field is required</div>
                            </div>
                        </b-form-group>

                        <!-- CODE -->
                        <b-form-group :class="{ 'form-group--error': $v.theme.code.$error }"
                                      id="form-code-group" label="Code:" label-for="form-code-input">
                            <b-form-input id="form-code-input"
                                    placeholder="Enter Code" required type="text"
                                    v-model.trim="$v.theme.code.$model"></b-form-input>
                            <div v-if="$v.theme.code.$dirty">
                                <div class="error" v-if="!$v.theme.code.required">Field is required</div>
                            </div>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>

            <div v-else-if="isEditing">
                <b-modal id="modal-theme-edit" :title="`Edit ${page_title}`"
                        @hidden="clearForm" @ok="updateTheme" @submit="showModal = false"
                        cancel-variant="danger" ok-title="Update"
                >
                    <form @submit.prevent="updateTheme">

                        <!-- NAME -->
                        <b-form-group :class="{ 'form-group--error': $v.theme.name.$error }"
                                      id="form-name-group-edit" label="Name:" label-for="form-name-input">
                            <b-form-input id="form-name-input"
                                    placeholder="Enter Name" required type="text"
                                    v-model.trim="$v.theme.name.$model"></b-form-input>
                            <div v-if="$v.theme.name.$dirty">
                                <div class="error" v-if="!$v.theme.name.required">Field is require</div>
                            </div>
                        </b-form-group>

                        <!-- CODE -->
                        <b-form-group :class="{ 'form-group--error': $v.theme.code.$error }"
                                      id="form-code-group-edit" label="Code:" label-for="form-code-input">
                            <b-form-input id="form-code-input"
                                    placeholder="Enter Code" required type="text"
                                    v-model.trim="$v.theme.code.$model"></b-form-input>
                            <div v-if="$v.theme.code.$dirty">
                                <div class="error" v-if="!$v.theme.code.required">Field is required</div>
                            </div>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>
          <div v-if="isAuth">
            <b-button class="float_btn" style="border-radius: 50%" v-b-modal.modal-theme variant="primary">
              <span>Add Theme</span> <i class="fas fa-plus-circle menu_icon"></i>
            </b-button>
          </div>

          <div style="margin: auto;">
            <loading-progress :indeterminate="indeterminate" :hide-background="hideBackground"
              :progress="progressPath" :size="size" rotate fillDuration="2" rotationDuration="1"/>
          </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import {theme_resource} from '@/utils/api_paths'
import TopNav from "../components/TopNav";
import {isAdmin, secureStoreGetAuthString, handleError, pageStartLoader, showFlashMessage} from '@/utils/util_functions'
import EventBus from '../components/EventBus';
import {required} from "vuelidate/lib/validators";

export default {
  name: 'Theme',
  components: {TopNav},

  data() {
    return {
      page_title: "Themes",
      response: [], themeList: [], search: '',
      theme: { name: '', code: '' },

      // variable to check user status and role
      isAuth: null,

      time: 2000, // loader-time

      // progressPath
      indeterminate: true, hideBackground: true, progressPath: 5, size: 180,

      // values for data modification
      old_code: null, showModal: true, isEditing: false,
    };
  },

  validations: { theme: { name: {required}, code: {required} } },

  mounted() {
    EventBus.$on('searchQuery', (payload) => {
        this.search = payload; this.searchData()
    })
  },

  computed: {
    filteredList() {
        return this.themeList.filter(theme => {
            return theme.name.toLowerCase().includes(this.search.toLowerCase())
        })
    }
  },

  created() { this.getTheme(); },

  methods: {
    // util functions
    onSubmit(evt) {
      this.$v.$touch();
      if (this.$v.$invalid) { evt.preventDefault(); return; }
      this.createTheme();
    },

    clearForm() {
          this.theme.name = null; this.theme.code = null;
          this.isEditing = false; this.$v.$reset();
    },

    fillFormForUpdate(name, code) {
          this.theme.name = name; this.theme.code = code; this.old_code = code;
          this.isEditing = true; this.showModal = true;
    },

    // stop&hide progressPath
    haltProgressPath(cont=false, path=0, size=0){
      this.indeterminate = cont; this.progressPath = path; this.size = size;
    },

    // api interaction functions
    getTheme() {
      this.isAuth = isAdmin()

      axios.get(theme_resource)
          .then((res) => {
            setTimeout(()=> {
              this.haltProgressPath(); this.themeList = this.response = res.data['message'];
            }, this.time)
          }).catch((error) => {
            // eslint-disable-next-line
            this.$log.error(error);
          });
    },

    createTheme: function () {
      let self = this; let loader = pageStartLoader(this)

      axios.post(theme_resource, {
          name: this.theme.name,
          code: this.theme.code,
      }, {
          headers: {
            Authorization: secureStoreGetAuthString()
          }
      }).then((response) => {
            setTimeout(()=> {
              loader.hide(); this.getTheme(); this.clearForm();
              showFlashMessage(self, 'success', 'Success', response.data['message'])
            },this.time)
          }).catch((error) => {
              this.$log.error(error); loader.hide();
              if (error.response) { handleError(this, error) }
          });
      this.clearForm();
    },

    updateTheme: function (evt) {
      this.$v.$touch();
      if (this.$v.$invalid) { evt.preventDefault()} else {
          let self = this; let loader = pageStartLoader(this);
          axios.put(theme_resource, {
              name: this.theme.name,
              code: this.theme.code,
          }, {
              headers:
                  {
                    code: this.old_code,
                    Authorization: secureStoreGetAuthString()
                  }
          }).then((response) => {
                setTimeout( () => {
                  loader.hide(); this.getTheme();
                  showFlashMessage(self, 'success', 'Success', response.data['message'])
                }, this.time)
              }).catch((error) => {
                  this.$log.error(error); loader.hide();
                  if (error.response) { handleError(this, error) }
              });
          this.clearForm();
      }
    },

    deleteTheme: function (code) {
      let self = this; let loader = pageStartLoader(this);

      axios.delete(theme_resource, {
          headers: {
            code: code,
            Authorization: secureStoreGetAuthString()
          }
      }).then((response) => {
            setTimeout(() => {
              loader.hide(); this.getTheme();
              showFlashMessage(self, 'success', 'Success', response.data['message'])
            }, this.time)
          }).catch((error) => {
              this.$log.error(error); loader.hide()
              if (error.response) {handleError(this, error)}
          });
      this.clearForm();
    },

    searchData() {
      return this.themeList.filter(theme => {
          return theme.name.toLowerCase().includes(this.search.toLowerCase())
      })
    }
  },
};
</script>
