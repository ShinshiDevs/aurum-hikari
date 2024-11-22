project = "Aurum"

author = "Shinshi Developers Team"
copyright = "%Y Shinshi Developers Team"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_inline_tabs",
    "notfound.extension",  # sphinx-notfound-page
    "autoapi.extension",
    "hoverxref.extension",
    "sphinxext.opengraph",
    "sphinx_last_updated_by_git",
]

napoleon_google_docstring = False

ogp_site_url = "https://shinshidevs.github.io/aurum-hikari"

autoapi_dirs = ["../aurum"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "hikari": ("https://docs.hikari-py.dev/en/stable", None),
}

autosummary_generate = True
display_toc = True

html_theme = "furo"
html_static_path = ["_static"]
html_theme_options = {
    "source_repository": "https://github.com/ShinshiDevs/aurum-hikari/",
    "source_branch": "main",
    "source_directory": "docs/",
    "sidebar_hide_name": True,
    "navigation_with_keys": True,
    "dark_logo": "logo-light.svg",
    "light_logo": "logo-dark.svg",
    "light_css_variables": {
        "color-brand-primary": "#54B8F0",
        "color-brand-content": "#54B8F0",
        "font-stack": "Inter, sans-serif",
        "font-stack--monospace": "Fira Code, monospace",
        "font-stack--headings": "Archivo, serif",
        "color-problematic": "#17181A",
        "color-foreground-primary": "#2B2D30", # for main text and headings
        "color-foreground-secondary": "#505359", # for secondary text
        "color-foreground-muted": "#6b6f76", # for muted text
        "color-background-primary": "#FBFDFF", # for content
        "color-background-secondary": "#FBFDFF", # for navigation + ToC
        "color-background-border": "#C8CDD2", # for UI borders
        "color-background-item": "#C8CDD2", # for "background" items (eg: copybutton)
    },
    "dark_css_variables": {
        "color-brand-primary": "#54B8F0",
        "color-brand-content": "#54B8F0",
        "font-stack": "Inter, sans-serif",
        "font-stack--monospace": "Fira Code, monospace",
        "font-stack--headings": "Archivo, serif",
        "color-problematic": "#FBFDFF",
        "color-foreground-primary": "#FBFDFF", # for main text and headings
        "color-foreground-secondary": "#FBFDFF", # for secondary text
        "color-foreground-muted": "#6b6f76", # for muted text,
        "color-background-primary": "#17181A", # for content
        "color-background-secondary": "#17181A", # for navigation + ToC
        "color-background-border": "#2B2D30", # for UI borders
        "color-background-item": "#505359", # for "background" items (eg: copybutton)
    },
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/ShinshiDevs/aurum-hikari",
            "html": "",
            "class": "fa-brands fa-solid fa-github fa-1.5x",
        },
        {
            "name": "Discord",
            "url": "https://dsc.gg/shinshi",
            "html": "",
            "class": "fa-brands fa-solid fa-discord fa-1.5x",
        },
    ],
}
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/fontawesome.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/solid.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/brands.min.css",
]
