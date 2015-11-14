#This file contains application specific table definitions

db.define_table('category_type',
   Field('name',notnull=True,unique=True),
   format = '%(name)s')

db.define_table('style_type',
   Field('name',notnull=True,unique=True),
   format = '%(name)s')

db.define_table('shape_type',
   Field('name',notnull=True,unique=True),
   format = '%(name)s')

db.define_table('size_type',
   Field('name',notnull=True,unique=True),
   format = '%(name)s')

db.define_table('price_group_type',
   Field('name',notnull=True,unique=True),
   format = '%(name)s')

#Following table is required to store products
db.define_table('product',
   Field('p_name',notnull=True,unique=True),
   Field('p_category','reference category_type'),
   Field('p_style','reference style_type'),
   Field('p_shape','reference shape_type'),
   Field('p_size','reference size_type'),
   Field('p_price_group','reference price_group_type'),
   Field('p_price','double'),
   Field('p_image','upload'),
   Field('p_sortable','integer'),
   auth.signature,
   format='%(p_name)s')
