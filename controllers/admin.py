@auth.requires_membership('admin')
def manage_users():
    grid = SQLFORM.smartgrid(db.auth_user,linked_tables=[])
    return dict(grid=grid)

@auth.requires_membership('admin')
def manage_products():
    grid = SQLFORM.smartgrid(db.product,linked_tables=[])
    return dict(grid=grid)
