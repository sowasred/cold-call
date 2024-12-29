const express = require('express');
const sitemapController = require('../controllers/sitemapController');

const router = express.Router();

router.post('/validate-sitemap', sitemapController.validateSitemap);
router.post('/extract-content', sitemapController.extractContent);
router.post('/download-content', sitemapController.downloadContent);

module.exports = router;