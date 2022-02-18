from django.db import models

from rareapi.models.post_reaction import PostReaction


class Post(models.Model):
    user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    publication_date = models.DateField(auto_now_add=True)
    image_url = models.ImageField(
        upload_to='postpics', height_field=None,
        width_field=None, max_length=None, null=True)
    content = models.TextField()
    approved = models.BooleanField(default=False)
    tags = models.ManyToManyField("Tag", through="PostTag", related_name="tags")
    
    # @property
    # def user_reactions(self):
        
    #     reactions = PostReaction.objects.filter(post=self, user=request.auth.user)