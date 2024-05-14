from django.urls import path

from .views import page_views, func_views

urlpatterns = [
    # = = = = = = = = = = = = = = = = = = = = = = = = = = =
    # 페이지
    # = = = = = = = = = = = = = = = = = = = = = = = = = = =

    # 인덱스
    path("", page_views.page_main),
    # 일반 카테고리 - 메인
    path("main", page_views.page_main),
    # 일반 카테고리 - 칵테일정보
    path("cocktailinfo/", page_views.page_cocktailinfo),
    # 일반 카테고리 - 칵테일정보 - 상세
    path("cocktailinfo/detail/<int:cno>", page_views.page_cocktailinfo_detail),
    # 일반 카테고리 - 칵테일정보 - 신규
    path("cocktailinfo/new", page_views.page_cocktailinfo_new),
    # 일반 카테고리 - 칵테일정보 - 수정
    path("cocktailinfo/mod/<int:cno>/", page_views.page_cocktailinfo_mod),
    # 일반 카테고리 - 칵테일계산기
    path("cocktailcalc/", page_views.page_cocktailcalc),
    # 일반 카테고리 - 칵테일계산기 - 상세
    path("cocktailcalc/detail", page_views.page_cocktailcalc_detail),
    # 일반 카테고리 - 커뮤니티
    path("community/", page_views.page_community),
    # 일반 카테고리 - 커뮤니티 - 상세
    path("community/detail/<int:bno>/", page_views.page_community_detail),
    # 일반 카테고리 - 커뮤니티 - 신규
    path("community/new", page_views.page_community_new),
    # 일반 카테고리 - 커뮤니티 - 수정
    path("community/mod/<int:bno>/", page_views.page_community_mod),
    # 일반 카테고리 - 칼럼
    path("column/", page_views.page_column),
    # 일반 카테고리 - 칼럼 - 상세
    path("column/detail/<int:bno>/", page_views.page_column_detail),
    # 일반 카테고리 - 칼럼 - 신규
    path("column/new", page_views.page_column_new),
    # 일반 카테고리 - 칼럼 - 수정
    path("column/mod/<int:bno>/", page_views.page_column_mod),
    # 일반 카테고리 - 공지사항
    path("notice/", page_views.page_notice),
    # 일반 카테고리 - 공지사항 - 상세
    path("notice/detail/<int:bno>/", page_views.page_notice_detail),
    # 일반 카테고리 - 공지사항 - 신규
    path("notice/new", page_views.page_notice_new),
    # 일반 카테고리 - 공지사항 - 수정
    path("notice/mod/<int:bno>/", page_views.page_notice_mod),
    # 로그인 - 회원가입
    path("sign_up/", page_views.page_signup),
    # 로그인 - 로그인
    path("sign_in/", page_views.page_signin),
    # 로그인 - 아이디 찾기
    path("find_id/", page_views.page_findid),
    # 로그인 - 비밀번호 찾기
    path("find_pw/", page_views.page_findpw),
    # 마이페이지 - 내정보 관리
    path("mypage_myinfo/", page_views.page_myinfo),
    # 마이페이지 - 비밀번호 변경
    path("mypage_mypwchange/", page_views.page_mypwchange),
    # 마이페이지 - 내 냉장고
    path("mypage_myrefrig/", page_views.page_myrefrig),
    # 마이페이지 - 작성글 보기
    path("mypage_myboard/", page_views.page_myboard),
    # 관리자 - 메인화면 설정
    path("admin_asetmain/", page_views.page_asetmain),
    # 관리자 - 칵테일 재료 관리
    path("admin_asetingrdnt/", page_views.page_asetingrdnt),

    # = = = = = = = = = = = = = = = = = = = = = = = = = = =
    # 요청
    # = = = = = = = = = = = = = = = = = = = = = = = = = = =

    # 일반 카테고리 - 칵테일정보 - 칵테일정보 등록
    path("cocktailinfo/req_saveaddcocktail", func_views.func_saveaddcocktail),
    # 일반 카테고리 - 칵테일정보 - 칵테일정보 수정
    path("cocktailinfo/req_savemodcocktail", func_views.func_savemodcocktail),
    # 일반 카테고리 - 칵테일정보 - 삭제
    path("cocktailinfo/req_delcocktail", func_views.func_delcocktail),
    # 일반 카테고리 - 칵테일정보 - 댓글등록
    path("cocktailinfo/req_addcktcmt/", func_views.func_cocktailinfo_addcomment),
    # 일반 카테고리 - 칵테일정보 - 댓글삭제
    path("cocktailinfo/req_delcktcmt/", func_views.func_cocktailinfo_delcomment),
    # 일반 카테고리 - 칵테일정보 - 댓글수정
    path("cocktailinfo/req_modcktcmt/", func_views.func_cocktailinfo_modcomment),
    # 일반 카테고리 - 게시판 - 글등록
    path("req_addbrd/", func_views.func_board_addboard),
    # 일반 카테고리 - 게시판 - 글삭제
    path("req_delbrd/", func_views.func_board_delboard),
    # 일반 카테고리 - 게시판 - 글수정
    path("req_modbrd/", func_views.func_board_modboard),
    # 일반 카테고리 - 게시판 - 댓글등록
    path("req_addbrdcmt/", func_views.func_board_addcomment),
    # 일반 카테고리 - 게시판 - 댓글삭제
    path("req_delcomment/", func_views.func_board_delcomment),
    # 일반 카테고리 - 게시판 - 댓글수정
    path("req_modcomment/", func_views.func_board_modcomment),
    # 로그인 - 회원가입 - ID 중복확인
    path("sign_up/req_dupid/", func_views.func_signup_dupid),
    # 로그인 - 회원가입 - 닉네임 중복확인
    path("sign_up/req_dupname/", func_views.func_signup_dupname),
    # 로그인 - 회원가입 - 회원가입 요청
    path("sign_up/req_signup/", func_views.func_signup),
    # 로그인 - 로그인 - 로그인 요청
    path("sign_in/req_signin/", func_views.func_signin),
    # 로그인 - 아이디 찾기 - 아이디 검색
    path("find_id/req_findid/", func_views.func_findid),
    # 로그인 - 비밀번호 찾기 - 비밀번호 찾기(찾아주진 않지만)
    path("find_pw/req_findpw/", func_views.func_findpw),
    # 로그인 - 로그아웃 요청
    path("req_signout/", func_views.func_signout),
    # 마이페이지 - 내정보 관리 - 닉네임 변경요청
    path("mypage_myinfo/req_namechange", func_views.func_namechange),
    # 마이페이지 - 비밀번호 변경 - 비밀번호 변경요청
    path("mypage_mypwchange/req_pwchange", func_views.func_pwchange),
    # 마이페이지 - 내 냉장고 - 냉장고 저장
    path("mypage_myrefrig/req_saverefrig", func_views.func_saverefrig),
    # 관리자 - 메인화면 설정 - 메인화면 게시글 저장
    path("admin_asetmain/req_savesetmain", func_views.func_savesetmain),
    # 관리자 - 칵테일 재료 관리 - 재료 추가 저장
    path("admin_asetingrdnt/req_saveaddingrdnt", func_views.func_saveaddingrdnt),
    # 관리자 - 칵테일 재료 관리 - 재료 삭제
    path("admin_asetingrdnt/req_delingrdnt", func_views.func_delingrdnt),
    # 관리자 - 칵테일 재료 관리 - 재료 수정
    path("admin_asetingrdnt/req_savemodingrdnt", func_views.func_savemodingrdnt),
]