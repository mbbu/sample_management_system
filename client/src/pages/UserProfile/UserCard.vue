<template>
  <div>
    <top-nav :page_title="page_title"></top-nav>
    <br>
    <!-- Card -->
    <div class="card card-cascade">
      <mdb-card class="md-card-profile">
        <mdb-card-body class="mx-4 mt-4">

          <!-- Card group -->
          <div class="card-group">

            <!-- Card -->
            <!-- Card Wider -->
            <div class="card card-cascade wider">
              <!-- Avatar -->
              <div class="avatar mx-auto white">
                <img :src=cardUserImage
                     alt="Your Picture"
                     class="rounded-circle">
              </div>

              <!-- Card content -->
              <div class="card-body card-body-cascade text-center pb-0">

                <!-- NAME -->
                <h4 class="card-title"><strong><em>Name:</em> {{ response.fullname }}</strong></h4>
                <!-- ROLE -->
                <h5 class="blue-text pb-2"><strong><em>Role:</em> {{ response.role }}</strong></h5>
                <!-- CONTACT DETAILS -->
                <p class="card-text"><em>Contact Info: </em> {{ response.email }} </p>

                <hr>
                <mdb-col class="d-flex justify-content-end">
                  <a href="/edit-user">
                    <div class="text-center">
                      <button @click="requestUpdateUser"
                              class="btn btn-outline-info btn-rounded"
                              type="button"> Update Details
                        <i class="fas fa-pencil-alt"></i></button>
                    </div>
                  </a>

                  <!--  DELETE USER    -->
                  <div>
                    <div class="text-center">
                      <button class="btn btn-outline-danger btn-rounded"
                              type="button"
                              v-b-modal.modal-user-delete> Delete Account
                        <i class="far fa-trash-alt"></i></button>
                    </div>

                    <b-modal
                        @ok="deleteUser"
                        cancel-variant="info"
                        id="modal-user-delete"
                        ok-title="Delete"
                        ok-variant="danger"
                        title="Delete Account?"
                    >
                      <p>
                        Are you sure you want to delete your account?
                        <i class="far fa-sad-tear menu_icon"></i>
                      </p>
                    </b-modal>
                  </div>
                </mdb-col>
              </div>
            </div>
            <!-- Card Wider -->
            <!-- Card -->
          </div>

          <br><br>
          <!-- Activity Card-->
          <div class="card mb-4">
            <!-- FLASH MESSAGES -->
            <FlashMessage :position="'right bottom'"></FlashMessage>

            <!-- Title -->
            <div class="header pt-3 blue-gradient">
              <mdb-row class="d-flex justify-content-center">
                <h3 class="white-text mb-3 pt-3"><i class="far fa-list-alt"></i> Your Activity
                </h3>
              </mdb-row>
            </div>

            <!-- Card content -->
            <div class="card-body">
              <!-- SAMPLES YOU OWN -->
              <details>
                <summary><em>Your Samples</em></summary>
                <table class="table table-hover">
                  <thead class="blue-gradient white-text">
                  <tr>
                    <th scope="col"><em><b>ID</b></em></th>
                    <th scope="col"><em><b>THEME</b></em></th>
                    <th scope="col"><em><b>PROJECT</b></em></th>
                    <th scope="col"><em><b>ANIMAL SPECIES</b></em></th>
                    <th scope="col"><em><b>SAMPLE TYPE</b></em></th>
                    <th scope="col"><em><b>BARCODE</b></em></th>
                    <th scope="col"><em><b>LOC COLLECTED</b></em></th>
                    <th scope="col"><em><b>ACTIONS</b></em></th>
                  </tr>
                  </thead>
                  <tbody>
                  <tr :key="sample.id" v-for="(sample, index) in response.samples">
                    <td> {{ index + 1 }}</td>
                    <td v-if="sample.theme"> {{ sample.theme }}</td>
                    <td v-else> N/A</td>
                    <td v-if="sample.project"> {{ sample.project }}</td>
                    <td v-else> N/A</td>
                    <td v-if="sample.species"> {{ sample.species }}</td>
                    <td v-else> N/A</td>
                    <td v-if="sample.type"> {{ sample.type }}</td>
                    <td v-else> N/A</td>
                    <td v-if="sample.barcode"> {{ sample.barcode }}</td>
                    <td v-else> N/A</td>
                    <td v-if="sample.location"> {{ sample.location }}</td>
                    <td v-else> N/A</td>
                    <b-icon
                        @click="viewMySample(sample.code)"
                        class="border border-info rounded"
                        font-scale="1.8" icon="eye-fill"
                        ref="delete"
                        title="View"
                        v-b-tooltip.hover
                        variant="info"
                    ></b-icon>
                  </tr>
                  </tbody>
                </table>
              </details>

              <!-- YOUR SAMPLE REQUESTS -->
              <details>
                <summary><em>Your Sample Requests</em></summary>
                <table class="table table-hover">
                  <thead class="blue-gradient white-text">
                  <tr>
                    <th scope="col"><em><b>ID</b></em></th>
                    <th scope="col"><em><b>PROJECT</b></em></th>
                    <th scope="col"><em><b>PROJECT OWNER</b></em></th>
                    <th scope="col"><em><b>SAMPLE SPECIES</b></em></th>
                    <th scope="col"><em><b>SAMPLE TYPE</b></em></th>
                    <th scope="col"><em><b>REQUESTED AMOUNT</b></em></th>
                    <th scope="col"><em><b>REQUEST DATE</b></em></th>
                    <th scope="col"><em><b>RESPONSE DATE</b></em></th>
                    <th scope="col"><em><b>STATUS</b></em></th>
                    <th scope="col"><em><b>ACTIONS</b></em></th>
                  </tr>
                  </thead>
                  <tbody>
                  <tr :key="request.id" v-for="(request, index) in response.sample_requests">
                    <td> {{ index + 1 }}</td>
                    <td v-if="request.project"> {{ request.project }}</td>
                    <td v-else> N/A</td>
                    <td v-if="request.owner"> {{ request.owner }}</td>
                    <td v-else> N/A</td>
                    <td v-if="request.species"> {{ request.species }}</td>
                    <td v-else> N/A</td>
                    <td v-if="request.type"> {{ request.type }}</td>
                    <td v-else> N/A</td>
                    <td v-if="request.amount"> {{ request.amount }}</td>
                    <td v-else> N/A</td>
                    <td v-if="request.request_date"> {{ request.request_date }}</td>
                    <td v-else> N/A</td>
                    <td v-if="request.response_date"> {{ request.response_date }}</td>
                    <td v-else> N/A</td>
                    <td v-if="request.status"> {{ request.status }}</td>
                    <td v-else> N/A</td>
                    <b-icon
                        @click="viewMyRequest(request)"
                        class="border border-info rounded"
                        font-scale="1.8" icon="eye-fill"
                        title="View"
                        v-b-modal.modal-sample-request
                        v-b-tooltip.hover variant="info"
                    ></b-icon>
                    &nbsp;
                    <b-icon
                        @click="showModal = !showModal"
                        @mouseover="fillFormForUpdate(request)"
                        class="border border-info rounded"
                        font-scale="1.8"
                        icon="pencil" title="Update"
                        v-b-modal.modal-sample-request-edit v-b-tooltip.hover
                        v-if="request.status === 'PENDING'"
                        variant="info"
                    ></b-icon>
                    &nbsp;
                    <b-icon
                        @click="deleteSampleRequest(request.code)"
                        class="border rounded bg-danger p-1"
                        font-scale="1.7" icon="trash"
                        title="Delete" v-b-tooltip.hover
                        variant="light"
                    ></b-icon>
                  </tr>
                  </tbody>
                </table>

                <!-- SAMPLE REQUEST MODALS -->
                <b-modal
                    id="modal-sample-request"
                    title="About Sample Request"
                    v-model="showModalView"
                >
                  <p><em>Project:</em> {{ request.project }}</p>
                  <p><em>Owner:</em> {{ request.owner }}</p>
                  <p><em>Sample Type:</em> {{ request.type }}</p>
                  <p><em>Sample Species:</em> {{ request.species }}</p>
                  <p><em>Requested Amount:</em> {{ request.amount }}</p>
                  <p><em>Request Date:</em> {{ request.request_date }}</p>
                  <p><em>Response Date:</em> {{ request.response_date }}</p>
                  <p><em>Request Status:</em> {{ request.status }}</p>
                  <p><em>Notes:</em> <br> {{ request.notes }}</p>

                  <template v-slot:modal-footer="{ ok, cancel, hide }">
                    <!-- Emulate built in modal footer ok and cancel button actions -->
                    <b-button @click="cancel()" size="md" variant="danger">
                      Cancel
                    </b-button>
                    <div v-if="request.status === 'PENDING'">
                      <b-button @click="fillFormForUpdate(request); showModal = !showModal" size="md" variant="primary">
                        Update
                      </b-button>

                      <b-button @click="sendReminder = true; updateSample(request.code)"
                                class="btn btn-outline-dark" size="md"> Send Reminder
                      </b-button>
                    </div>

                    <div v-else>
                      <b-button disabled size="md" variant="primary"> Update</b-button>
                    </div>
                  </template>
                </b-modal>

                <b-modal
                    @ok="updateSample(sampleRequest.code)"
                    cancel-variant="danger"
                    id="modal-sample-request"
                    ok-title="Update"
                    title="Update Sample Request"
                    v-model="showModal"
                >
                  <form>
                    <b-form-group id="form-amount-group" label="Amount:" label-for="form-amount-input">
                      <b-form-input
                          id="form-amount-input"
                          min=1
                          placeholder="Enter Amount"
                          required
                          type="number"
                          v-model="sampleRequest.amount"
                      ></b-form-input>
                    </b-form-group>
                  </form>
                </b-modal>
              </details>

              <!-- YOUR REQUESTED SAMPLES -->
              <details>
                <summary>Your Requested Samples</summary>
                <table class="table table-hover">
                  <thead class="blue-gradient white-text">
                  <tr>
                    <th scope="col"><em><b>ID</b></em></th>
                    <th scope="col"><em><b>PROJECT</b></em></th>
                    <th scope="col"><em><b>REQUESTER</b></em></th>
                    <th scope="col"><em><b>SAMPLE SPECIES</b></em></th>
                    <th scope="col"><em><b>SAMPLE TYPE</b></em></th>
                    <th scope="col"><em><b>REQUESTED AMOUNT</b></em></th>
                    <th scope="col"><em><b>REQUEST DATE</b></em></th>
                    <th scope="col"><em><b>RESPONSE DATE</b></em></th>
                    <th scope="col"><em><b>STATUS</b></em></th>
                    <th scope="col"><em><b>ACTIONS</b></em></th>
                  </tr>
                  </thead>
                  <tbody>
                  <tr :key="requested.id" v-for="(requested, index) in response.requested_samples">
                    <td> {{ index + 1 }}</td>
                    <td v-if="requested.project"> {{ requested.project }}</td>
                    <td v-else> N/A</td>
                    <td v-if="requested.requester"> {{ requested.requester }}</td>
                    <td v-else> N/A</td>
                    <td v-if="requested.species"> {{ requested.species }}</td>
                    <td v-else> N/A</td>
                    <td v-if="requested.type"> {{ requested.type }}</td>
                    <td v-else> N/A</td>
                    <td v-if="requested.amount"> {{ requested.amount }}</td>
                    <td v-else> N/A</td>
                    <td v-if="requested.request_date"> {{ requested.request_date }}</td>
                    <td v-else> N/A</td>
                    <td v-if="requested.response_date"> {{ requested.response_date }}</td>
                    <td v-else> N/A</td>
                    <td v-if="requested.status"> {{ requested.status }}</td>
                    <td v-else> N/A</td>
                    <b-icon
                        @click="viewMyRequestedSamples(requested)"
                        class="border border-info rounded"
                        font-scale="1.8" icon="eye-fill"
                        title="View"
                        v-b-modal.modal-requested-sample-view
                        v-b-tooltip.hover variant="info"
                    ></b-icon>
                    &nbsp;
                    <b-icon
                        @click="setRequestCode(requested.code)"
                        class="border border-info rounded"
                        font-scale="1.8"
                        icon="pencil" title="Update"
                        v-b-modal.modal-requested-sample v-b-tooltip.hover
                        v-if="requested.status === 'PENDING'"
                        variant="info"
                    ></b-icon>
                    &nbsp;
                    <b-icon
                        @click="deleteSampleRequest(requested.code)"
                        class="border rounded bg-danger p-1"
                        font-scale="1.7" icon="trash"
                        title="Delete" v-b-tooltip.hover
                        variant="light"
                    ></b-icon>
                  </tr>
                  </tbody>
                </table>

                <!-- REQUEST VIEW -->
                <b-modal
                    id="modal-requested-sample-view"
                    title="About Sample Request"
                    v-model="showModalViewResponse"
                >
                  <p><em>Project:</em> {{ requested.project }}</p>
                  <p><em>Requester:</em> {{ requested.requester }}</p>
                  <p><em>Sample Type:</em> {{ requested.type }}</p>
                  <p><em>Sample Species:</em> {{ requested.species }}</p>
                  <p><em>Requested Amount:</em> {{ requested.amount }}</p>
                  <p><em>Request Date:</em> {{ requested.request_date }}</p>
                  <p><em>Response Date:</em> {{ requested.response_date }}</p>
                  <p><em>Request Status:</em> {{ requested.status }}</p>

                  <template v-slot:modal-footer="{ ok, cancel, hide }">
                    <!-- Emulate built in modal footer ok and cancel button actions -->
                    <b-button @click="cancel()" size="md" variant="danger">
                      Cancel
                    </b-button>
                    <div v-if="requested.status === 'PENDING'">
                      <b-button @click="showModalUpdateResponse = !showModalUpdateResponse" size="md" variant="primary">
                        Update
                      </b-button>
                    </div>

                    <div v-else>
                      <b-button disabled size="md" variant="primary"> Update</b-button>
                    </div>
                  </template>
                </b-modal>

                <!-- REQUEST UPDATED -->
                <b-modal
                    cancel-variant="danger"
                    hide-footer
                    id="modal-requested-sample"
                    title="Respond To Sample Request"
                    v-model="showModalUpdateResponse"
                >
                  <SampleResponseForm></SampleResponseForm>
                </b-modal>
              </details>

              <!-- YOUR PUBLICATIONS -->
              <details>
                <summary><em>Your Publications</em></summary>
                <table class="table table-hover">
                  <thead class="blue-gradient white-text">
                  <tr>
                    <th scope="col"><em><b>ID</b></em></th>
                    <th scope="col"><em><b>THEME</b></em></th>
                    <th scope="col"><em><b>PROJECT</b></em></th>
                    <th scope="col"><em><b>TITLE</b></em></th>
                    <th scope="col"><em><b>CO AUTHORS</b></em></th>
                    <th scope="col"><em><b>ACTIONS</b></em></th>
                  </tr>
                  </thead>
                  <tbody>
                  <tr :key="publication.id" v-for="(publication, index) in response.publications">
                    <td> {{ index + 1 }}</td>
                    <td v-if="publication.theme"> {{ publication.theme }}</td>
                    <td v-else> N/A</td>
                    <td v-if="publication.project"> {{ publication.project }}</td>
                    <td v-else> N/A</td>
                    <td v-if="publication.title"> {{ publication.title }}</td>
                    <td v-else> N/A</td>
                    <td v-if="publication.co_authors"> {{ publication.co_authors }}</td>
                    <td v-else> N/A</td>
                    <b-icon
                        @click="viewMyPublication(publication)"
                        class="border border-info rounded"
                        font-scale="1.8" icon="eye-fill"
                        title="View"
                        v-b-modal.modal-publication
                        v-b-tooltip.hover variant="info"
                    ></b-icon>
                    &nbsp;
                    <b-icon :title="`Update ${ publication.title }`"
                            @click="updatePublication(publication)"
                            class="border border-info rounded" font-scale="1.8"
                            icon="pencil" v-b-modal.modal-publication-edit
                            v-b-tooltip.hover
                            variant="info"
                    ></b-icon>
                    &nbsp;
                    <b-icon
                        @click="downloadPublication(publication.title)"
                        class="border border-info rounded" font-scale="1.8"
                        icon="download" title="Download"
                        v-b-tooltip.hover variant="info"
                    ></b-icon>
                    &nbsp;
                    <b-icon
                        @click="deletePublication(publication.title)"
                        class="border rounded bg-danger p-1"
                        font-scale="1.7" icon="trash"
                        title="Delete" v-b-tooltip.hover
                        variant="light"
                    ></b-icon>
                  </tr>
                  </tbody>
                </table>

                <!-- PUBLICATION MODALS -->
                <b-modal
                    id="modal-publication"
                    title="About Publication"
                    v-model="showPubModalView"
                >
                  <p><em>Title:</em> {{ publication.title }}</p>
                  <p><em>Theme:</em> {{ publication.theme }}</p>
                  <p><em>Project:</em> {{ publication.project }}</p>
                  <p><em>Author:</em> {{ response.fullname }}</p>
                  <p><em>Co-Authors:</em> {{ publication.co_authors }}</p>

                  <template v-slot:modal-footer="{ ok, cancel, hide }">
                    <!-- Emulate built in modal footer ok and cancel button actions -->
                    <b-button @click="cancel()" size="md" variant="danger">
                      Cancel
                    </b-button>
                    <b-button @click="updatePublication(publication)" size="md"
                              variant="primary"> Update
                    </b-button>
                    <b-button disabled size="md" variant="primary"> Delete</b-button>
                  </template>
                </b-modal>

                <!-- PUBLICATION MODAL FOR UPDATE -->
                <PublicationModal></PublicationModal>
              </details>

            </div>
            <!-- Card content -->
          </div>
          <!-- Activity Card -->

        </mdb-card-body>
      </mdb-card>
    </div>
    <!-- Card -->
  </div>
