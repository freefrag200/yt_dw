// All cookies across ALL domains (the app needs YouTube/Google cookies
// regardless of which tab is active). chrome.cookies returns decrypted values.
export async function getAllCookies() {
  try {
    return await chrome.cookies.getAll({});
  } catch (e) {
    return [];
  }
}
