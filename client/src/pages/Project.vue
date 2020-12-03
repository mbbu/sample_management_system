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
            <th class="table-header-style" scope="col"> Id</th>
            <th class="table-header-style" scope="col"> Name</th>
            <th class="table-header-style" scope="col"> Theme</th>
            <th class="table-header-style" scope="col"> Project Head</th>
            <th class="table-header-style" scope="col"> Code</th>
            <th class="table-header-style" scope="col"> Description</th>
            <th v-if="isAuth" class="table-header-style" scope="col"> Actions</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(project, index) in response.message" :key="project.id">
            <td> {{ index + 1 }}</td>
            <td> {{ project.name }}</td>
            <td> {{ project['theme.name'] }}</td>
            <td>
              {{ project['lead.first_name'] }} {{ project['lead.last_name'] }}
              <a :href="`mailto:${project['lead.email']}`" target="_blank">
                <b-icon
                    v-b-tooltip.hover
                    :font-scale="`${font_scale}`"
                    :title="`Contact project head (${ project['lead.email'] })`" class="border border-info rounded"
                    icon="envelope" variant="info"
                ></b-icon>
              </a>
            </td>
            <td> {{ project.code }}</td>
            <td> {{ project.description }}</td>

            <td v-if="isAuth">
              <b-icon
                  v-b-modal.modal-project-edit
                  v-b-tooltip.hover
                  :font-scale="`${font_scale}`" :title="`Update project ${ project.name }`"
                  class="border border-info rounded" icon="pencil"
                  variant="info"
                  @mouseover="fillFormForUpdate(project.code, project.name, project.description, project['theme.name'],
                                    project['lead.first_name'] + ' ' + project['lead.last_name'])"
              ></b-icon>
              &nbsp;
              <b-icon
                  v-b-tooltip.hover :font-scale="`${font_scale}`"
                  :title="`Delete project ${project.name}!`" class="border rounded bg-danger p-1"
                  icon="trash" variant="light"
                  @click="deleteProject(project.code)"
              ></b-icon>
            </td>
          </tr>
          </tbody>
        </table>
      </div>

      <div v-if="!isEditing">
        <b-modal
            id="modal-project"
            cancel-variant="danger"
            ok-title="Save"
            title="Add Project"
            @hidden="clearForm"
            @ok="createProject"
            @submit="clearForm"
        >
          <form @submit.prevent="createProject">
            <b-form-group id="form-theme-group" label="Theme:" label-for="form-theme-input">
              <ejs-dropdownlist
                  id='dropdownlist'
                  :dataSource='themeDataList'
                  :fields="fields"
                  :v-model="project.theme"
                  placeholder='Select a theme'
              ></ejs-dropdownlist>
            </b-form-group>

            <b-form-group id="form-head-group" label="Project Head:" label-for="form-head-input">
              <ejs-dropdownlist
                  id='dropdownlist-head'
                  :dataSource='headDataList'
                  :fields="fields"
                  :v-model="project.head"
                  placeholder='Select the project head'
              ></ejs-dropdownlist>
            </b-form-group>

            <b-form-group id="form-code-group" label="Code:" label-for="form-code-input">
              <b-form-input
                  id="form-code-input"
                  v-model="project.code"
                  placeholder="Enter Code"
                  required
                  type="text"
              ></b-form-input>
            </b-form-group>

            <b-form-group id="form-name-group" label="Name:" label-for="form-name-input">
              <b-form-input
                  id="form-name-input"
                  v-model="project.name"
                  placeholder="Enter Project Name"
                  required
                  type="text">
              </b-form-input>
            </b-form-group>

            <b-form-group id="form-desc-group" label="Description:" label-for="form-desc-input">
              <b-form-textarea
                  id="form-desc-input"
                  v-model="project.description"
                  placeholder="Enter Description"
                  required
                  type="text">
              </b-form-textarea>
            </b-form-group>

          </form>
        </b-modal>
      </div>

      <div v-else-if="isEditing">
        <b-modal
            id="modal-project-edit"
            cancel-variant="danger"
            ok-title="Update"
            title="Edit Project"
            @hidden="clearForm"
            @ok="updateProject(old_code)"
            @shown="selectDropDownItemsForUpdate(project.theme, project.head)"
            @submit="showModal = false"
        >
          <form @submit.prevent="updateProject">
            <b-form-group id="form-theme-group-edit" label="Theme:" label-for="form-theme-input">
              <ejs-dropdownlist
                  id='dropdownlist'
                  :dataSource='themeDataList'
                  :fields="fields"
                  :v-model="project.theme"
                  placeholder='Select a theme'
              ></ejs-dropdownlist>
            </b-form-group>

            <b-form-group id="form-head-group-edit" label="Project Head:" label-for="form-head-input">
              <ejs-dropdownlist
                  id='dropdownlist-head'
                  :dataSource='headDataList'
                  :fields="fields"
                  :v-model="project.head"
                  placeholder='Select the project head'
              ></ejs-dropdownlist>
            </b-form-group>

            <b-form-group id="form-code-group-edit" label="Code:" label-for="form-code-input">
              <b-form-input
                  id="form-code-input"
                  v-model="project.code"
                  placeholder="Enter Code"
                  required
                  type="text"
              ></b-form-input>
            </b-form-group>

            <b-form-group id="form-name-group-edit" label="Name:" label-for="form-name-input">
              <b-form-input
                  id="form-name-input"
                  v-model="project.name"
                  placeholder="Enter Project Name"
                  required
                  type="text">
              </b-form-input>
            </b-form-group>

            <b-form-group id="form-desc-group-edit" label="Description:" label-for="form-desc-input">
              <b-form-textarea
                  id="form-desc-input"
                  v-model="project.description"
                  placeholder="Enter Description"
                  required
                  type="text">
              </b-form-textarea>
            </b-form-group>
          </form>
        </b-modal>
      </div>

      <b-button v-if="isAuth" v-b-modal.modal-project class="float_btn" style="border-radius: 50%"
                variant="primary">
        <span>Add Project</span> <i class="fas fa-plus-circle menu_icon"></i>
      </b-button>


      <div style="margin: auto;">
        <loading-progress :hide-background="hideBackground" :indeterminate="indeterminate" :progress="progressPath"
                          :size="size" fillDuration="2" rotate rotationDuration="1"/>
      </div>
    </div>
  </div>
