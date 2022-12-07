-- Table: public.ships

-- DROP TABLE IF EXISTS public.ships;

CREATE TABLE IF NOT EXISTS public.ships
(
    table_id integer NOT NULL DEFAULT nextval('ships_table_id_seq'::regclass),
    bearing smallint,
    ship_id smallint,
    identifier text COLLATE pg_catalog."default",
    category text COLLATE pg_catalog."default",
    shipclass text COLLATE pg_catalog."default",
    length smallint,
    width smallint,
    torpedolaunchers smallint,
    speed smallint,
    turn_radius smallint,
    location geometry
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.ships
    OWNER to postgres;