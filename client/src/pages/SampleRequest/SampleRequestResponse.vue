<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <top-nav :page_title="page_title"></top-nav>
                <section class="form-gradient" style="margin-top: 2%">
                    <mdb-row>
                        <mdb-col md="12">
                            <mdb-card>
                                <!-- FLASH MESSAGES -->
                                <FlashMessage :position="'right bottom'"></FlashMessage>
                                <div class="header pt-3 blue-gradient">
                                    <mdb-row class="d-flex justify-content-center">
                                        <h3 class="white-text mb-3 pt-3"><i class="fa fa-user"></i> {{ page_title }} :
                                        </h3>
                                    </mdb-row>
                                </div>

                                <mdb-card-body class="mx-4 mt-4">
                                  <SampleResponseForm></SampleResponseForm>
                                </mdb-card-body>
                            </mdb-card>
                        </mdb-col>
                    </mdb-row>
                </section>
            </div>
        </div>
    </div>
</template>

<script>
import TopNav from "../../components/TopNav";
import {required} from "vuelidate/lib/validators"
import {APPROVED_STATUS, DECLINED_STATUS} from "@/utils/constants";
import {mdbCard, mdbCardBody, mdbCol, mdbRow} from "mdbvue";
import SampleResponseForm from "@/components/SampleResponseForm";

export default {
  name: "SampleRequestResponse",
  components: {
    SampleResponseForm,
    mdbCard,
    mdbCardBody,
    mdbCol,
    mdbRow,
    TopNav
  },
  data() {
    return {
      page_title: "Sample Request Response",
      statusDataList: [
        {'Code': APPROVED_STATUS, 'Name': 'Approved'},
        {'Code': DECLINED_STATUS, 'Name': 'Declined'},
      ],
      fields: {
        text: 'Name',
        value: 'Code'
      },
      sampleResponse: {
        status: null,
        amount: null,
        notes: null
      }
    }
  },

  validations: {
    sampleResponse: {
      amount: {required}
    }
  },

  created() {
  }
}
</script>
