PGDMP  .    9                }            CotizacionTest    17.5 (Debian 17.5-1.pgdg120+1)    17.4 e    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            �           1262    17112    CotizacionTest    DATABASE     {   CREATE DATABASE "CotizacionTest" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';
     DROP DATABASE "CotizacionTest";
                     postgres    false            �            1259    17121 	   customers    TABLE     K  CREATE TABLE public.customers (
    id integer NOT NULL,
    type_client_id integer NOT NULL,
    entity_type character varying(1) NOT NULL,
    ruc character varying(11),
    dni character varying(8),
    doc_foreign character varying(20),
    name character varying(35),
    last_name character varying(40),
    business_name character varying(150),
    phone_number character varying(15) NOT NULL,
    email character varying(100) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    deleted_at timestamp without time zone
);
    DROP TABLE public.customers;
       public         heap r       postgres    false            �            1259    17124    customers_id_seq    SEQUENCE     �   CREATE SEQUENCE public.customers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.customers_id_seq;
       public               postgres    false    217            �           0    0    customers_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.customers_id_seq OWNED BY public.customers.id;
          public               postgres    false    218            �            1259    17125    extra_options    TABLE     .  CREATE TABLE public.extra_options (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    price numeric(10,2) NOT NULL,
    description text,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    deleted_at timestamp without time zone
);
 !   DROP TABLE public.extra_options;
       public         heap r       postgres    false            �            1259    17130    extra_options_id_seq    SEQUENCE     �   CREATE SEQUENCE public.extra_options_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.extra_options_id_seq;
       public               postgres    false    219            �           0    0    extra_options_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.extra_options_id_seq OWNED BY public.extra_options.id;
          public               postgres    false    220            �            1259    17131    order_detail_extra_options    TABLE       CREATE TABLE public.order_detail_extra_options (
    order_detail_id integer NOT NULL,
    extra_option_id integer NOT NULL,
    quantity numeric(10,2) NOT NULL,
    linear_meter numeric(10,2),
    width numeric(10,2),
    giga_select character varying(30)
);
 .   DROP TABLE public.order_detail_extra_options;
       public         heap r       postgres    false            �            1259    17134    order_details    TABLE     �  CREATE TABLE public.order_details (
    id integer NOT NULL,
    order_id integer NOT NULL,
    product_id integer NOT NULL,
    height numeric(10,2),
    width numeric(10,2),
    quantity integer NOT NULL,
    linear_meter numeric(10,2),
    subtotal numeric(10,2) NOT NULL,
    total_extra_options numeric(10,2) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    deleted_at timestamp without time zone
);
 !   DROP TABLE public.order_details;
       public         heap r       postgres    false            �            1259    17137    order_details_id_seq    SEQUENCE     �   CREATE SEQUENCE public.order_details_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.order_details_id_seq;
       public               postgres    false    222            �           0    0    order_details_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.order_details_id_seq OWNED BY public.order_details.id;
          public               postgres    false    223            �            1259    17138    order_status    TABLE     3  CREATE TABLE public.order_status (
    id integer NOT NULL,
    code character varying(10) NOT NULL,
    name character varying(50) NOT NULL,
    description text,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    deleted_at timestamp without time zone
);
     DROP TABLE public.order_status;
       public         heap r       postgres    false            �            1259    17143    order_status_id_seq    SEQUENCE     �   CREATE SEQUENCE public.order_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.order_status_id_seq;
       public               postgres    false    224            �           0    0    order_status_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.order_status_id_seq OWNED BY public.order_status.id;
          public               postgres    false    225            �            1259    17144    orders    TABLE     <  CREATE TABLE public.orders (
    id integer NOT NULL,
    customer_id integer NOT NULL,
    store_id integer NOT NULL,
    order_status_id integer NOT NULL,
    total_amount numeric(10,2) NOT NULL,
    profit_margin numeric(10,2) NOT NULL,
    discount_applied numeric(10,2) NOT NULL,
    final_amount numeric(10,2) NOT NULL,
    payment_method character varying(50),
    shipping_address character varying(200),
    notes text,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    deleted_at timestamp without time zone
);
    DROP TABLE public.orders;
       public         heap r       postgres    false            �            1259    17149    orders_id_seq    SEQUENCE     �   CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.orders_id_seq;
       public               postgres    false    226            �           0    0    orders_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;
          public               postgres    false    227            �            1259    17150    product_extra_options    TABLE     �   CREATE TABLE public.product_extra_options (
    product_id integer NOT NULL,
    extra_option_id integer NOT NULL,
    created_at timestamp without time zone
);
 )   DROP TABLE public.product_extra_options;
       public         heap r       postgres    false            �            1259    17153    product_product_types    TABLE     �   CREATE TABLE public.product_product_types (
    product_id integer NOT NULL,
    product_type_id integer NOT NULL,
    created_at timestamp without time zone
);
 )   DROP TABLE public.product_product_types;
       public         heap r       postgres    false            �            1259    17156    product_types    TABLE       CREATE TABLE public.product_types (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    deleted_at timestamp without time zone
);
 !   DROP TABLE public.product_types;
       public         heap r       postgres    false            �            1259    17161    product_types_id_seq    SEQUENCE     �   CREATE SEQUENCE public.product_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.product_types_id_seq;
       public               postgres    false    230            �           0    0    product_types_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.product_types_id_seq OWNED BY public.product_types.id;
          public               postgres    false    231            �            1259    17162    products    TABLE     �  CREATE TABLE public.products (
    id integer NOT NULL,
    sku character varying(20) NOT NULL,
    name character varying(150) NOT NULL,
    description character varying(150),
    unity_measure character varying(40) NOT NULL,
    price numeric(10,2) NOT NULL,
    image_url character varying(150),
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    deleted_at timestamp without time zone
);
    DROP TABLE public.products;
       public         heap r       postgres    false            �            1259    17167    products_id_seq    SEQUENCE     �   CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.products_id_seq;
       public               postgres    false    232            �           0    0    products_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;
          public               postgres    false    233            �            1259    17168    stores    TABLE     "  CREATE TABLE public.stores (
    id integer NOT NULL,
    code character varying(10),
    name character varying(100) NOT NULL,
    address character varying(255),
    phone_number character varying(15),
    email character varying(100),
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    deleted_at timestamp without time zone,
    phone_number_secondary character varying(15),
    yape_phone_number character varying(15),
    bcp_cta character varying(16),
    bcp_cci character varying(20)
);
    DROP TABLE public.stores;
       public         heap r       postgres    false            �            1259    17171    stores_id_seq    SEQUENCE     �   CREATE SEQUENCE public.stores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.stores_id_seq;
       public               postgres    false    234            �           0    0    stores_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.stores_id_seq OWNED BY public.stores.id;
          public               postgres    false    235            �            1259    17172    type_clients    TABLE     C  CREATE TABLE public.type_clients (
    id integer NOT NULL,
    code character varying(10) NOT NULL,
    name character varying(50) NOT NULL,
    margin double precision NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone,
    deleted_at timestamp without time zone
);
     DROP TABLE public.type_clients;
       public         heap r       postgres    false            �            1259    17175    type_clients_id_seq    SEQUENCE     �   CREATE SEQUENCE public.type_clients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.type_clients_id_seq;
       public               postgres    false    236            �           0    0    type_clients_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.type_clients_id_seq OWNED BY public.type_clients.id;
          public               postgres    false    237            �           2604    17176    customers id    DEFAULT     l   ALTER TABLE ONLY public.customers ALTER COLUMN id SET DEFAULT nextval('public.customers_id_seq'::regclass);
 ;   ALTER TABLE public.customers ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    218    217            �           2604    17177    extra_options id    DEFAULT     t   ALTER TABLE ONLY public.extra_options ALTER COLUMN id SET DEFAULT nextval('public.extra_options_id_seq'::regclass);
 ?   ALTER TABLE public.extra_options ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    220    219            �           2604    17178    order_details id    DEFAULT     t   ALTER TABLE ONLY public.order_details ALTER COLUMN id SET DEFAULT nextval('public.order_details_id_seq'::regclass);
 ?   ALTER TABLE public.order_details ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    223    222            �           2604    17179    order_status id    DEFAULT     r   ALTER TABLE ONLY public.order_status ALTER COLUMN id SET DEFAULT nextval('public.order_status_id_seq'::regclass);
 >   ALTER TABLE public.order_status ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    225    224            �           2604    17180 	   orders id    DEFAULT     f   ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);
 8   ALTER TABLE public.orders ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    227    226            �           2604    17181    product_types id    DEFAULT     t   ALTER TABLE ONLY public.product_types ALTER COLUMN id SET DEFAULT nextval('public.product_types_id_seq'::regclass);
 ?   ALTER TABLE public.product_types ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    231    230            �           2604    17182    products id    DEFAULT     j   ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);
 :   ALTER TABLE public.products ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    233    232            �           2604    17183 	   stores id    DEFAULT     f   ALTER TABLE ONLY public.stores ALTER COLUMN id SET DEFAULT nextval('public.stores_id_seq'::regclass);
 8   ALTER TABLE public.stores ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    235    234            �           2604    17184    type_clients id    DEFAULT     r   ALTER TABLE ONLY public.type_clients ALTER COLUMN id SET DEFAULT nextval('public.type_clients_id_seq'::regclass);
 >   ALTER TABLE public.type_clients ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    237    236            �          0    17121 	   customers 
   TABLE DATA           �   COPY public.customers (id, type_client_id, entity_type, ruc, dni, doc_foreign, name, last_name, business_name, phone_number, email, created_at, updated_at, deleted_at) FROM stdin;
    public               postgres    false    217   ��       �          0    17125    extra_options 
   TABLE DATA           i   COPY public.extra_options (id, name, price, description, created_at, updated_at, deleted_at) FROM stdin;
    public               postgres    false    219   p�       �          0    17131    order_detail_extra_options 
   TABLE DATA           �   COPY public.order_detail_extra_options (order_detail_id, extra_option_id, quantity, linear_meter, width, giga_select) FROM stdin;
    public               postgres    false    221   ݌       �          0    17134    order_details 
   TABLE DATA           �   COPY public.order_details (id, order_id, product_id, height, width, quantity, linear_meter, subtotal, total_extra_options, created_at, deleted_at) FROM stdin;
    public               postgres    false    222   ��       �          0    17138    order_status 
   TABLE DATA           g   COPY public.order_status (id, code, name, description, created_at, updated_at, deleted_at) FROM stdin;
    public               postgres    false    224   �       �          0    17144    orders 
   TABLE DATA           �   COPY public.orders (id, customer_id, store_id, order_status_id, total_amount, profit_margin, discount_applied, final_amount, payment_method, shipping_address, notes, created_at, updated_at, deleted_at) FROM stdin;
    public               postgres    false    226   V�       �          0    17150    product_extra_options 
   TABLE DATA           X   COPY public.product_extra_options (product_id, extra_option_id, created_at) FROM stdin;
    public               postgres    false    228   s�       �          0    17153    product_product_types 
   TABLE DATA           X   COPY public.product_product_types (product_id, product_type_id, created_at) FROM stdin;
    public               postgres    false    229   ؒ       �          0    17156    product_types 
   TABLE DATA           b   COPY public.product_types (id, name, description, created_at, updated_at, deleted_at) FROM stdin;
    public               postgres    false    230   W�       �          0    17162    products 
   TABLE DATA           �   COPY public.products (id, sku, name, description, unity_measure, price, image_url, created_at, updated_at, deleted_at) FROM stdin;
    public               postgres    false    232   �       �          0    17168    stores 
   TABLE DATA           �   COPY public.stores (id, code, name, address, phone_number, email, created_at, updated_at, deleted_at, phone_number_secondary, yape_phone_number, bcp_cta, bcp_cci) FROM stdin;
    public               postgres    false    234   ��       �          0    17172    type_clients 
   TABLE DATA           b   COPY public.type_clients (id, code, name, margin, created_at, updated_at, deleted_at) FROM stdin;
    public               postgres    false    236   }�       �           0    0    customers_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.customers_id_seq', 5, true);
          public               postgres    false    218            �           0    0    extra_options_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.extra_options_id_seq', 21, true);
          public               postgres    false    220            �           0    0    order_details_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.order_details_id_seq', 1, false);
          public               postgres    false    223            �           0    0    order_status_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.order_status_id_seq', 11, true);
          public               postgres    false    225            �           0    0    orders_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.orders_id_seq', 1, false);
          public               postgres    false    227            �           0    0    product_types_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.product_types_id_seq', 2, true);
          public               postgres    false    231            �           0    0    products_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.products_id_seq', 9, true);
          public               postgres    false    233            �           0    0    stores_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.stores_id_seq', 1, true);
          public               postgres    false    235            �           0    0    type_clients_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.type_clients_id_seq', 4, true);
          public               postgres    false    237            �           2606    17188    customers customers_dni_key 
   CONSTRAINT     U   ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_dni_key UNIQUE (dni);
 E   ALTER TABLE ONLY public.customers DROP CONSTRAINT customers_dni_key;
       public                 postgres    false    217            �           2606    17190 #   customers customers_doc_foreign_key 
   CONSTRAINT     e   ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_doc_foreign_key UNIQUE (doc_foreign);
 M   ALTER TABLE ONLY public.customers DROP CONSTRAINT customers_doc_foreign_key;
       public                 postgres    false    217            �           2606    17192    customers customers_email_key 
   CONSTRAINT     Y   ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_email_key UNIQUE (email);
 G   ALTER TABLE ONLY public.customers DROP CONSTRAINT customers_email_key;
       public                 postgres    false    217            �           2606    17194    customers customers_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.customers DROP CONSTRAINT customers_pkey;
       public                 postgres    false    217            �           2606    17196    customers customers_ruc_key 
   CONSTRAINT     U   ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_ruc_key UNIQUE (ruc);
 E   ALTER TABLE ONLY public.customers DROP CONSTRAINT customers_ruc_key;
       public                 postgres    false    217            �           2606    17198 $   extra_options extra_options_name_key 
   CONSTRAINT     _   ALTER TABLE ONLY public.extra_options
    ADD CONSTRAINT extra_options_name_key UNIQUE (name);
 N   ALTER TABLE ONLY public.extra_options DROP CONSTRAINT extra_options_name_key;
       public                 postgres    false    219            �           2606    17200     extra_options extra_options_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.extra_options
    ADD CONSTRAINT extra_options_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.extra_options DROP CONSTRAINT extra_options_pkey;
       public                 postgres    false    219            �           2606    17202 :   order_detail_extra_options order_detail_extra_options_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.order_detail_extra_options
    ADD CONSTRAINT order_detail_extra_options_pkey PRIMARY KEY (order_detail_id, extra_option_id);
 d   ALTER TABLE ONLY public.order_detail_extra_options DROP CONSTRAINT order_detail_extra_options_pkey;
       public                 postgres    false    221    221            �           2606    17204     order_details order_details_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.order_details
    ADD CONSTRAINT order_details_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.order_details DROP CONSTRAINT order_details_pkey;
       public                 postgres    false    222            �           2606    17206 "   order_status order_status_code_key 
   CONSTRAINT     ]   ALTER TABLE ONLY public.order_status
    ADD CONSTRAINT order_status_code_key UNIQUE (code);
 L   ALTER TABLE ONLY public.order_status DROP CONSTRAINT order_status_code_key;
       public                 postgres    false    224            �           2606    17208 "   order_status order_status_name_key 
   CONSTRAINT     ]   ALTER TABLE ONLY public.order_status
    ADD CONSTRAINT order_status_name_key UNIQUE (name);
 L   ALTER TABLE ONLY public.order_status DROP CONSTRAINT order_status_name_key;
       public                 postgres    false    224            �           2606    17210    order_status order_status_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.order_status
    ADD CONSTRAINT order_status_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.order_status DROP CONSTRAINT order_status_pkey;
       public                 postgres    false    224            �           2606    17212    orders orders_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_pkey;
       public                 postgres    false    226            �           2606    17214 0   product_extra_options product_extra_options_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.product_extra_options
    ADD CONSTRAINT product_extra_options_pkey PRIMARY KEY (product_id, extra_option_id);
 Z   ALTER TABLE ONLY public.product_extra_options DROP CONSTRAINT product_extra_options_pkey;
       public                 postgres    false    228    228            �           2606    17216 0   product_product_types product_product_types_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.product_product_types
    ADD CONSTRAINT product_product_types_pkey PRIMARY KEY (product_id, product_type_id);
 Z   ALTER TABLE ONLY public.product_product_types DROP CONSTRAINT product_product_types_pkey;
       public                 postgres    false    229    229            �           2606    17218 $   product_types product_types_name_key 
   CONSTRAINT     _   ALTER TABLE ONLY public.product_types
    ADD CONSTRAINT product_types_name_key UNIQUE (name);
 N   ALTER TABLE ONLY public.product_types DROP CONSTRAINT product_types_name_key;
       public                 postgres    false    230            �           2606    17220     product_types product_types_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.product_types
    ADD CONSTRAINT product_types_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.product_types DROP CONSTRAINT product_types_pkey;
       public                 postgres    false    230            �           2606    17222    products products_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.products DROP CONSTRAINT products_pkey;
       public                 postgres    false    232            �           2606    17224    products products_sku_key 
   CONSTRAINT     S   ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_sku_key UNIQUE (sku);
 C   ALTER TABLE ONLY public.products DROP CONSTRAINT products_sku_key;
       public                 postgres    false    232            �           2606    17226    stores stores_code_key 
   CONSTRAINT     Q   ALTER TABLE ONLY public.stores
    ADD CONSTRAINT stores_code_key UNIQUE (code);
 @   ALTER TABLE ONLY public.stores DROP CONSTRAINT stores_code_key;
       public                 postgres    false    234            �           2606    17228    stores stores_email_key 
   CONSTRAINT     S   ALTER TABLE ONLY public.stores
    ADD CONSTRAINT stores_email_key UNIQUE (email);
 A   ALTER TABLE ONLY public.stores DROP CONSTRAINT stores_email_key;
       public                 postgres    false    234            �           2606    17230    stores stores_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.stores
    ADD CONSTRAINT stores_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.stores DROP CONSTRAINT stores_pkey;
       public                 postgres    false    234            �           2606    17232 "   type_clients type_clients_code_key 
   CONSTRAINT     ]   ALTER TABLE ONLY public.type_clients
    ADD CONSTRAINT type_clients_code_key UNIQUE (code);
 L   ALTER TABLE ONLY public.type_clients DROP CONSTRAINT type_clients_code_key;
       public                 postgres    false    236            �           2606    17234 "   type_clients type_clients_name_key 
   CONSTRAINT     ]   ALTER TABLE ONLY public.type_clients
    ADD CONSTRAINT type_clients_name_key UNIQUE (name);
 L   ALTER TABLE ONLY public.type_clients DROP CONSTRAINT type_clients_name_key;
       public                 postgres    false    236            �           2606    17236    type_clients type_clients_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.type_clients
    ADD CONSTRAINT type_clients_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.type_clients DROP CONSTRAINT type_clients_pkey;
       public                 postgres    false    236            �           2606    17237 '   customers customers_type_client_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_type_client_id_fkey FOREIGN KEY (type_client_id) REFERENCES public.type_clients(id);
 Q   ALTER TABLE ONLY public.customers DROP CONSTRAINT customers_type_client_id_fkey;
       public               postgres    false    236    217    3320            �           2606    17242 J   order_detail_extra_options order_detail_extra_options_extra_option_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.order_detail_extra_options
    ADD CONSTRAINT order_detail_extra_options_extra_option_id_fkey FOREIGN KEY (extra_option_id) REFERENCES public.extra_options(id);
 t   ALTER TABLE ONLY public.order_detail_extra_options DROP CONSTRAINT order_detail_extra_options_extra_option_id_fkey;
       public               postgres    false    221    3284    219            �           2606    17247 J   order_detail_extra_options order_detail_extra_options_order_detail_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.order_detail_extra_options
    ADD CONSTRAINT order_detail_extra_options_order_detail_id_fkey FOREIGN KEY (order_detail_id) REFERENCES public.order_details(id);
 t   ALTER TABLE ONLY public.order_detail_extra_options DROP CONSTRAINT order_detail_extra_options_order_detail_id_fkey;
       public               postgres    false    222    3288    221            �           2606    17252 )   order_details order_details_order_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.order_details
    ADD CONSTRAINT order_details_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id);
 S   ALTER TABLE ONLY public.order_details DROP CONSTRAINT order_details_order_id_fkey;
       public               postgres    false    226    222    3296            �           2606    17257 +   order_details order_details_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.order_details
    ADD CONSTRAINT order_details_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);
 U   ALTER TABLE ONLY public.order_details DROP CONSTRAINT order_details_product_id_fkey;
       public               postgres    false    232    3306    222            �           2606    17262    orders orders_customer_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);
 H   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_customer_id_fkey;
       public               postgres    false    217    3278    226            �           2606    17267 "   orders orders_order_status_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_order_status_id_fkey FOREIGN KEY (order_status_id) REFERENCES public.order_status(id);
 L   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_order_status_id_fkey;
       public               postgres    false    3294    226    224                        2606    17272    orders orders_store_id_fkey    FK CONSTRAINT     |   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_store_id_fkey FOREIGN KEY (store_id) REFERENCES public.stores(id);
 E   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_store_id_fkey;
       public               postgres    false    234    3314    226                       2606    17277 @   product_extra_options product_extra_options_extra_option_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.product_extra_options
    ADD CONSTRAINT product_extra_options_extra_option_id_fkey FOREIGN KEY (extra_option_id) REFERENCES public.extra_options(id);
 j   ALTER TABLE ONLY public.product_extra_options DROP CONSTRAINT product_extra_options_extra_option_id_fkey;
       public               postgres    false    228    219    3284                       2606    17282 ;   product_extra_options product_extra_options_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.product_extra_options
    ADD CONSTRAINT product_extra_options_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);
 e   ALTER TABLE ONLY public.product_extra_options DROP CONSTRAINT product_extra_options_product_id_fkey;
       public               postgres    false    232    3306    228                       2606    17287 ;   product_product_types product_product_types_product_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.product_product_types
    ADD CONSTRAINT product_product_types_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);
 e   ALTER TABLE ONLY public.product_product_types DROP CONSTRAINT product_product_types_product_id_fkey;
       public               postgres    false    229    232    3306                       2606    17292 @   product_product_types product_product_types_product_type_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.product_product_types
    ADD CONSTRAINT product_product_types_product_type_id_fkey FOREIGN KEY (product_type_id) REFERENCES public.product_types(id);
 j   ALTER TABLE ONLY public.product_product_types DROP CONSTRAINT product_product_types_product_type_id_fkey;
       public               postgres    false    229    3304    230            �   �  x�}�Kn�0@��S�&�R+Y/��+oX�PY�d �F��� Y��X�r��@�ߌ�q�8la�g�VR�߇)�Sz��{�5Fá"6J�����i��/(��Z؆���Vyf��޿�vە A/H*�F�v�	�Xfx_��ܧ�1ż�>6�Oa��s�Ɏ���B�d��fw9�O劝P-�LX�}��y�}.���:��'�P���u�JjuH����p�������"�0��9�/2-zf����E�QΥ���-j��U����H2�r.�@w�qnc��x�1�>��۰��RBȴN�Tإ�
��*�,7��_ȮQ7\�hZ��X�b�՗we��9�j|��dx#�|���mqͅ7�2���\���Ć�VR/�����a�H�L;�ryY;�Z�~
ۼs      �   ]  x���Mr�0�5>�.F���L�j�E��F�U�+p��mz�N����	�1a�q�6�L�??=�B�k�KW��й�h�q����r�
��v�u�8���m�����F{�ukPmP���
�5֔GSq��U��%cK��BR��\t�qA����Cp�b76��KW�Lg��W`�
5��:�
)Z\� ��8��gFu��KBb�g�\\}�Ӆ�#2�tm�L�\!�z�'0�Ƃ0̒�0<zW��gݣ��q�an+�Js�<�xS�����c�I�\}Х��m�4��\��x�me�ΰ�1k�6�������U�<���[�V��u?���"a\LT�Q$o�-�/�|JK,c�T��\:���o|�WuD�R���s蒣ڽ���XPɹ����B���:�k����aY�P}��t�7І���'5�Lf�����d���0*&�D��OT��� ����XYFLM,Y��_p�n� ]X�\�o�Gh�9�*�Dޮmn�CQ�.+�M&��*I0����'=_ _���/�^P`~�Q�(�i��鲫=���B�:f�d�x��`f�9����La�rŸ����GW�j[��zݿ���������h\�|���M+�w�]o@:Q�}`"��v,�ֆd%ʭ.M�]���y��� ��Fn���$�:��ޏ �H�����5u/VD"J�<]+L��E�,G�X��nO>�VY�*1�>D���.:T����|shv%Y��`NF�q�OT�D�9lŅJ)���;��P�OR��͂�K��3OFa�?R�q��i�k-�����m2
n2tu��]ou�L��ȟ����]�����'�
r4�G�&^,��i1�      �      x������ � �      �      x������ � �      �   /  x�}��R�0���S����Nrc�2C�L`81��&�*V*;L�mx���y��d;1��	�U��o�۵Gf�dLf�g��)���xć3ʨd�5hF3�\��W���ߜ*�fK���0V������W�\�hn�0s�A�/(�[�s��Zq(�C|׏����O��CwEN�n=Lz>M'_ɨ�T���N��EEJ_��8�F�9DY���0w�J�%�#c\�Ѝ�(����B����錤9�i0y�f�ʦ@P��wZ�<���c�$Uax�/��^˛{�%��x�0�;Fꅎ�q�?BҐ�\��MI�$sL�.��e�G����ZUmWk	%[Ӵ�_kUr��_� )��`(�jxf��B��>dh5Ɵ�F���xN'Q���������z<%F�፜�����@6�iו^���H�d�i���Z�0t�����X�b�N~����qJg��e���Ӯ��2qT�a�E\��0#Q��:S+��]�B�Q�sv�O�n�^]��M�u����=]ۆ���д0�����'����p�w`�vI��$��pIT��M ���{������W�R�èEM~�j�ʬE+7Н�/V�Y�]B��Sb�VLc_�4�:y��0��]NFd�r��꼉U��7�j�{��Yz�����$^!��a�f퉽}�Z�����KO�١&K�������G	+V�_�����+!�F��촟`��XU�7_ƫ/�I�nB�����Ď��A���d/����$��[��T%���!LZ�t�c'��A�#�>���^��<�S�      �      x������ � �      �   U  x����m�0D��QN`����Ǳ��U��-uU��+������;�����!Ֆ��
Ϝ�9=q|��swyz��<s{�����ݍCq���84g�?y���Ƙ��cy�����v�e|������m�o�Z�.����!��Fk�C8eZN�7�p8u�f��2ơzu8�2Tws���h=ĩMz�a�UZ����ppe�L��>Z����G.%M�ie�[JQ�`�pe(�<z1����7�n~ �h�^�)Sv㰝:4�w3O�lơ;u8��ߪ���]�gh.�>B��V��Z��[����-�F[��6��}�������M.�X��Ь2�S�f�)�q��8\�8tk�S���<�e����Og	�/��:|�ó�����_||��?y�|1]�W����~��~u���C~�Пy>�=�~i̯Jn%��i?�Џy>�7�пq�{��Kr��V/��S;��reȮє��W�x��M�����ݓY�߾�}�-��[�e��0�ߟ�˽λ6�/L�u��i�M�!�24�����4�7��c��S43���C:�����Qz����8�N��<�3����}n�u�q��I's      �   o   x�mλ�0��[�5`B\�Z��\&{����2�5s'U3|x��X�k`�\k���m��R�To��i�#�q�}f�厼�^cFt���4E����1[�S��	�?�R3q      �   �   x�}�;�0E��^�l V<&�DCI�f)� ' 6�*��!�{z�8Vm�Hi�c���Nj�9L,)L@�gO@9�����L^�Xe]`;�:[�v��l�R�Ө��x�*$�~^�B#�@#���p�t�(`M�lL���Rz��Z?QC�      �   �  x���M��0�u=E/@-���N\�YWn
v�&| 3��S���2�Wa��y���򪋒���JV()��)M�W&WUW�z��V��5u�[�p��PɐJ�ܔ*��<��/��L8�wX�]y|��G�T����%'^/��T��q\�*��Zu/?LU��9(� �|�X�*�w@���Ҫ@�^K?�w8i��p�$��Л��띹�=7nL�lഏ���թ]-#�ʤ|*5?�������ڣjt�z����_)�)\F.#�L����L��t[�7����F�g��Pz�r�K'���/l_4Y����4XX7n����w<pNE ��߃����K�O��17\@�����O@-��/�7~+����^9��]�R0q�����r;�Z��̟>��~���x\�OEp�=��f�1�ݥ      �   �   x�}���0D��+<�q0�L@B��X�J��@�����w�Λ�ao�LLYº�;�8\�M�`��S8��^�`l��M�Y;��G-ӫ�
e�Ձ���`��Y��a�Y 1I����k�>כ�ɝ��!$�8���<�|"n�BL���n�`@a!4^��9p��"��{�CqrEQ| �.<v      �   �   x�}�A
�0 ��+��!���&�@��/�RJ��"��w��b��,��S'�8�i�U��Xu[~�B�F�Ʀ֮F� �����]�����tҦ%?�}f�9�S�Vytp�XmDl����Z��2�n0�j�+�n��Tr���߿P@�<����z%�� W�     