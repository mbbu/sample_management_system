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
                        <th scope="col"> Title</th>
                        <th scope="col"> Theme</th>
                        <th scope="col"> Project</th>
                        <th scope="col"> Author</th>
                        <th scope="col"> Co-Authors</th>
                        <th scope="col"> Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr :key="publication.id" v-for="(publication, index) in response.message">
                        <td> {{ index + 1 }}</td>
                        <td> {{publication.publication_title}}</td>
                        <td> {{publication['sample.theme.name']}}</td>
                        <td> {{publication['sample.project']}}</td>
                        <td>
                            {{publication['user.first_name']}} &nbsp; {{publication['user.last_name']}} &nbsp;
                            <b-icon
                                    icon="envelope" font-scale="1.5"
                                    class="border border-info rounded" variant="info"
                                    v-b-tooltip.hover :title="`Contact author(${ publication['user.email'] })`"
                            ></b-icon>
                        </td>
                        <td> {{publication['co_authors']}}</td>

                        <td>
                            <b-icon
                                    icon="pencil" font-scale="2.0"
                                    class="border border-info rounded" variant="info"
                                    v-b-tooltip.hover :title="`Update ${ publication.publication_title }`"
                                    v-b-modal.modal-publication-edit
                                    @mouseover="fillFormForUpdate(tray['rack.number'], tray.number, tray.code)"
                            ></b-icon>
                            &nbsp;
                            <b-icon
                                    icon="trash" font-scale="1.85"
                                    class="border rounded bg-danger p-1" variant="light"
                                    v-b-tooltip.hover :title="`Delete ${ publication.publication_title }!`"
                                    @click="deletePublication(publication.publication_title)"
                            ></b-icon>
                            &nbsp;
                            <b-icon
                                    icon="download" font-scale="2.0" title="Download"
                                    class="border border-info rounded" variant="info"
                                    v-b-tooltip.hover @click="downloadPublication(publication.publication_title)"
                            ></b-icon>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>

            <div v-if="!isEditing">
                <b-modal
                        :title="`Add ${page_title}`"
                        id="modal-publication"
                        ok-title="Save"
                        cancel-variant="danger"
                        @ok="createPublication"
                        @submit="clearForm"
                        @hidden="clearForm"
                >
                    <form @submit.prevent="createPublication">
                        <b-form-group id="form-user-group" label="Author:" label-for="form-user-input">
                            <ejs-dropdownlist
                                    id='dropdownlist'
                                    :dataSource='authorDataList'
                                    :fields="fields"
                                    placeholder='Select an author'
                                    :v-model="publication.user"
                            ></ejs-dropdownlist>
                        </b-form-group>

                        <b-form-group id="form-coauthors-group" label="Add CoAuthors:" label-for="form-coauthors-input">
                            <b-form-input
                                    id="form-pub-title-input"
                                    placeholder="Enter co-authors separated by a comma"
                                    required="true"
                                    type="text"
                                    v-model="publication.co_authors"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-sample-group" label="Sample:" label-for="form-sample-input">
                            <ejs-dropdownlist
                                    id='dropdownlist'
                                    :dataSource='sampleDataList'
                                    :fields="fields"
                                    placeholder='Select a sample'
                                    :v-model="publication.sample"
                            ></ejs-dropdownlist>
                        </b-form-group>

                        <b-form-group id="form-pub-title-group" label="Publication Title:"
                                      label-for="form-pub-title-input">
                            <b-form-input
                                    id="form-pub-title-input"
                                    placeholder="Enter a title"
                                    required="true"
                                    type="text"
                                    v-model="publication.title"
                            ></b-form-input>
                        </b-form-group>
                        <!-- todo: sample_results? can be changed to publication summary-->
                        <b-form-group id="form-sample-results-group" label="Sample Results:"
                                      label-for="form-sample-results-input">
                            <b-form-textarea
                                    id="form-sample-results-input"
                                    placeholder="Enter sample results"
                                    required="true"
                                    type="text"
                                    v-model="publication.sample_results">
                            </b-form-textarea>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>
            {{isEditing}}
            <div v-if="isEditing">
                <b-modal
                        :title="`Edit ${page_title}`"
                        id="modal-publication-edit"
                        ok-title="Update"
                        cancel-variant="danger"
                        @ok="UpdatePublication(old_title)"
                        @submit="showModal = false"
                        @hidden="clearForm"
                        @shown="selectItemForUpdate(publication.user, publication.sample)"
                >
                    <form @submit.prevent="updatePublication">
                        <b-form-group id="form-user-group-edit" label="Author:" label-for="form-user-input">
                            <ejs-dropdownlist
                                    id='dropdownlist'
                                    :dataSource='authorDataList'
                                    :fields="fields"
                                    placeholder='Select an author'
                                    :v-model="publication.user"
                            ></ejs-dropdownlist>
                        </b-form-group>

                        <b-form-group id="form-coauthors-group-edit" label="Add CoAuthors:"
                                      label-for="form-coauthors-input">
                            <b-form-input
                                    id="form-pub-title-input"
                                    placeholder="Enter co-authors separated by a comma"
                                    required="true"
                                    type="text"
                                    v-model="publication.co_authors"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group id="form-sample-group-edit" label="Sample:" label-for="form-sample-input">
                            <ejs-dropdownlist
                                    id='dropdownlist'
                                    :dataSource='sampleDataList'
                                    :fields="fields"
                                    placeholder='Select a sample'
                                    :v-model="publication.sample"
                            ></ejs-dropdownlist>
                        </b-form-group>

                        <b-form-group id="form-pub-title-group-edit" label="Publication Title:"
                                      label-for="form-pub-title-input">
                            <b-form-input
                                    id="form-pub-title-input"
                                    placeholder="Enter a title"
                                    required="true"
                                    type="text"
                                    v-model="publication.title"
                            ></b-form-input>
                        </b-form-group>
                        <!-- todo: sample_results? can be changed to publication summary-->
                        <b-form-group id="form-sample-results-group-edit" label="Sample Results:"
                                      label-for="form-sample-results-input">
                            <b-form-textarea
                                    id="form-sample-results-input"
                                    placeholder="Enter sample results"
                                    required="true"
                                    type="text"
                                    v-model="publication.sample_results">
                            </b-form-textarea>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>
            <b-button class="float_btn"
                      v-b-modal.modal-publication variant="primary"
            >Add Publication
            </b-button>
        </div>
    </div>
</template>

<script>
    import TopNav from "../components/TopNav";
    import axios from "axios";
    import {publication_resource} from "../utils/api_paths";
    import {secureStoreGetString, showFlashMessage} from "../utils/util_functions";

    export default {
        name: "Publication",
        data() {
            return {
                page_title: "Publications",
                response: [],
                publication: {
                    title: null,
                    sample: null,
                    user: null,
                    sample_results: null,
                    co_authors: null
                },

                //
                fields: {text: '', value: ''},
                sampleDataList: [],
                authorDataList: [],

                // values for data modification
                old_title: null,
                showModal: true,
                isEditing: false,
            }
        },

        methods: {

            // methods to interact with api
            getPublication() {
                // this.clearForm();
                axios.get(publication_resource)
                    .then((res) => {
                        this.$log.info("Response: " + res.status + " " + res.data['message']);
                        this.response = res.data;
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        this.$log.error(error);
                    });
            },

            deletePublication: function (title) {
                let self = this;
                axios.delete(publication_resource, {
                    headers:
                        {
                            title: title,
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getPublication();
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
        components: {TopNav},
        created() {
            this.getPublication();
        },
    }
</script>

<style scoped>

</style>