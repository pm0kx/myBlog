# -*- coding: UTF-8 -*-

from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
#from app.common.extensions import mail
from app.common import logger

logger = logger.Logger(logger="mails").getlog()

#发送邮箱的子线程类
class SendMailThread(Thread):
    def __init__(self,app,msg):
        super(SendMailThread,self).__init__()
        self.__app=app
        self.__msg=msg

    #异步发送邮件
    def send_async_mail(self,app,msg):
        with app.app_context():
            from app.common.extensions import mail
            logger.info("start send mail")
            mail.send(msg)

    # 发送邮件
    def run(self):
        self.send_async_mail(self.__app,self.__msg)

#封装邮件发送过程
def send_mail(subject,to,template=None,**kwargs):
    #获取当前app对象
    app=current_app._get_current_object()
    msg=Message(app.config['MAIL_SUBJECT_PREFIX'] + ' ' +subject,
                sender=app.config['MAIL_SENDER'],recipients=[to])
    #附件处理
    #if attachments:
    #    pass
    #处理大量邮件发送
    #if is_bulk:
    #    pass
    if template ==None:
        msg.html ='<p> test </p>'
        msg.body='测试邮件'
    else:
        msg.html=render_template(template + '.html',**kwargs)
        msg.body=render_template(template + '.txt',**kwargs)

    #子线程发送
    thr=SendMailThread(app,msg)
    thr.start()
    return thr


#异步发送邮件
# @email.route('/asyc_send/',methods=['POST','GET'])
# def sendAsycMail():
#     subject=u'异步发送邮件测试'
#     rec=['***@qq.com']
#     tp='email/send.html'
#     test='test'
#     #异步发送邮件
#     sendMail.send_mail(subject=subject,recv=rec,template=tp,test=test)
#     return 'Asyc Send!!!'
