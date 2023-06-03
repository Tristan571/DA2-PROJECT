from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.utils import timezone
import datetime
from decimal import Decimal
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import uuid

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Urole = (
        ('1', 'Admin'),
        ('2', 'Librarian'),
        ('3', 'Reader'),
        ('4', 'Manager'),
        ('5', 'Clerk')
    )
    role = models.CharField(max_length=20, choices=Urole, default='3')
    phone = models.CharField(max_length=10, blank=True, null=True, unique=True , validators=[RegexValidator(r'^0\d{9}$', 'Phone number must start with 0 and be 10 digits long')])
    idCard = models.CharField(max_length=12, blank=True, null=True, unique=True, validators=[RegexValidator(r'^\d{12}$', 'ID card number must be 12 digits long')])
    Pgender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=20, choices=Pgender, blank=True)
    readerCard = models.CharField(max_length=10, unique=True, default='1111111111', editable=False)

    def __str__(self):
        return  self.readerCard + ' - ' + self.user.first_name  + ' ' + self.user.last_name + ' - ' + self.user.username

    #Generate the unique reader card each time
    def save(self, *args, **kwargs):
        if not self.readerCard or self._state.adding:
            year = datetime.datetime.now().strftime("%Y")[2:]
            unique_id = str(uuid.uuid4().int & (1 << 32) - 1)[:8]
            self.readerCard = f"{year}{unique_id}"
        super().save(*args, **kwargs)

class Topic(models.Model):
    topicID = models.CharField(primary_key=True, max_length=20, help_text="Topic ID: TP + (A number). EX: TP01")
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.topicID + ': ' + self.name
    
    def save(self, *args, **kwargs):
        if not self.topicID:
            last_id = Topic.objects.order_by('-topicID').first()
            if last_id:
                self.topicID = 'TP' + format(int(last_id.topicID[2:]) + 1, "02d")
            else:
                self.topicID = 'TP01'
        super(Topic, self).save(*args, **kwargs)

class Language(models.Model):
    languageID = models.CharField(primary_key=True, max_length=2)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['languageID']

    def __str__(self):
        return self.languageID + ': ' + self.name


class Author(models.Model):
    authorID = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=100, unique = True)
    
    class Meta:
        ordering = ['authorID']

    # def clean(self):
    #     super().clean()
    #     if Author.objects.exclude(pk=self.pk).filter(name=self.name).exists():
    #         raise ValidationError('Author with this name already exists.')

    def __str__(self):
        return self.authorID + ': ' + self.name

    def save(self, *args, **kwargs):
        if not self.authorID:
            last_id = Author.objects.order_by('-authorID').first()
            if last_id:
                self.authorID = 'A' + format(int(last_id.authorID[1:]) + 1, "03d")
            else:
                self.authorID = 'A001'
        super(Author, self).save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     if not self.authorID:
    #         last_id = Author.objects.order_by('-authorID').first()
    #         if last_id:
    #             last_id_int = int(last_id.authorID[1:])
    #             new_id_int = last_id_int + 1
    #         else:
    #             new_id_int = 'A001'
    #         self.authorID = f'A{new_id_int:03d}'
    #     super(Author, self).save(*args, **kwargs)

class Publisher(models.Model):
    publisherID = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['publisherID']

    def __str__(self):
        return self.publisherID + ': ' + self.name

    def save(self, *args, **kwargs):
        if not self.publisherID:
            last_id = Publisher.objects.order_by('-publisherID').first()
            if last_id:
                self.publisherID = 'P' + format(int(last_id.publisherID[1:]) + 1, "03d")
            else:
                self.publisherID = 'P001'
        super(Publisher, self).save(*args, **kwargs)

class Position(models.Model):
    positionID = models.AutoField(primary_key=True)
    Pfloor = (
        ('1', 'F1'),
        ('2', 'F2'),
        ('3', 'F3'),
        ('4', 'F4'),
    )
    
    floor = models.CharField(max_length=20, choices=Pfloor)

    Pshelf = (
        ('1', 'Shelf 1'),
        ('2', 'Shelf 2'),
        ('3', 'Shelf 3'),
        ('4', 'Shelf 4'),
        ('5', 'Shelf 5'),
        ('6', 'Shelf 6'),
        ('7', 'Shelf 7'),
        ('8', 'Shelf 8'),
        ('9', 'Shelf 9'),
        ('10', 'Shelf 10'),
    )
    # shelve = MultiSelectField(choices=pshelve)
    shelf = models.CharField(max_length=20, choices=Pshelf, blank=True)

    Prow = (
        ('1', 'Row 1'),
        ('2', 'Row 2'),
        ('3', 'Row 3'),
        ('4', 'Row 4'),
        ('5', 'Row 5'),
    )
    # row = MultiSelectField(choices=Prow)
    row = models.CharField(max_length=20, choices=Prow)

    Pbay = (
        ('A', 'Bay A'),
        ('B', 'Bay B'),
    )
    # bay = MultiSelectField(choices=Pbay)
    bay = models.CharField(max_length=20, choices=Pbay)

    maxCarry = models.IntegerField(default=80)

    class Meta:
        ordering = ['floor', 'shelf', 'row', 'bay']
    def __str__(self):
        return "F: " + str(self.floor) + " - S: " + str(self.shelf) + " - R: " + str(self.row) + " - B: " + str(self.bay)

