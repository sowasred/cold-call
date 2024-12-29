const puppeteer = require('puppeteer');

exports.getPageContent = async (url) => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: 'networkidle0' });
  
  const content = await page.evaluate(() => {
    // Remove common elements
    const elementsToRemove = ['header', 'nav', 'footer'];
    elementsToRemove.forEach(tag => {
      const elements = document.getElementsByTagName(tag);
      for (let el of elements) {
        el.remove();
      }
    });

    // Focus on main content
    const mainContent = document.querySelector('main') || document.body;
    
    // Remove script and style tags
    const scriptsAndStyles = mainContent.querySelectorAll('script, style');
    scriptsAndStyles.forEach(el => el.remove());

    return mainContent.innerText;
  });

  await browser.close();
  return content;
};