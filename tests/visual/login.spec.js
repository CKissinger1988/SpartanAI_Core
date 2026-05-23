const { test, expect } = require('@playwright/test');

test.describe('SENTINELAI Supreme UI - Visual Validation', () => {
  
  test('LoginComponent: Static Visual Integrity', async ({ page }) => {
    await page.goto('http://localhost:3000');
    
    // Validate main elements existence
    await expect(page.locator('h1')).toHaveText('SENTINELAI');
    await expect(page.locator('text=Supreme Intelligence Portal')).toBeVisible();
    
    // Capture screenshot for visual comparison
    await page.screenshot({ path: 'tests/visual/screenshots/login-initial.png' });
  });

  test('LoginComponent: Interaction Bio-Feedback', async ({ page }) => {
    await page.goto('http://localhost:3000');
    
    const operatorInput = page.locator('#operator-id');
    await operatorInput.fill('CKissinger');
    
    // Capture glow effect
    await page.screenshot({ path: 'tests/visual/screenshots/login-glow-active.png' });
    
    const accessKey = page.locator('#access-key');
    await accessKey.fill('DIVINE_AUTHORITY_2026');
    
    const loginBtn = page.locator('button:has-text("ESTABLISH_UPLINK")');
    await loginBtn.hover();
    
    // Capture hover effect
    await page.screenshot({ path: 'tests/visual/screenshots/login-hover.png' });
  });

  test('LoginComponent: Authentication Handshake Animation', async ({ page }) => {
    await page.goto('http://localhost:3000');
    
    await page.locator('#operator-id').fill('CKissinger');
    await page.locator('#access-key').fill('wrong_key');
    await page.click('button:has-text("ESTABLISH_UPLINK")');
    
    // The handshake bar should appear
    await expect(page.locator('div >> nth=-3')).toBeVisible(); // Simplistic check for the bar
    
    // Wait for failure
    await expect(page.locator('text=ERROR')).toBeVisible({ timeout: 10000 });
    await page.screenshot({ path: 'tests/visual/screenshots/login-auth-fail.png' });
  });

});
