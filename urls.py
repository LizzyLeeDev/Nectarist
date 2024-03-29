from django.urls import path

from . import views

urlpatterns = [
    # 맵핑url, view.py, 별칭

    # 페이지 - 일반
    path("", views.page_main, name="main"),
    path("main", views.page_main, name="main2"),
    path("cocktailinfo/", views.page_cocktailinfo, name="cocktailinfo"),
    path("cocktailinfo/detail/<int:cno>", views.page_cocktailinfo_detail, name="cocktailinfo_detail"),
    path("cocktailcalc/", views.page_cocktailcalc, name="cocktailcalc"),
    path("cocktailcalc/detail", views.page_cocktailcalc_detail, name="cocktailcalc_detail"),
    path("community/", views.page_community, name="community"),
    path("community/new", views.page_community_new, name="community_new"),
    path("community/detail/<int:bno>/", views.page_community_detail, name="community_detail"),
    path("column/", views.page_column, name="column"),
    path("column/detail/<int:bno>/", views.page_column_detail, name="column_detail"),
    path("notice/", views.page_notice, name="notice"),
    path("notice/detail/<int:bno>/", views.page_notice_detail, name="notice_detail"),
    path("sign_up/", views.page_sign_up, name="sign_up"),
    path("sign_in/", views.page_sign_in, name="sign_up"),
    path("find_id/", views.find_id, name="find_id"),
    path("find_pw/", views.find_pw, name="find_pw"),

    # 페이지 - 마이페이지
    path("mypage_myinfo/", views.page_mypage_myinfo, name="myinfo"),
    path("mypage_myrefrig/", views.page_mypage_myrefrig, name="myrefrig"),

    # 페이지 - 관리자
    path("admin_setmain/", views.page_admin_setmain, name="setmain"),
    path("admin_addaboard/", views.page_admin_addaboard, name="addaboard"),

    # 회원가입 관련 요청
    path("sign_up/req_duplicate_id/", views.func_duplicate_id, name="func_duplicate_id"),
    path("req_duplicate_name/", views.func_duplicate_name, name="func_duplicate_name"),
    path("sign_up/req_signup/", views.func_sign_up, name="func_sign_up"),
    path("sign_in/req_signin/", views.func_sign_in, name="func_sign_in"),
    path("req_signout/", views.func_sign_out, name="func_sign_out"),
    path("req_namechange", views.req_namechange, name="req_namechange"),

    # 아이디/비밀번호 찾기 관련 요청
    path("find_id/search/", views.func_findid_search, name="func_findid_search"),
    path("find_pw/search/", views.func_findpw_search, name="func_findpw_search"),

    # 기타 요청
    path("req_add_cocktail_comment/", views.func_add_cocktail_comment, name="func_add_cocktail_comment"),
    path("req_add_board_comment/", views.func_add_board_comment, name="func_add_board_comment"),
    path("req_add_board/", views.func_add_board, name="func_add_board"),
    path("req_save_refrig/", views.func_save_refrig, name="func_save_refrig"),
    path("req_add_aboard/", views.func_add_aboard, name="func_add_aboard"),
    path("req_save_setmain/", views.func_save_setmain, name="func_save_setmain"),
]