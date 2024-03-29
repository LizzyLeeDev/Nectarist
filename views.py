from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.template import Template
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .models import *
from datetime import datetime
import math
import hashlib


# 공통 변수
categories = {
    'cocktailinfo': {
        'name': '칵테일정보', 
        'url': '/cocktailinfo/?page=1'
    },
    'cocktailcalc': {
        'name': '칵테일계산기', 
        'url': '/cocktailcalc'
    },
    'community': {
        'name': '커뮤니티', 
        'url': '/community/?page=1'
    },
    'column': {
        'name': '칼럼', 
        'url': '/column/?page=1'
    },
    'notice': {
        'name': '공지사항', 
        'url': '/notice/?page=1'
    },
}
mypage_subcategories = {
    'myinfo': {
        'name': '내정보 관리',
        'url': '/mypage_myinfo/'
    },
    'myrefrig': {
        'name': '내 냉장고',
        'url': '/mypage_myrefrig/'
    },
}
admin_subcategories = {
    'setmain': {
        'name': '메인화면 설정',
        'url': '/admin_setmain/?page=1'
    },
    'addaboard': {
        'name': '관리자 게시글 등록',
        'url': '/admin_addaboard/'
    },
}

# 공통 변수 추가
def add_global_context(request):
    context = {}
    context.update({"categories": categories})
    context.update({"mypage_subcategories": mypage_subcategories})
    context.update({"admin_subcategories": admin_subcategories})
    
    if 'is_login' in request.session and request.session['is_login'] == 'Y':
        context.update({'is_login': 'Y'})
        context.update({'login_id': request.session['login_id']})
        context.update({'login_data': NtUser.objects.get(nt_user_idx=request.session['login_id'])})
    else:
        context.update({"is_login": 'N'})

    return context

# url-page 연결
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

def page_cocktailinfo(request):
    context = add_global_context(request)

    # menu info
    context.update({"category_current": "cocktailinfo"})
    context.update({"category_name": "칵테일정보"})
    context.update({"category_exp": "칵테일 정보와 레시피를 확인하실 수 있습니다."})

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

def page_cocktailinfo_detail(request, cno):
    context = add_global_context(request)

    # menu info
    context.update({"category_current": "cocktailinfo"})
    context.update({"category_name": "칵테일정보"})
    context.update({"category_exp": "칵테일 정보와 레시피를 확인하실 수 있습니다."})

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

def page_cocktailcalc(request):
    context = add_global_context(request)

    # menu info
    context.update({"category_current": "cocktailcalc"})
    context.update({"category_name": "칵테일계산기"})
    context.update({"category_exp": "가진 재료로 만들수 있는 칵테일을 계산할 수 있습니다."})

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

@csrf_exempt
def page_cocktailcalc_detail(request):
    context = add_global_context(request)

    # menu info
    context.update({"category_current": "cocktailcalc"})
    context.update({"category_name": "칵테일계산기"})
    context.update({"category_exp": "가진 재료로 만들수 있는 칵테일을 계산할 수 있습니다."})

    # selected ingrd
    selected_join = request.POST.get("selected")
    selected = list(map(int, selected_join.split(',')))

    # 만들수 있는 칵테일 목록과 재료가 하나 부족한 칵테일 목록
    all_complete_cocktail = []
    sub_complete_cocktail = []
    added = []
    tested = [];

    # (1) 현재 선택된 재료를 하나라도 포함하는 칵테일 목록을 불러온다
    preSelectedCocktail = NtCocktailRecipe.objects.filter(nt_ingrdnt_idx_fk__in=selected)
    for cocktail in preSelectedCocktail:
        cocktail_info = {}
        ingrd_names = []
        cocktail_ingrd_no = []
        cocktail_obj = NtCocktail.objects.get(nt_cocktail_idx=int(cocktail.nt_cocktail_idx_fk.nt_cocktail_idx))
        cocktail_ingrd_full = NtCocktailRecipe.objects.filter(nt_cocktail_idx_fk=cocktail_obj)
        for cocktailIngrd in cocktail_ingrd_full:
            cocktail_ingrd_no.append(int(cocktailIngrd.nt_ingrdnt_idx_fk.nt_ingrdnt_idx))
            ingrd_names.append(cocktailIngrd.nt_ingrdnt_idx_fk.nt_ingrdnt_nm)
        # (2) 칵테일 재료 중 선택된 재료에 포함되지 않는 재료 계산
        calculated = [i for i in cocktail_ingrd_no if i not in selected]
        # (3) 만들수 있으면 목록에 추가
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

def page_community(request):
    context = add_global_context(request)

    # menu info
    context.update({"category_current": "community"})
    context.update({"write_permission": "Y"})
    context.update({"category_name": "커뮤니티"})
    context.update({"category_exp": "칵테일에 대해 얘기하는 게시판입니다."})

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

