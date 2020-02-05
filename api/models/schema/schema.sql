--
-- PostgreSQL database dump
--

-- Dumped from database version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)

--
-- Name: users; Type: TABLE; Schema: public; Owner: jeffkim
--

DROP TABLE IF EXISTS users;
CREATE TABLE users
(
    id           integer                     NOT NULL,
    role_id      integer                     NOT NULL,
    email        character varying(65)       NOT NULL,
    first_name   character varying(65)       NOT NULL,
    last_name    character varying(65)       NOT NULL,
    password     character varying(128)      NOT NULL,
    created_at   timestamp without time zone NOT NULL,
    created_by   character varying(65)       NOT NULL,
    updated_at   timestamp without time zone,
    updated_by   character varying(65),
    is_deleted   boolean                     NOT NULL,
    deleted_at   timestamp without time zone,
    deleted_by   character varying(65),
    housedata_id integer
);

