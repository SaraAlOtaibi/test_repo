from django.db import models
import datetime
import bcrypt

class UserManager(models.Manager):
    def validateRegister(self, post_data):
        errors = []
        if len(post_data['first_name']) < 1:
            errors.append('Please fill the first name field ')
        elif len(post_data['first_name']) < 2:
            errors.append('First name field can\'t be less than two characters')
        if len(post_data['last_name']) < 1:
            errors.append('Please fill the last name field ')
        elif len(post_data['last_name']) < 3:
            errors.append('Last name field can\'t be less than three characters')
        if  len(post_data['email']) < 1:
            errors.append('Please enter the email ')
        elif not self.validateEmail(post_data['email']):
            errors.append('Email is not in correct format')
        if User.objects.filter(email=post_data['email']).exists():
            errors.append('The email already exists' )
        if len(post_data['pw']) < 1 :
            errors.append('Please Enter the password field' )
        elif len(post_data['pw']) < 8 :
            errors.append('Password must be of lenght 8 or more' )
        if len(post_data['pw2']) < 1 :
            errors.append('Please Confirm the password' )
        if  post_data['pw'] != post_data['pw2'] :
            errors.append('Passwrod does not match')


        return errors

    def validateLogin(self, post_data):
        errors = []
        user = User.objects.filter(email=post_data['email'])
        print('******************************')
        print(user)
        if len(post_data['email']) < 1:
            errors.append('Please enter the email ')
        else:
            if not self.validateEmail(post_data['email']):
                errors.append('Email is not in correct format')
            else: 
                if not user.exists():
                    errors.append('The email is not registerd' )
                else: 
                    if len(post_data['pw']) < 1 :
                        errors.append('Please Enter the password field' )
                    elif not bcrypt.checkpw(post_data['pw'].encode(), user[0].password.encode()):
                        errors.append('Incorrect Password')


        return errors

    def validateEmail(self, email):
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

class WishManager(models.Manager):
    def validateWish(self, post_data):
        errors = []
        if len(post_data['name']) < 1:
            errors.append('Please fill the wish field ')
        elif len(post_data['name']) < 3:
            errors.append('Wish field can\'t be less than 3 characters')
        if len(post_data['desc']) < 1:
            errors.append('Please fill the description field ')
        elif len(post_data['desc']) < 3:
            errors.append('Description field can\'t be less than 3 characters')
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return f"<User object: ID : {self.id} first_name : {self.first_name}, last_name : {self.last_name}, email {self.email}>\n"


class Wish(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField()
    status = models.CharField(max_length=45, default='pending')
    granted_date = models.DateTimeField()
    wisher = models.ForeignKey(User, related_name="wishes", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = WishManager()

    #def __str__(self):
    #    return f"<Wish object: Name : {self.name} Description : {self.desc} ID : {self.id}>\n"