def page_community_new(request):
    context = add_global_context(request)

    # menu info
    context.update({"category_current": "community"})
    context.update({"category_name": "커뮤니티"})
    context.update({"category_exp": "칵테일에 대해 얘기하는 게시판입니다."})

    # board type
    context.update({"board_type": "03"})

    # cocktail list
    cocktail_list = NtCocktail.objects.filter()
    context.update({"cocktail_list": cocktail_list})

    return render(request, 'sites/board_new.html', context)

def page_community_detail(request, bno):
    context = add_global_context(request)

    # menu info
    context.update({"category_current": "community"})
    context.update({"category_name": "커뮤니티"})
    context.update({"category_exp": "칵테일에 대해 얘기하는 게시판입니다."})

    # menu detail data
    context.update({"bno": bno})
    detail_data = NtBoard.objects.select_related('nt_user_idx_fk').get(nt_board_idx=bno)
    context.update({"detail_data": detail_data})

    # cocktail comment data
    comment_data = NtBoardComment.objects.select_related('nt_user_idx_fk').filter(nt_board_idx_fk=bno)
    context.update({"comment_data": comment_data})

    return render(request, 'sites/board_detail.html', context)

def page_column(request):
    context = add_global_context(request)

    # menu info
    context.update({"category_current": "column"})
    context.update({"write_permission": "N"})
    context.update({"category_name": "칼럼"})
    context.update({"category_exp": "칵테일에 관련된 칼럼을 연재하는 곳입니다."})

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

def page_column_detail(request, bno):
    context = add_global_context(request)

    # menu info
    context.update({"category_current": "column"})
    context.update({"category_name": "칼럼"})
    context.update({"category_exp": "칵테일에 관련된 칼럼을 연재하는 곳입니다."})

    # menu detail data
    context.update({"bno": bno})
    detail_data = NtBoard.objects.select_related('nt_user_idx_fk').get(nt_board_idx=bno)
    context.update({"detail_data": detail_data})

    # cocktail comment data
    comment_data = NtBoardComment.objects.select_related('nt_user_idx_fk').filter(nt_board_idx_fk=bno)
    context.update({"comment_data": comment_data})

    return render(request, 'sites/board_detail.html', context)

def page_notice(request):
    context = add_global_context(request)

    # menu info
    context.update({"category_current": "notice"})
    context.update({"write_permission": "N"})
    context.update({"category_name": "공지사항"})
    context.update({"category_exp": "넥타리스트 운영과 관련된 공지사항입니다."})

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

def page_notice_detail(request, bno):
    context = add_global_context(request)

    # menu info
    context.update({"category_current": "notice"})
    context.update({"category_name": "공지사항"})
    context.update({"category_exp": "넥타리스트 운영과 관련된 공지사항입니다."})

    # menu detail data
    context.update({"bno": bno})
    detail_data = NtBoard.objects.select_related('nt_user_idx_fk').get(nt_board_idx=bno)
    context.update({"detail_data": detail_data})

    # cocktail comment data
    comment_data = NtBoardComment.objects.select_related('nt_user_idx_fk').filter(nt_board_idx_fk=bno)
    context.update({"comment_data": comment_data})

    return render(request, 'sites/board_detail.html', context)

def page_sign_up(request):
    context = add_global_context(request)
    return render(request, 'sites/sign_up.html', context)

def page_sign_in(request):
    context = add_global_context(request)
    context.update({"category_current": "sign_in"})
    return render(request, 'sites/sign_in.html', context)

# 회원가입 및 마이페이지
def find_id(request):
    context = add_global_context(request)
    context.update({"category_current": "find_id"})
    return render(request, 'sites/find_id.html', context)

def find_pw(request):
    context = add_global_context(request)
    context.update({"category_current": "find_pw"})
    return render(request, 'sites/find_pw.html', context)

def page_mypage_myinfo(request):
    context = add_global_context(request)
    context.update({"category_current": "myinfo"})
    return render(request, 'sites/mypage_myinfo.html', context)

def page_mypage_myrefrig(request):
    context = add_global_context(request)

    # user ingredient list
    user_ingrd_data = NtUserIngrdnt.objects.select_related('nt_ingrdnt_idx_fk').filter(nt_user_idx_fk=request.session['login_id'])
    context.update({"user_ingrd_data": user_ingrd_data})

    # all ingredient list
    ingrd_data = NtIngrdnt.objects.filter()
    context.update({"ingrd_data": ingrd_data})

    context.update({"category_current": "myrefrig"})
    return render(request, 'sites/mypage_myrefrig.html', context)

