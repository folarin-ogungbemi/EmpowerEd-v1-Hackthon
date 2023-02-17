from django.db import models
from django.utils import timezone


class User(models.Model):
    ROLES = (
        ('Mentor', 'Mentor'),
        ('Student', 'Student'),
        ('Parent', 'Parent'),
    )

    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLES)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            if self.role == 'Student':
                Student.objects.create(user_id=self)
            elif self.role == 'Parent':
                Parent.objects.create(user_id=self)
            elif self.role == 'Mentor':
                Mentor.objects.create(user_id=self)


class Mentor(models.Model):
    mentor_id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    area_of_expertise = models.CharField(max_length=255)
    userpic = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user_id.name} ({self.area_of_expertise} mentor)'


class Parent(models.Model):
    parent_id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    userpic = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user_id.name}'


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(default=timezone.now)
    interests = models.TextField()
    parent = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True)
    userpic = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user_id.name}'


class Relationship(models.Model):
    relationship_id = models.AutoField(primary_key=True)
    mentor_id = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.mentor_id.user_id.name}|{self.student_id.user_id.name}'


class Lesson(models.Model):
    lesson_id = models.AutoField(primary_key=True)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
