<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <top-nav :page_title="page_title" v-bind:search_query.sync="search"></top-nav>

                <!-- FLASH MESSAGES -->
                <FlashMessage :position="'right bottom'"></FlashMessage>
                <br>

                <!--TOP-PAGINATION-->
                <v-page :total-row="filteredList.pg_len" @page-change="pageInfo" align="center"
                        v-model="current"></v-page>
                <br>
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
                    <tr :key="publication.id" v-for="(publication, index) in filteredList.arr">
                        <td> {{ index + 1 }}</td>
                        <td> {{publication.publication_title}}</td>
                        <td> {{publication['sample.theme.name']}}</td>
                        <td> {{publication['sample.project']}}</td>
                        <td>
                            {{publication['user.first_name']}} &nbsp; {{publication['user.last_name']}} &nbsp;
                            <a :href="`mailto:${publication['user.email']}`" target="_blank">
                                <b-icon
                                        :title="`Contact author(${ publication['user.email'] })`"
                                        class="border border-info rounded"
                                        font-scale="1.5" icon="envelope"
                                        v-b-tooltip.hover variant="info"
                                ></b-icon>
                            </a>
                        </td>
                        <td> {{publication['co_authors']}}</td>

                        <td>
                            <b-icon
                                    :title="`Update ${ publication.publication_title }`" @mouseover="fillFormForUpdate(publication.publication_title, publication['sample.theme.name'],
                                     publication['user.first_name'], publication['user.last_name'], publication['co_authors'], publication.sample_results)"
                                    class="border border-info rounded" font-scale="2.0"
                                    icon="pencil" v-b-modal.modal-publication-edit
                                    v-b-tooltip.hover
                                    variant="info"
                            ></b-icon>
                            &nbsp;
                            <b-icon
                                    :title="`Delete ${ publication.publication_title }!`"
                                    @click="deletePublication(publication.publication_title)"
                                    class="border rounded bg-danger p-1" font-scale="1.85"
                                    icon="trash" v-b-tooltip.hover
                                    variant="light"
                            ></b-icon>
                            &nbsp;
                            <b-icon
                                    @click="downloadPublication(publication.publication_title)"
                                    class="border border-info rounded" font-scale="2.0"
                                    icon="download" title="Download"
                                    v-b-tooltip.hover variant="info"
                            ></b-icon>
                        </td>
                    </tr>
                    </tbody>
                </table>
                <!--TOP-PAGINATION-->
                <v-page :total-row="filteredList.pg_len" @page-change="pageInfo" align="center"
                        v-model="current"></v-page>
                <br>
            </div>

            <div v-if="!isEditing">
                <b-modal
                        :title="`Add ${page_title}`"
                        @hidden="clearForm"
                        @ok="onSubmit"
                        @submit="showModal=false"
                        cancel-variant="danger"
                        id="modal-publication"
                        ok-title="Save"
                >
                    <form @submit.prevent="createPublication">
                        <!--SAMPLE-->
                        <b-form-group id="form-sample-group" label="Sample:" label-for="form-sample-input">
                            <ejs-dropdownlist
                                    :dataSource='sampleDataList'
                                    :fields="fields"
                                    @change="prepareCreate"
                                    id='dropdownlist'
                                    placeholder='Select a sample'
                                    v-model.trim="$v.publication.sample.$model"
                            ></ejs-dropdownlist>
                            <div v-if="$v.publication.sample.$dirty">
                                <div class="error" v-if="!$v.publication.sample.required">Field is required</div>
                            </div>
                        </b-form-group>

                        <!--AUTHOR-->
                        <b-form-group id="form-user-group" label="Authors:" label-for="form-user-input">
                            <b-form-input
                                    disabled="disabled"
                                    id="form-user-input"
                                    placeholder="Enter author's name"
                                    required
                                    type="text"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group :class="{ 'form-group--error': $v.publication.co_authors.$error }"
                                      id="form-coauthors-group" label="Add CoAuthors:" label-for="form-coauthors-input">
                            <b-form-input
                                    id="form-pub-title-input"
                                    placeholder="Enter co-authors separated by a comma"
                                    required
                                    type="text"
                                    v-model.trim="$v.publication.co_authors.$model"
                            ></b-form-input>
                            <div v-if="$v.publication.co_authors.$dirty">
                                <div class="error" v-if="!$v.publication.co_authors.required">Field is required</div>
                            </div>
                        </b-form-group>

                        <b-form-group :class="{ 'form-group--error': $v.publication.title.$error }"
                                      id="form-pub-title-group" label="Publication Title:"
                                      label-for="form-pub-title-input">
                            <b-form-input
                                    id="form-pub-title-input"
                                    placeholder="Enter a title"
                                    required
                                    type="text"
                                    v-model.trim="$v.publication.title.$model"
                            ></b-form-input>
                            <div v-if="$v.publication.title.$dirty">
                                <div class="error" v-if="!$v.publication.title.required">Field is required</div>
                            </div>
                        </b-form-group>
                        <!-- todo: sample_results? can be changed to publication summary-->
                        <b-form-group :class="{ 'form-group--error': $v.publication.title.$error }"
                                      id="form-sample-results-group" label="Sample Results:"
                                      label-for="form-sample-results-input">
                            <b-form-textarea
                                    id="form-sample-results-input"
                                    placeholder="Enter sample results"
                                    required
                                    type="text"
                                    v-model.trim="$v.publication.sample_results.$model">
                            </b-form-textarea>
                            <div v-if="$v.publication.sample_results.$dirty">
                                <div class="error" v-if="!$v.publication.sample_results.required">Field is required
                                </div>
                            </div>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>
            <div v-if="isEditing">
                <b-modal
                        :title="`Edit ${page_title}`"
                        @hidden="clearForm"
                        @ok="updatePublication"
                        @submit="showModal = false"
                        cancel-variant="danger"
                        id="modal-publication-edit"
                        ok-title="Update"
                >
                    <form>
                        <!--SAMPLE-->
                        <b-form-group id="form-sample-group-edit" label="Sample:" label-for="form-sample-input">
                            <ejs-dropdownlist
                                    :dataSource='sampleDataList'
                                    :fields="fields"
                                    @change="prepareCreate"
                                    id='dropdownlist'
                                    placeholder='Select a sample'
                                    v-model.trim="$v.publication.sample.$model"
                            ></ejs-dropdownlist>
                            <div v-if="$v.publication.sample.$dirty">
                                <div class="error" v-if="!$v.publication.sample.required">Field is required</div>
                            </div>
                        </b-form-group>

                        <!--AUTHOR-->
                        <b-form-group id="form-user-group-edit" label="Authors:" label-for="form-user-input">
                            <b-form-input
                                    disabled="disabled"
                                    id="form-user-input"
                                    placeholder="Enter author's name"
                                    required
                                    type="text"
                            ></b-form-input>
                        </b-form-group>

                        <b-form-group :class="{ 'form-group--error': $v.publication.co_authors.$error }"
                                      id="form-coauthors-group-edit" label="Add CoAuthors:"
                                      label-for="form-coauthors-input">
                            <b-form-input
                                    id="form-pub-title-input"
                                    placeholder="Enter co-authors separated by a comma"
                                    required
                                    type="text"
                                    v-model.trim="$v.publication.co_authors.$model"
                            ></b-form-input>
                            <div v-if="$v.publication.co_authors.$dirty">
                                <div class="error" v-if="!$v.publication.co_authors.required">Field is required</div>
                            </div>
                        </b-form-group>

                        <b-form-group :class="{ 'form-group--error': $v.publication.title.$error }"
                                      id="form-pub-title-group-edit" label="Publication Title:"
                                      label-for="form-pub-title-input">
                            <b-form-input
                                    id="form-pub-title-input"
                                    placeholder="Enter a title"
                                    required
                                    type="text"
                                    v-model.trim="$v.publication.title.$model"
                            ></b-form-input>
                            <div v-if="$v.publication.title.$dirty">
                                <div class="error" v-if="!$v.publication.title.required">Field is required</div>
                            </div>
                        </b-form-group>
                        <!-- todo: sample_results? can be changed to publication summary-->
                        <b-form-group :class="{ 'form-group--error': $v.publication.title.$error }"
                                      id="form-sample-results-group-edit" label="Sample Results:"
                                      label-for="form-sample-results-input">
                            <b-form-textarea
                                    id="form-sample-results-input"
                                    placeholder="Enter sample results"
                                    required
                                    type="text"
                                    v-model.trim="$v.publication.sample_results.$model">
                            </b-form-textarea>
                            <div v-if="$v.publication.sample_results.$dirty">
                                <div class="error" v-if="!$v.publication.sample_results.required">Field is required
                                </div>
                            </div>
                        </b-form-group>
                    </form>
                </b-modal>
            </div>
            <b-button class="float_btn" style="border-radius: 50%" v-b-modal.modal-publication variant="primary">
                <span>Add Publication</span> <i class="fas fa-plus-circle menu_icon"></i>
            </b-button>
        </div>
    </div>
