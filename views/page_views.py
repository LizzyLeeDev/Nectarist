# = = = = = = = = = = = = = = = = = = = = = = = = = = =
# IMPORT
# = = = = = = = = = = = = = = = = = = = = = = = = = = =

# 페이징
from django.core.paginator import Paginator
# MATH : 페이징 계산
import math
# 렌더
from django.shortcuts import render
# CSRF 해제
from django.views.decorators.csrf import csrf_exempt
# 모델
from ..models import *
# 공통 뷰
from .main_views import *

# = = = = = = = = = = = = = = = = = = = = = = = = = = =
# 공통
# = = = = = = = = = = = = = = = = = = = = = = = = = = =

# 메뉴 정보 추가
def add_menu_context(context, category):
    context.update({"category_current": category})
    context.update({"category_name": categories[category]["name"]})
    context.update({"category_exp": categories[category]["exp"]})

# = = = = = = = = = = = = = = = = = = = = = = = = = = =
# 일반 카테고리
# = = = = = = = = = = = = = = = = = = = = = = = = = = =

# 메인
def page_main(request):
    # menu info
    context = add_global_context(request)
    context.update({"category_current": "main"})

    # main carousel
    carousel_list = NtBoard.objects.order_by('-nt_board_idx').filter(nt_board_main_yn='Y')
    context.update({"carousel_list": carousel_list})

    # column list
    column_list = NtBoard.objects.order_by('-nt_board_idx').filter(nt_board_type='02')
    column_paginator = Paginator(column_list, 5)
    column_page_data = column_paginator.get_page(1)
    context.update({"column_list": column_page_data})

    # community list
    community_list = NtBoard.objects.order_by('-nt_board_idx').filter(nt_board_type='03')
    community_paginator = Paginator(community_list, 5)
    community_page_data = community_paginator.get_page(1)
    context.update({"community_list": community_page_data})

    # cocktail list
    cocktail_list = NtCocktail.objects.order_by('-nt_cocktail_idx')
    cocktail_paginator = Paginator(cocktail_list, 4)
    cocktail_page_data = cocktail_paginator.get_page(1)
    context.update({"cocktail_list": cocktail_page_data})

    return render(request, 'sites/main.html', context)

# 칵테일정보
def page_cocktailinfo(request):
    context = add_global_context(request)
    add_menu_context(context, "cocktailinfo")

    # write permission
    if context["is_login"] == "Y" and context["login_data"].nt_user_admin_yn == "Y":
        context.update({"write_permission": "Y"})
    else:
        context.update({"write_permission": "N"})

    # menu list data
    list_data = NtCocktail.objects.order_by('-nt_cocktail_idx')
    context.update({"list_data": list_data})
    
    # menu list paging
    page = request.GET.get('page')
    paginator = Paginator(list_data, 8)
    page_data = paginator.get_page(page)
    last_page = math.ceil(paginator.count / paginator.per_page)
    context.update({"last_page": last_page})
    context.update({"page_data": page_data})

    return render(request, 'sites/cocktailinfo.html', context)

# 칵테일정보 - 상세
def page_cocktailinfo_detail(request, cno):
    context = add_global_context(request)
    add_menu_context(context, "cocktailinfo")

    # write permission
    if context["is_login"] == "Y" and context["login_data"].nt_user_admin_yn == "Y":
        context.update({"write_permission": "Y"})
    else:
        context.update({"write_permission": "N"})
        
    # menu detail data
    context.update({"cno": cno})
    detail_data = NtCocktail.objects.get(nt_cocktail_idx=cno)
    context.update({"detail_data": detail_data})

    # cocktail recipe data
    recipe_data = NtCocktailRecipe.objects.select_related('nt_ingrdnt_idx_fk').filter(nt_cocktail_idx_fk=cno)
    context.update({"recipe_data": recipe_data})

    # cocktail comment data
    comment_data = NtCocktailComment.objects.select_related('nt_user_idx_fk').filter(nt_cocktail_idx_fk=cno)
    context.update({"comment_data": comment_data})

    return render(request, 'sites/cocktailinfo_detail.html', context)

