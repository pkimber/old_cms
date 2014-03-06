# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from cms.management.commands import (
    demo_data_cms,
    init_app_cms,
)


class TestCommand(TestCase):

    def test_demo_data(self):
        """ Test the management command """
        command = demo_data_cms.Command()
        command.handle()

    def test_init_app(self):
        """ Test the management command """
        command = init_app_cms.Command()
        command.handle()
