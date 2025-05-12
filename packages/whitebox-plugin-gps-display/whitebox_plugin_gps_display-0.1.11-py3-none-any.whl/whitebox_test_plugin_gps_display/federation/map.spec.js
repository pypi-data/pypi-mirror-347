import { test } from '@tests/setup'
import { expect } from '@playwright/test';

test.beforeEach(async ({page}) => {
  // The map is rendered on the dashboard page
  await page.goto('/dashboard');
})

test('should render the map', async ({page}) => {
  // Ensure map container is loaded
  const mapContainer = await page.locator('.c_map_area');
  await expect(mapContainer).toBeVisible();

  // Ensure Leaflet map is loaded
  const leafletMap = await page.locator('.leaflet-container')
      .nth(0);  // Currently, we're rendering two maps to workaround a bug,
                // hence the nth(0) selector. This will be handled in issue #253
                // https://gitlab.com/whitebox-aero/whitebox/-/issues/253
  await expect(leafletMap).toBeVisible();
})

test('should render marker after location_update message', async ({page}) => {
    // Ensure Leaflet map is loaded
  const leafletMap = await page.locator('.leaflet-container')
      .nth(0);  // Currently, we're rendering two maps to workaround a bug,
                // hence the nth(0) selector. This will be handled in issue #253
                // https://gitlab.com/whitebox-aero/whitebox/-/issues/253
  await expect(leafletMap).toBeVisible();

  const marker = await leafletMap.locator('.leaflet-marker-icon');

  // Before the message, the marker should not be visible
  await expect(marker).not.toBeVisible();

  // Simulate the location_update message
  await page.evaluate(() => {
    const message = {
      type: 'location_update',
      latitude: 0,
      longitude: 0,
    };

    // Create the event and pass it to the socket
    const event = new MessageEvent('message', {
      data: JSON.stringify(message)
    });
    const flightSocket = Whitebox.sockets.getSocket('flight', false);
    flightSocket.dispatchEvent(event);
  })

  // After the message, the marker should be rendered and visible
  await expect(marker).toBeVisible();
});
