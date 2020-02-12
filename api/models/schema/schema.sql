--
-- PostgreSQL database dump
--

-- Dumped from database version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)

--
-- Name: users; Type: TABLE; Schema: public; Owner: jeffkim
--
DROP TABLE IF EXISTS role;
CREATE TABLE role
(
    id          integer primary key autoincrement,
    code        character varying(20) NOT NULL,
    name        character varying(50) NOT NULL,
    description character varying(255)
);


DROP TABLE IF EXISTS users;
CREATE TABLE users
(
    id           integer PRIMARY KEY AUTOINCREMENT,
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
    housedata_id integer,

    foreign key (role_id) references role (id)
);

DROP TABLE IF EXISTS laboratory;
CREATE TABLE laboratory
(
    id   integer PRIMARY KEY AUTOINCREMENT,
    name character varying(65) NOT NULL,
    room integer               NOT NULL,
    code character varying(65) NOT NULL
);


DROP TABLE IF EXISTS freezer;
CREATE TABLE freezer
(
    id            integer primary key autoincrement,
    laboratory_id integer,
    room          character varying(65) NOT NULL,
    number        integer               NOT NULL,
    code          character varying(65) NOT NULL,
    foreign key (laboratory_id) references laboratory (id)
);

DROP TABLE IF EXISTS chamber;

CREATE TABLE chamber
(
    id         integer PRIMARY KEY AUTOINCREMENT,
    freezer_id integer,
    type       character varying(50) NOT NULL,
    code       character varying(65) NOT NULL,
    foreign key (freezer_id) references freezer (id)
);

DROP TABLE IF EXISTS rack;
CREATE TABLE rack
(
    id         integer primary key autoincrement,
    chamber_id integer,
    number     integer               NOT NULL,
    code       character varying(65) NOT NULL,
    foreign key (chamber_id) references chamber (id)
);