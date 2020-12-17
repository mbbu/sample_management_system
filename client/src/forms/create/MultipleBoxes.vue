<template>
  <div>
    <b-modal id="modal-box" :title="`Add ${page_title} - (Creating Multiple Boxes)`"
             cancel-variant="danger" ok-title="Save" @hidden="clearForm"
             @ok="onSubmit" @submit="showModal=false"
    >
      <form @submit.prevent="createBoxes">
        <!--NUMBER-->
        <b-form-group id="form-number-group" :class="{ 'form-group--error': $v.box.number.$error }"
                      label="Number of Boxes:" label-for="form-number-input">
          <b-form-input id="form-number-input" v-model.trim="$v.box.number.$model" min=1
                        placeholder="Enter number of boxes to create" required type="number"></b-form-input>
          <div v-if="$v.box.number.$dirty">
            <div v-if="!$v.box.number.required" class="error">Field is required</div>
            <div v-if="!$v.box.number.minValue" class="error">Number cannot be less than 1</div>
          </div>
        </b-form-group>

        <br><div>Box Dimensions i.e. Slots in box</div><br>

        <!--DIMENSIONS FOR SLOTS-->
        <div class="d-flex justify-content-center">
          <b-form-group id="form-row-group"
                        :class="{ 'form-group--error': $v.box.rows.$error }" label="Rows:" label-for="form-rows-input">
            <b-form-input id="form-rows-input"
                          v-model.trim="$v.box.rows.$model" min=1 placeholder="Enter num of rows" required
                          type="number"></b-form-input>

            <div v-if="$v.box.rows.$dirty">
              <div v-if="!$v.box.rows.required" class="error">Field is required</div>
              <div v-if="!$v.box.rows.minValue" class="error">Rows cannot be less than 1</div>
            </div>
          </b-form-group>

          <b-form-group id="form-cols-group"
                        :class="{ 'form-group--error': $v.box.cols.$error }" label="Cols:" label-for="form-cols-input">
            <b-form-input id="form-cols-input"
                          v-model.trim="$v.box.cols.$model" min=1 placeholder="Enter num of columns" required
                          type="number"></b-form-input>

            <div v-if="$v.box.cols.$dirty">
              <div v-if="!$v.box.cols.required" class="error">Field is required</div>
              <div v-if="!$v.box.cols.minValue" class="error">Columns cannot be less than 1</div>
            </div>
          </b-form-group>
        </div>
      </form>
    </b-modal>
  </div>
</template>

<script>
import {minValue, required} from "vuelidate/lib/validators";
import {handleError, pageStartLoader, secureStoreGetAuthString, showFlashMessage} from "@/utils/util_functions";
import axios from "axios";
import {box_resource} from "@/utils/api_paths";
import EventBus from "@/components/EventBus";

export default {
  name: "MultipleBoxes",

  data(){
    return {
      page_title: 'Boxes',
      box: {number: 0, cols: 0, rows: 0}
    }
  },

  validations: {
    box: {
        number: {required, minValue: minValue(1)},
        rows: {required, minValue: minValue(1)},
        cols: {required, minValue: minValue(1)},
    }
  },

  methods: {
    onSubmit(evt) {
        this.$v.$touch();
        if (this.$v.$invalid) { evt.preventDefault(); return;}
        this.createBoxes();
    },

    clearForm(){
      this.box.number = 0; this.box.rows = 0; this.box.cols = 0;
    },

    createBoxes: function () {
        let self = this; let loader = pageStartLoader(this);

        axios.post(box_resource, {
            number: this.box.number, rows: this.box.rows, cols: this.box.cols,
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
  }
}
</script>

<style scoped>

</style>