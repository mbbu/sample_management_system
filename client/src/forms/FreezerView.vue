<template>
  <div id="app">
    <div id="container">
      <b-modal id="modal-freezer-view" title="Freezer View">
        <div class="row">
          <div class="col">
            <!--CHAMBER-->
            <div class="col form-group">
              <b-form-group id="chamber" label="Chamber:" label-for="form-chamber-input">
                <ejs-dropdownlist
                    id='chamber-dropdownlist' ref='chamber'
                    :dataSource='chamberData' :enabled='chamberEnabled' :fields='chamberFields'
                    placeholder='Select a chamber' @change="fillFormFieldsDependentOnChamber"
                ></ejs-dropdownlist>
              </b-form-group>
            </div>

            <!--RACK-->
            <div class="col form-group">
              <b-form-group id="rack" label="Rack:" label-for="form-rack-input">
                <ejs-dropdownlist
                    id='rack-dropdownlist' ref='rack'
                    :dataSource='rackData' :enabled='rackEnabled' :fields='rackFields'
                    placeholder='Select a rack' @change="fillFormFieldsDependentOnRack"
                ></ejs-dropdownlist>
              </b-form-group>
            </div>
          </div>

          <div class="col">
            <!--TRAY-->
            <div class="col form-group">
              <b-form-group id="tray" label="Tray:" label-for="form-tray-input">
                <ejs-dropdownlist
                    id='tray-dropdownlist' ref='tray'
                    :dataSource='trayData' :enabled='trayEnabled' :fields='trayFields'
                    placeholder='Select a tray' @change="fillFormFieldsDependentOnTray"
                ></ejs-dropdownlist>
              </b-form-group>
            </div>

            <!--BOX-->
            <div class="col form-group">
              <b-form-group id="box" label="Box:" label-for="form-box-input">
                <ejs-dropdownlist
                    id='box-dropdownlist' ref='box'
                    :dataSource='boxData' :enabled='boxEnabled' :fields='boxFields'
                    placeholder='Select a box' @change="fillFormFieldsDependentOnBox"
                ></ejs-dropdownlist>
              </b-form-group>
            </div>
          </div>
        </div>
        <div class="justify-content-center">
<!--          <div class="col justify-content-center">-->
            <rectangle></rectangle>
<!--          </div>-->
        </div>
      </b-modal>
    </div>
  </div>
</template>

<script>
import Rectangle from "@/components/Rectangle";
import {extractChamberData, getItemDataList} from "@/utils/util_functions";
import { freezer_resource} from "@/utils/api_paths";
import EventBus from "@/components/EventBus";
export default {
  name: "FreezerView",

  components: {Rectangle},

  data() {
    return{
      freezerCode: '',
      chamberData: [], chamberFields: {text: '', value: ''}, chamberEnabled: true,
      rackData: [], rackFields: {text: '', value: ''}, rackEnabled: false,
      trayData: [], trayFields: {text: '', value: ''}, trayEnabled: false,
      boxData: [], boxFields: {text: '', value: ''}, boxEnabled: false
    }
  },

  mounted() {
    EventBus.$on('freezerSet', freezer=>{
      this.freezerCode = freezer
      this.onLoadPage()
    })
  },

  methods: {
    onLoadPage(){
      getItemDataList(freezer_resource, {q: this.freezerCode}).then(data => {
        this.chamberData = []
        this.$log.info('chamber data received',data)
        let chamberList = extractChamberData(data);
        this.$log.info('chamber data extracted',chamberList)

        // update local variables with data from API
        this.chamberFields = chamberList['fields'];
        for (let i = 0; i < chamberList.items.length; i++) {
          this.chamberData.push({
            'Code': chamberList.items[i].Code,
            'Name': chamberList.items[i].Name,
          });
        }
        this.$log.info('Chamber data', this.chamberData)
      })
    },

    fillFormFieldsDependentOnChamber(){},
    fillFormFieldsDependentOnRack(){},
    fillFormFieldsDependentOnTray(){},
    fillFormFieldsDependentOnBox(){},
  },
}
</script>

<style scoped>

</style>