# 칵테일정보 - 신규
def page_cocktailinfo_new(request):
    context = add_global_context(request)
    add_menu_context(context, "cocktailinfo")

    # cocktail ingrdnt type data
    cting_data = NtIngrdnt.objects.order_by('nt_ingrdnt_idx')
    context.update({"cting_data": cting_data})

    # page type
    context.update({"page_type": "new"})

    return render(request, 'sites/cocktailinfo_new.html', context)

# 칵테일정보 - 수정
def page_cocktailinfo_mod(request, cno):
    context = add_global_context(request)
    add_menu_context(context, "cocktailinfo")
        
    # menu detail data
    context.update({"cno": cno})
    detail_data = NtCocktail.objects.get(nt_cocktail_idx=cno)
    context.update({"detail_data": detail_data})

    # cocktail recipe data
    recipe_data = NtCocktailRecipe.objects.select_related('nt_ingrdnt_idx_fk').filter(nt_cocktail_idx_fk=cno)
    context.update({"recipe_data": recipe_data})
    
    # cocktail ingrdnt type data
    cting_data = NtIngrdnt.objects.order_by('nt_ingrdnt_idx')
    context.update({"cting_data": cting_data})

    # page type
    context.update({"page_type": "mod"})

    return render(request, 'sites/cocktailinfo_new.html', context)

# 칵테일계산기
def page_cocktailcalc(request):
    context = add_global_context(request)
    add_menu_context(context, "cocktailcalc")

    # user ingredient list
    if 'is_login' in request.session and request.session['is_login'] == 'Y':
        user_ingrd_data = NtUserIngrdnt.objects.select_related('nt_ingrdnt_idx_fk').filter(nt_user_idx_fk=request.session['login_id'])
        context.update({"user_ingrd_data": user_ingrd_data})
    else:
        context.update({"user_ingrd_data": []})

    # all ingredient list
    ingrd_data = NtIngrdnt.objects.filter()
    context.update({"ingrd_data": ingrd_data})

    return render(request, 'sites/cocktailcalc.html', context)

# 칵테일계산기 - 상세
@csrf_exempt
def page_cocktailcalc_detail(request):
    context = add_global_context(request)
    add_menu_context(context, "cocktailcalc")

    # selected ingrd
    selected_join = request.POST.get("selected")
    selected = list(map(int, selected_join.split(',')))

    # 만들수 있는 칵테일 목록과 재료가 하나 부족한 칵테일 목록
    all_complete_cocktail = []
    sub_complete_cocktail = []
    added = []
    tested = []

    # (1) 현재 선택된 재료를 하나라도 포함하는 칵테일 목록을 불러온다
    preSelectedCocktail = NtCocktailRecipe.objects.filter(nt_ingrdnt_idx_fk__in=selected)
    for cocktail in preSelectedCocktail:
        cocktail_info = {}
        # 그리고 해당 칵테일의 모든 재료 정보를 조회
        ingrd_names = []
        cocktail_ingrd_no = []
        cocktail_obj = NtCocktail.objects.get(nt_cocktail_idx=int(cocktail.nt_cocktail_idx_fk.nt_cocktail_idx))
        cocktail_ingrd_full = NtCocktailRecipe.objects.filter(nt_cocktail_idx_fk=cocktail_obj)
        for cocktailIngrd in cocktail_ingrd_full:
            cocktail_ingrd_no.append(int(cocktailIngrd.nt_ingrdnt_idx_fk.nt_ingrdnt_idx))
            ingrd_names.append(cocktailIngrd.nt_ingrdnt_idx_fk.nt_ingrdnt_nm)
        # (2) 칵테일 재료 중 선택된 재료에 포함되지 않는 재료 계산
        calculated = [i for i in cocktail_ingrd_no if i not in selected]
        # (3) 재료 다 있음 / 재료 한개 부족한 대상 칵테일을 오브젝트로 만들어 목록에 추가
        if len(calculated) <= 1:
            cocktail_info['cocktail_idx'] = int(cocktail_obj.nt_cocktail_idx)
            cocktail_info['cocktail_name'] = cocktail_obj.nt_cocktail_nm
            cocktail_info['cocktail_thumbnail'] = cocktail_obj.nt_cocktail_thumbnail
            cocktail_info['cocktail_ingname'] = ', '.join(ingrd_names)
            # 중복검사
            if cocktail_info['cocktail_idx'] not in added:
                if len(calculated) == 0:
                    all_complete_cocktail.append(cocktail_info)
                    added.append(cocktail_info['cocktail_idx'])
                elif len(calculated) == 1:
                    sub_complete_cocktail.append(cocktail_info)
                    added.append(cocktail_info['cocktail_idx'])

    context.update({"tested": tested})
    context.update({"all_complete_cocktail": all_complete_cocktail})
    context.update({"sub_complete_cocktail": sub_complete_cocktail})

    return render(request, 'sites/cocktailcalc_detail.html', context)

