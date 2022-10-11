-- Table: public.missiles_info

-- DROP TABLE IF EXISTS public.missiles_info;

CREATE TABLE IF NOT EXISTS public.missiles_info
(
    name text COLLATE pg_catalog."default",
    blast real,
    speed real
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.missiles_info
    OWNER to postgres;