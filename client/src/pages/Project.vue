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
                      <th class="table-header-style" scope="col" v-if="isAuth"> Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr :key="project.id" v-for="(project, index) in response.message">
                        <td> {{ index + 1 }}</td>
                        <td> {{ project.name }}</td>
                        <td> {{ project['theme.name'] }}</td>
                        <td>
                            {{ project['lead.first_name'] }} {{ project['lead.last_name'] }}
                            <a :href="`mailto:${project['lead.email']}`" target="_blank">
                                <b-icon
                                        :title="`Contact project head (${ project['lead.email'] })`"
                                        class="border border-info rounded"
                                        :font-scale="`${font_scale}`" icon="envelope"
                                        v-b-tooltip.hover variant="info"
                                ></b-icon>
                            </a>
                        </td>
                        <td> {{ project.code }}</td>
                        <td> {{ project.description }}</td>

                      <td v-if="isAuth">
                        <b-icon
                            :title="`Update project ${ project.name }`"
                            @mouseover="fillFormForUpdate(project.code, project.name, project.description, project['theme.name'],
                                    project['lead.first_name'] + ' ' + project['lead.last_name'])"
                            class="border border-info rounded" :font-scale="`${font_scale}`"
                            icon="pencil" v-b-modal.modal-project-edit
                            v-b-tooltip.hover
                            variant="info"
                        ></b-icon>
                        &nbsp;
                            <b-icon
                                    :title="`Delete project ${project.name}!`" @click="deleteProject(project.code)"
                                    class="border rounded bg-danger p-1" :font-scale="`${font_scale}`"
                                    icon="trash" v-b-tooltip.hover
                                    variant="light"
                            ></b-icon>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>

            <div v-if="!isEditing">
                <b-modal
                        @hidden="clearForm"
                        @ok="createProject"
                        @submit="clearForm"
                        cancel-variant="danger"
                        id="modal-project"
                        ok-title="Save"
                        title="Add Project"
                >
                    <form @submit.prevent="createProject">
                        <b-form-group id="form-theme-group" label="Theme:" label-for="form-theme-input">
                            <ejs-dropdownlist
                                    :dataSource='themeDataList'
                                    :fields="fields"
                                    :v-model="project.theme"
                                    id='dropdownlist'
                                    placeholder='Select a theme'
                            ></ejs-dropdownlist>
                        </b-form-group>

                        <b-form-group id="form-head-group" label="Project Head:" label-for="form-head-input">
                            <ejs-dropdownlist
                                    :dataSource='headDataList'
                                    :fields="fields"
                                    :v-model="project.head"
                                    id='dropdownlist-head'
                                    placeholder='Select the project head'
                            ></ejs-dropdownlist>
                        </b-form-group>

                        <b-form-group id="form-code-group" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required
                                    type="text"
                                    v-model="project.code"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-name-group" label="Name:" label-for="form-name-input">
                            <b-form-input
                                    id="form-name-input"
                                    placeholder="Enter Project Name"
                                    required
                                    type="text"
                                    v-model="project.name">
                            </b-form-input>
                        </b-form-group>

                        <b-form-group id="form-desc-group" label="Description:" label-for="form-desc-input">
                            <b-form-textarea
                                    id="form-desc-input"
                                    placeholder="Enter Description"
                                    required
                                    type="text"
                                    v-model="project.description">
                            </b-form-textarea>
                        </b-form-group>

                    </form>
                </b-modal>
            </div>

            <div v-else-if="isEditing">
                <b-modal
                        @hidden="clearForm"
                        @ok="updateProject(old_code)"
                        @shown="selectDropDownItemsForUpdate(project.theme, project.head)"
                        @submit="showModal = false"
                        cancel-variant="danger"
                        id="modal-project-edit"
                        ok-title="Update"
                        title="Edit Project"
                >
                    <form @submit.prevent="updateProject">
                        <b-form-group id="form-theme-group-edit" label="Theme:" label-for="form-theme-input">
                            <ejs-dropdownlist
                                    :dataSource='themeDataList'
                                    :fields="fields"
                                    :v-model="project.theme"
                                    id='dropdownlist'
                                    placeholder='Select a theme'
                            ></ejs-dropdownlist>
                        </b-form-group>

                        <b-form-group id="form-head-group-edit" label="Project Head:" label-for="form-head-input">
                            <ejs-dropdownlist
                                    :dataSource='headDataList'
                                    :fields="fields"
                                    :v-model="project.head"
                                    id='dropdownlist-head'
                                    placeholder='Select the project head'
                            ></ejs-dropdownlist>
                        </b-form-group>

                        <b-form-group id="form-code-group-edit" label="Code:" label-for="form-code-input">
                            <b-form-input
                                    id="form-code-input"
                                    placeholder="Enter Code"
                                    required
                                    type="text"
                                    v-model="project.code"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-name-group-edit" label="Name:" label-for="form-name-input">
                            <b-form-input
                                    id="form-name-input"
                                    placeholder="Enter Project Name"
                                    required
                                    type="text"
                                    v-model="project.name">
                            </b-form-input>
                        </b-form-group>

                        <b-form-group id="form-desc-group-edit" label="Description:" label-for="form-desc-input">
                            <b-form-textarea
                                    id="form-desc-input"
                                    placeholder="Enter Description"
                                    required
                                    type="text"
                                    v-model="project.description">
                            </b-form-textarea>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>

          <b-button class="float_btn" style="border-radius: 50%" v-b-modal.modal-project v-if="isAuth"
                    variant="primary">
            <span>Add Project</span> <i class="fas fa-plus-circle menu_icon"></i>
          </b-button>


          <div style="margin: auto;">
            <loading-progress
              :indeterminate="indeterminate"
              :hide-background="hideBackground"
              :progress="progressPath"
              :size="size"
              rotate
              fillDuration="2"
              rotationDuration="1"
            />
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
  isResearcher, pageStartLoader,
  respondTo401,
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
                    this.$log.info("Theme list json: ", JSON.stringify(themeList));

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
                    this.$log.info("User list json: ", JSON.stringify(headList));

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
                console.log("THEME:" + theme)
                console.log("HEAD:" + head)
                let elementTheme = document.getElementById("dropdownlist");
                elementTheme.value = theme;

                let elementHead = document.getElementById("dropdownlist-head");
                elementHead.value = head;
            },
          // stop&hide progressPath
