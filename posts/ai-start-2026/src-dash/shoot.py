from playwright.sync_api import sync_playwright
url = 'file:///C:/Users/Matt/Documents/business-dashboards-demo/restaurant.html'
HIDE = r"""()=>{document.querySelectorAll('body *').forEach(e=>{if(e.children.length>3)return;const t=(e.innerText||'').trim();
  if(/^Now viewing as/.test(t)||/^(Demo by Three Village Local|Want one for your business\?)$/.test(t)){let x=e;while(x.parentElement&&x.parentElement.children.length===1&&x.parentElement!==document.body)x=x.parentElement;x.style.visibility='hidden'}});
  const rb=document.querySelector('.role-banner');if(rb)rb.style.display='none';scrollTo(0,0)}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_context(viewport={'width': 1440, 'height': 940}, device_scale_factor=2).new_page()
    pg.goto(url, wait_until='networkidle'); pg.wait_for_timeout(1500)
    for i in range(3):
        pg.click('#roleBtn'); pg.wait_for_timeout(300)
        pg.locator('.role-opt').nth(i).click(); pg.wait_for_timeout(4500)
        pg.evaluate(HIDE); pg.wait_for_timeout(400)
        pg.screenshot(path='src-dash/role%d.png' % i)
    b.close()
