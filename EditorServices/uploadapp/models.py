from django.db import models
import random
import os

class BgFileToolModel(models.Model):

    class Meta:
        db_table = 'tbl_file_data'
        verbose_name = "BG File"
        verbose_name_plural = "BG File"
        ordering = ("-created_at",)

    name = models.CharField(max_length=256)
    file = models.FileField(blank=False,upload_to='layers', null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0}".format(self.file)

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

    def file_type(self):

        name, extension = os.path.splitext(self.file.name)
        if extension:
            return "image"

    def get_alternate_name(self):
        allowed_chars = ''.join((string.ascii_letters, string.digits))
        unique_id = ''.join(random.choice(allowed_chars) for _ in range(5))
        return unique_id
