<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-sm-12">
        <top-nav :page_title="page_title" v-bind:search_query.sync="search"></top-nav>

        <!-- FLASH MESSAGES -->
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
            <th class="table-header-style" scope="col"> Study Block(Site)</th>
            <th class="table-header-style" scope="col"> Date of Collection</th>
            <th class="table-header-style" scope="col"> Cattle ID</th>
            <th v-if="isAuth" class="table-header-style" scope="col"> Actions</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(house_hold_data, index) in matchFiltersAndSearch.arr" :key="house_hold_data.id">
            <td> {{ index + 1 }}</td>
            <td> {{ house_hold_data['study_block.name'] }}</td>
            <td> {{ house_hold_data.date_collected }}</td>
            <td> {{ house_hold_data.cattle_id }}</td>

            <td v-if="isAuth">
              <b-icon
                  v-b-modal.modal-house-data
                  v-b-tooltip.hover
                  :font-scale="`${font_scale}`" class="border border-info rounded"
                  icon="eye-fill"
                  title="View"
                  variant="info" @click="viewHouseData(house_hold_data)"
              ></b-icon>
              &nbsp;
              <b-icon
                  v-b-modal.modal-house_hold_data-edit
                  v-b-tooltip.hover :font-scale="`${font_scale}`"
                  :title="`Update house_hold_data ${ house_hold_data.farmer }`" class="border border-info rounded"
                  icon="pencil" variant="info"
                  @mouseover="fillFormForUpdate(house_hold_data)"
              ></b-icon>
              &nbsp;
              <b-icon
                  v-b-tooltip.hover
                  :font-scale="`${font_scale}`"
                  :title="`Delete house_hold_data ${house_hold_data.farmer}!`" class="border rounded bg-danger p-1"
                  icon="trash" variant="light"
                  @click="deleteHouseHoldData(house_hold_data.code)"
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

      <!--MODAL TO SHOW EXTRA DATA-->
      <b-modal id="modal-house-data"
               title="House Hold Info"
      >
        <h4><em>Cattle Id:</em> {{ house_data.cattle_id }}</h4><br>

        <vue-tiny-tabs id="my-view-tabs" :anchor="false" :closable="false" :hideTitle="true" class="tinytabs tabs">
          <div id="farmer-info-view" class="section tab">
            <h4 class="title"><small><b>General Info</b></small></h4>
            <!--SITE-->
            <p><em>Site:</em> {{ house_data['study_block.area'] }}</p>
            <!--STUDY-BLOCK-->
            <p><em>Study Block:</em> {{ house_data['study_block.name'] }}</p>
            <!--DATE COLLECTED-->
            <p><em>Date Collected:</em> {{ house_data.date_collected }}</p>
            <!--FARMER-->
            <p><em>Farmer Name:</em> {{ house_data.farmer }}</p>
          </div>

          <div id="cattle-info-view" class="section tab">
            <h4 class="title"><small><b>Cattle Info</b></small></h4>
            <!--CATTLE_ID-->


            <!--CATTLE NAME-->
            <p><em>Cattle Name:</em> {{ house_data.cattle_name }}</p>

            <!--CATTLE COLOR-->
            <p><em>Color:</em> {{ house_data.cattle_color }}</p>


            <!--CATTLE COLLAR-->
            <p><em>Collar:</em> {{ house_data.collar }}</p>

            <!--CATTLE Sex-->
            <p><em>Sex:</em> {{ house_data.cattle_sex }}</p>
          </div>

          <div id="health-info-view" class="section tab">
            <h4 class="title"><small><b>Health Info</b></small></h4>

            <!--CATTLE WEIGHT-->
            <p><em>Weight:</em> {{ house_data.weight }} kg</p>

            <!--CATTLE PCV-->
            <p><em>PCV:</em> {{ house_data.pcv }}</p>

            <!--CATTLE Diagnosis-->
            <p><em>Diagnosis(Dx):</em> <br> {{ house_data.diagnosis }}</p>

            <!--CATTLE Treatment-->
            <p><em>Treatment(Rx):</em> <br> {{ house_data.treatment }}</p>

            <!--CATTLE CC/ML-->
            <p><em>Dosage:</em> {{ house_data.cc }} cc</p>

            <!--CATTLE Notes-->
            <p><em>Notes:</em> <br> {{ house_data.notes }}</p>
          </div>
        </vue-tiny-tabs>

        <template v-slot:modal-footer="{ ok, cancel, hide }">
          <!-- Emulate built in modal footer ok and cancel button actions -->
          <b-button size="md" variant="primary-outline" @click="cancel()">Cancel</b-button>
          <b-button v-b-modal.modal-house_hold_data-edit data-dismiss="modal" data-target="#modal-house_hold_data-edit"
                    data-toggle="modal" size="md" variant="primary"
                    @click="fillFormForUpdate(house_data)"> Update
          </b-button>
          <b-button size="md"
                    variant="danger" @click=" close() && deleteHouseHoldData(house_data.code)"> Delete
          </b-button>
        </template>
      </b-modal>

      <div v-if="!isEditing">
        <b-modal id="modal-house_hold_data"
                 :title="`Add ${page_title}`" cancel-variant="danger" ok-title="Save"
                 @hidden="clearForm" @ok="onSubmit" @submit="showModal=false"
        >
          <form @submit.prevent="createHouseHoldData">
            <vue-tiny-tabs id="mytabs" :anchor="false" :closable="false" :hideTitle="true" class="tinytabs tabs">
              <div id="farmer-info" class="section tab">
                <h4 class="title"><small><b>Farmer Info</b></small></h4>

                <!--STUDY-BLOCK-->
                <b-form-group :class="{ 'form-group--error': $v.house_hold_data.study_block.$error }"
                    id="form-study_block-group" label="Study Block:" label-for="form-study_block-input">
                  <ejs-dropdownlist
                      id='dropdownlist'
                      :dataSource='studyBlockDataList'
                      :fields="fields"
                      v-model.trim="$v.house_hold_data.study_block.$model"
                      placeholder='Select a study block'
                  ></ejs-dropdownlist>
                  <div v-if="$v.house_hold_data.study_block.$dirty">
                      <div class="error" v-if="!$v.house_hold_data.study_block.required">Field is required</div>
                  </div>
                </b-form-group>

                <!--FARMER-->
                <b-form-group :class="{ 'form-group--error': $v.house_hold_data.farmer.$error }"
                    id="form-farmer-group" label="Farmer Name:" label-for="form-farmer-input">
                  <b-form-input id="form-farmer-input" v-model.trim="$v.house_hold_data.farmer.$model"
                                placeholder="Enter Farmer Name" required type="text"></b-form-input>
                </b-form-group>
                <div v-if="$v.house_hold_data.farmer.$dirty">
                    <div class="error" v-if="!$v.house_hold_data.farmer.required">Field is required</div>
                </div>
              </div>

              <div id="cattle-info" class="section tab">
                <h4 class="title"><small><b>Cattle Info</b></small></h4>
                <!--CATTLE_ID-->
                <b-form-group :class="{ 'form-group--error': $v.house_hold_data.cattle_id.$error }"
                    id="form-cattle_id-group" label="Cattle ID:" label-for="form-cattle_id-input">
                  <b-form-input id="form-cattle_id-input" v-model.trim="$v.house_hold_data.cattle_id.$model"
                                placeholder="Enter Cattle ID" required type="text"></b-form-input>
                  <div v-if="$v.house_hold_data.cattle_id.$dirty">
                    <div class="error" v-if="!$v.house_hold_data.cattle_id.required">Field is required</div>
                  </div>
                </b-form-group>

                <!--CATTLE NAME-->
                <b-form-group :class="{ 'form-group--error': $v.house_hold_data.cattle_name.$error }"
                    id="form-cattle_name-group" label="Cattle Name:" label-for="form-cattle_name-input">
                  <b-form-input id="form-cattle_name-input" v-model.trim="$v.house_hold_data.cattle_name.$model"
                                placeholder="Enter Cattle Name" required type="text"></b-form-input>
                  <div v-if="$v.house_hold_data.cattle_name.$dirty">
                    <div class="error" v-if="!$v.house_hold_data.cattle_name.required">Field is required</div>
                  </div>
                </b-form-group>

                <!--CATTLE COLOR-->
                <b-form-group :class="{ 'form-group--error': $v.house_hold_data.cattle_color.$error }"
                    id="form-cattle-color-group" label="Cattle Color:" label-for="form-cattle-color-input">
                  <b-form-input id="form-cattle-color-input" v-model.trim="$v.house_hold_data.cattle_color.$model"
                                placeholder="Enter Cattle Color" required type="text"></b-form-input>
                  <div v-if="$v.house_hold_data.cattle_color.$dirty">
                    <div class="error" v-if="!$v.house_hold_data.cattle_color.required">Field is required</div>
                  </div>
                </b-form-group>
                
                <!--CATTLE COLLAR-->
                <b-form-group :class="{ 'form-group--error': $v.house_hold_data.collar.$error }"
                    id="form-cattle-collar-group" label="Collar:" label-for="form-cattle-collar-input">
                  <b-form-input id="form-cattle-collar-input" v-model.trim="$v.house_hold_data.collar.$model"
                                placeholder="Enter Collar" required type="text"></b-form-input>
                  <div v-if="$v.house_hold_data.collar.$dirty">
                    <div class="error" v-if="!$v.house_hold_data.collar.required">Field is required</div>
                  </div>
                </b-form-group>

                <!--CATTLE Sex-->
                <div :class="{ 'form-group--error': $v.house_hold_data.cattle_sex.$error }" id="cattle-sex">
                  <p>Cattle Sex:</p>
                  <input id="male" v-model.trim="$v.house_hold_data.cattle_sex.$model" type="radio" value="Male">
                  <label for="male">Male</label>
                  <br>
                  <input id="female" v-model.trim="$v.house_hold_data.cattle_sex.$model" type="radio" value="Female">
                  <label for="female">Female</label>
                  <br>
                  <div v-if="$v.house_hold_data.cattle_sex.$dirty">
                    <div class="error" v-if="!$v.house_hold_data.cattle_sex.required">Field is required</div>
                  </div>
                </div>
              </div>

              <div id="health-info" class="section tab">
                <h4 class="title"><small><b>Health Info</b></small></h4>

                <!--CATTLE WEIGHT-->
                <b-form-group :class="{ 'form-group--error': $v.house_hold_data.weight.$error }"
                    id="form-weight-group" label="Weight:" label-for="form-weight-input">
                  <b-form-input id="form-weight-input" v-model.trim="$v.house_hold_data.weight.$model"
                                min=1 placeholder="Enter Weight" required type="number"></b-form-input>
                  <div v-if="$v.house_hold_data.weight.$dirty">
                    <div class="error" v-if="!$v.house_hold_data.weight.required">Field is required</div>
                    <div class="error" v-if="!$v.house_hold_data.weight.minValue">Minimum value is 1</div>
                  </div>
                </b-form-group>

                <!--CATTLE PCV-->
                <b-form-group :class="{ 'form-group--error': $v.house_hold_data.pcv.$error }"
                    id="form-pcv-group" label="PCV(Packed Cell Volume):" label-for="form-pcv-input">
                  <b-form-input id="form-pcv-input" v-model.trim="$v.house_hold_data.pcv.$model"
                                placeholder="Enter PCV" required type="text"></b-form-input>
                  <div v-if="$v.house_hold_data.pcv.$dirty">
                    <div class="error" v-if="!$v.house_hold_data.pcv.required">Field is required</div>
                  </div>
                </b-form-group>

                <!--CATTLE Diagnosis-->
                <b-form-group :class="{ 'form-group--error': $v.house_hold_data.diagnosis.$error }"
                    id="form-diagnosis-group" label="Diagnosis:" label-for="form-diagnosis-input">
                  <b-form-input id="form-diagnosis-input" v-model.trim="$v.house_hold_data.diagnosis.$model"
                                placeholder="Enter Diagnosis" required type="text"></b-form-input>
                  <div v-if="$v.house_hold_data.diagnosis.$dirty">
                    <div class="error" v-if="!$v.house_hold_data.diagnosis.required">Field is required</div>
                  </div>
                </b-form-group>

                <!--CATTLE Treatment-->
                <b-form-group :class="{ 'form-group--error': $v.house_hold_data.treatment.$error }"
                    id="form-treatment-group" label="Treatment:" label-for="form-treatment-input">
                  <b-form-input id="form-treatment-input" v-model.trim="$v.house_hold_data.treatment.$model"
                                placeholder="Enter Treatment" required type="text"></b-form-input>
                  <div v-if="$v.house_hold_data.treatment.$dirty">
                    <div class="error" v-if="!$v.house_hold_data.treatment.required">Field is required</div>
                  </div>
                </b-form-group>

                <!--CATTLE CC/ML-->
                <b-form-group :class="{ 'form-group--error': $v.house_hold_data.cc.$error }" 
                    id="form-cc/ml-group" label="Dosage:" label-for="form-cc/ml-input">
                  <b-form-input id="form-cc/ml-input" v-model.trim="$v.house_hold_data.cc.$model"
                                placeholder="Enter cc/ml" required type="number"></b-form-input>
                  <div v-if="$v.house_hold_data.cc.$dirty">
                    <div class="error" v-if="!$v.house_hold_data.cc.required">Field is required</div>
                  </div>
                </b-form-group>

                <!--CATTLE Notes-->
                <b-form-group :class="{ 'form-group--error': $v.house_hold_data.notes.$error }" 
                    id="form-notes-group" label="Notes:" label-for="form-notes-input">
                  <b-form-textarea id="form-notes-input" v-model.trim="$v.house_hold_data.notes.$model"
                                   placeholder="Enter Notes" required type="text"></b-form-textarea>
                  <div v-if="$v.house_hold_data.notes.$dirty">
                    <div class="error" v-if="!$v.house_hold_data.notes.required">Field is required</div>
                  </div>
                </b-form-group>
              </div>
            </vue-tiny-tabs>
          </form>
        </b-modal>
      </div>

      <div v-else-if="isEditing">
        <b-modal id="modal-house_hold_data-edit" :title="`Edit ${page_title}`"
                 cancel-variant="danger" ok-title="Update"
                 @hidden="clearForm" @ok="updateHouseHoldData(old_code)"
                 @shown="selectDropDownItemsForUpdate(house_hold_data.study_block)"
                 @submit="showModal = false"
        >
          <form @submit.prevent="updateHouseHoldData">
            <vue-tiny-tabs id="mytabs" :anchor="false" :closable="false" :hideTitle="true" class="tinytabs tabs">
              <div id="farmer-info-edit" class="section tab">
                <h4 class="title"><small><b>Farmer Info</b></small></h4>

                <!--STUDY-BLOCK-->
                <b-form-group :class="{ 'form-group--error': $v.house_hold_data.study_block.$error }"
                    id="form-study_block-group-edit" label="Study Block:" label-for="form-study_block-input">
                  <ejs-dropdownlist
                      id='dropdownlist'
                      :dataSource='studyBlockDataList'
                      :fields="fields"
                      v-model.trim="$v.house_hold_data.study_block.$model"
                      placeholder='Select a study block'
                  ></ejs-dropdownlist>
                  <div v-if="$v.house_hold_data.study_block.$dirty">
                      <div class="error" v-if="!$v.house_hold_data.study_block.required">Field is required</div>
                  </div>
                </b-form-group>

                <!--FARMER-->
                <b-form-group :class="{ 'form-group--error': $v.house_hold_data.farmer.$error }"
                    id="form-farmer-group-edit" label="Farmer Name:" label-for="form-farmer-input">
                  <b-form-input id="form-farmer-input" v-model.trim="$v.house_hold_data.farmer.$model"
                                placeholder="Enter Farmer Name" required type="text"></b-form-input>
                </b-form-group>
                <div v-if="$v.house_hold_data.farmer.$dirty">
                    <div class="error" v-if="!$v.house_hold_data.farmer.required">Field is required</div>
                </div>
              </div>

              <div id="cattle-info-edit" class="section tab">
                <h4 class="title"><small><b>Cattle Info</b></small></h4>
                <!--CATTLE_ID-->
                <b-form-group :class="{ 'form-group--error': $v.house_hold_data.cattle_id.$error }"
                    id="form-cattle_id-group-edit" label="Cattle ID:" label-for="form-cattle_id-input">
                  <b-form-input id="form-cattle_id-input" v-model.trim="$v.house_hold_data.cattle_id.$model"
                                placeholder="Enter Cattle ID" required type="text"></b-form-input>
                  <div v-if="$v.house_hold_data.cattle_id.$dirty">
                    <div class="error" v-if="!$v.house_hold_data.cattle_id.required">Field is required</div>
                  </div>
                </b-form-group>

                <!--CATTLE NAME-->
                <b-form-group :class="{ 'form-group--error': $v.house_hold_data.cattle_name.$error }"
                    id="form-cattle_name-group-edit" label="Cattle Name:" label-for="form-cattle_name-input">
                  <b-form-input id="form-cattle_name-input" v-model.trim="$v.house_hold_data.cattle_name.$model"
                                placeholder="Enter Cattle Name" required type="text"></b-form-input>
                  <div v-if="$v.house_hold_data.cattle_name.$dirty">
                    <div class="error" v-if="!$v.house_hold_data.cattle_name.required">Field is required</div>
                  </div>
                </b-form-group>

                <!--CATTLE COLOR-->
                <b-form-group :class="{ 'form-group--error': $v.house_hold_data.cattle_color.$error }"
                    id="form-cattle-color-group-edit" label="Cattle Color:" label-for="form-cattle-color-input">
                  <b-form-input id="form-cattle-color-input" v-model.trim="$v.house_hold_data.cattle_color.$model"
                                placeholder="Enter Cattle Color" required type="text"></b-form-input>
                  <div v-if="$v.house_hold_data.cattle_color.$dirty">
                    <div class="error" v-if="!$v.house_hold_data.cattle_color.required">Field is required</div>
                  </div>
                </b-form-group>

                <!--CATTLE COLLAR-->
                <b-form-group :class="{ 'form-group--error': $v.house_hold_data.collar.$error }"
                    id="form-cattle-collar-group-edit" label="Collar:" label-for="form-cattle-collar-input">
                  <b-form-input id="form-cattle-collar-input" v-model.trim="$v.house_hold_data.collar.$model"
                                placeholder="Enter Collar" required type="text"></b-form-input>
                  <div v-if="$v.house_hold_data.collar.$dirty">
                    <div class="error" v-if="!$v.house_hold_data.collar.required">Field is required</div>
                  </div>
                </b-form-group>

                <!--CATTLE Sex-->
                <div :class="{ 'form-group--error': $v.house_hold_data.cattle_sex.$error }" id="cattle-sex-edit">
                  <p>Cattle Sex:</p>
                  <input id="male-edit" v-model.trim="$v.house_hold_data.cattle_sex.$model" type="radio" value="Male">
                  <label for="male">Male</label>
                  <br>
                  <input id="female-edit" v-model.trim="$v.house_hold_data.cattle_sex.$model" type="radio" value="Female">
                  <label for="female">Female</label>
                  <br>
                  <div v-if="$v.house_hold_data.cattle_sex.$dirty">
                    <div class="error" v-if="!$v.house_hold_data.cattle_sex.required">Field is required</div>
                  </div>
                </div>
              </div>

              <div id="health-info-edit" class="section tab">
                <h4 class="title"><small><b>Health Info</b></small></h4>

                <!--CATTLE WEIGHT-->
                <b-form-group :class="{ 'form-group--error': $v.house_hold_data.weight.$error }"
                    id="form-weight-group-edit" label="Weight:" label-for="form-weight-input">
                  <b-form-input id="form-weight-input" v-model.trim="$v.house_hold_data.weight.$model"
                                min=1 placeholder="Enter Weight" required type="number"></b-form-input>
                  <div v-if="$v.house_hold_data.weight.$dirty">
                    <div class="error" v-if="!$v.house_hold_data.weight.required">Field is required</div>
                    <div class="error" v-if="!$v.house_hold_data.weight.minValue">Minimum value is 1</div>
                  </div>
                </b-form-group>

                <!--CATTLE PCV-->
                <b-form-group :class="{ 'form-group--error': $v.house_hold_data.pcv.$error }"
                    id="form-pcv-group-edit" label="PCV(Packed Cell Volume):" label-for="form-pcv-input">
                  <b-form-input id="form-pcv-input" v-model.trim="$v.house_hold_data.pcv.$model"
                                placeholder="Enter PCV" required type="text"></b-form-input>
                  <div v-if="$v.house_hold_data.pcv.$dirty">
                    <div class="error" v-if="!$v.house_hold_data.pcv.required">Field is required</div>
                  </div>
                </b-form-group>

                <!--CATTLE Diagnosis-->
                <b-form-group :class="{ 'form-group--error': $v.house_hold_data.diagnosis.$error }"
                    id="form-diagnosis-group-edit" label="Diagnosis:" label-for="form-diagnosis-input">
                  <b-form-input id="form-diagnosis-input" v-model.trim="$v.house_hold_data.diagnosis.$model"
                                placeholder="Enter Diagnosis" required type="text"></b-form-input>
                  <div v-if="$v.house_hold_data.diagnosis.$dirty">
                    <div class="error" v-if="!$v.house_hold_data.diagnosis.required">Field is required</div>
                  </div>
                </b-form-group>

                <!--CATTLE Treatment-->
                <b-form-group :class="{ 'form-group--error': $v.house_hold_data.treatment.$error }"
                    id="form-treatment-group-edit" label="Treatment:" label-for="form-treatment-input">
                  <b-form-input id="form-treatment-input" v-model.trim="$v.house_hold_data.treatment.$model"
                                placeholder="Enter Treatment" required type="text"></b-form-input>
                  <div v-if="$v.house_hold_data.treatment.$dirty">
                    <div class="error" v-if="!$v.house_hold_data.treatment.required">Field is required</div>
                  </div>
                </b-form-group>

                <!--CATTLE CC/ML-->
                <b-form-group :class="{ 'form-group--error': $v.house_hold_data.cc.$error }"
                    id="form-cc/ml-group-edit" label="Dosage:" label-for="form-cc/ml-input">
                  <b-form-input id="form-cc/ml-input" v-model.trim="$v.house_hold_data.cc.$model"
                                placeholder="Enter cc/ml" required type="number"></b-form-input>
                  <div v-if="$v.house_hold_data.cc.$dirty">
                    <div class="error" v-if="!$v.house_hold_data.cc.required">Field is required</div>
                  </div>
                </b-form-group>

                <!--CATTLE Notes-->
                <b-form-group :class="{ 'form-group--error': $v.house_hold_data.notes.$error }"
                    id="form-notes-group-edit" label="Notes:" label-for="form-notes-input">
                  <b-form-textarea id="form-notes-input" v-model.trim="$v.house_hold_data.notes.$model"
                                   placeholder="Enter Notes" required type="text"></b-form-textarea>
                  <div v-if="$v.house_hold_data.notes.$dirty">
                    <div class="error" v-if="!$v.house_hold_data.notes.required">Field is required</div>
                  </div>
                </b-form-group>
              </div>
            </vue-tiny-tabs>
          </form>
        </b-modal>
      </div>

      <b-button v-if="isAuth" v-b-modal.modal-house_hold_data class="float_btn" style="border-radius: 50%"
                variant="primary">
        <span>Add House Data</span> <i class="fas fa-plus-circle menu_icon"></i>
      </b-button>

      <div style="margin: auto;">
        <loading-progress
            :hide-background="hideBackground" :indeterminate="indeterminate" :progress="progressPath" :size="size"
            fillDuration="2" rotate rotationDuration="1"/>
      </div>
    </div>
  </div>
