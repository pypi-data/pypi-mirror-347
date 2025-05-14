### analyser-hj3415

#### Introduction 
analyser_hj3415 manage the database.

---
#### Requirements

pandas>=2.2.2
pymongo>=4.8.0
sqlalchemy>=2.0.31
utils-hj3415>=2.0.1
scraper-hj3415>=2.0.0

---
#### API

---
#### Install


---
#### Composition
analyser_hj3415 모듈은 세가지 파트로 구성되어 있습니다.

1. setting 모듈 
setting 모듈은 데이터베이스를 활성화하고 주소를 설정하는 역할을 합니다. 
데이터베이스의 주소와 활성화 여부를 파일에 저장합니다.

```python
from analyser_hj3415 import setting

# 현재 데이터 베이스 상태를 DbSetting 클래스 형식으로 반환한다.
db_setting = setting.load_df()

# 현재 데이터베이스 상태 출력
print(db_setting)

# 몽고db 주소 변경 (2가지 방식)
setting.chg_mongo_addr('mongodb://192.168.0.173:27017')
db_setting.mongo_addr = 'mongodb://192.168.0.173:27017'

# sqlite3 주소 변경 (2가지 방식)
setting.chg_sqlite3_path('/home/hj3415/Stock/_db')
db_setting.sqlite3_path = '/home/hj3415/Stock/_db'

# 데이터베이스를 기본값으로 설정합니다.
# DEF_MONGO_ADDR = 'mongodb://localhost:27017'
# DEF_WIN_SQLITE3_PATH = 'C:\\_db'
# DEF_LINUX_SQLITE3_PATH = '/home/hj3415/Stock/_db'
setting.set_default()

# 각 데이터베이스 사용 설정
setting.turn_on_mongo()
setting.turn_off_mongo()
setting.turn_off_sqlite3()
setting.turn_on_sqlite3()
```

2. mongo 모듈
몽고db를 데이터베이스로 사용할 경우를 위한 함수들의 모듈입니다.
현재는 몽고db를 비활성화 할 경우 올바로 작동하지 않기 때문에 디폴트 데이터베이스 입니다. 

1) Base 클래스

모든 데이터베이스 클래스의 기반 클래스로 실제 직접 사용하지 않음.

```python
from analyser_hj3415.mongo import Base
base = Base(db='mi', col='kospi')

# db 주소를 변경함. 단 파일에 저장되는 것이 아니라 클래스 내부에서 일시적으로 설정하는 것임 
base.chg_addr('mongodb://192.168.0.173:27017')

# 현재 설정된 db 주소, db 명, 컬렉션을 반환함.
base.get_status()
# ('mongodb://192.168.0.173:27017', 'mi', 'kospi')

# 데이터 베이스 관리 함수
base.get_all_db()
```

2 - 1) Corps 클래스

DB 내에서 종목에 관련된 기반클래스로 db명은 6자리 숫자 코드명임.

```python
from analyser_hj3415.mongo import Corps

corps = Corps(code='005930', page='c101')

# 코드를 변경함. 6자리 숫자인지 확인 후 설정함.
corps.chg_code('005490')

# 페이지를 변경함. 페이지명의 유효성 확인 후 설정함.
# ('c101', 'c104y', 'c104q', 'c106', 'c108', 'c103손익계산서q', 'c103재무상태표q', 'c103현금흐름표q', 'c103손익계산서y', 'c103재무상태표y', 'c103현금흐름표y', 'dart')
corps.chg_page(page='c108')

# 데이터 베이스 관리 함수
corps.get_all_codes()
corps.del_all_codes()
corps.drop_corp(code='005930')
corps.get_all_pages()
corps.drop_all_pages(code='005930')
corps.drop_page(code='005930', page='c101')
corps.get_all_item()
```

2 - 2) MI 클래스

DB 내에서 Market index 관련 클래스

```python
from analyser_hj3415.mongo import MI
mi = MI(index='kospi')

# 인덱스를 변경함. 인덱스명의 유효성 확인 후 설정
# ('aud', 'chf', 'gbond3y', 'gold', 'silver', 'kosdaq', 'kospi', 'sp500', 'usdkrw', 'wti', 'avgper', 'yieldgap', 'usdidx')
mi.chg_index(index='gold')

# 저장된 가장 최근 값 반환
mi.get_recent()

# 데이터를 저장함.
mi.save(mi_dict={'date': '2021.07.21', 'value': '1154.50'})

# 데이터 베이스 관리 함수
mi.get_all_indexes()
mi.drop_all_indexes()
mi.drop_index(index='silver')
mi.get_all_item()
```

2 - 3) DartByDate 클래스

dart_hj3415의 dart 모듈에서 dart 데이터프레임을 추출하면 각 날짜별 컬렉션으로 저장하는 클래스

```python
from dart_hj3415 import dart
from analyser_hj3415.mongo import DartByDate

date = '20210812'
dart_db = DartByDate(date=date)

# 오늘 날짜의 dart 데이터프레임을 추출하여 데이터베이스에 저장 
df = dart.get_df(edate=date)
dart_db.save(df)

# 공시 데이터를 데이터프레임으로 반환한다. 
dart_db.get_data()
dart_db.get_data(title='임원ㆍ주요주주특정증권등소유상황보고서')
```

2 - 4) EvalByDate 클래스

eval_hj3415의 eval 모듈에서 eval 데이터프레임을 추출하여 저장하거나 불러올때 사용.
(실제로 eval_hj3415.eval.make_today_eval_df()에서 오늘자 데이터프레임을 항상 저장한다)

```python
import pandas as pd
import datetime
from analyser_hj3415.mongo import EvalByDate

today_str = datetime.datetime.today().strftime('%Y%m%d')
eval_db = EvalByDate(date=today_str)

# 오늘 날짜의 dart 데이터프레임을 추출하여 데이터베이스에 저장 
eval_db.save(pd.DataFrame())

# 공시 데이터를 데이터프레임으로 반환한다. 
eval_db.get_data()
```

2 - 5) Noti 클래스

dart_hj3415의 analysis 모듈에서 공시를 분석하여 의미있는 공시를 노티하고 노티한 기록을 저장하는 클래스

```python
from analyser_hj3415.mongo import Noti
noti_db = Noti()

# 저장이 필요한 노티 데이터를 딕셔너리로 전달하여 데이터베이스에 저장
data = {'code': '005930',
        'rcept_no': '20210514000624',
        'rcept_dt': '20210514',
        'report_nm': '임원ㆍ주요주주특정증권등소유상황보고서',
        'point': 2,
        'text': '등기임원이 1.0억 이상 구매하지 않음.'}
noti_db.save(noti_dict=data)

# 오래된 노티 데이터를 정리하는 함수
noti_db.cleaning_data(days_ago=15)
```

3) Corps 

C101 페이지 관리 클래스

```python
from analyser_hj3415.mongo import C101
c101 = C101(code='005930')
...
```

구현 클래스는 C101, C108, C106, C103, C104

3. sqlite 모듈
sqlite3를 데이테베이스로 사용할 경우를 위한 함수들의 모듈입니다.
현재 sqlite3는 사용하지 않기 때문에 작동하지 않습니다.

```python
from analyser_hj3415 import sqlite

```
---