def page_admin_setmain(request):
    context = add_global_context(request)

    # menu info
    context.update({"category_current": "setmain"})

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

def page_admin_addaboard(request):
    context = add_global_context(request)
    context.update({"category_current": "addaboard"})
    return render(request, 'sites/admin_addaboard.html', context)

# 기능
def req_namechange(request):
    name = request.GET.get("name")
    user = request.session['login_id']
    user_obj = NtUser.objects.get(nt_user_idx=user)

    user_obj.nt_user_nickname = name
    user_obj.save()

    ret = {"change_result": "Y"}
    return JsonResponse(ret)

def func_duplicate_id(request):
    input_id = request.GET.get("inputid")
    is_duplicate = "N"
    try:
        check_id = NtUser.objects.get(nt_user_id=input_id)
        if check_id is not None:
            is_duplicate = "Y"
    except:
        is_duplicate = "N"
    ret = {"is_duplicate": is_duplicate}
    return JsonResponse(ret)

def func_duplicate_name(request):
    input_name = request.GET.get("inputname")
    is_duplicate = "N"
    try:
        check_name = NtUser.objects.get(nt_user_nickname=input_name)
        if check_name is not None:
            is_duplicate = "Y"
    except:
        is_duplicate = "N"
    ret = {"is_duplicate": is_duplicate}
    return JsonResponse(ret)

def func_sign_up(request):
    ret = {"sign_up_result": "N"}
    sign_up_id = request.GET.get("id")
    sign_up_pw = request.GET.get("pw")
    sign_up_name = request.GET.get("name")
    sign_up_email = request.GET.get("email")

    encrypted = hashlib.sha256(str(sign_up_pw).encode())
    encrypted_hash = encrypted.hexdigest()

    new_user = NtUser(nt_user_id=sign_up_id, nt_user_pw=encrypted_hash, nt_user_email=sign_up_email, nt_user_nickname=sign_up_name, nt_user_admin_yn="N")
    new_user.save()

    ret["sign_up_result"] = "Y"
    ret["sign_up_id"] = sign_up_id
    return JsonResponse(ret)

def func_sign_in(request):
    ret = {"sign_in_result": "N"}
    sign_in_id = request.GET.get("id")
    sign_in_pw = request.GET.get("pw")

    try:
        userdata = NtUser.objects.get(nt_user_id=sign_in_id)

        encrypted = hashlib.sha256(str(sign_in_pw).encode())
        encrypted_hash = encrypted.hexdigest()

        if userdata is not None and userdata.nt_user_pw == encrypted_hash:
            ret["sign_in_result"] = "Y"
            request.session['is_login'] = "Y"
            request.session['login_id'] = userdata.nt_user_idx
    except:
        pass

    return JsonResponse(ret)

def func_sign_out(request):
    request.session.flush()
    ret = {"sign_out_result": "Y"}
    return JsonResponse(ret)

def func_findid_search(request):
    input_email = request.GET.get("inputemail")
    is_id_exist = "N"
    ret_id = ""

    try:
        find_user = NtUser.objects.get(nt_user_email=input_email)
        if find_user is not None:
            is_id_exist = "Y"
            ret_id = find_user.nt_user_id
    except:
        is_id_exist = "N"

    ret = {"is_id_exist": is_id_exist, "ret_id": ret_id}
    return JsonResponse(ret)

def func_findpw_search(request):
    input_id = request.GET.get("inputid")
    input_email = request.GET.get("inputemail")
    is_id_exist = "N"

    try:
        find_user = NtUser.objects.get(nt_user_id=input_id, nt_user_email=input_email)
        if find_user is not None:
            is_id_exist = "Y"

            new_temp_pass = get_random_string(length=10)
            encrypted = hashlib.sha256(str(new_temp_pass).encode())
            encrypted_hash = encrypted.hexdigest()

            find_user.nt_user_pw = encrypted_hash
            find_user.save()
            
            send_mail_subject = "[Nectarist] 임시 비밀번호 안내입니다."
            send_mail_contents_html = render_to_string("templates/pw_email.html", {"new_temp_pass": new_temp_pass})
            send_mail_contents_text = strip_tags(send_mail_contents_html)
            
            send_mail(
                send_mail_subject,
                send_mail_contents_text,
                "settings.EMAIL_HOST_USER",
                ["lizzy.lee.dev@gmail.com"],
                fail_silently=True
            )
    except:
        is_id_exist = "N"

    ret = {"is_id_exist": is_id_exist}
    return JsonResponse(ret)

