<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <top-nav :page_title="page_title"></top-nav>

                <FlashMessage :position="'center bottom'"></FlashMessage>
                <br> <br>
                <table class="table table-hover">
                    <thead>
                    <tr>
                        <th scope="col"> Id</th>
                        <th scope="col"> Theme</th>
                        <th scope="col"> Project</th>
                        <th scope="col"> Owner (P.I)</th>
                        <th scope="col"> Location Collected</th>
                        <th scope="col"> Animal Species</th>
                        <th scope="col"> BarCode</th>
                        <th scope="col"> Actions</th>
                    </tr>
                    </thead>

                    <tbody>
                    <tr :key="sample.id" v-for="(sample, index) in response.message">
                        <td> {{ index + 1 }}</td>
                        <td> {{ sample['theme.name'] }}</td>
                        <td> {{ sample.project }}</td>
                        <td> {{ sample.project_owner }}</td>
                        <td> {{ sample.location_collected }}</td>
                        <td> {{ sample.animal_species }}</td>
                        <td> {{ sample.barcode }}</td>


                        <td>
                            <b-icon
                                    @click="viewSample(sample.code)"
                                    class="border border-info rounded" font-scale="1.95"
                                    icon="eye-fill" title="View Sample"
                                    v-b-tooltip.hover variant="info"
                            ></b-icon>
                            &nbsp;
                            <b-icon
                                    :title="`Update ${ sample.code }`"
                                    class="border border-info rounded" font-scale="1.90"
                                    icon="pencil" v-b-modal.modal-publication-edit
                                    v-b-tooltip.hover
                                    variant="info"
                            ></b-icon>

                            &nbsp;
                            <b-icon
                                    :title="`Delete ${ sample.code }!`"
                                    @click="deleteSample(sample.code)"
                                    class="border rounded bg-danger p-1" font-scale="1.85"
                                    icon="trash" v-b-tooltip.hover
                                    variant="light"
                            ></b-icon>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
            <a href="/addsample">
                <b-button class="float_btn" variant="primary">Add Sample</b-button>
            </a>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import {sample_resource} from "../../utils/api_paths";
    import TopNav from "../../components/TopNav";
    import {countDownTimer, secureStoreGetString, showFlashMessage} from "../../utils/util_functions";

    export default {
        name: "Sample",
        data() {
            return {
                page_title: "Samples",
                response: [],
            };
        },
        methods: {
            // methods to interact with api
            getSamples() {
                // this.clearForm();
                axios.get(sample_resource)
                    .then((res) => {
                        this.$log.info("Response: " + res.status + " " + res.data['message']);
                        this.response = res.data;
                    })
                    .catch((error) => {
                        // eslint-disable-next-line
                        this.$log.error(error);
                    });
            },

            deleteSample: function (code) {
                let self = this;
                axios.delete(sample_resource, {
                    headers:
                        {
                            code: code,
                            Authorization: secureStoreGetString()
                        }
                })
                    .then((response) => {
                        this.getSamples();
                        showFlashMessage(self, 'success', response.data['message'], '');
                    })
                    .catch((error) => {
                        this.$log.error(error);
                        if (error.response) {
                            if (error.response.status === 401) {
                                showFlashMessage(self, 'error', "Session Expired", 'You need to log in to perform this operation');
                                countDownTimer(self, 3, '/login')
                            } else {
                                showFlashMessage(self, 'error', error.response.data['message'], '');
                            }
                        }
                    });
            },
        },
        components: {TopNav},
        created() {
            this.getSamples();
        },
    };
</script>
