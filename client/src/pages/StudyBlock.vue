<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-sm-12">
        <top-nav :page_title="page_title" v-bind:search_query.sync="search"></top-nav>

        <FlashMessage :position="'right bottom'"></FlashMessage>
        <br>

        <!-- FILTER CARD SECTION -->
        <filter-card :all-filters="allFilters"></filter-card>
        <br>

        <!--TOP-PAGINATION-->
        <v-page v-model="current" :total-row="matchFiltersAndSearch.pg_len" align="center"
                @page-change="pageInfo"></v-page>
        <br>
        <table class=" table table-hover">
          <thead>
          <tr>
            <th class="table-header-style" scope="col"> Id</th>
            <th class="table-header-style" scope="col"> Site</th>
            <th class="table-header-style" scope="col"> Area</th>
            <th class="table-header-style" scope="col"> Code</th>
            <th v-if="isAuth" class="table-header-style" scope="col"> Actions</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(study_block, index) in matchFiltersAndSearch.arr" :key="study_block.id">
            <td> {{ index + 1 }}</td>
            <td> {{ study_block.area }}</td>
            <td> {{ study_block.name }}</td>
            <td> {{ study_block.code }}</td>

            <td v-if="isAuth">
              <b-icon
                  v-b-modal.modal-study_block-edit
                  v-b-tooltip.hover
                  :font-scale="`${font_scale}`" :title="`Update ${ study_block.name }`"
                  class="border border-info rounded" icon="pencil"
                  variant="info"
                  @mouseover="fillFormForUpdate(study_block.area, study_block.name, study_block.code)"
              ></b-icon>
              &nbsp;
              <b-icon
                  v-b-tooltip.hover :font-scale="`${font_scale}`"
                  :title="`Delete ${study_block.name}!`" class="border rounded bg-danger p-1"
                  icon="trash" variant="light"
                  @click="deleteStudyBlock(study_block.code)"
              ></b-icon>
            </td>
          </tr>
          </tbody>
        </table>
        <!--BOTTOM-PAGINATION-->
        <v-page v-model="current" :total-row="matchFiltersAndSearch.pg_len" align="center"
                @page-change="pageInfo"></v-page>
        <br>
      </div>

      <div v-if="!isEditing">
        <b-modal
            id="modal-study_block"
            cancel-variant="danger"
            ok-title="Save"
            title="Add StudyBlock"
            @hidden="clearForm"
            @ok="onSubmit"
            @submit="showModal = false"
        >
          <form @submit.prevent="createStudyBlock">

            <!-- AREA -->
            <b-form-group id="form-area-group"
                          :class="{ 'form-group--error': $v.study_block.area.$error }" label="Area:" label-for="form-area-input">
              <b-form-input
                  id="form-area-input" v-model.trim="$v.study_block.area.$model"
                  placeholder="Enter Area" required type="text"
              ></b-form-input>
              <div v-if="$v.study_block.area.$dirty">
                <div v-if="!$v.study_block.area.required" class="error">Field is required</div>
              </div>
            </b-form-group>

            <!-- NAME -->
            <b-form-group id="form-name-group"
                          :class="{ 'form-group--error': $v.study_block.name.$error }" label="Name:" label-for="form-name-input">
              <b-form-input
                  id="form-name-input"
                  v-model.trim="$v.study_block.name.$model"
                  placeholder="Enter Name"
                  required
                  type="text"
              ></b-form-input>
              <div v-if="$v.study_block.name.$dirty">
                <div v-if="!$v.study_block.name.required" class="error">Field is
                  required
                </div>
              </div>
            </b-form-group>

            <!-- CODE -->
            <b-form-group id="form-code-group"
                          :class="{ 'form-group--error': $v.study_block.code.$error }" label="Code:" label-for="form-code-input">
              <b-form-input
                  id="form-code-input"
                  v-model.trim="$v.study_block.code.$model"
                  placeholder="Enter Code"
                  required
                  type="text"></b-form-input>
              <div v-if="$v.study_block.code.$dirty">
                <div v-if="!$v.study_block.code.required" class="error">Field is
                  required
                </div>
              </div>
            </b-form-group>
          </form>
        </b-modal>
      </div>

      <div v-else-if="isEditing">
        <b-modal
            id="modal-study_block-edit"
            cancel-variant="danger"
            ok-title="Update"
            title="Edit StudyBlock"
            @hidden="clearForm"
            @ok="updateStudyBlock"
            @submit="showModal = false"
        >
          <form @submit.prevent="updateStudyBlock">

            <!-- AREA -->
            <b-form-group id="form-area-group-edit"
                          :class="{ 'form-group--error': $v.study_block.area.$error }" label="Name:" label-for="form-area-input">
              <b-form-input
                  id="form-area-input" v-model.trim="$v.study_block.area.$model"
                  placeholder="Enter Area" required type="text"
              ></b-form-input>
              <div v-if="$v.study_block.area.$dirty">
                <div v-if="!$v.study_block.area.required" class="error">Field is required</div>
              </div>
            </b-form-group>

            <!-- NAME -->
            <b-form-group id="form-name-group-edit"
                          :class="{ 'form-group--error': $v.study_block.name.$error }" label="Name:" label-for="form-name-input">
              <b-form-input
                  id="form-name-input"
                  v-model.trim="$v.study_block.name.$model"
                  placeholder="Enter Name"
                  required
                  type="text"
              ></b-form-input>
              <div v-if="$v.study_block.name.$dirty">
                <div v-if="!$v.study_block.name.required" class="error">Field is
                  required
                </div>
              </div>
            </b-form-group>

            <!-- CODE -->
            <b-form-group id="form-code-group-edit"
                          :class="{ 'form-group--error': $v.study_block.code.$error }" label="Code:" label-for="form-code-input">
              <b-form-input
                  id="form-code-input"
                  v-model.trim="$v.study_block.code.$model"
                  placeholder="Enter Code"
                  required
                  type="text"></b-form-input>
              <div v-if="$v.study_block.code.$dirty">
                <div v-if="!$v.study_block.code.required" class="error">Field is
                  required
                </div>
              </div>
            </b-form-group>
          </form>
        </b-modal>
      </div>
      <div v-if="isAuth">
        <b-button v-b-modal.modal-study_block class="float_btn" style="border-radius: 50%" variant="primary">
          <span>Add StudyBlock</span> <i class="fas fa-plus-circle menu_icon"></i>
        </b-button>
      </div>

      <div style="margin: auto;">
        <loading-progress :hide-background="hideBackground" :indeterminate="indeterminate" :progress="progressPath"
                          :size="size" fillDuration="2" rotate rotationDuration="1"/>
      </div>
    </div>
  </div>