def get_upload_path(instance, filename):
    # Construct the desired filename using the bookID
    # For example, if the bookID is "ABC123" and the uploaded file is "image.jpg", the filename will be "ABC123.jpg"
    ext = filename.split('.')[-1]
    filename = f"{instance.bookID}.{ext}"
    return f"static/images/{filename}"

class Book(models.Model):
    bookID = models.CharField(primary_key=True, max_length=25)
    name = models.CharField(max_length=100, blank=True)
    image = models.ImageField(blank=True, upload_to=get_upload_path, default='static\errorimg\errorimg.png')
    year = models.IntegerField(default=timezone.now().year, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    # rentPrice = models.(default=0, blank=True)
    stock = models.IntegerField(default=0, blank=True)
    pages = models.IntegerField(default=0, blank=True)
    condition = models.IntegerField(default=100, blank=True)
    topicID = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True, null=True)
    authorID = models.ManyToManyField(Author)
    languageID = models.ManyToManyField(Language)
    publisherID = models.ManyToManyField(Publisher)
    positionID = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(default=timezone.now())
    quantity = models.IntegerField(default=0, blank=True)

    class Meta:
        ordering = ['-created'] #order by updated and created, -updated and -created to order new up & cre first

    def clean(self):
        if self.price < 0:
            raise ValidationError('Price must be higher than 0')
        if self.pages < 0:
            raise ValidationError('Pages must be higher than 0')
        if self.condition <= 0 or self.condition > 100:
            raise ValidationError('Condition must be between 0 and 100')
    def __str__(self):
        return  self.bookID + " - " + str(self.positionID )+ ' - '+ self.name

class BookRental(models.Model):
    rentalID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bookID = models.ForeignKey(Book, on_delete=models.CASCADE)
    rentCondition = models.IntegerField(blank=True)
    rentDate = models.DateTimeField(default=timezone.now())
    returnCondition = models.IntegerField(default = rentCondition, blank=True, null=True)
    returnDate = models.DateTimeField(blank=True, null=True)
    extraFee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    totalFee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        ordering = ['-rentDate']
    
    def clean(self):
        if self.returnDate < self.rentDate:
            raise ValidationError('Return date must be equal to or later than rental date.')

    def save(self, *args, **kwargs):
        if not self.pk: # if the instance is a new record
            # Set the rent condition to the book's condition by default
            self.rentCondition = self.bookID.condition
            self.bookID.quantity = 0

        if self.pk and self.returnCondition == None:
                self.returnCondition = self.rentCondition
        if self.pk and self.returnDate != None:
            if self.returnDate >= self.rentDate:
                rental_period = self.returnDate - self.rentDate
                # calculate the total fee as rental_period multiplied with 1.5
                totalrentdays = rental_period.days

                if totalrentdays > 14:
                    overduedays = totalrentdays - 14 
                    self.extraFee = overduedays * 2
                    self.totalFee = (totalrentdays - 14 + 1) * 1.5
            else:
                self.totalFee = 0

            if self.returnCondition < self.rentCondition:
                if self.rentCondition - self.returnCondition > 0 and self.rentCondition - self.returnCondition < 10:
                    self.extraFee = self.bookID.price * Decimal(0.15)
                elif self.rentCondition - self.returnCondition <= 50 and self.rentCondition - self.returnCondition >= 10:
                    self.extraFee = self.bookID.price * Decimal(0.6)
                elif self.rentCondition - self.returnCondition > 50:
                    self.extraFee = self.bookID.price + 5 #Charge fee
       
        super(BookRental, self).save(*args, **kwargs)
        if self.returnDate != None: # If the book is returned
            # Update the condition of the associated book
            self.bookID.condition = self.returnCondition
            self.bookID.stock = self.bookID.stock + 1
            
            self.bookID.save()
        elif self.returnDate == None: # If the book is not returned
            self.bookID.stock = self.bookID.stock - 1
            self.bookID.save()

    def __str__(self):
        return str(self.rentalID) + " - " + str(self.user.profile.readerCard) + " - " + str(self.bookID.name)


