# Django HTMX

Django project for explaining how HTML works. It serves the following resources:

* `/`: HTML page including HTML code for loading the same image twice every three seconds. The first image is included embedded, by refreshing the content of a `div` element with a `IMG` element including the image, embedded, obtained by getting `/image_embedded`. The second image is included by reference, by refreshing the content of a `div` element with a `IMG` element including a reference to the image, obtained by getting `/image_html` (which will trigger getting `/image`)
* `/image`: Image, as `image/jpeg` (bytes)
* `/image_embedded`: HTML with a `IMG` element, with the image embedded
* `/image_html`: HTML with a `IMG`, with the image (`/image`) referenced

The image shown in all cases is downloaded from its original location every time `/image` or `/image_embedded` is invoked with `GET`.