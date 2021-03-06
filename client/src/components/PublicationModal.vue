<template>
  <b-modal
      @hidden="clearForm"
      @ok="onSubmit"
      @shown="prepareCreate"
      cancel-variant="danger"
      id="modal-publication-edit"
      ok-title="Update"
      title="Edit Publication"
      v-model="showModalUpdate"
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
            id="form-pub-coauthors-input"
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
</template>

<script>
import {required} from "vuelidate/lib/validators";
import {
  getSelectedItemSetTextFieldValue,
  respondTo401,
  secureStoreGetAuthString,
  showFlashMessage
} from "@/utils/util_functions";
import {publication_resource} from "@/utils/api_paths";
import axios from "axios";
import EventBus from "@/components/EventBus";

export default {
  name: "PublicationModal",
  data() {
    return {
      publication: {
        title: null,
        sample: null,
        user: null,
        sample_results: null,
        co_authors: null
      },

      fields: {text: '', value: ''},
      sampleDataList: [],
      authorDataList: [],
      publicationList: [],

      showModalUpdate: false,

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
    EventBus.$on('update-publication', payload => {
      this.publication.title = this.old_title = payload.publication_title !== undefined ? payload.publication_title : payload.title
      this.publication.sample = payload['sample.code'] !== undefined ? payload['sample.code'] : payload.sample
      this.publication.user = (payload['user.first_name'] + " " + payload['user.last_name']) !== undefined + " " + undefined
          ? payload['user.first_name'] + " " + payload['user.last_name'] : payload.user
      this.publication.sample_results = payload.sample_results
      this.publication.co_authors = payload.co_authors

      // additional data for modal form
      this.showModalUpdate = !this.showModalUpdate
      this.sampleDataList = payload.sampleDataList
      this.fields = payload.fields

      this.prepareCreate()
    })

  },
  methods: {
    onSubmit(evt) {
      this.$v.$touch();
      if (this.$v.$invalid) {
        evt.preventDefault()
        return;
      }
      this.showModalUpdate = !this.showModalUpdate
      this.updatePublication();
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
      this.showModalUpdate = false
    },

    prepareCreate() {
      let dropdownSelection = getSelectedItemSetTextFieldValue(this.sampleDataList, this.publication.sample);

      if (dropdownSelection !== undefined) {
        this.publication.user = dropdownSelection.authorCode
        this.publication.sample = dropdownSelection.sampleCode
        document.getElementById("form-user-input").value = dropdownSelection.authorText;
      }
    },

    updatePublication: function () {
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
          Authorization: secureStoreGetAuthString()
        }
      })
          .then((response) => {
            showFlashMessage(self, 'success', response.data['message'], '');
            this.clearForm();

            // notify parent in order to update data
            EventBus.$emit('update-success')
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
}
</script>