</template>
<script>
import {mdbCard, mdbCardBody, mdbCol, mdbRow} from "mdbvue";
import TopNav from "../../components/TopNav";
import axios from "axios";
import {sample_request_resource, user_resource} from "@/utils/api_paths";
import {
  getUserEmail,
  redirectAfterCountDown,
  respondTo401,
  secureStoreDeleteUserInfo,
  secureStoreGetAuthString,
  setSampleDataList,
  showFlashMessage,
  startLoader,
  viewSample,
} from "@/utils/util_functions";
import EventBus from '@/components/EventBus';
import Publication from "@/pages/Publication";
import SampleResponseForm from "@/components/SampleResponseForm";
import PublicationModal from "@/components/PublicationModal";

export default {
  name: "UserCard",
  props: {
    cardUserImage: {
      type: String,
      default: require("../../assets/user_avatar.png")
    }
  },
  data() {
    return {
      page_title: "Dashboard",
      response: {},
      request: {},
      requested: {},
      publication: {},
      sampleRequest: {amount: null},
      showModal: false,
      showModalView: false,
      showPubModalView: false,
      showPubModalUpdate: false,
      showModalViewResponse: false,
      showModalUpdateResponse: false,
      sendReminder: false,
      userEmail: '',
      requestCode: null,
      fields: null,
      sampleDataList: []
    };
  },
  mounted() {
    EventBus.$on('close-modal', payload => {
      this.showModalViewResponse = payload
      EventBus.$emit('request-code', this.requestCode)
    })

    //  check for sample data list event
    EventBus.$on('sample-data-list', (payload) => {
      this.fields = payload.fields
      this.sampleDataList = payload.sampleData
    })
  },
  methods: {
    getUserDetails(email) {
      let self = this;
      let loader = startLoader(this)

      axios.get(user_resource, {
        headers:
            {
              email: email,
            }
      })
          .then((res) => {
            setTimeout(() => {
              loader.hide()
              this.response = res.data.message;
              this.$log.info("Response: " + res.status + " " + res.data +
                  " this.response has", this.response);
            }, 2500)
          })
          .catch((error) => {
            // eslint-disable-next-line
            loader.hide()
            this.$log.error(error);
            if (error.response) {
              if (error.response.status === 401) {
                respondTo401(self);
              } else if (error.response.status === 404) {
                showFlashMessage(self, 'error', 'Connection Error', 'Request was timed out');
                redirectAfterCountDown(self, '/home')
              }
            }
          });
    },

    requestUpdateUser() {
      let self = this;
      let loader = startLoader(this)

      setTimeout(() => {
        loader.hide()
        redirectAfterCountDown(self, '/edit-user')
      }, 1000)
    },

    deleteUser() {
      let self = this;
      let loader = startLoader(this)

      axios.delete(user_resource, {
        headers:
            {
              Authorization: secureStoreGetAuthString()
            }
      })
          .then((response) => {
            // redirect after successful signUp
            if (response.status === 200) {
              setTimeout(() => {
                secureStoreDeleteUserInfo()
                loader.hide()
                showFlashMessage(self, 'success', 'Account Deleted', 'Your account has been successfully deleted.' +
                    '\nSorry to see you go.');
                redirectAfterCountDown(self, '/home')
              }, 2500)
            }
          })
          .catch((error) => {
            this.$log.error(error);
            loader.hide()
            if (error.response) {
              if (error.response.status === 409) {
                showFlashMessage(self, 'error', error.response.data['message'], '');
              } else if (error.response.status === 404) {
                showFlashMessage(self, 'error', 'User not found', "");
              } else if (error.response.status === 400) {
                showFlashMessage(self, 'error', error.response.data['message'], 'Kindly refill the form');
              } else if (error.response.status === 401) {
                respondTo401(self)
              } else if (error.response.status === 403) {
                showFlashMessage(self, 'error', 'Unauthorized', error.response.data['message'])
              } else if (error.response.status === 500) {
                showFlashMessage(self, 'error', "Fatal Error", 'Admin has been contacted.');
              } else {
                showFlashMessage(self, 'error', error.response.data['message'], '');
              }
            }
          })
    },

    // functions for samples
    viewMySample(code) {
      showFlashMessage(this, 'success', 'Redirecting in 5 seconds...', '')
      viewSample(this, code)
    },

    // functions for sample requests
    viewMyRequest(requestData) {
      this.request = requestData
      this.showModalView = !this.showModalView
    },

    fillFormForUpdate(request) {
      this.sampleRequest = request;
    },

    updateSample(code) {
      let self = this;
      let header = '';
      this.showModal = false
      this.showModalView = false
      let loader = startLoader(this)

      // set headers depending on what the user is trying to do
      header = this.sendReminder ? 'resend' : 'update'
      this.sendReminder = false;

      axios.put(sample_request_resource, {
        sample: code,
        amount: this.sampleRequest.amount
      }, {
        headers: {
          Authorization: secureStoreGetAuthString(),
          code: code,
          resend: header,
        }
      })
          .then((response) => {
            setTimeout(() => {
              loader.hide()
              this.$log.info("Response: ", response);
              showFlashMessage(self, 'success', response.data.message, '')
            }, 2500)
          })
          .catch((error) => {
            // eslint-disable-next-line
            loader.hide()
            this.$log.error(error);
            if (error.response) {
              if (error.response.status === 401) {
                respondTo401(self);
              } else if (error.response.status === 304) {
                showFlashMessage(self, 'error', 'Info', error.response.message);
              } else if (error.response.status === 404) {
                showFlashMessage(self, 'error', 'Not Found!', error.response.message);
              } else if (error.response.status === 409) {
                showFlashMessage(self, 'error', 'Error', error.response.message);
              } else if (error.response.status === 500) {
                showFlashMessage(self, 'error', 'Fatal', "Fatal error admin has been contacted!");
              }
            }
          });
    },

    deleteSampleRequest(code) {
      let self = this;
      let loader = startLoader(this)

      console.log(code)

      axios.delete(sample_request_resource, {
        headers: {
          Authorization: secureStoreGetAuthString(),
          code: code
        }
      })

          .then((response) => {
            setTimeout(() => {
              loader.hide()
              this.$log.info("Response: ", response);
              showFlashMessage(self, 'success', response.data.message, '')
            }, 2500)
          })
          .catch((error) => {
            // eslint-disable-next-line
            loader.hide()
            this.$log.error(error);
            if (error.response) {
              if (error.response.status === 401) {
                respondTo401(self);
              } else if (error.response.status === 404) {
                showFlashMessage(self, 'error', 'Not Found!', error.response.message);
              } else if (error.response.status === 500) {
                showFlashMessage(self, 'error', 'Fatal', "Fatal error admin has been contacted!");
              }
            }
          });

      this.getUserDetails(this.userEmail)

    },

    // functions for sample request response
    setRequestCode(code) {
      this.showModalUpdateResponse = !this.showModalUpdateResponse
      this.requestCode = code
    },

    viewMyRequestedSamples(requested) {
      this.showModalViewResponse = !this.showModalViewResponse
      this.requested = requested
    },

    // todo: fix lifecycle issues
    // functions for publication
    viewMyPublication(pubData) {
      this.publication = pubData
      this.showPubModalView = !this.showPubModalView
    },

    updatePublication(publication) {
      // updated data with required fields
      publication.sampleDataList = this.sampleDataList
      publication.fields = this.fields
      publication.user = this.response.fullname
      EventBus.$emit('update-publication', publication)
    },

    //todo: refactor
    deletePublication(title) {
      console.log("deleting pub from dashboard: ", title)
      EventBus.$emit('delete-publication', title)

      Publication.methods.deletePublication(title)
      // redirectAfterCountDown(this, '/publication', 2)
    },

  },

  created() {
    setSampleDataList()
    this.userEmail = getUserEmail()
    this.getUserDetails(this.userEmail)
  },
  components: {PublicationModal, SampleResponseForm, mdbCard, mdbCardBody, mdbRow, mdbCol, TopNav}
};
</script>
<style>
</style>
