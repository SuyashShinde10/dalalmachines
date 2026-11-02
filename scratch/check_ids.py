import re

with open('D:/st.ourhtmldemo.com/scratch/generate_enlarged_spec.py', encoding='utf-8') as f:
    text = f.read()

r_matches = re.findall(r'"id":\s*"(ROUTE-\d+)"', text)
m_matches = re.findall(r'"id":\s*"(ERP-MOD-\d+)"', text)
print('Routes count:', len(r_matches), r_matches[0], 'to', r_matches[-1])
print('Modules count:', len(m_matches), m_matches[0], 'to', m_matches[-1])

