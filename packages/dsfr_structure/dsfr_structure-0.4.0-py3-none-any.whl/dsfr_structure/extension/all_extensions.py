from markdown.extensions import Extension

from dsfr_structure.extension import (
    accordion,
    alert,
    badge,
    blockquote,
    col,
    row,
    table,
    tile,
    card
)


class AllExtensions(Extension):
    def extendMarkdown(self, md):
        blockquote_ext = blockquote.DsfrBlockQuoteExtension()
        blockquote_ext.extendMarkdown(md)

        table_ext = table.DsfrTableExtension()
        table_ext.extendMarkdown(md)

        accordion_ext = accordion.DsfrAccordionExtension()
        accordion_ext.extendMarkdown(md)

        alert_ext = alert.DsfrAlertExtension()
        alert_ext.extendMarkdown(md)

        badge_ext = badge.DsfrBadgeExtension()
        badge_ext.extendMarkdown(md)

        row_ext = row.DsfrRowExtension()
        row_ext.extendMarkdown(md)

        col_ext = col.DsfrColExtension()
        col_ext.extendMarkdown(md)

        tile_ext = tile.DsfrTileExtension()
        tile_ext.extendMarkdown(md)

        card_ext = card.DsfrCardExtension()
        card_ext.extendMarkdown(md)


def makeExtension(**kwargs):
    return AllExtensions(**kwargs)
