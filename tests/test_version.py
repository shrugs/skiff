#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is part of skiff.
# http://github.com/Shrugs/skiff

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2014 Matt Condon m@cond.in

from preggy import expect

from skiff import __version__
from tests.base import TestCase


class VersionTestCase(TestCase):
    def test_has_proper_version(self):
        expect(__version__).to_equal("0.1.0")
