PGDMP     !    -    	            z           project2    14.5    14.5 
    M           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            N           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            O           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            P           1262    31160    project2    DATABASE     S   CREATE DATABASE project2 WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'C';
    DROP DATABASE project2;
                postgres    false            �            1259    32190    primary_roads    TABLE     �   CREATE TABLE public.primary_roads (
    gid integer NOT NULL,
    linearid character varying(22),
    fullname character varying(100),
    rttyp character varying(1),
    mtfcc character varying(5),
    geom public.geometry(MultiLineString,4326)
);
 !   DROP TABLE public.primary_roads;
       public         heap    postgres    false            �            1259    32189    primary_roads_gid_seq    SEQUENCE     �   CREATE SEQUENCE public.primary_roads_gid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.primary_roads_gid_seq;
       public          postgres    false    216            Q           0    0    primary_roads_gid_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.primary_roads_gid_seq OWNED BY public.primary_roads.gid;
          public          postgres    false    215            �           2604    32193    primary_roads gid    DEFAULT     v   ALTER TABLE ONLY public.primary_roads ALTER COLUMN gid SET DEFAULT nextval('public.primary_roads_gid_seq'::regclass);
 @   ALTER TABLE public.primary_roads ALTER COLUMN gid DROP DEFAULT;
       public          postgres    false    216    215    216            �           2606    32195     primary_roads primary_roads_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY public.primary_roads
    ADD CONSTRAINT primary_roads_pkey PRIMARY KEY (gid);
 J   ALTER TABLE ONLY public.primary_roads DROP CONSTRAINT primary_roads_pkey;
       public            postgres    false    216            �           1259    34143    primary_roads_geom_idx    INDEX     O   CREATE INDEX primary_roads_geom_idx ON public.primary_roads USING gist (geom);
 *   DROP INDEX public.primary_roads_geom_idx;
       public            postgres    false    216           