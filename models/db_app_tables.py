#This file contains application specific table definitions

#Following table is required to store products
'''
db.define_table('product',
   Field('name',notnull=True,unique=True),
   Field('type','reference product_type'),
   Field('style','reference style_type'),
   Field('shape','reference shape_type'),
   Field('size','reference size_type'),
   Field('price_group','reference price_group_type'),
   Field('price','double'),
   Field('image','upload'),
   Field('sortable','integer'),
   auth.signature,
   format='%(name)s')

db.define_table('product_type',
   Field('name',notnull=True,unique=True))

db.define_table('style_type',
   Field('name',notnull=True,unique=True))

db.define_table('shape_type',
   Field('name',notnull=True,unique=True))

db.define_table('size_type',
   Field('name',notnull=True,unique=True))

db.define_table('price_group_type',
   Field('name',notnull=True,unique=True))
'''
