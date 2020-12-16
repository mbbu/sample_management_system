<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-sm-12">
        <top-nav :page_title="page_title"></top-nav>

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
          <tr v-for="(role, index) in response.message" :key="role.id">
            <td> {{ index + 1 }}</td>
            <td> {{ role.name }}</td>
            <td> {{ role.code }}</td>
            <td> {{ role.description }}</td>

            <td>
              <b-icon
                  v-b-modal.modal-user-role-edit
                  v-b-tooltip.hover
                  :title="`Update ${ role.name }`" class="border border-info rounded"
                  font-scale="2.0" icon="pencil"
                  variant="info"
                  @mouseover="fillFormForUpdate(role.name, role.code, role.description)"
              ></b-icon>
              &nbsp;
              <b-icon
                  v-b-tooltip.hover :title="`Delete ${role.name}!`"
                  class="border rounded bg-danger p-1" font-scale="1.85"
                  icon="trash" variant="light"
                  @click="deleteUserRole(role.code)"
              ></b-icon>
            </td>
          </tr>
          </tbody>
        </table>
      </div>

      <div v-if="!isEditing">
        <b-modal
            id="modal-user-role"
            cancel-variant="danger"
            ok-title="Save"
            title="Add User Role"
            @hidden="clearForm"
            @ok="createUserRole"
            @submit="showModal = false"
        >
          <form @submit.prevent="createUserRole">

            <b-form-group id="form-name-group" label="Name:" label-for="form-name-input">
              <b-form-input
                  id="form-name-input"
                  v-model="name"
                  placeholder="Enter Name"
                  required
                  type="text"
              ></b-form-input>
            </b-form-group>

            <b-form-group id="form-code-group" label="Code:" label-for="form-code-input">
              <b-form-input
                  id="form-code-input"
                  v-model="code"
                  placeholder="Enter Code"
                  required
                  type="text"></b-form-input>
            </b-form-group>

            <b-form-group id="form-desc-group" label="Description:" label-for="form-desc-input">
              <b-form-textarea
                  id="form-desc-input"
                  v-model="desc"
                  placeholder="Enter Description"
                  required
                  type="text"
              ></b-form-textarea>
            </b-form-group>
          </form>
        </b-modal>
      </div>

      <div v-else-if="isEditing">
        <b-modal
            id="modal-user-role-edit"
            cancel-variant="danger"
            ok-title="Update"
            title="Edit User Role"
            @hidden="clearForm"
            @ok="updateUserRole(old_code)"
            @submit="showModal = false"
        >
          <form>

            <b-form-group id="form-name-group-edit" label="Name:" label-for="form-name-input">
              <b-form-input
                  id="form-name-input"
                  v-model="name"
                  placeholder="Enter Name"
                  required
                  type="text"
              ></b-form-input>
            </b-form-group>

            <b-form-group id="form-code-group-edit" label="Code:" label-for="form-code-input">
              <b-form-input
                  id="form-code-input"
                  v-model="code"
                  placeholder="Enter Code"
                  required
                  type="text"></b-form-input>
            </b-form-group>

            <b-form-group id="form-desc-group-edit" label="Description:" label-for="form-desc-input">
              <b-form-textarea
                  id="form-desc-input"
                  v-model="desc"
                  placeholder="Enter Description"
                  required
                  type="text"
              ></b-form-textarea>
            </b-form-group>
          </form>
        </b-modal>
      </div>
      <b-button v-b-modal.modal-user-role
                class="float_btn" variant="primary"
      >Add User Role
      </b-button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import {role_resource} from '@/utils/api_paths'
import TopNav from "../../components/TopNav";
import {handleError, secureStoreGetAuthString, showFlashMessage, startLoader} from "../../utils/util_functions";

export default {
  name: "UserRole",
  data() {
    return {
      page_title: "User Roles",
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

    getUserRole() {
      axios.get(role_resource)
          .then((res) => {
            this.response = res.data;
          })
          .catch((error) => {
            // eslint-disable-next-line
            this.$log.error(error);
          });
    },

    createUserRole: function () {
      let loader = startLoader(this)
      axios.post(role_resource, {
        name: this.name,
        code: this.code,
        description: this.desc,
      }, {
        headers: {
          Authorization: secureStoreGetAuthString()
        }
      }).then((response) => {
        setTimeout(() => {
          this.getUserRole();
          this.clearForm();
          loader.hide()
          showFlashMessage(this, 'success', response.data['message'], "")
        }, 2500)
      }).catch((error) => {
        handleError(this, error, loader)
      });
      this.clearForm();
    },

    updateUserRole: function (code) {
      let loader = startLoader(this)
      axios.put(role_resource, {
        name: this.name,
        code: this.code,
        description: this.desc,
      }, {
        headers:
            {
              code: code,
              Authorization: secureStoreGetAuthString()
            }
      }).then((response) => {
        setTimeout(() => {
          this.getUserRole();
          showFlashMessage(this, 'success', response.data['message'], "")
        }, 2500)
      }).catch((error) => {
        handleError(this, error, loader)
      });
      this.clearForm();
    },

    deleteUserRole: function (code) {
      let loader = startLoader(this)
      axios.delete(role_resource, {
        headers:
            {
              code: code,
              Authorization: secureStoreGetAuthString()
            }
      }).then((response) => {
        setTimeout(() => {
          this.getUserRole();
          showFlashMessage(this, 'success', response.data['message'], "")
        }, 2500)
      }).catch((error) => {
        handleError(this, error, loader)
      })
    }
  },
  created() {
    this.getUserRole();
  },
  components: {TopNav}
};
</script>