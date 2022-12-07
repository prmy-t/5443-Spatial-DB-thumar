-- Table: public.bbox

-- DROP TABLE IF EXISTS public.bbox;

CREATE TABLE IF NOT EXISTS public.bbox
(
    box geometry,
    section text COLLATE pg_catalog."default",
    center geometry,
    width integer,
    height integer
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.bbox
    OWNER to postgres;