<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <top-nav :page_title="page_title" v-bind:search_query.sync="search"></top-nav>
                <section class="form-gradient" style="margin-top: 2%">
                    <mdb-row>
                        <mdb-col md="12">
                            <mdb-card>
                                <div class="header pt-3 blue-gradient">
                                    <mdb-row class="d-flex justify-content-center">
                                        <h3 class="white-text mb-3 pt-3"> {{ page_title }}
                                        </h3>
                                    </mdb-row>
                                </div>

                                <mdb-card-body class="mx-4 mt-4">
                                    <div class="d-flex justify-content-center">
                                        <h3><i class="fas fa-sad-tear menu_icon_large_danger"></i>
                                            Sorry we could not find what you were looking for!</h3>
                                    </div>
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
    import TopNav from "../components/TopNav";
    import {mdbCard, mdbCardBody, mdbCol, mdbRow} from "mdbvue";

    export default {
        name: "PageNotFound",
        data() {
            return {
                page_title: "Page Not Found!",
                search: '',
            }
        },
        components: {
            mdbCard,
            mdbCardBody,
            mdbCol,
            mdbRow,
            TopNav
        }
    }
</script>
