import sys, json, csv
from pathlib import Path
from tempfile import TemporaryDirectory
from datetime import date, timedelta
from unittest.mock import patch

ROOT = Path('/workspace/scratch/3b0e239b04fd/verification-main')
PROTO = ROOT / '05-Final/prototype'
sys.path.insert(0, str(PROTO))
import pandas as pd
from streamlit.testing.v1 import AppTest
import streamlit as st
import exchange_rates as fx
from smart.auth import hash_password, verify_password
from smart.forecast import forecast_in_home_currency

def note(case, message):
    print(f'{case}: {message}', flush=True)

def forecast_app():
    a = AppTest.from_file(str(PROTO/'app.py'), default_timeout=30)
    a.session_state['user_role'] = 'student'
    a.run()
    a.sidebar.radio[0].set_value('Forecast and alerts').run()
    assert not a.exception
    return a

# Exact fixture conversion, additional to the manually observed live-rate runs.
with patch('exchange_rates.get_rates', return_value=({'EUR': .2}, '2026-11-23', 'Controlled fixture')):
    assert forecast_in_home_currency(1000,300,10,30,'EUR') == 80
    assert forecast_in_home_currency(950,350,10,30,'EUR') == 50
note('TC-07', 'Controlled conversion at 1 EUR = 5 MYR: EUR80 before and EUR50 after the RM50 expense; PASS (function-level supplement).')

# Exercise rendered alert boundary states, not only the comparator function.
rates = {'EUR': .2, 'USD': .25, 'CNY': 1.6, 'INR': 22., 'SAR': .9}
fixture_today = date.today()
history = [{ 'date':(fixture_today-timedelta(days=i)).isoformat(), 'base':'EUR', 'quote':'MYR', 'rate':5.0 } for i in range(30)]
from io import BytesIO
def history_response(*args, **kwargs):
    return BytesIO(json.dumps(history).encode())
with patch('exchange_rates.get_rates', side_effect=lambda: (dict(rates), '2026-11-23', 'Controlled fixture')), patch('urllib.request.urlopen', side_effect=history_response):
    a=forecast_app()
    a.number_input[0].set_value(5.)
    next(b for b in a.button if b.label=='Save target').click().run()
    for current in (4.99,5.,5.01):
        rates['EUR']=1/current
        a.run()
        assert not a.exception
        green=any('Good time to transfer' in x.value for x in a.success)
        assert green == (current>=5.)
        assert any('Checked ' in x.value for x in a.caption)
        note('TC-08', f'AppTest rendered current={current:.2f}, target=5.00, alert={green}; rate and timestamp displayed; PASS.')
    # Fresh no-target session checks the controlled average. Manual clear-target failure remains open.
    rates['EUR']=1/4.99
    b=forecast_app()
    assert any('30-day average: 5.0000' in x.value for x in b.markdown)
    assert not any('Good time to transfer' in x.value for x in b.success)
    rates['EUR']=.2
    b.run()
    assert any('Good time to transfer' in x.value for x in b.success)
    note('TC-09', 'Fresh blank target uses controlled 30-day average5; below/equal states correct. Previously saved-target clearing failure reported manually remains FAIL; not retested as fixed.')

