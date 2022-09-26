import os

from PIL import ImageOps
from django import forms
from stdimage import StdImageField
from stdimage.models import StdImageFieldFile



class WEBPFieldFile(StdImageFieldFile):

    @classmethod
    def get_variation_name(cls, file_name, variation_name):
        path = super().get_variation_name(file_name, variation_name)
        path, ext = os.path.splitext(path)
        return '%s.webp' % path

    @classmethod
    def process_variation(cls, variation, image):
        """Process variation before actual saving."""
        save_kwargs = {}
        file_format = 'WEBP'
        save_kwargs['format'] = file_format

        resample = variation['resample']

        if variation['width'] is None:
            variation['width'] = image.size[0]

        if variation['height'] is None:
            variation['height'] = image.size[1]

        factor = 1
        while image.size[0] / factor \
                > 2 * variation['width'] \
                and image.size[1] * 2 / factor \
                > 2 * variation['height']:
            factor *= 2
        if factor > 1:
            image.thumbnail(
                (int(image.size[0] / factor),
                 int(image.size[1] / factor)),
                resample=resample
            )

        size = variation['width'], variation['height']
        size = tuple(int(i) if i is not None else i
                     for i in size)

        image = image.convert('RGB')
        save_kwargs['optimize'] = True
        save_kwargs['quality'] = 70
        if size[0] * size[1] > 10000:  # roughly <10kb
            save_kwargs['progressive'] = True

        if variation['crop']:
            image = ImageOps.fit(
                image,
                size,
                method=resample
            )
        else:
            image.thumbnail(
                size,
                resample=resample
            )

        save_kwargs.update(variation['kwargs'])

        return image, save_kwargs


class WEBPField(StdImageField):
    attr_class = WEBPFieldFile