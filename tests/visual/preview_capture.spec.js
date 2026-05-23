const { test } = require('@playwright/test');

test.describe('SENTINELAI I, Robot UI Preview', () => {
  
  test.beforeEach(async ({ page }) => {
    // Navigate to the local login page on port 3001
    await page.goto('http://localhost:3001/login.html');
  });

  test('Capture LoginComponent', async ({ page }) => {
    await page.setViewportSize({ width: 1200, height: 800 });
    // Wait for the slide-in animation and backdrop filter
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'previews/login_page.png' });
    console.log('[PREVIEW]: Login Page Captured.');
  });

  test('Capture Tactical Dashboard', async ({ page }) => {
    // Go directly to the dashboard
    await page.goto('http://localhost:3001/index.html');
    
    // Ensure we only interact with the relevant portal
    await page.waitForSelector('text=SENTINELAI // INFRASTRUCTURE', { timeout: 20000 });
    await page.setViewportSize({ width: 1400, height: 900 });
    
    // Allow for gauge animations and avoid scanning arbitrary system dirs
    await page.waitForTimeout(3000);
    
    await page.screenshot({ path: 'previews/dashboard_infrastructure.png' });
    console.log('[PREVIEW]: Infrastructure Dashboard Captured.');
  });

});
