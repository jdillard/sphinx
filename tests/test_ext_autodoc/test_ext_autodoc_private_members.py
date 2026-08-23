"""Test the autodoc extension.  This tests mainly for private-members option."""

from __future__ import annotations

import pytest

from sphinx.ext.autodoc._shared import _AutodocConfig

from tests.test_ext_autodoc.autodoc_util import do_autodoc

pytestmark = pytest.mark.usefixtures('inject_autodoc_root_into_sys_path')


def test_private_field() -> None:
    config = _AutodocConfig(autoclass_content='class')
    options = {'members': None}
    actual = do_autodoc('module', 'target.private', config=config, options=options)
    assert actual == [
        '',
        '.. py:module:: target.private',
        '',
        '',
        '.. py:data:: _PUBLIC_CONSTANT',
        '   :module: target.private',
        '   :value: None',
        '',
        '   :meta public:',
        '',
        '',
        '.. py:function:: _public_function(name)',
        '   :module: target.private',
        '',
        '   public_function is a docstring().',
        '',
        '   :meta public:',
        '',
    ]


def test_private_field_after_indented_field() -> None:
    # regression test for #11728: a `:meta private:` field must still be
    # honored even if it follows a field whose body contains indented
    # content (e.g. a bulleted list under `:raises:`).
    config = _AutodocConfig(autoclass_content='class')
    options = {'members': None}
    actual = do_autodoc('module', 'target.private', config=config, options=options)
    assert '.. py:function:: private_function_after_indented_field(name)' not in actual


def test_private_field_and_private_members() -> None:
    config = _AutodocConfig(autoclass_content='class')
    options = {
        'members': None,
        'private-members': None,
    }
    actual = do_autodoc('module', 'target.private', config=config, options=options)
    assert actual == [
        '',
        '.. py:module:: target.private',
        '',
        '',
        '.. py:data:: PRIVATE_CONSTANT',
        '   :module: target.private',
        '   :value: None',
        '',
        '   :meta private:',
        '',
        '',
        '.. py:data:: _PUBLIC_CONSTANT',
        '   :module: target.private',
        '   :value: None',
        '',
        '   :meta public:',
        '',
        '',
        '.. py:function:: _public_function(name)',
        '   :module: target.private',
        '',
        '   public_function is a docstring().',
        '',
        '   :meta public:',
        '',
        '',
        '.. py:function:: private_function(name)',
        '   :module: target.private',
        '',
        '   private_function is a docstring().',
        '',
        '   :meta private:',
        '',
        '',
        '.. py:function:: private_function_after_indented_field(name)',
        '   :module: target.private',
        '',
        '   private_function_after_indented_field is a docstring().',
        '',
        '   :raises ValueError:',
        '       - if the condition is not met',
        '       - if something else happens',
        '   :meta private:',
        '',
    ]


def test_private_members() -> None:
    config = _AutodocConfig(autoclass_content='class')
    options = {
        'members': None,
        'private-members': '_PUBLIC_CONSTANT,_public_function',
    }
    actual = do_autodoc('module', 'target.private', config=config, options=options)
    assert actual == [
        '',
        '.. py:module:: target.private',
        '',
        '',
        '.. py:data:: _PUBLIC_CONSTANT',
        '   :module: target.private',
        '   :value: None',
        '',
        '   :meta public:',
        '',
        '',
        '.. py:function:: _public_function(name)',
        '   :module: target.private',
        '',
        '   public_function is a docstring().',
        '',
        '   :meta public:',
        '',
    ]


def test_private_attributes() -> None:
    config = _AutodocConfig(autoclass_content='class')
    options = {'members': None}
    actual = do_autodoc('class', 'target.private.Foo', config=config, options=options)
    assert actual == [
        '',
        '.. py:class:: Foo()',
        '   :module: target.private',
        '',
        '',
        '   .. py:attribute:: Foo._public_attribute',
        '      :module: target.private',
        '      :value: 47',
        '',
        '      A public class attribute whose name starts with an underscore.',
        '',
        '      :meta public:',
        '',
    ]


def test_private_attributes_and_private_members() -> None:
    config = _AutodocConfig(autoclass_content='class')
    options = {
        'members': None,
        'private-members': None,
    }
    actual = do_autodoc('class', 'target.private.Foo', config=config, options=options)
    assert actual == [
        '',
        '.. py:class:: Foo()',
        '   :module: target.private',
        '',
        '',
        '   .. py:attribute:: Foo._public_attribute',
        '      :module: target.private',
        '      :value: 47',
        '',
        '      A public class attribute whose name starts with an underscore.',
        '',
        '      :meta public:',
        '',
        '',
        '   .. py:attribute:: Foo.private_attribute',
        '      :module: target.private',
        '      :value: 11',
        '',
        '      A private class attribute whose name does not start with an underscore.',
        '',
        '      :meta private:',
        '',
    ]
