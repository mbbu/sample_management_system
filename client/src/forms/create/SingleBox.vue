<template>
<div>
  <b-modal id="modal-box" :title="`Add ${page_title}`"
        @hidden="clearForm" @ok="onSubmit" @submit="showModal=false"
        cancel-variant="danger" ok-title="Save"
  >
    <form @submit.prevent="createBox">
        <!--TRAY-->
        <b-form-group id="form-tray-group" label="Tray Number:" label-for="form-tray-input">
            <ejs-dropdownlist id='dropdownlist'
                    :dataSource='trayDataList' :fields="fields"
                    placeholder='Select a tray' v-model.trim="$v.box.tray.$model"
            ></ejs-dropdownlist>
            <div v-if="$v.box.tray.$dirty">
                <div class="error" v-if="!$v.box.tray.required">Field is required</div>
            </div>
        </b-form-group>

        <!--LABEL-->
        <b-form-group :class="{ 'form-group--error': $v.box.label.$error }"
                      id="form-label-group" label="Box Label:" label-for="form-label-input">
            <b-form-input id="form-label-input"
                    placeholder="Enter box label" required type="text"
                    v-model.trim="$v.box.label.$model"></b-form-input>
            <div v-if="$v.box.label.$dirty">
                <div class="error" v-if="!$v.box.label.required">Field is required</div>
            </div>
        </b-form-group>

        <!--CODE-->
        <b-form-group :class="{ 'form-group--error': $v.box.code.$error }"
                      code-for="form-code-input" id="form-code-group" label="Code:">
            <b-form-input id="form-code-input"
                    placeholder="Enter Code" required type="text"
                    v-model.trim="$v.box.code.$model"></b-form-input>
            <div v-if="$v.box.code.$dirty">
                <div class="error" v-if="!$v.box.code.required">Field is required</div>
            </div>
        </b-form-group>

        <!--DIMENSIONS FOR SLOTS-->
          <div class="d-flex justify-content-center">
            <b-form-group :class="{ 'form-group--error': $v.box.rows.$error }"
                      id="form-row-group" label="Rows:" label-for="form-rows-input">
              <b-form-input id="form-rows-input"
                      placeholder="Enter num of rows" required min=1 type="number"
                      v-model.trim="$v.box.rows.$model"></b-form-input>

              <div v-if="$v.box.rows.$dirty">
                    <div class="error" v-if="!$v.box.rows.required">Field is required</div>
                    <div class="error" v-if="!$v.box.rows.minValue">Rows cannot be less than 1</div>
              </div>
            </b-form-group>

              <b-form-group :class="{ 'form-group--error': $v.box.cols.$error }"
                      id="form-cols-group" label="Cols:" label-for="form-cols-input">
                  <b-form-input id="form-cols-input"
                            placeholder="Enter num of columns" required min=1 type="number"
                            v-model.trim="$v.box.cols.$model"></b-form-input>

                  <div v-if="$v.box.cols.$dirty">
                        <div class="error" v-if="!$v.box.cols.required">Field is required</div>
                        <div class="error" v-if="!$v.box.cols.minValue">Columns cannot be less than 1</div>
                  </div>
                </b-form-group>
            </div>
    </form>
  </b-modal>

</div>
</template>

<script>
import {
  extractTrayData,
  getItemDataList, handleError,
  pageStartLoader,
  secureStoreGetAuthString,
  showFlashMessage
} from "@/utils/util_functions";
import {box_resource, tray_resource} from "@/utils/api_paths";
import axios from "axios";
import {minValue, required} from "vuelidate/lib/validators";
import EventBus from "@/components/EventBus";

export default {
  name: "SingleBox",

  data(){
    return {
      page_title: 'Box',
      box: { tray: '', label: '', code: '', rows: '', cols: '' },
      trayDataList: [],
      fields: {text: '', value: ''},
    }
  },

  validations: {
    box: {
        tray: {required}, code: {required}, label: {required},
        rows: {required, minValue: minValue(1)},
        cols: {required, minValue: minValue(1)},
    }
  },

  methods: {
    onLoadPage() {
      getItemDataList(tray_resource).then(data => {
          let trayList = extractTrayData(data);

          // update local variables with data from API
          this.fields = trayList['fields'];
          for (let i = 0; i < trayList.items.length; i++) {
              this.trayDataList.push({ 'Code': trayList.items[i].Code, 'Name': trayList.items[i].Name});
          }
      });
    },

    onSubmit(evt) {
        this.$v.$touch();
        if (this.$v.$invalid) { evt.preventDefault(); return;}
        this.createBox();
    },

    clearForm() {
        this.box.tray = null; this.box.code = null;
        this.box.label = null; this.isEditing = false; this.$v.$reset();
    },

    createBox: function () {
        let self = this; let loader = pageStartLoader(this);

        axios.post(box_resource, {
            tray: this.box.tray, label: this.box.label,
            code: this.box.code, rows: this.box.rows, cols: this.box.cols,
        }, {
            headers:
                {
                  Authorization: secureStoreGetAuthString()
                }
        }).then((response) => {
              setTimeout(()=> {
                loader.hide(); EventBus.$emit('box-created');
                showFlashMessage(self, 'success', response.data['message'], '');
              },this.time)
            }).catch((error) => { handleError(this, error, loader) });
        this.clearForm();
    },
  },
  created() { this.onLoadPage() }
}
</script>

<style scoped>

</style>