</template>

<script>
    import TopNav from "../components/TopNav";
    import axios from "axios";
    import {publication_resource, sample_resource} from "../utils/api_paths";
    import {
        extractApiDataForPub,
        getItemDataList,
        getSelectedItemSetTextFieldValue,
        paginate,
        respondTo401,
        secureStoreGetString,
        showFlashMessage
    } from "../utils/util_functions";
    import EventBus from '../components/EventBus';
    import {required} from "vuelidate/lib/validators";

    export default {
        name: "Publication",
        data() {
            return {
                page_title: "Publications",
                response: [],
                search: '',
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
                publicationList: [],

                // values for data modification
                old_title: null,
                showModal: true,
                isEditing: false,

                // data for pagination
                current: 1,
            }
        },

        validations: {
            publication: {
                title: {required},
                sample: {required},
                user: {required},
                sample_results: {required},
                co_authors: {required}
            },
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
                    this.publicationList = searchList // eslint-disable-line
                    return paginate(searchList)
                }
                return paginate(this.publicationList)
            },
        },

        methods: {
            //UTIL Fn
            pageInfo(info) {
                EventBus.$emit('page-info', {'pgInfo': info, 'pgData': this.publicationList})
            },

            onSubmit(evt) {
                this.$v.$touch();
                if (this.$v.$invalid) {
                    // stop here if form is invalid
                    evt.preventDefault()
                    return;
                }
                this.createPublication();
            },

            clearForm() {
                this.isEditing = false;
                this.old_title = null;
                this.publication.title = null;
                this.publication.sample = null;
                this.publication.user = null;
                this.publication.co_authors = null;
                this.publication.sample_results = null;
                this.$v.$reset();
            },

            fillFormForUpdate(title, theme, first_name, last_name, co_authors, sample_results) {
                this.isEditing = true;
                this.old_title = title;
                this.publication.title = title;
                this.publication.sample = theme;
                this.publication.user = first_name + " " + last_name;
                this.publication.co_authors = co_authors;
                this.publication.sample_results = sample_results;
            },

            onLoadPage() {
                getItemDataList(sample_resource).then(data => {
                    let sampleList = extractApiDataForPub(data);

                    // update local variables with data from API
                    this.fields = sampleList['fields'];
                    for (let i = 0; i < sampleList.items.length; i++) {
                        this.sampleDataList.push({
                            'Code': sampleList.items[i].sampleCode,
                            'Name': sampleList.items[i].sampleName,
                            'authorCode': sampleList.items[i].authorCode,
                            'authorName': sampleList.items[i].authorName
                        });
                    }
                })
                this.getPublication()
            },

            // methods to interact with api
            getPublication() {
                this.clearForm();
                axios.get(publication_resource)
                    .then((res) => {
                        this.$log.info("Response: " + res.status + " ", res.data['message']);
                        this.publicationList = this.response = res.data['message'];
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        this.$log.error(error);
                    });
            },

            prepareCreate() {
                let dropdownSelection = getSelectedItemSetTextFieldValue(this.sampleDataList, this.publication.sample);
                this.publication.user = dropdownSelection.authorCode
                this.publication.sample = dropdownSelection.sampleCode
                document.getElementById("form-user-input").value = dropdownSelection.authorText;
            },

            createPublication() {
                let self = this;

                axios.post(publication_resource, {
                    publication_title: this.publication.title,
                    sample: this.publication.sample,
                    user: this.publication.user,
                    sample_results: this.publication.sample_results,
                    co_authors: this.publication.co_authors
                }, {
                    headers: {
                        Authorization: secureStoreGetString()
                    }
                })
                    .then((response) => {
                        this.getPublication();
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
                                respondTo401(self);
                            } else {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            }
                        }
                    });
                this.clearForm();
            },

            updatePublication: function (evt) {
                this.$v.$touch();
                if (this.$v.$invalid) {
                    evt.preventDefault()
                } else {
                    let self = this;
                    axios.put(publication_resource, {
                        publication_title: this.publication.title,
                        sample: this.publication.sample,
                        user: this.publication.user,
                        sample_results: this.publication.sample_results,
                        co_authors: this.publication.co_authors
                    }, {
                        headers: {
                            title: this.old_title,
                            Authorization: secureStoreGetString()
                        }
                    })
                        .then((response) => {
                            this.getPublication();
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
                                    respondTo401(self);
                                } else if (error.response.status === 403) {
                                    showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
                                } else {
                                    showFlashMessage(self, 'error', error.response.data['message'], '');
                                }
                            }
                        });
                    this.clearForm();
                }
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
                        this.clearForm();
                    })
                    .catch((error) => {
                        this.$log.error(error);
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
                this.clearForm();
            },

            searchData() {
                return this.response.filter(pub => {
                    let byTitle = pub.publication_title.toLowerCase().includes(this.search.toLowerCase())
                    let byTheme = pub['sample.theme.name'].toLowerCase().includes(this.search.toLowerCase())
                    let byProject = pub['sample.project'].toLowerCase().includes(this.search.toLowerCase())
                    let byAuthor = pub['user.first_name'].toLowerCase().includes(this.search.toLowerCase())
                    let byCoAuthor = pub['co_authors'].toLowerCase().includes(this.search.toLowerCase())

                    if (byTitle) {
                        return byTitle
                    } else if (byTheme) {
                        return byTheme
                    } else if (byProject) {
                        return byProject
                    } else if (byAuthor) {
                        return byAuthor
                    } else if (byCoAuthor) {
                        return byCoAuthor
                    }
                })
            }
        },
        components: {TopNav},
        created() {
            this.onLoadPage();
        },
    }
</script>

<style scoped>

</style>