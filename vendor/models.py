from django.db import models
from account.models import User, UserProfile
from account.utils import send_notification

class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='user_profile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=100)
    vendor_licence = models.ImageField(upload_to='vendor/licence')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vendor_name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            #update
            orgi = Vendor.objects.get(pk=self.pk)
            if orgi.is_approved != self.is_approved:
                mail_template = 'account/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved
                }
                if self.is_approved == True:
                    #send notification email
                    mail_subject = 'Congratulations! you restaurant has been approved'
                    send_notification(mail_subject, mail_template, context)
                else:
                    #send notification email
                    mail_subject = "We're sorry! you are not eligible to publish your menu on our marketplace"
                    send_notification(mail_subject, mail_template, context)


        return super(Vendor, self).save(*args, **kwargs)
