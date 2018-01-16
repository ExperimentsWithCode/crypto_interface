--
-- PostgreSQL database dump
--

-- Dumped from database version 9.4.5
-- Dumped by pg_dump version 9.6.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: mention_bodies; Type: TABLE; Schema: public; Owner: patrickmckelvy
--

CREATE TABLE mention_bodies (
    id integer NOT NULL,
    thread_id character varying NOT NULL,
    body text NOT NULL,
    parent_id character varying,
    mention_body_id character varying NOT NULL
);


ALTER TABLE mention_bodies OWNER TO patrickmckelvy;

--
-- Name: comments_id_seq; Type: SEQUENCE; Schema: public; Owner: patrickmckelvy
--

CREATE SEQUENCE comments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE comments_id_seq OWNER TO patrickmckelvy;

--
-- Name: comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: patrickmckelvy
--

ALTER SEQUENCE comments_id_seq OWNED BY mention_bodies.id;


--
-- Name: mention_bodies id; Type: DEFAULT; Schema: public; Owner: patrickmckelvy
--

ALTER TABLE ONLY mention_bodies ALTER COLUMN id SET DEFAULT nextval('comments_id_seq'::regclass);


--
-- Name: mention_bodies comments_pkey; Type: CONSTRAINT; Schema: public; Owner: patrickmckelvy
--

ALTER TABLE ONLY mention_bodies
    ADD CONSTRAINT comments_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

