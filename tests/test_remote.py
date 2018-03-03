"""Test the cfg_load.paths module."""

# core modules
import os
import unittest

# internal modules
import cfg_load.remote


class RemoteTest(unittest.TestCase):
    """Tests for the cfg_load.paths module."""

    def test_load_http(self):
        source = ('https://martin-thoma.com/images/2017/02/'
                  'Martin_Thoma_web_thumb.jpg')
        sink = 'ignore_image-random.jpg'
        cfg_load.remote.load(source, sink)
        os.remove(sink)

    def test_load_ftp(self):
        source = ('ftp://ftp.hp.com/pub/hpdm/Documentation/WhitePapers/4.5/'
                  'WP_HPDM_FTP_Configuration.pdf')
        sink = 'ignore_pdf-random.pdf'
        cfg_load.remote.load(source, sink)
        os.remove(sink)