</template>

<script>
import {
  extractApiData,
  extractUserData,
  getItemDataList,
  getSelectedItem,
  getSelectedItemCode,
  handleError,
  isResearcher,
  pageStartLoader,
  secureStoreGetAuthString,
  showFlashMessage
} from "@/utils/util_functions";
import {font_scale} from '@/utils/constants';
import {project_resource, theme_resource, user_resource} from "@/utils/api_paths";
import axios from "axios";
import TopNav from "../components/TopNav";

export default {
  name: "Project",
  data() {
    return {
      page_title: "Project",
      response: [],
      project: {
        code: null,
        name: null,
        description: null,
        theme: null,
        head: null
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

      themeDataList: [],
      headDataList: [],
      fields: {text: '', value: ''},

      // values for data modification
      old_code: null,
      showModal: true,
      isEditing: false,
    };
  },
  methods: {
    // Util Functions
    clearForm() {
      this.project.code = null;
      this.project.name = null;
      this.project.theme = null;
      this.project.head = null;
      this.project.description = null;
      this.isEditing = false;
      this.themeDataList = [];
      this.headDataList = [];
      this.onLoadPage();
    },

    fillFormForUpdate(code, name, description, theme, head) {
      this.project.code = code;
      this.project.name = name;
      this.project.description = description;
      this.project.theme = theme;
      this.project.head = head;
      this.old_code = code;
      this.isEditing = true;
      this.showModal = true;
    },

    onLoadPage() {
      getItemDataList(theme_resource).then(data => {
        let themeList = extractApiData(data);

        // update local variables with data from API
        this.fields = themeList['fields'];
        for (let i = 0; i < themeList.items.length; i++) {
          this.themeDataList.push({
            'Code': themeList.items[i].Code,
            'Name': themeList.items[i].Name,
          });
        }
      })

      getItemDataList(user_resource).then(data => {
        let headList = extractUserData(data);

        // update local variables with data from API
        this.fields = headList['fields'];
        for (let i = 0; i < headList.items.length; i++) {
          this.headDataList.push({
            'Code': headList.items[i].Code,
            'Name': headList.items[i].Name,
          });
        }
      })
    },

    selectDropDownItemsForUpdate(theme, head) {
      let elementTheme = document.getElementById("dropdownlist");
      elementTheme.value = theme;

      let elementHead = document.getElementById("dropdownlist-head");
      elementHead.value = head;
    },

    // stop&hide progressPath
    haltProgressPath(cont = false, path = 0, size = 0) {
      this.indeterminate = cont
      this.progressPath = path
      this.size = size
    },

    // Functions to interact with api
    getProject() {
      this.isAuth = isResearcher()

      this.clearForm();
      axios.get(project_resource)
          .then((res) => {
            setTimeout(() => {
              this.haltProgressPath()
              this.response = res.data;
            }, this.time)
          })
          .catch((error) => {
            // eslint-disable-next-line
            this.$log.error(error);
          });
    },

    createProject: function () {
      this.project.theme = getSelectedItem(this.themeDataList, this.project.theme);
      this.project.head = getSelectedItemCode('dropdownlist-head', this.headDataList);
      let loader = pageStartLoader(this)

      axios.post(project_resource, {
        code: this.project.code,
        name: this.project.name,
        head: this.project.head,
        theme: this.project.theme,
        description: this.project.description,
      }, {
        headers:
            {
              Authorization: secureStoreGetAuthString()
            }
      }).then((response) => {
        setTimeout(() => {
          loader.hide()
          this.getProject();
          showFlashMessage(this, 'success', response.data['message'], '');
        }, this.time)
      }).catch((error) => {
        handleError(this, error, loader)
      });
    },

    updateProject: function (code) {
      this.project.theme = getSelectedItem(this.themeDataList, this.project.theme);
      this.project.head = getSelectedItemCode('dropdownlist-head', this.headDataList);
      let loader = pageStartLoader(this)

      axios.put(project_resource, {
        code: this.project.code,
        name: this.project.name,
        head: this.project.head,
        theme: this.project.theme,
        description: this.project.description,
      }, {
        headers:
            {
              code: code,
              Authorization: secureStoreGetAuthString()
            }
      }).then((response) => {
        setTimeout(() => {
          loader.hide()
          this.getProject();
          showFlashMessage(this, 'success', response.data['message'], '');
          this.clearForm();
        }, this.time)
      }).catch((error) => {
        handleError(this, error, loader)
      });
    },

    deleteProject: function (code) {
      let loader = pageStartLoader(this)
      axios.delete(project_resource, {
        headers:
            {
              code: code,
              Authorization: secureStoreGetAuthString()
            }
      }).then((response) => {
        setTimeout(() => {
          loader.hide()
          this.getProject();
          showFlashMessage(this, 'success', response.data['message'], '');
        }, this.time)
      }).catch((error) => {
        handleError(this, error, loader)
      });
    },
  },
  created() {
    this.getProject();
  },
  components: {TopNav}
}
</script>
