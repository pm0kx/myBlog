#encoding: utf-8

from flask import render_template,redirect,url_for,flash,request
from flask_login import login_user, logout_user
from flask_login import login_required, current_user
from app.common.mails import send_mail
from app.common import logger
# from flask_principal import Identity, AnonymousIdentity
# from flask_principal import identity_changed, current_app

# from app import db,openid
from app.common.extensions import openid
from app.common.db import db

from . import main
from app.models import User,Mail
from app.common.forms import LoginForm,RegisterForm,OpenIDForm,ChangePasswordForm

logger = logger.Logger(logger="home_view").getlog()

@main.route('/')
def index(page=1):
    """View function for main page"""

    return render_template("index.html")


@main.route('/login', methods=['GET', 'POST'])
@openid.loginhandler
def login():
    """View function for login."""

    # Will be check the account whether rigjt.
    form = LoginForm()

    # Create the object for OpenIDForm
    openid_form = OpenIDForm()

    # Send the request for login to relay party(URL).
    if openid_form.validate_on_submit():
        return openid.trg_login(
            openid_form.openid_url.data,
            ask_for=['nickname', 'email'],
            ask_for_optional=['fullname'])

    # Try to login the relay party failed.
    openid_errors = openid.fetch_error()
    if openid_errors:
        flash(openid_errors, category="danger")

    # Will be check the account whether rigjt.
    if form.validate_on_submit():
        # Using session to check the user's login status
        # Add the user's name to cookie.
        # session['username'] = form.username.data
        user = User.query.filter_by(username=form.username.data).one()

        # Using the Flask-Login to processing and check the login status for user
        # Remember the user's login status.
        login_user(user, remember=form.remember.data)

        # identity_changed.send(
        #     current_app._get_current_object(),
        #     identity=Identity(user.id))
        flash("You have been logged in.", category="success")
        return redirect(url_for('post.list'))

    return render_template('main/login.html',
                           form=form,
                           openid_form=openid_form
                           )



@main.route('/logout', methods=['GET', 'POST'])
def logout():
    """View function for logout."""

    # Using the Flask-Login to processing and check the logout status for user.
    logout_user()

    # identity_changed.send(
    #     current_app._get_current_object(),
    #     identity=AnonymousIdentity())
    flash("You have been logged out.", category="success")
    return redirect(url_for('main.index'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    """View function for Register."""

    # Will be check the username whether exist.
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User()
        # new_user = User(username=form.username.data,
        #                 password=form.password.data)
        new_user.username=form.username.data
        new_user.password='abcd1234' #default password
        new_user.nick_name=form.nickname.data
        new_user.full_name=form.fullname.data
        new_user.address=form.address.data
        new_user.birthday=form.birthday.data
        new_user.gender=form.gender.data
        new_user.status=1  #0：禁用，2：启用
        new_user.confirmed=False    #未确认

        mail =Mail(form.email.data)
        mail.user_id=new_user.id
        mail.status=1

        if new_user.address !=None:
            logger.info(new_user.address)
        db.session.add(new_user)
        db.session.add(mail)
        db.session.commit()

        logger.info("send  a confirmation email .")

        token = new_user.generate_confirmation_token()
        send_mail('Confirm Your Account', form.email.data,
                  'main/email/confirm', user=new_user, token=token)
        # send_email(form.email.data, 'Confirm Your Account',
        #            'main/email/confirm', user=new_user, token=token)
        flash('A confirmation email has been sent to you by email.',category="success")
        # flash('Your user has been created, please login.',category="success")

        return redirect(url_for('main.login'))
    return render_template('main/register.html',form=form)

@main.route('/confirm/<string:token>')
@login_required
def confirm(token):
    if current_user.confirmed :
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

@main.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    email=Mail.query.join(User).filter(User.id == current_user.id).first()

    send_mail('Confirm Your Account',email.email,
        'main/email/confirm',user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@main.route('/change-password',methods=['GET', 'POST'])
@login_required
def change_password():
    """View function for update_password"""

    form = ChangePasswordForm()

    if form.validate_on_submit():
        if current_user.check_password(form.old_passwd.data):
            # 修改密码
            current_user.password=form.new_passwd.data

            db.session.add(current_user)
            
            db.session.commit()

            flash('Your user password  has been changed, please relogin.',category="success")
            return redirect(url_for('main.logout'))
        else:
            flash('Invalid password.',category="faild")

    return render_template('main/change_password.html',form=form)


@main.route('/reset-password/<string:user_id>',methods=['GET','POST'])
# @login_required
def reset_password(user_id):
    """View function for reset_password"""

    user = User.query.filter_by(id=user_id).first()
    
    user.password = 'abcd1234'

    db.session.add(user)
    db.session.commit()

    flash("password have been reset.", category="success")
    return redirect(url_for('main.index'))



@main.route('/edit-userinfo',methods=['GET', 'POST'])
@login_required
def edit_userinfo():
    """View function for update_userinfo"""
    return 'hello'


@main.route('/userinfo',methods=['GET'])
@login_required
def get_userinfo():
    """View function for get userinfo"""

    # user = User.query.get_or_404(user_id)

    return render_template('main/user_detial.html',
                           user=current_user)



@main.route('/about',methods=['GET'])
#@login_required
def about():
    """View function for about page"""
    return render_template('main/about.html')


@main.route('/test-mail',methods=['GET'])
def send_email():
    """View function for about page"""

    logger.info("send  a test email .")
    user1 = User()
    user1.username='test'
    send_mail('TEST MAIL', 'zhu14623@163.com','main/email/confirm', user=user1, token='token')
    #send_mail('TEST MAIL', 'zhu14623@163.com')

    return redirect(url_for('main.index'))

# @home.route('/about',methods=['GET'])
# def get_meun():
#     pass

@main.before_app_request
def confirmed_check():
    """
    同时满足以下3 个条件时，before_app_request 处理程序会拦截请求。
    (1) 用户已登录（current_user.is_authenticated() 必须返回True）。
    (2) 用户的账户还未确认。
    (3) 请求的端点（使用request.endpoint 获取）为指定的端点
    """
    confirm_check=['post.add_post','main.edit_userinfo','post.edit_post']
    if current_user.is_authenticated:
        #current_user.ping()
        logger.info(request.endpoint)
        if not current_user.confirmed \
                and request.endpoint in confirm_check:
            return redirect(url_for('main.unconfirmed'))


@main.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('main/unconfirmed.html')

