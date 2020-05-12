<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <top-nav :page_title="page_title"></top-nav>

                <FlashMessage :position="'center bottom'"></FlashMessage>
                <br> <br>
                <table class=" table table-hover">
                    <thead>
                    <tr>
                        <th scope="col"> Id</th>
                        <th scope="col"> Name</th>
                        <th scope="col"> Theme</th>
                        <th scope="col"> Project Head</th>
                        <th scope="col"> Code</th>
                        <th scope="col"> Description</th>
                        <th scope="col"> Actions</th>
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
                                        font-scale="1.5" icon="envelope"
                                        v-b-tooltip.hover variant="info"
                                ></b-icon>
                            </a>
                        </td>
                        <td> {{ project.code }}</td>
                        <td> {{ project.description }}</td>

                        <td>
                            <b-icon
                                    :title="`Update project ${ project.name }`"
                                    @mouseover="fillFormForUpdate(project.code, project.name, project.description, project['theme.name'],
                                    project['lead.first_name'] + ' ' + project['lead.last_name'])"
                                    class="border border-info rounded" font-scale="2.0"
                                    icon="pencil" v-b-modal.modal-project-edit
                                    v-b-tooltip.hover
                                    variant="info"
                            ></b-icon>
                            &nbsp;
                            <b-icon
                                    :title="`Delete project ${project.name}!`" @click="deleteProject(project.code)"
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
                                    required="true"
                                    type="text"
                                    v-model="project.code"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-name-group" label="Name:" label-for="form-name-input">
                            <b-form-input
                                    id="form-name-input"
                                    placeholder="Enter Project Name"
                                    required="true"
                                    type="text"
                                    v-model="project.name">
                            </b-form-input>
                        </b-form-group>

                        <b-form-group id="form-desc-group" label="Description:" label-for="form-desc-input">
                            <b-form-textarea
                                    id="form-desc-input"
                                    placeholder="Enter Description"
                                    required="true"
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
                                    required="true"
                                    type="text"
                                    v-model="project.code"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-name-group-edit" label="Name:" label-for="form-name-input">
                            <b-form-input
                                    id="form-name-input"
                                    placeholder="Enter Project Name"
                                    required="true"
                                    type="text"
                                    v-model="project.name">
                            </b-form-input>
                        </b-form-group>

                        <b-form-group id="form-desc-group-edit" label="Description:" label-for="form-desc-input">
                            <b-form-textarea
                                    id="form-desc-input"
                                    placeholder="Enter Description"
                                    required="true"
                                    type="text"
                                    v-model="project.description">
                            </b-form-textarea>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>
            <b-button class="float_btn"
                      v-b-modal.modal-project variant="primary"
            >Add Project
            </b-button>
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
        secureStoreGetString,
        showFlashMessage
    } from "../utils/util_functions";
    import {project_resource, theme_resource, user_resource} from "../utils/api_paths";
    import axios from "axios";
    import TopNav from "@/components/TopNav";

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

            // Functions to interact with api
            getProject() {
                this.clearForm();
                axios.get(project_resource)
                    .then((res) => {
                        this.$log.info("Response: " + res.status + " ", res.data['message']);
                        this.response = res.data;
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

                axios.post(project_resource, {
                    code: this.project.code,
                    name: this.project.name,
                    head: this.project.head,
                    theme: this.project.theme,
                    description: this.project.description,
                }, {
                    headers:
                        {
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getProject();
                        showFlashMessage(self, 'success', response.data['message'], '');
                        this.clearForm();
                    })
                    .catch((error) => {
                        this.clearForm();
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 409) {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            } else if (error.response.status === 400) {
                                showFlashMessage(self, 'error', error.response.data['message'], 'Kindly refill the form');
                            } else if (error.response.status === 401) {
                                showFlashMessage(self, 'error', "Session Expired", 'You need to log in to perform this operation');
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
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getProject();
                        showFlashMessage(self, 'success', response.data['message'], '');
                        this.clearForm();
                    })
                    .catch((error) => {
                        this.clearForm();
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 304) {
                                showFlashMessage(self, 'info', 'Record not modified!', '');
                            } else if (error.response.status === 401) {
                                showFlashMessage(self, 'error', "Session Expired", 'You need to log in to perform this operation');
                            } else {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            }
                        }
                    });
            },

            deleteProject: function (code) {
                let self = this;
                axios.delete(project_resource, {
                    headers:
                        {
                            code: code,
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getProject();
                        showFlashMessage(self, 'success', response.data['message'], '');
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 401) {
                                showFlashMessage(self, 'error', "Session Expired", 'You need to log in to perform this operation');
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