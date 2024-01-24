"""Help text for model fields."""

from utils.markdown import MARKDOWN_HELP_TEXT


class Notice:
    """Help text for Notice model fields."""

    NOTICE_CLASS = """
    <ul style='margin-left: 2rem;'>
        <li style='list-style: disc;'>
            A style class to set a color scheme for the notice - uses
            <a
                href='https://getbootstrap.com/docs/5.0/components/alerts/'
                target='_blank'
            >standard bootstrap styling</a>
            (
                <em>info</em>: blue,
                <em>warning</em>: orange,
            ).
        </li>
        <li style='list-style: disc;'>
            Use the <em>Cover Image</em> model for displaying banner images.
            <span class="text-danger">
              The <em>image</em> class is deprecated
            </span>
            - existing image notices should be migrated to
            <em>Cover Image</em> records.
        </li>
    </ul>
    """

    STATIC_DISPLAY = """
    <ul style='margin-left: 2rem;'>
        <li style='list-style: disc;'>
            Display the notice as a static block beneath the GA logo, in addition
            to the default rotating notice (i.e. the banner beneath the navbar).
        </li>
        <li style='list-style: disc;'>
            Ideally, this should be checked
            <b style='color: firebrick;'>only for a single, high-priority notice</b>
            to prevent cluttering of the landing page.
        </li>
        <li style='list-style: disc;'>
            Static notices show the <b>body</b> on the landing page in addition
            to the <b>short description</b>. If the block notice is dismissed
            by the user, they can still access and click through the rotating
            notice.
        </li>
    </ul>
    """

    SHORT_DESCRIPTION = """
    <ul style='margin-left: 2rem;'>
        <li style='list-style: disc;'>
            This will be displayed on the landing page (200 char max) as plain
            text or inline HTML (e.g.
            <code>&lt;em&gt;</code>,
            <code>&lt;b&gt;</code>
            tags).
        </li>
        <li style='list-style: disc;'>
            No <code>&lt;a&gt;</code> tags please, as this creates a confusing
            user experience (link within link).
        </li>
        <li style='list-style: disc;'>
            This will be shown as a single line of text above the navbar,
            <b>which will be cut off if too long</b>,
            especially on small screens! Please check the length is reasonable
            before publishing.
        </li>
    </ul>
    """

    BODY = f"""
    <ul style='margin-left: 2rem;'>
        <li style='list-style: disc;'>
            {MARKDOWN_HELP_TEXT}
        </li>
        <li style='list-style: disc;'>
            <b>This text will be displayed on a dedicated webpage</b>
            that is linked to from the landing page notice.
            If this field is left blank, there will be no link.
            For notices with <b>static display</b>, this will be displayed on
            the landing page in a block element, in addition to the dedicated
            webpage.
        </li>
    </ul>
    """

    MATERIAL_ICON = """
    Optional. A valid Material Design icon ID to be displayed with the title
    (e.g. <em>check_box</em>).
    <a href="https://fonts.google.com/icons" target="_blank">
    Browse 2500+ icons here
    </a>.
    """


class CoverImage:

    DISPLAY_HEIGHT = """
    For most images this should be left at the default (300px).
    For more square images this can be increased, but try not to let the image
    taking over the whole landing page. If you want an image to span the full
    width, try increasing this value.
    """

    IMG = """
    An ideal resolution for banner-style images is 1000x300px. It is
    recommended to publish the image only after viewing the landing page to
    confirm that the display is acceptable.
    """
