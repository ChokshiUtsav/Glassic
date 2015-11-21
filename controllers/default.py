# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

import datetime
balance=0

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    return dict(message=T('Welcome to web2py!'))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


def browseandshop():
    category_list=db(db.category_type.id>0).select().as_list()
    style_list=db(db.style_type.id>0).select().as_list()
    shape_list=db(db.shape_type.id>0).select().as_list()
    size_list=db(db.size_type.id>0).select().as_list()
    price_group_list=db(db.price_group_type.id>0).select().as_list()
    if request.args(0):
        filterCriteria=str(request.args(0))
        field=filterCriteria.split("=")[0]
        value=filterCriteria.split("=")[1]
        p_field="p_"+field.split("_")[0]
        product_list=[]
        if field=='category_type':
            valId1 = db(db.category_type.name==value).select(db.category_type.id).as_list()
            if len(valId1)!=0:
                valId=int(valId1[0]['id'])
                product_list=db(db.product.p_category==valId).select(db.product.id,
                                                          db.product.p_name,
                                                          db.product.p_image,
                                                          db.product.p_price).as_list()
        elif field=='style_type':
            valId1 = db(db.style_type.name==value).select(db.style_type.id).as_list()
            if len(valId1)!=0:
                valId=int(valId1[0]['id'])
                product_list=db(db.product.p_style==valId).select(db.product.id,
                                                          db.product.p_name,
                                                          db.product.p_image,
                                                          db.product.p_price).as_list()
        elif field=='shape_type':
            valId1 = db(db.shape_type.name==value).select(db.shape_type.id).as_list()
            if len(valId1)!=0:
                valId=int(valId1[0]['id'])
                product_list=db(db.product.p_shape==valId).select(db.product.id,
                                                          db.product.p_name,
                                                          db.product.p_image,
                                                          db.product.p_price).as_list()
        elif field=='size_type':
            valId1 = db(db.size_type.name==value).select(db.size_type.id).as_list()
            if len(valId1)!=0:
                valId=int(valId1[0]['id'])
                product_list=db(db.product.p_size==valId).select(db.product.id,
                                                          db.product.p_name,
                                                          db.product.p_image,
                                                          db.product.p_price).as_list()
        elif field=='price_group_type':
            valId1 = db(db.price_group_type.name==value).select(db.price_group_type.id).as_list()
            if len(valId1)!=0:
                valId=int(valId1[0]['id'])
                product_list=db(db.product.p_price_group==valId).select(db.product.id,
                                                          db.product.p_name,
                                                          db.product.p_image,
                                                          db.product.p_price).as_list()

        #response.flash=field+value+p_field+str(valId)
    else:
        product_list=db(db.product.id>0).select(db.product.id,
                                                db.product.p_name,
                                                db.product.p_image,
                                                db.product.p_price).as_list()
    return locals()

@auth.requires_login()
#To maintain cart across session
def maintain_cart():
    key=str(request.args(0))
    if not session.cart:
        session.cart={}
        #response.flash="Found Empty Cart"
    if key in session.cart:
        del session.cart[key]
    else:
        session.cart[key]=1

@auth.requires_login()
#To see and process the cart
def yourcart():
    if request.args(0):
        key=str(request.args(0))
        del session.cart[key]
    if not session.cart:
        session.flash = 'Add something to cart'
        redirect(URL('default', 'browseandshop'))
    else:
        product_list=[]
        for i in session.cart:
            for row in db(db.product.id==int(i)).select(db.product.id,db.product.p_name,db.product.p_image,db.product.p_price):
                product_list.append(row)
    return locals()

@auth.requires_login()
def placeOrderValidation(form):

    pmode = str(form.vars.payment_mode)
    totalPrice=int(session.totalPrice)
    dmode = str(form.vars.delivery_mode)

    if dmode=='Speed Transit':
        totalPrice = totalPrice + 100

    if pmode=='Pay Using Wallet':
        if  totalPrice > balance:
            form.errors.payment_mode = 'Insufficient balance!! Please use COD or fill wallet!'
        else:
            session.totalPrice = totalPrice

    if pmode=='Cash On Delivery':
        if totalPrice < 1200 :
            form.errors.payment_mode = 'Can not place an order of less than 1200 on COD.'
        else:
            session.totalPrice = totalPrice