# 커뮤니티
def page_community(request):
    context = add_global_context(request)
    add_menu_context(context, "community")

    # write permission
    context.update({"write_permission": "Y"})

    # menu list data
    list_data = NtBoard.objects.select_related('nt_user_idx_fk').order_by('-nt_board_idx').filter(nt_board_type='03')    
    context.update({"list_data": list_data})
    
    # menu list paging
    page = request.GET.get('page')
    paginator = Paginator(list_data, 10)
    page_data = paginator.get_page(page)
    last_page = math.ceil(paginator.count / paginator.per_page)
    context.update({"last_page": last_page})
    context.update({"page_data": page_data})

    # menu list comment count
    return render(request, 'sites/board_list.html', context)

# 커뮤니티 - 상세
def page_community_detail(request, bno):
    context = add_global_context(request)
    add_menu_context(context, "community")

    # admin permission
    if context["is_login"] == "Y" and context["login_data"].nt_user_admin_yn == "Y":
        context.update({"write_permission": "Y"})
    else:
        context.update({"write_permission": "N"})

    # menu detail data
    context.update({"bno": bno})
    detail_data = NtBoard.objects.select_related('nt_user_idx_fk').get(nt_board_idx=bno)
    context.update({"detail_data": detail_data})

    # 글 태그
    if detail_data.nt_board_cocktail != '':
        board_tag = list(map(int, detail_data.nt_board_cocktail.split(',')))
        board_tag_cocktail = NtCocktail.objects.filter(nt_cocktail_idx__in=board_tag)
        context.update({"board_tag_cocktail": board_tag_cocktail})
    else:
        context.update({"board_tag_cocktail": None})

    # cocktail comment data
    comment_data = NtBoardComment.objects.select_related('nt_user_idx_fk').filter(nt_board_idx_fk=bno)
    context.update({"comment_data": comment_data})

    # 글 작성자 권한
    if context["is_login"] == "Y" and detail_data.nt_user_idx_fk.nt_user_idx == request.session['login_id']:
        context.update({"write_permission": "Y"})

    return render(request, 'sites/board_detail.html', context)

# 커뮤니티 - 신규
def page_community_new(request):
    context = add_global_context(request)
    add_menu_context(context, "community")

    # board type
    context.update({"board_type": "03"})

    # cocktail list
    cocktail_list = NtCocktail.objects.filter()
    context.update({"cocktail_list": cocktail_list})

    # page type
    context.update({"page_type": "new"})

    return render(request, 'sites/board_new.html', context)

# 커뮤니티 - 수정
def page_community_mod(request, bno):
    context = add_global_context(request)
    add_menu_context(context, "community")

    # board type
    context.update({"board_type": "03"})

    # cocktail list
    cocktail_list = NtCocktail.objects.filter()
    context.update({"cocktail_list": cocktail_list})
        
    # board detail data
    context.update({"bno": bno})
    detail_data = NtBoard.objects.get(nt_board_idx=bno)
    context.update({"detail_data": detail_data})

    # page type
    context.update({"page_type": "mod"})

    return render(request, 'sites/board_new.html', context)

