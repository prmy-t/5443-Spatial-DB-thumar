-- Table: public.ship_armors

-- DROP TABLE IF EXISTS public.ship_armors;

CREATE TABLE IF NOT EXISTS public.ship_armors
(
    ship_id smallint,
    hull smallint,
    deck smallint
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.ship_armors
    OWNER to postgres;