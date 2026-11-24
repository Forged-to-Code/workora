"""Smoke test for standalone preview. Requires Playwright and Chromium."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os
html=Path(__file__).resolve().parents[2]/'Workora_Demo.html'
if not html.exists(): html=Path(__file__).resolve().parents[1]/'Workora_Demo.html'
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1440,'height':1000})
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    # The sandbox blocks browser navigation. Inject HTML into the blank page;
    # storage shim exercises persistence API calls but not across browser restarts.
    page.evaluate("""()=>{const m=new Map();Object.defineProperty(window,'localStorage',{value:{getItem:k=>m.get(k)||null,setItem:(k,v)=>m.set(k,String(v)),removeItem:k=>m.delete(k)}})}""")
    page.set_content(html.read_text());page.wait_for_timeout(200)
    assert page.locator('h1').inner_text().startswith('Good work.');assert page.locator('.category-card').count()==12
    def route(path):
        page.evaluate('(p)=>{location.hash=p}',path);page.wait_for_timeout(150)
    page.get_by_role('textbox',name='Search jobs').fill('Electrician within 5 km, ₹800 per day')
    page.locator('.search-submit').click();page.wait_for_timeout(200)
    assert page.locator('.job-card').count()==1,page.locator('.results').inner_text()
    page.get_by_role('button',name='Save Site Electrician').click()
    page.get_by_role('button',name='Apply now').click();assert page.get_by_role('button',name='Applied').count()==1
    page.get_by_role('button',name='Map view').click();assert page.locator('.offline-map').count()==1
    page.get_by_role('button',name='Site Electrician',exact=True).click();page.wait_for_timeout(150);assert 'Site Electrician' in page.locator('h1').inner_text()
    route('/login');page.get_by_role('button',name='Continue as demo worker').click();page.wait_for_timeout(150)
    page.get_by_role('button',name='saved jobs').click();assert page.locator('.job-card').count()==1
    page.get_by_role('button',name='applications',exact=True).click();assert page.get_by_text('Submitted',exact=True).count()==1
    route('/verification');page.get_by_role('button',name='Use synthetic sample').click();page.get_by_role('checkbox').check();page.get_by_role('button',name='Submit for review').click();assert page.locator('.status').inner_text()=='Pending Review'
    route('/admin');page.get_by_role('button',name='Enter demo review mode').click();page.get_by_role('button',name='Approve').click();route('/verification');assert page.locator('.status').inner_text()=='Verified'
    route('/login');page.get_by_role('button',name='Employer',exact=True).click();page.get_by_role('button',name='Continue as demo employer').click();page.wait_for_timeout(150);page.get_by_role('button',name='post a job',exact=True).first.click()
    page.get_by_label('Job title').fill('Test Electrician');page.get_by_label('Business name').fill('Fictional Business');page.get_by_label('Working hours').fill('9 AM – 5 PM');page.get_by_label('Required skills (comma separated)').fill('Electrical work');page.get_by_label('Wage (₹)').fill('1000');page.get_by_label('Description').fill('Fictional work for smoke testing.');page.get_by_role('button',name='Publish job').click();assert page.get_by_text('Test Electrician',exact=True).count()==1
    page.get_by_role('button',name='Close',exact=True).click();assert page.get_by_text('closed · ₹1,000/day').count()==1
    page.get_by_role('button',name='applicants',exact=True).click();page.locator('.panel select').first.select_option('Shortlisted');assert page.locator('.panel select').first.input_value()=='Shortlisted'
    for r in ['/','/jobs','/about','/employers','/how','/contact','/faq','/privacy','/terms','/cookies','/verification','/login','/signup','/worker-dashboard','/employer-dashboard','/admin']:
        route(r);assert page.locator('main h1, main h2').count()>0,r
    route('/faq');assert page.locator('details').count()==24;page.get_by_role('textbox',name='Search FAQs').fill('microphone');assert 0<page.locator('details').count()<24
    route('/');page.set_viewport_size({'width':390,'height':844});page.wait_for_timeout(150);assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1');page.screenshot(path=str(html.parent/'workora_mobile_preview.png'))
    page.get_by_role('button',name='Toggle navigation').click();assert page.locator('nav.open').count()==1
    assert not errors,errors
    print('PASS: homepage, category cards, wage/radius query, bookmark, apply, map, details, worker dashboard, document review, employer posting and closing, applicant status, 16 routes, FAQ search, mobile layout/menu; no uncaught browser errors.')
    browser.close()
