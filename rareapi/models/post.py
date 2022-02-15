from django.db import models


class Post(models.Model):
    user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    publication_date = models.DateField(auto_now_add=True)
    image_url = models.URLField()
    content = models.TextField()
    approved = models.BooleanField()
    tags = models.ManyToManyField("Tag", through="PostTag", related_name="tags")
