"""Help text for model fields."""

from utils.markdown import MARKDOWN_HELP_TEXT


class Notice:
    """Help text for Notice model fields."""

    notice_class = """
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
            Image notices always have <em>static display</em>, with no
            title/description text. Use for displaying banners e.g. event posters.
        </li>
        <li>
            N.B. short/wide images work much better than square ones!
        </li>
    </ul>
    """

    static_display = """
    <ul style='margin-left: 2rem;'>
        <li style='list-style: disc;'>
            Display the notice as a static block beneath the GA logo, rather than
            the default rotating notice (i.e. the banner beneath the navbar).
        </li>
        <li style='list-style: disc;'>
            Ideally, this should be checked
            <b style='color: firebrick;'>only for a single, high-priority notice</b>
            to prevent cluttering of the landing page.
        </li>
        <li style='list-style: disc;'>
            Static notices show the <b>body</b> on the landing page instead
            of the <b>short description</b> and do not link to a webpage.
        </li>
        <li style='list-style: disc;'>
            Notices with <em>image</em> class always have static display,
            so this option will be ignored.
        </li>
    </ul>
    """

    short_description = """
    <ul style='margin-left: 2rem;'>
        <li style='list-style: disc;'>
            This will be displayed on the landing page (200 char max) as plain
            text or inline HTML (e.g.
            <code>&lt;a&gt;</code>,
            <code>&lt;b&gt;</code>
            tags).
        </li>
        <li style='list-style: disc;'>
            If not <em>static</em> display (default), this will be shown as a
            single line of text above the navbar,
            <b>which will be cut off if too long</b>,
            especially on small screens!
        </li>
        <li style='list-style: disc;'>
            If <em>static</em> display is enabled, this field is ignored in favour
            of the <em>title</em> and <em>body</em> fields.
        </li>
    </ul>
    """

    body = f"""
    <ul style='margin-left: 2rem;'>
        <li style='list-style: disc;'>
            {MARKDOWN_HELP_TEXT}
        </li>
        <li style='list-style: disc;'>
            Unless <em>static display</em> is enabled,
            <b>This text will be displayed on a dedicated webpage</b>
            that is linked to from the landing page notice.
            If this field is left blank, there will be no link.
        </li>
        <li style='list-style: disc;'>
            When using the <em>image</em> notice class, images will be rendered
            with full width and max-height of 250px. You can override this by using
            an <code>&lt;img&gt;</code> tag and setting the <code>style</code>
            attribute.
        </li>
    </ul>
    """

    material_icon = """
    Optional. A valid Material Design icon ID to be displayed with the title
    (e.g. <em>check_box</em>).
    <a href="https://fonts.google.com/icons" target="_blank">
    Browse 2500+ icons here
    </a>.
    """
