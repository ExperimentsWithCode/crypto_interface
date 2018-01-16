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
-- Name: coin_mentions; Type: TABLE; Schema: public; Owner: patrickmckelvy
--

CREATE TABLE coin_mentions (
    id integer NOT NULL,
    coin_id character varying NOT NULL,
    mention_body_id character varying NOT NULL,
    is_thread_title boolean,
    is_thread_body boolean,
    is_comment_body boolean,
    "timestamp" timestamp without time zone DEFAULT '2018-01-14 23:55:37.089743'::timestamp without time zone,
    num_mentions integer
);


ALTER TABLE coin_mentions OWNER TO patrickmckelvy;

--
-- Name: j_coins_comments_id_seq; Type: SEQUENCE; Schema: public; Owner: patrickmckelvy
--

CREATE SEQUENCE j_coins_comments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE j_coins_comments_id_seq OWNER TO patrickmckelvy;

--
-- Name: j_coins_comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: patrickmckelvy
--

ALTER SEQUENCE j_coins_comments_id_seq OWNED BY coin_mentions.id;


--
-- Name: coin_mentions id; Type: DEFAULT; Schema: public; Owner: patrickmckelvy
--

ALTER TABLE ONLY coin_mentions ALTER COLUMN id SET DEFAULT nextval('j_coins_comments_id_seq'::regclass);


--
-- Name: coin_mentions j_coins_comments_pkey; Type: CONSTRAINT; Schema: public; Owner: patrickmckelvy
--

ALTER TABLE ONLY coin_mentions
    ADD CONSTRAINT j_coins_comments_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

