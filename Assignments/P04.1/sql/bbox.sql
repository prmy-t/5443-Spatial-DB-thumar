-- Table: public.bbox

-- DROP TABLE IF EXISTS public.bbox;

CREATE TABLE IF NOT EXISTS public.bbox
(
    box geometry,
    center geometry
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.bbox
    OWNER to postgres;