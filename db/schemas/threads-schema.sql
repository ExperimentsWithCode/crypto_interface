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
-- Name: threads; Type: TABLE; Schema: public; Owner: patrickmckelvy
--

CREATE TABLE threads (
    id integer NOT NULL,
    thread_id character varying NOT NULL,
    forum_id character varying NOT NULL,
    title text,
    body text
);


ALTER TABLE threads OWNER TO patrickmckelvy;

--
-- Name: threads_id_seq1; Type: SEQUENCE; Schema: public; Owner: patrickmckelvy
--

CREATE SEQUENCE threads_id_seq1
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE threads_id_seq1 OWNER TO patrickmckelvy;

--
-- Name: threads_id_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: patrickmckelvy
--

ALTER SEQUENCE threads_id_seq1 OWNED BY threads.id;


--
-- Name: threads id; Type: DEFAULT; Schema: public; Owner: patrickmckelvy
--

ALTER TABLE ONLY threads ALTER COLUMN id SET DEFAULT nextval('threads_id_seq1'::regclass);


--
-- Name: threads threads_pkey; Type: CONSTRAINT; Schema: public; Owner: patrickmckelvy
--

ALTER TABLE ONLY threads
    ADD CONSTRAINT threads_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

