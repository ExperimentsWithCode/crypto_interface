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
-- Name: coins; Type: TABLE; Schema: public; Owner: patrickmckelvy
--

CREATE TABLE coins (
    id integer NOT NULL,
    coin_id character varying(10),
    coin_long_name character varying(30),
    price_btc double precision,
    price_eth double precision,
    price_usd double precision,
    mkt_cap double precision,
    data_timestamp timestamp without time zone
);


ALTER TABLE coins OWNER TO patrickmckelvy;

--
-- Name: coins_id_seq; Type: SEQUENCE; Schema: public; Owner: patrickmckelvy
--

CREATE SEQUENCE coins_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE coins_id_seq OWNER TO patrickmckelvy;

--
-- Name: coins_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: patrickmckelvy
--

ALTER SEQUENCE coins_id_seq OWNED BY coins.id;


--
-- Name: coins id; Type: DEFAULT; Schema: public; Owner: patrickmckelvy
--

ALTER TABLE ONLY coins ALTER COLUMN id SET DEFAULT nextval('coins_id_seq'::regclass);


--
-- Name: coins coins_pkey; Type: CONSTRAINT; Schema: public; Owner: patrickmckelvy
--

ALTER TABLE ONLY coins
    ADD CONSTRAINT coins_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