# 칼럼
def page_column(request):
    context = add_global_context(request)
    add_menu_context(context, "column")

    # write permission
    if context["is_login"] == "Y" and context["login_data"].nt_user_admin_yn == "Y":
        context.update({"write_permission": "Y"})
    else:
        context.update({"write_permission": "N"})

    # menu list data
    list_data = NtBoard.objects.select_related('nt_user_idx_fk').order_by('-nt_board_idx').filter(nt_board_type='02')    
    context.update({"list_data": list_data})
    
    # menu list paging
    page = request.GET.get('page')
    paginator = Paginator(list_data, 10)
    page_data = paginator.get_page(page)
    last_page = math.ceil(paginator.count / paginator.per_page)
    context.update({"last_page": last_page})
    context.update({"page_data": page_data})

    # menu list comment count
    return render(request, 'sites/board_list.html', context)

# 칼럼 - 상세
def page_column_detail(request, bno):
    context = add_global_context(request)
    add_menu_context(context, "column")

    # admin permission
    if context["is_login"] == "Y" and context["login_data"].nt_user_admin_yn == "Y":
        context.update({"write_permission": "Y"})
    else:
        context.update({"write_permission": "N"})

    # menu detail data
    context.update({"bno": bno})
    detail_data = NtBoard.objects.select_related('nt_user_idx_fk').get(nt_board_idx=bno)
    context.update({"detail_data": detail_data})

    # 글 태그
    if detail_data.nt_board_cocktail != '':
        board_tag = list(map(int, detail_data.nt_board_cocktail.split(',')))
        board_tag_cocktail = NtCocktail.objects.filter(nt_cocktail_idx__in=board_tag)
        context.update({"board_tag_cocktail": board_tag_cocktail})
    else:
        context.update({"board_tag_cocktail": None})

    # cocktail comment data
    comment_data = NtBoardComment.objects.select_related('nt_user_idx_fk').filter(nt_board_idx_fk=bno)
    context.update({"comment_data": comment_data})

    return render(request, 'sites/board_detail.html', context)

# 칼럼 - 신규
def page_column_new(request):
    context = add_global_context(request)
    add_menu_context(context, "column")

    # board type
    context.update({"board_type": "02"})

    # cocktail list
    cocktail_list = NtCocktail.objects.filter()
    context.update({"cocktail_list": cocktail_list})

    # page type
    context.update({"page_type": "new"})

    return render(request, 'sites/board_new.html', context)

# 칼럼 - 수정
def page_column_mod(request, bno):
    context = add_global_context(request)
    add_menu_context(context, "column")

    # board type
    context.update({"board_type": "02"})

    # cocktail list
    cocktail_list = NtCocktail.objects.filter()
    context.update({"cocktail_list": cocktail_list})
        
    # board detail data
    context.update({"bno": bno})
    detail_data = NtBoard.objects.get(nt_board_idx=bno)
    context.update({"detail_data": detail_data})

    # page type
    context.update({"page_type": "mod"})

    return render(request, 'sites/board_new.html', context)

# 공지사항
def page_notice(request):
    context = add_global_context(request)
    add_menu_context(context, "notice")

    # write permission
    if context["is_login"] == "Y" and context["login_data"].nt_user_admin_yn == "Y":
        context.update({"write_permission": "Y"})
    else:
        context.update({"write_permission": "N"})

    # menu list data
    list_data = NtBoard.objects.select_related('nt_user_idx_fk').order_by('-nt_board_idx').filter(nt_board_type='01')    
    context.update({"list_data": list_data})
    
    # menu list paging
    page = request.GET.get('page')
    paginator = Paginator(list_data, 10)
    page_data = paginator.get_page(page)
    last_page = math.ceil(paginator.count / paginator.per_page)
    context.update({"last_page": last_page})
    context.update({"page_data": page_data})

    # menu list comment count
    return render(request, 'sites/board_list.html', context)

