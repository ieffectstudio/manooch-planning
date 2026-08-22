/**
 * add_new_line.js
 * -----------------------------------------------
 * Console helper for https://panel.hisms.ir/order/product_list.html
 *
 * - add_new_line(num)   : check ONE number (TEST ONLY, never saves)
 * - testAll()           : loop through all numbers until the last
 * - viewResults()       : print/return available / unavailable / unknown arrays
 *
 * Paste this whole file into the browser DevTools console (F12) on the product
 * form page. Then call add_new_line("...") or testAll().
 *
 * NOTE: This version is TEST-ONLY. It never clicks the save (ذخیره) button.
 */
(function () {
  const NUMBERS = [
    "50002106758493","50002937012586","50002692274310","50002162398065","50002958443021",
    "50002173846509","50002388590146","50002960917352","50002518842976","50002219386051",
    "50002370465182","50002369994208","50002907036514","50002681849037","50002694813752",
    "50002199964830","50002785572014","50002159673481","50002433785096","50002508874263",
    "50002512759036","50002594631805","50002927364012","50002212347596","50002160258749",
    "50002898730154","50002424065937","50002435791820","50002187346021","50002531574983",
    "50002428460375","50002791148203","50002150079361","50002669182043","50002440347158",
    "50002371729608","50002304896571","50002256840792","50002785436125","50002675846192",
    "50002571649803","50002116472058","50002959236840","50002168274903","50002314885036",
    "50004711592386","50004480271394","50004825468390","50004649375218","50004382645901",
    "50004461072839","50004263659401","50004209471156","50004502467813","50004665015743",
    "50004625298736","50004712856309","50004310074251","50004164271903","50004418673920",
    "50004404196738","50004218295406","50004491637058","50004958271360","50004790538642",
    "50004451279408","50004358631729","50004732298015","50004944158601","50004584175029",
    "50004956372140","50004544871096","50004944083521","50004721768043","50004221537806",
    "50004255631094","50004550864293","50004946372158","50004514863029","50004688760314",
    "50004803452980","50004117682405","50004405591768","50004812637405","50004860792648",
    "50004796853170","50004632875346","50004945874061","50004197073954","50004752681047",
    "50004197286504","50004410978562","50004361670298","50004573756801","50004399786104"
  ];

  window.availableNumbers   = [];
  window.unavailableNumbers = [];
  window.unknownNumbers     = [];

  const config = {
    inputDelay: 150,   // pause after typing before clicking بررسی
    alertWait: 6000,   // max time to wait for the alert to appear
    okDelay: 250,      // pause around clicking the alert OK button
    betweenDelay: 300  // pause between numbers during testAll()
  };

  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const q = s => document.querySelector(s);
  const visible = el => {
    if (!el) return false;
    const st = getComputedStyle(el);
    return st.display !== 'none' && st.visibility !== 'hidden' && el.offsetParent !== null;
  };

  async function waitForAlert(timeout) {
    const start = Date.now();
    while (Date.now() - start < timeout) {
      const el = q('.sweet-alert.showSweetAlert');
      if (el && visible(el)) return el;
      await sleep(150);
    }
    return null;
  }

  // Check ONE number (test only, never saves).
  window.add_new_line = async function (num) {
    const input    = q('#numberLength');
    const checkBtn = q('#check_number');
    let result = { num, status: 'unknown', message: '' };

    input.value = num;
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
    await sleep(config.inputDelay);

    checkBtn.click();

    const alertEl = await waitForAlert(config.alertWait);
    if (alertEl) {
      await sleep(config.okDelay);
      const successIcon = alertEl.querySelector('.sa-success');
      const errorIcon   = alertEl.querySelector('.sa-error');
      const lead = alertEl.querySelector('p.lead, .lead');
      result.message = lead ? lead.textContent.trim() : '';
      result.status = (visible(successIcon) && !visible(errorIcon)) ? 'available' : 'unavailable';

      const ok = alertEl.querySelector('.confirm');
      if (ok) ok.click();
      await sleep(config.okDelay);
    }

    const bucket = result.status === 'available' ? window.availableNumbers
                 : result.status === 'unavailable' ? window.unavailableNumbers
                 : window.unknownNumbers;
    bucket.push(result.num);

    console.log(`${num} -> ${result.status}`, result.message);
    return result;
  };

  // Loop through ALL numbers, one by one, until the last one.
  window.testAll = async function () {
    for (let i = 0; i < NUMBERS.length; i++) {
      await window.add_new_line(NUMBERS[i]);
      await sleep(config.betweenDelay);
      console.log(`-> ${i + 1}/${NUMBERS.length} done`);
    }
    return window.viewResults();
  };

  // Results:
  window.viewResults = function () {
    console.log('Available  :', window.availableNumbers.length, window.availableNumbers);
    console.log('Unavailable:', window.unavailableNumbers.length, window.unavailableNumbers);
    console.log('Unknown    :', window.unknownNumbers.length, window.unknownNumbers);
    return { available: window.availableNumbers, unavailable: window.unavailableNumbers, unknown: window.unknownNumbers };
  };
})();
