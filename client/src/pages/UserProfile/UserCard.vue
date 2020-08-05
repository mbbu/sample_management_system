<template>
  <div>
    <top-nav :page_title="page_title"></top-nav>

    <!-- FLASH MESSAGES -->
    <FlashMessage :position="'right bottom'"></FlashMessage>
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
            <!-- Title -->
            <div class="header pt-3 blue-gradient">
              <mdb-row class="d-flex justify-content-center">
                <h3 class="white-text mb-3 pt-3"><i class="far fa-list-alt"></i> Your Activity
                </h3>
              </mdb-row>
            </div>

            <!-- Card content -->
            <div class="card-body">
              <em>Your Samples</em>
              <table class="table table-hover">
                <thead class="blue-gradient white-text">
                <tr>
                  <th scope="col"><em><b>ID</b></em></th>
                  <th scope="col"><em><b>THEME</b></em></th>
                  <th scope="col"><em><b>PROJECT</b></em></th>
                  <th scope="col"><em><b>ANIMAL SPECIES</b></em></th>
                  <th scope="col"><em><b>SAMPLE TYPE</b></em></th>
                  <th scope="col"><em><b>BARCODE</b></em></th>
                  <th scope="col"><em><b>CODE</b></em></th>
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
                  <td v-if="sample.code"> {{ sample.code }}</td>
                  <td v-else> N/A</td>
                  <b-icon
                      @click="viewSample(sample.code)"
                      class="border border-info rounded"
                      font-scale="1.8" icon="eye-fill"
                      title="View"
                      v-b-tooltip.hover
                      variant="info"
                  ></b-icon>
                  &nbsp;
                  <b-icon
                      class="border rounded bg-danger p-1"
                      font-scale="1.7" icon="trash"
                      title="Delete" v-b-tooltip.hover
                      variant="light"
                  ></b-icon>
                </tr>
                </tbody>
              </table>

              <em>Your Sample Requests</em>
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
                      class="border border-info rounded"
                      font-scale="1.8" icon="eye-fill"
                      title="View"
                      v-b-tooltip.hover
                      variant="info"
                  ></b-icon>
                  &nbsp;
                  <b-icon
                      class="border rounded bg-danger p-1"
                      font-scale="1.7" icon="trash"
                      title="Delete" v-b-tooltip.hover
                      variant="light"
                  ></b-icon>
                </tr>
                </tbody>
              </table>

              <em>Your Publications</em>
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
                      class="border border-info rounded"
                      font-scale="1.8" icon="eye-fill"
                      title="View"
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
                </tr>
                </tbody>
              </table>

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
import {user_resource} from "@/utils/api_paths";
import {
  countDownTimer,
  getUserEmail,
  respondTo401,
  secureStoreDeleteString,
  secureStoreGetString,
  showFlashMessage,
  startLoader,
  viewSample,
} from "@/utils/util_functions";

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
      response: null,
    };
  },
  methods: {
    viewSample,
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
                countDownTimer(self, 3, '/home')
              }
            }
          });
    },

    requestUpdateUser() {
      let self = this;
      let loader = startLoader(this)

      setTimeout(() => {
        loader.hide()
        countDownTimer(self, 1, '/edit-user')
      }, 1000)
    },

    deleteUser() {
      let self = this;
      let loader = startLoader(this)

      axios.delete(user_resource, {
        headers:
            {
              Authorization: secureStoreGetString()
            }
      })
          .then((response) => {
            // redirect after successful signUp
            if (response.status === 200) {
              setTimeout(() => {
                secureStoreDeleteString()
                loader.hide()
                showFlashMessage(self, 'success', 'Account Deleted', 'Your account has been successfully deleted.' +
                    '\nSorry to see you go.');
                countDownTimer(self, 3, '/home')
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
    }
  },
  created() {
    let email = getUserEmail()
    this.getUserDetails(email)
  },
  components: {mdbCard, mdbCardBody, mdbRow, mdbCol, TopNav}
};
</script>
<style></style>
