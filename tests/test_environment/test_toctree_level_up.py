"""Test toctree ``:level-up:`` promotion (#8287)."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from docutils import nodes

from sphinx import addnodes
from sphinx._cli.util.errors import strip_escape_sequences
from sphinx.environment.adapters.toctree import global_toctree_for_doc
from sphinx.testing.util import assert_node

if TYPE_CHECKING:
    from sphinx.testing.util import SphinxTestApp


def _toc_children(item: nodes.list_item) -> list[tuple[str, object]]:
    """Return ``('section', title)`` / ``('toctree', includefiles)`` pairs."""
    if len(item) < 2 or not isinstance(item[1], nodes.bullet_list):
        return []
    result: list[tuple[str, object]] = []
    for child in item[1]:
        if isinstance(child, addnodes.toctree):
            result.append(('toctree', list(child['includefiles'])))
        elif isinstance(child, nodes.list_item):
            result.append(('section', child[0].astext()))
    return result


@pytest.mark.sphinx('xml', testroot='toctree-level-up')
@pytest.mark.test_params(shared_result='test_toctree_level_up')
def test_level_up_env_tocs(app: SphinxTestApp) -> None:
    app.build()

    title_item = app.env.tocs['index'][0]
    assert isinstance(title_item, nodes.list_item)
    children = _toc_children(title_item)
    assert children == [
        ('toctree', ['defaults', 'over']),
        ('section', 'Intro header'),
        ('toctree', ['page1']),
        ('section', 'Later sibling'),
        ('section', 'Level two'),
        ('toctree', ['page2']),
        ('section', 'Hidden section'),
        ('toctree', ['hidden']),
        ('section', 'Numbered section'),
        ('toctree', ['numbered']),
    ]

    assert isinstance(title_item[1], nodes.bullet_list)
    level_two = title_item[1][4]
    assert isinstance(level_two, nodes.list_item)
    assert _toc_children(level_two) == [('section', 'Nested')]


@pytest.mark.sphinx('xml', testroot='toctree-level-up')
@pytest.mark.test_params(shared_result='test_toctree_level_up')
def test_toc_level_up_directive_and_override(app: SphinxTestApp) -> None:
    app.build()

    title_item = app.env.tocs['defaults'][0]
    assert isinstance(title_item, nodes.list_item)
    children = _toc_children(title_item)
    assert children == [
        ('section', 'Section A'),
        ('toctree', ['default']),
        ('section', 'Section B'),
    ]

    assert isinstance(title_item[1], nodes.bullet_list)
    section_b = title_item[1][2]
    assert isinstance(section_b, nodes.list_item)
    assert isinstance(section_b[1], nodes.bullet_list)
    subsection = section_b[1][0]
    assert isinstance(subsection, nodes.list_item)
    assert _toc_children(subsection) == [('toctree', ['override'])]


@pytest.mark.sphinx('xml', testroot='toctree-level-up')
@pytest.mark.test_params(shared_result='test_toctree_level_up')
def test_level_up_over_promotion_warns(app: SphinxTestApp) -> None:
    app.build()

    # Promoted to a sibling of the document title, then stopped with a warning.
    toc = app.env.tocs['over']
    assert isinstance(toc[0], nodes.list_item)
    assert toc[0][0].astext() == 'Over'
    assert _toc_children(toc[0]) == [('section', 'Deep')]
    assert_node(toc[1], addnodes.toctree, includefiles=['over-child'])

    warnings = strip_escape_sequences(app.warning.getvalue())
    assert 'toctree :level-up: 5 exceeds the number of containing sections' in warnings
    assert '[toc.level_up]' in warnings


@pytest.mark.sphinx('html', testroot='toctree-level-up')
def test_level_up_html_global_toc(app: SphinxTestApp) -> None:
    app.build()
    toctree = global_toctree_for_doc(
        app.env,
        'index',
        app.builder,
        tags=app.tags,
        collapse=False,
        includehidden=True,
    )
    assert toctree is not None
    # Hidden include of defaults/over, then promoted siblings of local sections.
    titles = [
        entry[0].astext()
        for entry in toctree.findall(nodes.list_item)
        if entry[0].astext()
        in {'Defaults', 'Over', 'Page 1', 'Page 2', 'Hidden page', 'Numbered page'}
    ]
    assert titles == [
        'Defaults',
        'Over',
        'Page 1',
        'Page 2',
        'Hidden page',
        'Numbered page',
    ]


@pytest.mark.sphinx('html', testroot='toctree-level-up')
def test_level_up_html_in_page_order(app: SphinxTestApp) -> None:
    app.build()
    content = (app.outdir / 'index.html').read_text(encoding='utf8')
    before = content.index('Paragraph before toctree')
    after = content.index('Paragraph after toctree')
    # The visible list stays where the directive was written.
    page1 = content.index('main-toctree')
    later = content.index('Later sibling content')
    assert before < page1 < after < later