# 공지사항 - 상세
def page_notice_detail(request, bno):
    context = add_global_context(request)
    add_menu_context(context, "notice")

    # admin permission
    if context["is_login"] == "Y" and context["login_data"].nt_user_admin_yn == "Y":
        context.update({"write_permission": "Y"})
    else:
        context.update({"write_permission": "N"})

    # menu detail data
    context.update({"bno": bno})
    detail_data = NtBoard.objects.select_related('nt_user_idx_fk').get(nt_board_idx=bno)
    context.update({"detail_data": detail_data})

    # 글 태그
    if detail_data.nt_board_cocktail != '':
        board_tag = list(map(int, detail_data.nt_board_cocktail.split(',')))
        board_tag_cocktail = NtCocktail.objects.filter(nt_cocktail_idx__in=board_tag)
        context.update({"board_tag_cocktail": board_tag_cocktail})
    else:
        context.update({"board_tag_cocktail": None})

    # cocktail comment data
    comment_data = NtBoardComment.objects.select_related('nt_user_idx_fk').filter(nt_board_idx_fk=bno)
    context.update({"comment_data": comment_data})

    return render(request, 'sites/board_detail.html', context)

# 공지사항 - 신규
def page_notice_new(request):
    context = add_global_context(request)
    add_menu_context(context, "notice")

    # board type
    context.update({"board_type": "01"})

    # cocktail list
    cocktail_list = NtCocktail.objects.filter()
    context.update({"cocktail_list": cocktail_list})

    # page type
    context.update({"page_type": "new"})

    return render(request, 'sites/board_new.html', context)

# 공지사항 - 수정
def page_notice_mod(request, bno):
    context = add_global_context(request)
    add_menu_context(context, "notice")

    # board type
    context.update({"board_type": "01"})

    # cocktail list
    cocktail_list = NtCocktail.objects.filter()
    context.update({"cocktail_list": cocktail_list})
        
    # board detail data
    context.update({"bno": bno})
    detail_data = NtBoard.objects.get(nt_board_idx=bno)
    context.update({"detail_data": detail_data})

    # page type
    context.update({"page_type": "mod"})

    return render(request, 'sites/board_new.html', context)

# = = = = = = = = = = = = = = = = = = = = = = = = = = =
# 로그인
# = = = = = = = = = = = = = = = = = = = = = = = = = = =

# 회원가입
def page_signup(request):
    context = add_global_context(request)
    add_menu_context(context, "signup")

    return render(request, 'sites/sign_up.html', context)

# 로그인
def page_signin(request):
    context = add_global_context(request)
    add_menu_context(context, "signin")

    return render(request, 'sites/sign_in.html', context)

# 아이디 찾기
def page_findid(request):
    context = add_global_context(request)
    add_menu_context(context, "findid")

    return render(request, 'sites/find_id.html', context)

# 비밀번호 찾기
def page_findpw(request):
    context = add_global_context(request)
    add_menu_context(context, "findpw")

    return render(request, 'sites/find_pw.html', context)

# = = = = = = = = = = = = = = = = = = = = = = = = = = =
# 마이페이지
# = = = = = = = = = = = = = = = = = = = = = = = = = = =

# 내정보 관리
def page_myinfo(request):
    context = add_global_context(request)
    add_menu_context(context, "myinfo")

    try:
        if request.session['is_login'] == 'Y':
            return render(request, 'sites/mypage_myinfo.html', context)
        else:
            return render(request, 'sites/mypage_kick.html', context)
    except:
        return render(request, 'sites/mypage_kick.html', context)

# 비밀번호 변경
def page_mypwchange(request):
    context = add_global_context(request)
    add_menu_context(context, "mypwchange")

    try:
        if request.session['is_login'] == 'Y':
            return render(request, 'sites/mypage_mypwchange.html', context)
        else:
            return render(request, 'sites/mypage_kick.html', context)
    except:
        return render(request, 'sites/mypage_kick.html', context)

