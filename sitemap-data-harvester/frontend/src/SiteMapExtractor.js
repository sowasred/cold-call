import React, { useState } from 'react';
import axios from 'axios';

function SitemapExtractor() {
  const [sitemapUrl, setSitemapUrl] = useState('');
  const [isValidUrl, setIsValidUrl] = useState(false);
  const [isExtracting, setIsExtracting] = useState(false);
  const [status, setStatus] = useState('');

  const validateSitemap = async () => {
    try {
      const response = await axios.post('http://localhost:5001/api/validate-sitemap', { url: sitemapUrl });
      setIsValidUrl(response.data.isValid);
      setStatus(response.data.isValid ? 'Valid sitemap URL' : 'Invalid sitemap URL');
    } catch (error) {
      setStatus('Error validating sitemap');
    }
  };

  const extractContent = async () => {
    setIsExtracting(true);
    setStatus('Extracting content...');
    try {
      const response = await axios.post('http://localhost:5001/api/extract-content', { url: sitemapUrl });
      setStatus(`Extraction complete. ${response.data.totalPages} pages processed.`);
    } catch (error) {
      setStatus('Error extracting content');
    }
    setIsExtracting(false);
  };

  const downloadContent = async () => {
    try {
      const response = await axios.post('http://localhost:5001/api/download-content', 
        { url: sitemapUrl },
        { responseType: 'blob' }
      );
      
      // Extract filename from Content-Disposition header
      const contentDisposition = response.headers['content-disposition'];
      const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
      const matches = filenameRegex.exec(contentDisposition);
      const filename = matches && matches[1] ? matches[1].replace(/['"]/g, '') : 'combined_content.txt';

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      if (error.response) {
        // r responded with a status other than 2xx
        setStatus(`Error: ${error.response.data.error}`);
        console.error('Download error:', error.response.data);
      } else if (error.request) {
        // Request was made but no response received
        setStatus('No response from server');
        console.error('Download error:', error.request);
      } else {
        // Something else happened
        setStatus('Error downloading content');
        console.error('Download error:', error.message);
      }
    }
  };

  return (
    <div className="container">
      <h1>Sitemap Content Extractor</h1>
      <input
        type="text"
        value={sitemapUrl}
        onChange={(e) => setSitemapUrl(e.target.value)}
        placeholder="Enter sitemap URL"
      />
      <button onClick={validateSitemap}>Validate URL</button>
      <button onClick={extractContent} disabled={!isValidUrl || isExtracting}>
        Start Extraction
      </button>
      <button onClick={downloadContent} disabled={!isValidUrl || isExtracting}>
        Download All Content
      </button>
      <div id="status">{status}</div>
    </div>
  );
}

export default SitemapExtractor;