@auth.requires_login()
def placeorder():
    global balance
    form = SQLFORM.factory(
        Field('first_name','string' ,requires=IS_NOT_EMPTY()),
        Field('last_name','string',requires=IS_NOT_EMPTY()),
        Field('email_address', requires=IS_EMAIL()),
        Field('shipping_address', requires=IS_NOT_EMPTY()),
        Field('shipping_city', requires=IS_NOT_EMPTY()),
        Field('zip_code', requires=IS_NOT_EMPTY()),
        Field('contact', 'string',length=10,requires=IS_NOT_EMPTY()),
        Field('payment_mode',requires=IS_IN_SET(['Cash On Delivery','Pay Using Wallet'])),
        Field('delivery_mode',requires=IS_IN_SET(['Speed Transit','Normal Transit'])),
    )
    form.vars.first_name=auth.user.first_name
    form.vars.last_name=auth.user.last_name
    form.vars.email_address=auth.user.email
    form.vars.shipping_address=auth.user.address
    form.vars.shipping_city=auth.user.city
    form.vars.zip_code=auth.user.zip
    form.vars.contact=auth.user.phone

    row=db(db.auth_user.id==auth.user_id).select(db.auth_user.wallet)
    balance=int(row[0]['wallet'])

    if form.process(onvalidation=placeOrderValidation,message_onfailure="Please fill all values correctly!").accepted:
        dmid = db(db.delivery_type.name==form.vars.delivery_mode).select(db.delivery_type.id)
        pmid = db(db.payment_type.name==form.vars.payment_mode).select(db.payment_type.id)
        dmsid = db(db.delivery_status_type.name=='Shipped').select(db.delivery_status_type.id)
        date = datetime.date.today()
        new_order_id=db.orders.insert(user_id=auth.user_id,
                         total_price=int(session.totalPrice),
                         delivery_mode=dmid[0],
                         payment_mode=pmid[0],
                         delivery_status=dmsid[0],
                         order_date=date,
                         first_name=form.vars.first_name,
                         last_name=form.vars.last_name,
                         email_address=form.vars.email_address,
                         shipping_address=form.vars.shipping_address,
                         shipping_city=form.vars.shipping_city,
                         zip=form.vars.zip_code,
                         contact=form.vars.contact,
                         )
        for i in session.cart:
            db.ordered_items.insert(order_id=new_order_id,product_id=int(i))

        #Updating user's wallet
        if str(form.vars.payment_mode)=='Pay Using Wallet':
            wallet_balance=balance-int(session.totalPrice)
            db(db.auth_user.id==auth.user_id).update(wallet=wallet_balance)

        #Send Mail to user
        msg_list={}
        msg_list['first_name']=form.vars.first_name
        msg_list['last_name']=form.vars.last_name
        msg_list['email_address']=form.vars.email_address
        msg_list['shipping_address']=form.vars.shipping_address
        msg_list['shipping_city']=form.vars.shipping_city
        msg_list['zip_code']=form.vars.zip_code
        msg_list['id']=new_order_id
        msg_list['order_date']=datetime.date.today()
        product_list=[]
        for i in session.cart:
            for row in db(db.product.id==int(i)).select(db.product.id,db.product.p_name,db.product.p_image,db.product.p_price):
                product_list.append(row)
        msg_list['ordered_products']=product_list
        msg_list['delivery_mode']=form.vars.delivery_mode
        msg_list['payment_mode']=form.vars.payment_mode
        msg_list['delivery_status']='Will be shipped'

        context=dict(msg_list=msg_list)
        message=response.render('default/mail.html',context)
        mail.send(to=[str(form.vars.email_address)],
                  subject='You have successfully placed an order on Glassy',
                  message=message)

        #Making cart empty
        session.cart={}
        session.totalPrice=0

        redirect(URL('default','yourorders'))
    return dict(form=form)

@auth.requires_login()
def yourorders():
    order_list=db(db.orders.user_id==auth.user_id).select(db.orders.id,
                                                         db.orders.order_date,
                                                         db.orders.delivery_mode,
                                                         db.orders.payment_mode,
                                                         db.orders.delivery_status,
                                                         db.orders.total_price,
                                                         orderby=~db.orders.order_date).as_list()

    product_list={}
    for i in range(len(order_list)):
        cur_order_id = order_list[i]['id']
        tempList1=db(db.ordered_items.order_id==cur_order_id).select(db.ordered_items.product_id).as_list()
        tempList2=[]
        for j in range(len(tempList1)):
            cur_prod_id=tempList1[j]['product_id']
            tempRow=db(db.product.id==cur_prod_id).select(db.product.p_name).as_list()
            tempList2.append(tempRow[0]['p_name'])
        product_list[cur_order_id]=tempList2

    delivery_mode_list=db(db.delivery_type.id>0).select(db.delivery_type.id,db.delivery_type.name).as_list()
    payment_mode_list=db(db.payment_type.id>0).select(db.payment_type.id,db.payment_type.name).as_list()
    delivery_status_list=db(db.delivery_status_type.id>0).select(db.delivery_status_type.id,db.delivery_status_type.name).as_list()

    return locals()

@auth.requires_login()
def maintain_wishlist():
    key=str(request.args(0))
    if not session.wishlist:
        session.wishlist={}
        response.flash="Found Empty Wishlist"
    if key in session.wishlist:
        del session.wishlist[key]
    else:
        session.wishlist[key]=1
        response.flash=session.wishlist

@auth.requires_login()
def wishlist():

    user=db(db.wishlist.user_id == auth.user_id).select(db.wishlist.product_id).as_list()
    product_list=[]

    for pid in user:
        for row in db(db.product.id==pid['product_id']).select(db.product.id,
                                                               db.product.p_name,
                                                               db.product.p_image,
                                                               db.product.p_price):
            product_list.append(row)

    k=[]
    for i in user:
        k.append(i['product_id'])

    for i in session.wishlist:
        if int(i) not in k :
            db.wishlist.insert(user_id=auth.user_id,product_id=i)
            for row in db(db.product.id==i).select(db.product.id,db.product.p_name,db.product.p_image,db.product.p_price):
                    product_list.append(row)

    return locals()