haltProgressPath(cont=false, path=0, size=0){
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
                    setTimeout(()=> {
                    this.haltProgressPath()
                    this.$log.info("Response: " + res.status + " ", res.data['message']);
                    this.response = res.data;
                    }, this.time)
                  })
                  .catch((error) => {
                    // eslint-disable-next-line
                    this.$log.error(error);
                    });
            },

            createProject: function () {
                let self = this;
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
                })
                    .then((response) => {
                      setTimeout(()=> {
                        loader.hide()
                        this.getProject();
                        showFlashMessage(self, 'success', response.data['message'], '');
                        this.clearForm();
                        },this.time)
                    })
                    .catch((error) => {
                        this.clearForm();
                        this.$log.error(error);
                        loader.hide();
                        if (error.response) {
                            if (error.response.status === 409) {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            } else if (error.response.status === 400) {
                                showFlashMessage(self, 'error', error.response.data['message'], 'Kindly refill the form');
                            } else if (error.response.status === 401) {
                                respondTo401(self);
                            } else if (error.response.status === 403) {
                                showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
                            } else {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            }
                        }
                    });
            },

            updateProject: function (code) {
                let self = this;
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
                })
                    .then((response) => {
                      setTimeout(()=> {
                        loader.hide()
                        this.getProject();
                        showFlashMessage(self, 'success', response.data['message'], '');
                        this.clearForm();
                        },this.time)
                    })
                    .catch((error) => {
                        this.clearForm();
                        loader.hide();
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 304) {
                                showFlashMessage(self, 'info', 'Record not modified!', '');
                            } else if (error.response.status === 401) {
                                respondTo401(self);
                            } else if (error.response.status === 403) {
                                showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
                            } else {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            }
                        }
                    });
            },

            deleteProject: function (code) {
                let self = this;
                let loader = pageStartLoader(this)
                axios.delete(project_resource, {
                    headers:
                        {
                            code: code,
                          Authorization: secureStoreGetAuthString()
                        }
                })
                    .then((response) => {
                      setTimeout(()=> {
                        loader.hide()
                        this.getProject();
                        showFlashMessage(self, 'success', response.data['message'], '');
                      },this.time)
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        loader.hide();
                        if (error.response) {
                            if (error.response.status === 401) {
                                respondTo401(self);
                            } else if (error.response.status === 403) {
                                showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
                            } else {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            }
                        }
                    });
            },
        },
        created() {
            this.getProject();
        },
        components: {TopNav}
    }
</script>

<style scoped>

</style>