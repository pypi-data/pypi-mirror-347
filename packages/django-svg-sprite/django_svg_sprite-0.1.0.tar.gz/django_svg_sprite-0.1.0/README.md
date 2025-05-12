# django-svg-sprite

A Django template tag for easy use of SVG sprites in templates.

## Quick start

1. Add `django_svg_sprite` to your `INSTALLED_APPS` setting like this:

        INSTALLED_APPS = [
            ...,
            'django_svg_sprite',
        ]

2. Set the `SVG_SPRITE` setting to the SVG sprite file to be used, e.g.:

        SVG_SPRITE = 'bootstrap-icons.svg'

    The full path will be looked up using Django's `staticfiles` app, if configured.

3. Use the tag in your template, e.g.:

        {% load svg_sprite %}

        ...

        {% svg_sprite 'hand-thumbs-up' fill='red' class='bi' %}

The `{% svg_sprite %}` tag can be used with one or more arguments. The first argument is the `id` of the SVG sprite. If a `title` argument is given, a title element will be added to the SVG element. All other arguments are added as attributes to the SVG tag.

## License

This project is licensed under the MIT license.