# 내 냉장고
def page_myrefrig(request):
    context = add_global_context(request)
    add_menu_context(context, "myrefrig")

    try:
        if request.session['is_login'] == 'Y':
            # user ingredient list
            user_ingrd_data = NtUserIngrdnt.objects.select_related('nt_ingrdnt_idx_fk').filter(nt_user_idx_fk=request.session['login_id'])
            context.update({"user_ingrd_data": user_ingrd_data})

            # all ingredient list
            ingrd_data = NtIngrdnt.objects.filter()
            context.update({"ingrd_data": ingrd_data})

            return render(request, 'sites/mypage_myrefrig.html', context)
        else:
            return render(request, 'sites/mypage_kick.html', context)
    except:
        return render(request, 'sites/mypage_kick.html', context)
    
# 작성글 보기
def page_myboard(request):
    context = add_global_context(request)
    add_menu_context(context, "myboard")

    try:
        if request.session['is_login'] == 'Y':
            # 사용자 작성글 목록
            list_data = NtBoard.objects.order_by('-nt_board_idx').filter(nt_board_type='03', nt_user_idx_fk=request.session['login_id'])
            context.update({"list_data": list_data})
    
            # menu list paging
            page = request.GET.get('page')
            paginator = Paginator(list_data, 10)
            page_data = paginator.get_page(page)
            last_page = math.ceil(paginator.count / paginator.per_page)
            context.update({"last_page": last_page})
            context.update({"page_data": page_data})

            return render(request, 'sites/mypage_myboard.html', context)
        else:
            return render(request, 'sites/mypage_kick.html', context)
    except:
        return render(request, 'sites/mypage_kick.html', context)


# = = = = = = = = = = = = = = = = = = = = = = = = = = =
# 관리자
# = = = = = = = = = = = = = = = = = = = = = = = = = = =

# 메인화면 설정
def page_asetmain(request):
    context = add_global_context(request)
    add_menu_context(context, "admin_asetmain")

    try:
        user = request.session['login_id']
        user_obj = NtUser.objects.get(nt_user_idx=user)

        if user_obj is not None and user_obj.nt_user_admin_yn == 'Y':
            # menu list data
            list_data = NtBoard.objects.order_by('-nt_board_idx').filter(nt_board_type__in=['01','02'])
            context.update({"list_data": list_data})
            
            # menu list paging
            page = request.GET.get('page')
            paginator = Paginator(list_data, 10)
            page_data = paginator.get_page(page)
            last_page = math.ceil(paginator.count / paginator.per_page)
            context.update({"last_page": last_page})
            context.update({"page_data": page_data})

            return render(request, 'sites/admin_setmain.html', context)
        else:
            return render(request, 'sites/admin_kick.html', context)
    except:
            return render(request, 'sites/admin_kick.html', context)
    
# 칵테일 재료 관리
def page_asetingrdnt(request):
    context = add_global_context(request)
    add_menu_context(context, "admin_asetingrdnt")

    try:
        user = request.session['login_id']
        user_obj = NtUser.objects.get(nt_user_idx=user)

        if user_obj is not None and user_obj.nt_user_admin_yn == 'Y':
            # ingrdnt type data
            context.update({"ingtype_data": ingrdnt_type})

            # menu list data
            list_data = NtIngrdnt.objects.order_by('-nt_ingrdnt_idx')
            context.update({"list_data": list_data})
            
            # menu list paging
            page = request.GET.get('page')
            paginator = Paginator(list_data, 20)
            page_data = paginator.get_page(page)
            last_page = math.ceil(paginator.count / paginator.per_page)
            context.update({"last_page": last_page})
            context.update({"page_data": page_data})

            return render(request, 'sites/admin_setingrdnt.html', context)
        else:
            return render(request, 'sites/admin_kick.html', context)
    except:
            return render(request, 'sites/admin_kick.html', context)