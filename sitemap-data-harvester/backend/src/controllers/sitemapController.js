const sitemapService = require('../services/sitemapService');
const path = require('path');


exports.validateSitemap = async (req, res) => {
  try {
    const { url } = req.body;
    const isValid = await sitemapService.validateSitemap(url);
    res.json({ isValid });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

exports.extractContent = async (req, res) => {
  try {
    const { url } = req.body;
    const result = await sitemapService.extractContent(url);
    res.json(result);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

exports.downloadContent = async (req, res) => {
  try {
    const { url } = req.body;
    const content = await sitemapService.getCombinedContent(url);
    
    // Generate custom filename
    const parsedUrl = new URL(url);
    // Handle cases where the hostname might not have subdomains
    const hostnameParts = parsedUrl.hostname.split('.');
    const siteName = hostnameParts.length > 1 ? hostnameParts[hostnameParts.length - 2] : hostnameParts[0];

    // Ensure that the sitemap name is correctly extracted
    let sitemapName = path.basename(parsedUrl.pathname, '.xml');
    if (!sitemapName || sitemapName === '/') {
      sitemapName = 'sitemap';
    }
    const customFileName = `${siteName}-${sitemapName}.txt`;

    res.setHeader('Content-Type', 'text/plain');
    res.setHeader('Content-Disposition', `attachment; filename="${customFileName}"`);
    res.setHeader('Access-Control-Expose-Headers', 'Content-Disposition');

    res.send(content);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};