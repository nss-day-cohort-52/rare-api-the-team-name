from django.db import models


class Post(models.Model):
    user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255)
    publication_date = models.DateField(auto_now_add=True)
    image_url = models.ImageField(
        upload_to='postpics', height_field=None,
        width_field=None, max_length=1000, null=True)
    content = models.TextField(max_length=1000)
    approved = models.BooleanField(default=False)
    tags = models.ManyToManyField("Tag", through="PostTag", related_name="tags")