</template>

<script>
import {
  extractApiData,
  getItemDataList,
  getSelectedItemCode,
  handleError,
  isResearcher,
  pageStartLoader,
  paginate,
  secureStoreGetAuthString,
  showFlashMessage
} from "@/utils/util_functions";
import {font_scale} from '@/utils/constants';
import {house_hold_data_resource, study_block_resource} from "@/utils/api_paths";
import axios from "axios";
import TopNav from "@/components/TopNav";
import EventBus from '@/components/EventBus';
import VueTinyTabs from 'vue-tiny-tabs';
import FilterCard from "@/components/FilterCard";
import {minValue, required} from "vuelidate/lib/validators";

export default {
  name: "HouseHoldData",

  data() {
    return {
      page_title: "HouseHoldData",
      house_hold_data: {
        farmer: '', cattle_id: '', cattle_name: '', cattle_color: '', cc: '', notes: '', date_collected: null,
        cattle_sex: '', collar: '', pcv: '', diagnosis: '', treatment: '', study_block: '', weight: 0
      },

      house_data: {}, font_scale,

      // search
      search: '', response: [],

      // filters
      filters: [], houseDataList: [],

      // variable to check user status and role
      isAuth: null,

      time: 2000, // loader-time

      // progressPath
      indeterminate: true, hideBackground: true, progressPath: 5, size: 180,

      studyBlockDataList: [],
      fields: {text: '', value: ''},

      // values for data modification
      old_code: null, showModal: true, isEditing: false,

      // data for pagination
      current: 1, page_array: [], page_info: {},
    };
  },

  validations: {
    house_hold_data: {
      farmer: {required}, cattle_id: {required}, cattle_name: {required}, cattle_color: {required},
      cc: {required}, notes: {required}, cattle_sex: {required}, collar: {required}, pcv: {required},
      diagnosis: {required}, treatment: {required}, study_block: {required}, weight: {required, minValue: minValue(1)}
    }
  },

  mounted() {
    EventBus.$on('searchQuery', (payload) => {
      this.search = payload;
      this.searchData();
    })

    EventBus.$on('filters', (payload) => {
      this.filters = payload
      if (this.filters.length === 0) {
        this.houseDataList = this.response
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
              .map(({['study_block.area']: site}) => site)
              .filter((value, index, self) => self.indexOf(value) === index),
        },
        {
          'By Area': this.response
              .map(({['study_block.name']: area}) => area)
              .filter((value, index, self) => self.indexOf(value) === index),
        },
        {
          'By Date': this.response
              .map(({date_collected: date}) => date)
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

      /* houseDataList,which is a copy of response, is passed as the data here instead of response to avoid
      mutating response data.*/
      let filteredData = this.filterData(this.houseDataList)

      let filterBySite = filteredData.site
      let filterByArea = filteredData.area
      let filterByDate = filteredData.date

      if (searchList !== null) {
        return paginate(searchList)
      } else if (this.filters.length > 1) {
        // Possibly, multiple filters have been applied. Return the array with the least elements
        return filterBySite.length < filterByArea.length ?
            paginate(filterBySite) : paginate(filterByArea)
      } else if (filterBySite !== null && filterBySite.length > 0) {
        this.houseDataList = filterBySite // eslint-disable-line
        this.filterData(filterBySite)
        return paginate(filterBySite)
      } else if (filterByArea !== null && filterByArea.length > 0) {
        this.houseDataList = filterByArea // eslint-disable-line
        this.filterData(filterByArea)
        return paginate(filterByArea)
      } else if (filterByDate !== null && filterByDate.length > 0) {
        this.houseDataList = filterByDate // eslint-disable-line
        this.filterData(filterByDate)
        return paginate(filterByDate)
      }
      return paginate(this.houseDataList)
    },
  },

  methods: {
    // Util Functions
    onSubmit(evt) {
      this.$v.$touch();
      if (this.$v.$invalid) { evt.preventDefault();
        this.$log.info('validations', this.$v.house_hold_data)
      return;}
      this.createHouseHoldData();
    },

    clearForm() {
      this.house_hold_data.farmer = '';
      this.house_hold_data.cattle_id = '';
      this.house_hold_data.cattle_name = '';
      this.house_hold_data.cattle_color = '';
      this.house_hold_data.cattle_sex = '';
      this.house_hold_data.collar = '';
      this.house_hold_data.pcv = '';
      this.house_hold_data.diagnosis = '';
      this.house_hold_data.treatment = '';
      this.house_hold_data.cc = '';
      this.house_hold_data.notes = '';
      this.house_hold_data.study_block = '';
      this.house_hold_data.weight = 0;
      this.isEditing = false;
      this.studyBlockDataList = [];
      this.onLoadPage();
    },

    fillFormForUpdate(data) {
      this.house_hold_data.farmer = data.farmer;
      this.house_hold_data.cattle_id = data.cattle_id;
      this.house_hold_data.cattle_name = data.cattle_name;
      this.house_hold_data.cattle_color = data.cattle_color;
      this.house_hold_data.cattle_sex = data.cattle_sex;
      this.house_hold_data.collar = data.collar;
      this.house_hold_data.pcv = data.pcv;
      this.house_hold_data.diagnosis = data.diagnosis;
      this.house_hold_data.treatment = data.treatment;
      this.house_hold_data.cc = data.cc;
      this.house_hold_data.notes = data.notes;
      this.house_hold_data.weight = data.weight;
      this.house_hold_data.study_block = data['study_block.name'];
      this.old_code = data.code;
      this.isEditing = true;
      this.showModal = true;
    },

    onLoadPage() {
      getItemDataList(study_block_resource).then(data => {
        let study_blockList = extractApiData(data);

        // update local variables with data from API
        this.fields = study_blockList['fields'];
        for (let i = 0; i < study_blockList.items.length; i++) {
          this.studyBlockDataList.push({
            'Code': study_blockList.items[i].Code,
            'Name': study_blockList.items[i].Name,
          });
        }
      })
      this.getHouseHoldData();
    },

    selectDropDownItemsForUpdate(study_block) {
      let elementTheme = document.getElementById("dropdownlist");
      elementTheme.value = study_block;
    },

    // stop&hide progressPath
    haltProgressPath(cont = false, path = 0, size = 0) {
      this.indeterminate = cont;
      this.progressPath = path;
      this.size = size
    },

    viewHouseData(house_data) {
      this.house_data = house_data
    },

    // pagination
    pageInfo(info) {
      EventBus.$emit('page-info', {'pgInfo': info, 'pgData': this.houseDataList})
    },

    /* Methods associated with searching and filtering of data in the page */
    filterData(data) {
      let filterBySite = this.filters.length
          ? data.filter(hhd => this.filters.some(filter => hhd['study_block.area'].match(filter)))
          : null // site

      let filterByArea = this.filters.length
          ? data.filter(hhd => this.filters.some(filter => hhd['study_block.name'].match(filter)))
          : null // area

      let filterByDate = this.filters.length
          ? data.filter(hhd => this.filters.some(filter => hhd.date_collected.match(filter)))
          : null // area

      return {'site': filterBySite, 'area': filterByArea, 'date': filterByDate}
    },

    // search fn
    searchData() {
      return this.response.filter(hhd => {
        return hhd.cattle_id.toLowerCase().includes(this.search.toLowerCase())
      })
    },

    // Functions to interact with api
    getHouseHoldData() {
      this.isAuth = isResearcher();
      axios.get(house_hold_data_resource)
          .then((res) => {
            setTimeout(() => {
                  this.haltProgressPath();
                  this.houseDataList = this.response = res.data['message'];
                }
                , this.time)
          }).catch((error) => {
        // eslint-disable-next-line
        this.$log.error(error);
      });
    },

    createHouseHoldData: function () {
      this.house_hold_data.study_block = getSelectedItemCode('dropdownlist', this.studyBlockDataList);
      let loader = pageStartLoader(this)

      axios.post(house_hold_data_resource, {
        farmer: this.house_hold_data.farmer, cattle_id: this.house_hold_data.cattle_id,
        cattle_name: this.house_hold_data.cattle_name, cattle_color: this.house_hold_data.cattle_color,
        cattle_sex: this.house_hold_data.cattle_sex, collar: this.house_hold_data.collar,
        pcv: this.house_hold_data.pcv, diagnosis: this.house_hold_data.diagnosis,
        treatment: this.house_hold_data.treatment, cc: this.house_hold_data.cc, weight: this.house_hold_data.weight,
        notes: this.house_hold_data.notes, study_block: this.house_hold_data.study_block,
      }, {
        headers:
            {
              Authorization: secureStoreGetAuthString()
            }
      }).then((response) => {
        setTimeout(() => {
          loader.hide();
          this.getHouseHoldData();
          showFlashMessage(this, 'success', response.data['message'], '');
        }, this.time)
      }).catch((error) => {
        handleError(this, error, loader)
      });
      this.clearForm();
    },

    updateHouseHoldData: function (code) {
      this.house_hold_data.study_block = getSelectedItemCode('dropdownlist', this.studyBlockDataList);
      let loader = pageStartLoader(this)

      axios.put(house_hold_data_resource, {
        farmer: this.house_hold_data.farmer, cattle_id: this.house_hold_data.cattle_id,
        cattle_name: this.house_hold_data.cattle_name, cattle_color: this.house_hold_data.cattle_color,
        cattle_sex: this.house_hold_data.cattle_sex, collar: this.house_hold_data.collar,
        pcv: this.house_hold_data.pcv, diagnosis: this.house_hold_data.diagnosis,
        treatment: this.house_hold_data.treatment, cc: this.house_hold_data.cc, weight: this.house_hold_data.weight,
        notes: this.house_hold_data.notes, study_block: this.house_hold_data.study_block,
      }, {
        headers:
            {
              code: code,
              Authorization: secureStoreGetAuthString()
            }
      }).then((response) => {
        setTimeout(() => {
          loader.hide();
          this.getHouseHoldData();
          showFlashMessage(this, 'success', response.data['message'], '');
        }, this.time)
      }).catch((error) => {
        handleError(this, error, loader)
      });
      this.clearForm();
    },

    deleteHouseHoldData: function (code) {
      let loader = pageStartLoader(this)
      axios.delete(house_hold_data_resource, {
        headers:
            {
              code: code,
              Authorization: secureStoreGetAuthString()
            }
      }).then((response) => {
        setTimeout(() => {
          loader.hide()
          showFlashMessage(this, 'success', response.data['message'], '');
          this.getHouseHoldData();
        }, this.time)
      }).catch((error) => {
        handleError(this, error, loader)
      });
    },
  },

  created() {
    this.onLoadPage();
  },

  components: {TopNav, VueTinyTabs, FilterCard}
}
</script>