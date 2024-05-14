# = = = = = = = = = = = = = = = = = = = = = = = = = = =
# IMPORT
# = = = = = = = = = = = = = = = = = = = = = = = = = = =

# 모델
from ..models import *

# = = = = = = = = = = = = = = = = = = = = = = = = = = =
# 공통 변수
# = = = = = = = = = = = = = = = = = = = = = = = = = = =

# 카테고리 정보
categories = {
    'cocktailinfo': {
        'name': '칵테일정보',
        'url': '/cocktailinfo/?page=1',
        'exp': '칵테일 정보와 레시피를 확인하실 수 있습니다.'
    },
    'cocktailcalc': {
        'name': '칵테일계산기', 
        'url': '/cocktailcalc', 
        'exp': '가진 재료로 만들수 있는 칵테일을 계산할 수 있습니다.'
    },
    'community': {
        'name': '커뮤니티', 
        'url': '/community/?page=1', 
        'exp': '칵테일에 대해 얘기하는 게시판입니다.'
    },
    'column': {
        'name': '칼럼', 
        'url': '/column/?page=1',
        'exp': '칵테일에 관련된 칼럼을 연재하는 곳입니다.'
    },
    'notice': {
        'name': '공지사항', 
        'url': '/notice/?page=1', 
        'exp': '넥타리스트 운영과 관련된 공지사항입니다.'
    },
    'signup': {
        'name': '회원가입', 
        'url': '/sign_up', 
        'exp': '넥타리스트 회원 등록 화면입니다.'
    },
    'signin': {
        'name': '로그인', 
        'url': '/sign_in', 
        'exp': '회원가입시 입력한 아이디와 패스워드로 로그인하실 수 있습니다.'
    },
    'findid': {
        'name': '아이디 찾기', 
        'url': '/find_id', 
        'exp': '가입된 이메일로 아이디를 검색합니다.'
    },
    'findpw': {
        'name': '비밀번호 찾기', 
        'url': '/find_pw', 
        'exp': '가입된 아이디의 비밀번호를 변경합니다.'
    },
    'myinfo': {
        'name': '내정보 관리',
        'url': '/mypage_myinfo/', 
        'exp': ''
    },
    'mypwchange': {
        'name': '비밀번호 변경',
        'url': '/mypage_mypwchange/', 
        'exp': ''
    },
    'myrefrig': {
        'name': '내 냉장고',
        'url': '/mypage_myrefrig/', 
        'exp': ''
    },
    'myboard': {
        'name': '작성글 보기',
        'url': '/mypage_myboard/', 
        'exp': ''
    },
    'admin_asetmain': {
        'name': '메인화면 설정',
        'url': '/admin_asetmain/?page=1', 
        'exp': ''
    },
    'admin_asetingrdnt': {
        'name': '칵테일 재료 관리',
        'url': '/admin_asetingrdnt/?page=1', 
        'exp': ''
    }
}

# 카테고리 목록 - 일반
category_list_main = [
    'cocktailinfo',
    'cocktailcalc',
    'community',
    'column',
    'notice'
]

# 카테고리 목록 - 마이페이지
category_list_mypage = [
    'myinfo',
    'mypwchange',
    'myrefrig',
    'myboard'
]

# 카테고리 목록 - 관리자 페이지
category_list_admin = [
    'admin_asetmain',
    'admin_asetingrdnt'
]

# 게시판 번호
# 01 공지사항 02 칼럼 03 커뮤니티

# 재료 종류
ingrdnt_type = {
    '01': '베이스',
    '02': '재료',
    '03': '기타'
}

# = = = = = = = = = = = = = = = = = = = = = = = = = = =
# 공통 
# = = = = = = = = = = = = = = = = = = = = = = = = = = =

# 공통 변수 추가
def add_global_context(request):
    context = {}
    context.update({"categories": categories})
    context.update({"category_list_main": category_list_main})
    context.update({"category_list_mypage": category_list_mypage})
    context.update({"category_list_admin": category_list_admin})
    
    if 'is_login' in request.session and request.session['is_login'] == 'Y':
        context.update({'is_login': 'Y'})
        context.update({'login_id': request.session['login_id']})
        context.update({'login_data': NtUser.objects.get(nt_user_idx=request.session['login_id'])})
    else:
        context.update({"is_login": 'N'})

    return context