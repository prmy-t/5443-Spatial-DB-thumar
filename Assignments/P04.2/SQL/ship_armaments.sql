-- Table: public.ship_armaments

-- DROP TABLE IF EXISTS public.ship_armaments;

CREATE TABLE IF NOT EXISTS public.ship_armaments
(
    ship_id smallint,
    gun_name text COLLATE pg_catalog."default",
    gun_info text COLLATE pg_catalog."default",
    ammo_type text[] COLLATE pg_catalog."default",
    ammo text[] COLLATE pg_catalog."default",
    gun_rof smallint,
    gun_propellant smallint,
    pos smallint
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.ship_armaments
    OWNER to postgres;