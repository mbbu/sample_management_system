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
                                <h4 class="card-title"><strong>Alison Belmont</strong></h4>
                                <!-- ROLE -->
                                <h5 class="blue-text pb-2"><strong>Graffiti Artist</strong></h5>
                                <!-- CONTACT DETAILS -->
                                <p class="card-text">Sed ut perspiciatis unde omnis iste natus sit voluptatem
                                    accusantium
                                    doloremque
                                    laudantium, totam rem aperiam. </p>

                                <hr>
                                <mdb-col class="d-flex justify-content-end">
                                    <a href="/edit-user">
                                        <div class="text-center">
                                            <button @click="requestUpdateSample"
                                                    class="btn btn-outline-info btn-rounded"
                                                    type="button"> Update Details
                                                <i class="fas fa-pencil-alt"></i></button>
                                        </div>
                                    </a>
                                    <div class="text-center">
                                        <button @click="deleteSample(sample.code)"
                                                class="btn btn-outline-danger btn-rounded"
                                                type="button"> Delete Account
                                            <i class="far fa-trash-alt"></i></button>
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
                                    <th scope="col"><em><b>THEME</b></em></th>
                                    <th scope="col"><em><b>PROJECT</b></em></th>
                                    <th scope="col"><em><b>ANIMAL SPECIES</b></em></th>
                                    <th scope="col"><em><b>BARCODE</b></em></th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr>
                                </tr>
                                </tbody>
                            </table>

                            <em>Your Sample Requests</em>
                            <table class="table table-hover">
                                <thead class="blue-gradient white-text">
                                <tr>
                                    <th scope="col"><em><b>PROJECT OWNER</b></em></th>
                                    <th scope="col"><em><b>SAMPLE OWNER</b></em></th>
                                    <th scope="col"><em><b>ANIMAL SPECIES</b></em></th>
                                    <th scope="col"><em><b>REQUEST STATUS</b></em></th>
                                    <th scope="col"><em><b>ACTIONS</b></em></th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr>
                                </tr>
                                </tbody>
                            </table>

                            <em>Your Publications</em>
                            <table class="table table-hover">
                                <thead class="blue-gradient white-text">
                                <tr>
                                    <th scope="col"><em><b>THEME</b></em></th>
                                    <th scope="col"><em><b>PROJECT</b></em></th>
                                    <th scope="col"><em><b>TITLE</b></em></th>
                                    <th scope="col"><em><b>CO AUTHORS</b></em></th>
                                    <th scope="col"><em><b>ACTIONS</b></em></th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr>
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
    import TopNav from "@/components/TopNav";

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
                page_title: "Me"
            };
        },
        components: {mdbCard, mdbCardBody, mdbRow, mdbCol, TopNav}
    };
</script>
<style></style>
