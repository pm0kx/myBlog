#encoding: utf-8

from flask_login import  current_user
from flask_wtf import FlaskForm
from app.common import logger
#from flask_wtf import RecaptchaField
from wtforms.validators import DataRequired, Length,EqualTo, URL, Length, Email
from wtforms import (
    widgets,
    StringField,
    TextField,
    TextAreaField,
    PasswordField,
    BooleanField,
    SubmitField,
    SelectField,
    HiddenField,
    DateField, 
    DateTimeField,
    ValidationError
)

from app.models import User,Role,Tag,Mail

logger = logger.Logger(logger="form").getlog()

class CommentForm(FlaskForm):
    """Form vaildator for comment."""

    # Set some field(InputBox) for enter the data.
    # patam validators: setup list of validators
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(max=255)])

    text = TextAreaField(u'Comment', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    """Register Form."""

    username = StringField('用户名', [DataRequired(), Length(max=36)])
    nickname = StringField('昵称', [DataRequired(), Length(max=36)])
    fullname = StringField('姓名', [DataRequired(), Length(max=36)])
    email = StringField('电子邮箱', validators=[DataRequired(), Length(1, 64),Email()])
    address = StringField('地址', [DataRequired()])

    birthday = StringField('出生年月',[DataRequired()])
    gender = SelectField('性别', [DataRequired()])
    #在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__( *args,**kwargs)
        self.gender.choices=[('2','请选择'),('1','男'),('0','女')]

    # def validate_email(self, field):
    #     if User.query.filter_by(email=field.data).first():
    #         raise ValidationError('Email already registered.')

    def validate(self):
        check_validate = super(RegisterForm, self).validate()
        logger.info("start check_validate !")
        # If validator no pass
        if not check_validate:
            logger.info("check_validate false")
            return False

        if Mail.query.filter_by(email=self.email.data).all():
            #raise ValidationError('Email already registered.')
            self.username.errors.append('Email already registered.')
            logger.info("Email already registered.")
            return False

        # Check the user whether already exist.
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('User with that name already exists.')
            logger.info("User with that name already exists.")
            return False
        logger.info("validate pass")
        return True

class ChangePasswordForm(FlaskForm):
    """update passwd Form."""
    # userid = HiddenField()
    old_passwd = PasswordField('原始密码', [DataRequired(), Length(min=8)])
    new_passwd = PasswordField('新密码', [DataRequired(), Length(min=8)])
    comfirm_new_passwd = PasswordField('确认新密码', [DataRequired(), EqualTo('new_passwd')])

    # def __init__(self, *args, **kwargs):
    #     super(RegisterForm, self).__init__( *args,**kwargs)
    #     self.userid=

    # def validate(self):
    #     check_validate = super(ChangePasswordForm, self).validate()

    #     # If validator no pass
    #     if not check_validate:
    #         return False

    #     # Check the user whether already exist.
    #     user = User.query.filter(id=self.userid,password=self.old_passwd.data).first()
    #     if user ==None:
    #         self.username.errors.append('User with that password input error.')
    #         return False
    #     return True


class LoginForm(FlaskForm):
    """Login Form"""

    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField("Remember Me")


    def validate(self):
        """Validator for check the account information."""
        check_validata = super(LoginForm, self).validate()

        # If validator no pass
        if not check_validata:
            return False

        # Check the user whether exist.
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username or password.')
            return False

        # Check the password whether right.
        if not user.verify_password(self.password.data):
            self.username.errors.append('Invalid username or password.')
            return False
        #if not (user.status ==1 and user.confirmed is True):
        #    self.username.errors.append('请先完成邮箱验证或者联系管理员')
        #    return False

        return True

class PostForm(FlaskForm):
    """Post Form."""

    title = StringField('Title', [DataRequired(), Length(max=255)])
    text = TextAreaField('Blog Content', [DataRequired()])
    tag = SelectField('tag', [DataRequired()])
    #在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__( *args,**kwargs)
        self.tag.choices = [(tag.id,tag.name) for tag in Tag.query.order_by(Tag.name).all()]
       #self.tag.choices=[('0','请选择'),('1','other'),('2','popular')]

class RoleSelectForm(FlaskForm):
    role = SelectField('Role', coerce=int)
    #在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(RoleSelectForm, self).__init__( *args,**kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        #choices需要一个列表里面包含数个键值对应的元组

    #也可以在初始化后使用
    # form.role.choices =  [(role.id, role.name) for role in Role.query.order_by(Role.name).all()] 来添加选项


# class TagSelectForm(FlaskForm):
#     tag = SelectField('tag', coerce=int)
#     #在构造化Form实例时指定selectField的choices内容,
#     def __init__(self, *args, **kwargs):
#         super(TagSelectForm, self).__init__( *args,**kwargs)
#         self.tag.choices = [tag.name for tag in Tag.query.order_by(Tag.name).all()]



class CKTextAreaWidget(widgets.TextArea):
    """CKeditor form for Flask-Admin."""

    def __call__(self, field, **kwargs):
        """Define callable type(class)."""

        # Add a new class property ckeditor: `<input class=ckedior ...>`
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    """Create a new Field type."""

    # Add a new widget `CKTextAreaField` inherit from TextAreaField.
    widget = CKTextAreaWidget()


class OpenIDForm(FlaskForm):
    """OpenID Form."""

    openid_url = StringField('OpenID URL', [DataRequired(), URL()])