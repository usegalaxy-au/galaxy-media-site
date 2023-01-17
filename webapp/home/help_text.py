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
                <em>danger</em>: red
            ).
        </li>
        <li style='list-style: disc;'>
            Use the <em>image</em> class for displaying an image. For this,
            the body should consist of an HTML <code>&lt;img&gt;</code> tag
            only (or markdown equivalent).
        </li>
        <li style='list-style: disc;'>
            Image notices always have <b>static display</b>, with no
            title/description text. Use for displaying banners e.g. event posters.
        </li>
        <li style='list-style: disc;'>
            Short/wide images work much better than square ones!
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
        <li style='list-style: disc;'>
            Notices with <em>image</em> class always have static display,
            so this option will be ignored.
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
        <li style='list-style: disc;'>
            When using the <em>image</em> notice class, images will be rendered
            with full width and max-height of 250px. You can override this by
            using an <code>&lt;img&gt;</code> tag and setting the
            <code>style</code> attribute.
        </li>
        <li style='list-style: disc;'>
            When using the <em>image</em> notice class, you can upload an image
            and link to it using the
            <a href="/admin/home/mediaimage/">Media images</a> model.
            Otherwise you might just link to images hosted elsewhere e.g.
            github.
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