</template>

<script>
import {required} from "vuelidate/lib/validators";
import EventBus from "@/components/EventBus";
import {
  handleError,
  isAdmin,
  pageStartLoader,
  paginate,
  secureStoreGetAuthString,
  showFlashMessage
} from "@/utils/util_functions";
import {font_scale} from '@/utils/constants';
import axios from "axios";
import {study_block_resource} from "@/utils/api_paths";
import TopNav from "@/components/TopNav";
import FilterCard from "@/components/FilterCard";

export default {
  name: "StudyBlock",
  data() {
    return {
      page_title: "Study Blocks",
      response: [],
      search: '',
      studyBlockList: [],
      filters: [],

      study_block: {area: '', name: '', code: ''},

      font_scale,

      // variable to check user status and role
      isAuth: null,

      // loader-time
      time: 2000,

      // progressPath
      indeterminate: true, hideBackground: true, progressPath: 5, size: 180,

      // values for data modification
      old_code: null, showModal: true, isEditing: false,

      // data for pagination
      current: 1, page_array: [], page_info: {},
    };
  },

  validations: {study_block: {area: {required}, name: {required}, code: {required}}},

  mounted() {
    EventBus.$on('searchQuery', (payload) => {
      this.search = payload
      this.searchData()
    })

    EventBus.$on('filters', (payload) => {
      this.filters = payload
      if (this.filters.length === 0) {
        this.studyBlockList = this.response
      }
    })
  },

  computed: {
    /**
     * return a list of dictionaries containing the filters required
     */
    allFilters: function () {
      return [
        {
          'By Site': this.response
              .map(({area: site}) => site)
              .filter((value, index, self) => self.indexOf(value) === index),
        },
      ]
    },

    /**
     * function checks for any filters or searches applied to the data and returns filtered/searched list.
     * @returns {null|[]|*}
     */
    matchFiltersAndSearch: function () {
      let searchList = this.search ? this.searchData() : null

      /* studyBlockList,which is a copy of response, is passed as the data here instead of response to avoid
      mutating response data.*/
      let filteredData = this.filterData(this.studyBlockList)

      let filterBySite = filteredData.site
      let filterByArea = filteredData.area

      if (searchList !== null) {
        return paginate(searchList)
      } else if (this.filters.length > 1) {
        // Possibly, multiple filters have been applied. Return the array with the least elements
        return filterBySite.length < filterByArea.length ?
            paginate(filterBySite) : paginate(filterByArea)
      } else if (filterBySite !== null && filterBySite.length > 0) {
        this.studyBlockList = filterBySite // eslint-disable-line
        this.filterData(filterBySite)
        return paginate(filterBySite)
      } else if (filterByArea !== null && filterByArea.length > 0) {
        this.freezerList = filterByArea // eslint-disable-line
        this.filterData(filterByArea)
        return paginate(filterByArea)
      }
      return paginate(this.studyBlockList)
    },
  },

  methods: {
    // util functions
    onSubmit(evt) {
      this.$v.$touch();
      if (this.$v.$invalid) {
        evt.preventDefault()
        return;
      }
      this.createStudyBlock();
    },

    clearForm() {
      this.study_block.area = null;
      this.study_block.name = null;
      this.study_block.code = null;
      this.isEditing = false;
      this.$v.$reset();
    },

    fillFormForUpdate(area, name, code) {
      this.study_block.area = area;
      this.study_block.name = name;
      this.study_block.name = name;
      this.study_block.code = code;
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

    // pagination
    pageInfo(info) {
      EventBus.$emit('page-info', {'pgInfo': info, 'pgData': this.studyBlockList})
    },

    // api interaction functions
    getStudyBlock() {
      this.isAuth = isAdmin()

      axios.get(study_block_resource)
          .then((res) => {
            setTimeout(() => {
              this.haltProgressPath();
              this.studyBlockList = this.response = res.data['message'];
            }, this.time)
          })
          .catch((error) => {
            // eslint-disable-next-line
            this.$log.error(error);
          });
    },

    createStudyBlock: function () {
      let self = this;
      let loader = pageStartLoader(this)

      axios.post(study_block_resource, {
        area: this.study_block.area,
        name: this.study_block.name,
        code: this.study_block.code,
      }, {
        headers: {
          Authorization: secureStoreGetAuthString()
        }
      }).then((response) => {
            setTimeout(() => {
              loader.hide()
              this.getStudyBlock();
              showFlashMessage(self, 'success', 'Success', response.data['message'])
            }, this.time)
          }).catch((error) => {handleError(this, error, loader)});
      this.clearForm();
    },

    updateStudyBlock: function (evt) {
      this.$v.$touch();
      if (this.$v.$invalid) {
        evt.preventDefault()
      } else {
        let self = this;
        let loader = pageStartLoader(this)
        axios.put(study_block_resource, {
          area: this.study_block.area,
          name: this.study_block.name,
          code: this.study_block.code,
        }, {
          headers:
              {
                code: this.old_code,
                Authorization: secureStoreGetAuthString()
              }
        })
            .then((response) => {
              setTimeout(() => {
                loader.hide()
                this.getStudyBlock();
                showFlashMessage(self, 'success', 'Success', response.data['message'])
              }, this.time)
            }).catch((error) => { handleError(this, error, loader) });
        this.clearForm();
      }
    },

    deleteStudyBlock: function (code) {
      let self = this;
      let loader = pageStartLoader(this)

      axios.delete(study_block_resource, {
        headers: {
          code: code,
          Authorization: secureStoreGetAuthString()
        }
      }).then((response) => {
        setTimeout(() => {
          loader.hide()
          this.getStudyBlock();
          showFlashMessage(self, 'success', 'Success', response.data['message'])
        }, this.time)
      }).catch((error) => { handleError(this, error, loader) });
      this.clearForm();
    },

    /* Methods associated with searching and filtering of data in the page */
    filterData(data) {
      let filterBySite = this.filters.length
          ? data.filter(study_block => this.filters.some(filter => study_block.area.match(filter)))
          : null // site

      let filterByArea = this.filters.length
          ? data.filter(study_block => this.filters.some(filter => study_block.name.match(filter)))
          : null // area

      return {'site': filterBySite, 'area': filterByArea}
    },

    searchData() {
      return this.response.filter(study_block => {
        return study_block.name.toLowerCase().includes(this.search.toLowerCase())
      })
    }
  },
  created() {
    this.getStudyBlock();
  }, components: {TopNav, FilterCard}
}

</script>