def func_add_cocktail_comment(request):
    cno = int(request.GET.get("cno"))
    comment_text = request.GET.get("text")
    cocktail_obj = NtCocktail.objects.get(nt_cocktail_idx=cno)
    user = request.session['login_id']
    user_obj = NtUser.objects.get(nt_user_idx=user)

    new_comment = NtCocktailComment(nt_cocktail_comment_text=comment_text, nt_cocktail_comment_dt=datetime.now(), nt_cocktail_idx_fk=cocktail_obj, nt_user_idx_fk=user_obj)
    new_comment.save()

    ret = {"add_comment_result": "Y"}
    return JsonResponse(ret)

def func_add_board(request):
    btype = request.GET.get("type")
    title = request.GET.get("title")
    text = request.GET.get("text")
    tag = request.GET.get("tag")

    user = request.session['login_id']
    user_obj = NtUser.objects.get(nt_user_idx=user)

    new_board = NtBoard()
    new_board.nt_board_type = btype
    new_board.nt_board_subject = title
    new_board.nt_board_contents = text
    new_board.nt_board_cocktail = tag
    new_board.nt_board_dt = datetime.now()
    new_board.nt_board_main_yn = 'N'
    new_board.nt_board_delete_yn = 'N'
    new_board.nt_user_idx_fk = user_obj

    new_board.save()

    ret = {"add_board_result": "Y"}
    return JsonResponse(ret)

def func_add_board_comment(request):
    bno = int(request.GET.get("bno"))
    comment_text = request.GET.get("text")
    board_obj = NtBoard.objects.get(nt_board_idx=bno)
    user = request.session['login_id']
    user_obj = NtUser.objects.get(nt_user_idx=user)

    new_comment = NtBoardComment()
    new_comment.nt_board_comment_text = comment_text
    new_comment.nt_board_comment_dt = datetime.now()
    new_comment.nt_board_idx_fk = board_obj
    new_comment.nt_user_idx_fk = user_obj
    new_comment.save()

    ret = {"add_comment_result": "Y"}
    return JsonResponse(ret)

@csrf_exempt
def func_save_refrig(request):
    selectedJoin = request.GET.get("selected")
    selected = selectedJoin.split(',')
    deletedJoin = request.GET.get("deleted")
    deleted = deletedJoin.split(',')
    user = request.session['login_id']
    user_obj = NtUser.objects.get(nt_user_idx=user)

    if deletedJoin != '':
        for ino in deleted:
            try:
                user_ingrd_obj = NtUserIngrdnt.objects.get(nt_user_idx_fk=request.session['login_id'], nt_ingrdnt_idx_fk=int(ino))
                user_ingrd_obj.delete()
            except:
                pass

    if selectedJoin != '':
        for ino in selected:
            try:
                user_ingrd_obj = NtUserIngrdnt.objects.get(nt_user_idx_fk=request.session['login_id'], nt_ingrdnt_idx_fk=int(ino))
            except:
                ingrd_obj = NtIngrdnt.objects.get(nt_ingrdnt_idx=int(ino))
                new_useringrd = NtUserIngrdnt.objects.create(nt_user_idx_fk=user_obj, nt_ingrdnt_idx_fk=ingrd_obj, nt_user_ingrdnt_amt='', nt_user_ingrdnt_unit='')

    ret = {"save_refrig_result": "Y"}
    return JsonResponse(ret)

def func_save_setmain(request):
    selectedJoin = request.GET.get("selected")
    selected = selectedJoin.split(',')
    deletedJoin = request.GET.get("deleted")
    deleted = deletedJoin.split(',')

    if deletedJoin != '':
        for bno in deleted:
            try:
                board_obj = NtBoard.objects.get(nt_board_idx=int(bno))
                board_obj.nt_board_main_yn = 'N'
                board_obj.save()
            except:
                pass

    if selectedJoin != '':
        for bno in selected:
            try:
                board_obj = NtBoard.objects.get(nt_board_idx=int(bno))
                board_obj.nt_board_main_yn = 'Y'
                board_obj.save()
            except:
                pass

    ret = {"save_setmain_result": "Y"}
    return JsonResponse(ret)

def func_add_aboard(request):
    user = request.session['login_id']
    user_obj = NtUser.objects.get(nt_user_idx=user)
    
    new_aboard = NtBoard()
    new_aboard.nt_board_type = request.POST.get("boardType")
    new_aboard.nt_board_subject = request.POST.get("title")
    new_aboard.nt_board_contents = request.POST.get("text")
    new_aboard.nt_board_cocktail = request.POST.get("tag")
    new_aboard.nt_board_thumbnail = request.FILES['thumbnail']
    new_aboard.nt_board_dt = datetime.now()
    new_aboard.nt_board_main_yn = 'N'
    new_aboard.nt_board_delete_yn = 'N'
    new_aboard.nt_user_idx_fk = user_obj
    new_aboard.save()

    ret = {"add_board_result": "Y"}
    return JsonResponse(ret)