with TemporaryDirectory() as d:
    cache = Path(d)/'rates.csv'
    initial={c:r for c,r in zip(fx.TARGET_CURRENCIES,[.2,.25,1.6,22.,.9])}
    changed={c:r*1.01 for c,r in initial.items()}
    day0=date(2026,11,21)
    with patch.object(fx,'CACHE_FILE',cache):
        for day, quotes in [(day0-timedelta(days=1), initial),(day0,changed)]:
            with patch.object(fx,'fetch_rates',return_value=(quotes,day.isoformat())), patch.object(fx,'fetch_rate_history',return_value={day:quotes}):
                fx._refresh(day)
                assert fx._latest(fx._read_cache()) == (quotes,day.isoformat())
        saved=cache.read_bytes()
        with patch.object(fx,'fetch_rates',side_effect=OSError('Simulated service outage')):
            try: fx._refresh(day0+timedelta(days=1))
            except OSError: pass
            else: raise AssertionError('Expected simulated outage')
        assert cache.read_bytes()==saved
        note('TC-14', 'Controlled successful update for all5 currencies on two consecutive days; failed refresh preserves latest valid CSV. Adapter fallback is checked below. Cache TTL3600seconds verified by source review.')
        for hours in (24,48):
            simulated=day0+timedelta(hours=hours)
            class FrozenDate(date):
                @classmethod
                def today(cls): return simulated
                @classmethod
                def fromisoformat(cls,value): return date.fromisoformat(value)
            st.cache_data.clear()
            with patch.object(fx,'date',FrozenDate), patch.object(fx,'urlopen',side_effect=OSError('Simulated service outage')), patch('urllib.request.urlopen',side_effect=OSError('Simulated service outage')):
                a=forecast_app()
                assert not a.exception
                assert any('last saved exchange rates from 2026-11-21' in x.value for x in a.warning)
                vals={x.label:x.value for x in a.metric}
                assert vals['Estimated balance on 31 Oct']=='RM 420.46'
                assert vals['Estimate in EUR']=='EUR 84.93'
                assert any('Good time to transfer' in x.value or 'Below your target' in x.value for x in [*a.success,*a.info])
                note('TC-21',f'Simulated outage +{hours}hours: rendered forecastRM420.46, EUR84.93 and alert work using saved2026-11-21 rates; no live requests succeed; PASS.')
    st.cache_data.clear()

# Two local dummy records with the same password must have distinct salt/hash.
password='LocalSyntheticCheck2026!'
hashes=[hash_password(password),hash_password(password)]
assert hashes[0]!=hashes[1]
assert all(verify_password(password,h) for h in hashes)
assert all(h.startswith('pbkdf2_sha256$600000$') for h in hashes)
records=list(csv.DictReader((PROTO/'data/users.csv').open()))
assert all(r['password_hash'].startswith('pbkdf2_sha256$') for r in records)
budget=PROTO/'data/budgets.csv'
before=budget.read_bytes()
calls=[]
def attempted_editor_change(data,**kwargs):
    calls.append(kwargs.get('disabled'))
    edited=data.copy()
    edited.loc[edited.index[0],'category']='Other'
    return edited
with patch('streamlit.data_editor',side_effect=attempted_editor_change):
    a=AppTest.from_file(str(PROTO/'app.py'),default_timeout=30)
    a.session_state['user_role']='sponsor'
    a.run()
    assert not a.exception
    assert a.sidebar.radio[0].options == [':material/dashboard: Dashboard']
    assert all(x.disabled for x in a.text_input)
    assert next(x for x in a.button if x.label=='Save budget').disabled
    assert calls and all(v is True for v in calls)
    assert (a.session_state['sample_transactions']['category_source']=='auto').all()
    assert budget.read_bytes()==before
note('TC-20','Different salted hashes for identical dummy passwords; stored demo records hashed; Sponsor controls disabled and injected editor change not committed; budget file unchanged. Manual sponsor no-add/edit/delete checks also recorded. PASS for supported app actions.')

tx=pd.read_csv(PROTO/'data/transactions.csv')
survey=pd.read_csv(ROOT/'02-Requirements/survey/responses.csv')
assert list(tx.columns)==['date','merchant','amount','currency']
assert len(survey)==20
assert not any(any(term in c.lower() for term in ['email','name','card','account number']) for c in survey.columns)
note('TC-23','Reviewed synthetic transaction declaration, transaction fields,20 anonymous survey rows with no name/email fields and P1-P5 UAT notes; demo emails are synthetic login accounts. PASS for reviewed evidence.')
print('SUPPLEMENTAL CHECKS COMPLETED',flush=True)
