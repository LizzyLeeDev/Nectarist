# = = = = = = = = = = = = = = = = = = = = = = = = = = =
# IMPORT
# = = = = = = = = = = = = = = = = = = = = = = = = = = =

# 파일 삭제
import os
# JSON
import json
from django.http import JsonResponse
# 시간
from datetime import datetime
# 비밀번호 찾기 - 랜덤 문자열 생성
from django.utils.crypto import get_random_string
# 비밀번호 찾기 - 메일 발송
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
# CSRF 해제
from django.views.decorators.csrf import csrf_exempt
# 모델
from ..models import *
# 비밀번호 해시
import hashlib

# = = = = = = = = = = = = = = = = = = = = = = = = = = =
# 공통
# = = = = = = = = = = = = = = = = = = = = = = = = = = =

# = = = = = = = = = = = = = = = = = = = = = = = = = = =
# 일반 카테고리
# = = = = = = = = = = = = = = = = = = = = = = = = = = =

# 칵테일정보 - 칵테일등록
def func_saveaddcocktail(request):
    new_cocktail = NtCocktail()
    new_cocktail.nt_cocktail_nm = request.POST.get("name")
    new_cocktail.nt_cocktail_engnm = request.POST.get("engname")
    new_cocktail.nt_cocktail_recipe = request.POST.get("recipe")
    new_cocktail.nt_cocktail_thumbnail = request.FILES['thumbnail']
    new_cocktail.nt_cocktail_memo = request.POST.get("memo")
    new_cocktail.save()

    new_cocktail_idx = new_cocktail.pk

    ing_list_tmp = request.POST.get("ingrdnt")
    ing_list = json.loads(ing_list_tmp)
    for ing in ing_list:
        new_ing = NtCocktailRecipe()
        new_ing.nt_cocktail_idx_fk = NtCocktail.objects.get(nt_cocktail_idx=new_cocktail_idx)
        new_ing.nt_ingrdnt_idx_fk = NtIngrdnt.objects.get(nt_ingrdnt_idx=ing["ingrdnt"])
        new_ing.nt_cocktail_recipe_amt = ing["amt"]
        new_ing.nt_cocktail_recipe_unit = ing["unit"]
        new_ing.save(force_insert=True)
    
    ret = {"add_result": "Y", "cocktail_id": new_cocktail_idx}
    return JsonResponse(ret)

# 칵테일정보 - 칵테일삭제
def func_delcocktail(request):
    cno = request.GET.get("cno")

    # 재료 삭제
    try:
        del_ingrdnt = NtCocktailRecipe.objects.filter(nt_cocktail_idx_fk=cno)
        del_ingrdnt.delete()
    except:
        pass

    # 칵테일정보 삭제
    del_cocktail = NtCocktail.objects.get(nt_cocktail_idx=cno)
    if del_cocktail.nt_cocktail_thumbnail:
        os.remove(del_cocktail.nt_cocktail_thumbnail.path)
    del_cocktail.delete()

    ret = {"del_result": "Y"}
    return JsonResponse(ret)

# 칵테일정보 - 칵테일수정
def func_savemodcocktail(request):
    cno = request.POST.get("cno")
    mod_cocktail = NtCocktail.objects.get(nt_cocktail_idx=cno)
    mod_cocktail.nt_cocktail_nm = request.POST.get("name")
    mod_cocktail.nt_cocktail_engnm = request.POST.get("engname")
    mod_cocktail.nt_cocktail_recipe = request.POST.get("recipe")
    mod_cocktail.nt_cocktail_memo = request.POST.get("memo")

    # 섬네일
    try:
        if request.FILES['thumbnail']:
            if mod_cocktail.nt_cocktail_thumbnail:
                os.remove(mod_cocktail.nt_cocktail_thumbnail.path)
            mod_cocktail.nt_cocktail_thumbnail = request.FILES['thumbnail']
    except:
        pass
    
    mod_cocktail.save()

    try:
        del_ingrdnt = NtCocktailRecipe.objects.filter(nt_cocktail_idx_fk=cno)
        del_ingrdnt.delete()
    except:
        pass

    ing_list_tmp = request.POST.get("ingrdnt")
    ing_list = json.loads(ing_list_tmp)
    for ing in ing_list:
        new_ing = NtCocktailRecipe()
        new_ing.nt_cocktail_idx_fk = NtCocktail.objects.get(nt_cocktail_idx=cno)
        new_ing.nt_ingrdnt_idx_fk = NtIngrdnt.objects.get(nt_ingrdnt_idx=ing["ingrdnt"])
        new_ing.nt_cocktail_recipe_amt = ing["amt"]
        new_ing.nt_cocktail_recipe_unit = ing["unit"]
        new_ing.save(force_insert=True)

    ret = {"mod_result": "Y"}
    return JsonResponse(ret)

# 칵테일정보 - 댓글등록
def func_cocktailinfo_addcomment(request):
    cno = int(request.GET.get("cno"))
    comment_text = request.GET.get("text")
    cocktail_obj = NtCocktail.objects.get(nt_cocktail_idx=cno)
    user = request.session['login_id']
    user_obj = NtUser.objects.get(nt_user_idx=user)

    new_comment = NtCocktailComment(nt_cocktail_comment_text=comment_text, nt_cocktail_comment_dt=datetime.now(), nt_cocktail_idx_fk=cocktail_obj, nt_user_idx_fk=user_obj)
    new_comment.save()

    ret = {"add_comment_result": "Y"}
    return JsonResponse(ret)

# 칵테일정보 - 댓글삭제
def func_cocktailinfo_delcomment(request):
    cmno = int(request.GET.get("cmno"))
    NtCocktailComment.objects.filter(nt_cocktail_comment_idx=cmno).delete()

    return JsonResponse({"del_result": "Y"})

# 칵테일정보 - 댓글수정
def func_cocktailinfo_modcomment(request):
    cmno = int(request.GET.get("cmno"))
    comment_text = request.GET.get("text")

    mod_comment = NtCocktailComment.objects.get(nt_cocktail_comment_idx=cmno)
    mod_comment.nt_cocktail_comment_text = comment_text
    mod_comment.save()

    ret = {"mod_comment_result": "Y"}
    return JsonResponse(ret)

# 게시판 - 글등록
def func_board_addboard(request):
    user = request.session['login_id']
    user_obj = NtUser.objects.get(nt_user_idx=user)

    new_board = NtBoard()
    new_board.nt_board_type = request.POST.get("type")
    new_board.nt_board_subject = request.POST.get("title")
    new_board.nt_board_contents = request.POST.get("text")
    new_board.nt_board_cocktail = request.POST.get("tag")
    new_board.nt_board_thumbnail = request.FILES.get("thumbnail")
    new_board.nt_board_dt = datetime.now()
    new_board.nt_board_main_yn = 'N'
    new_board.nt_board_delete_yn = 'N'
    new_board.nt_user_idx_fk = user_obj


    new_board.save()

    ret = {"add_board_result": "Y", "board_id": new_board.pk}
    return JsonResponse(ret)

# 게시판 - 글삭제
def func_board_delboard(request):
    bno = request.GET.get("bno")

    # 덧글 삭제
    try:
        del_comment = NtBoardComment.objects.filter(nt_board_idx_fk=bno)
        del_comment.delete()
    except:
        pass

    # 칵테일정보 삭제
    del_board = NtBoard.objects.get(nt_board_idx=bno)
    if del_board.nt_board_thumbnail:
        os.remove(del_board.nt_board_thumbnail.path)
    del_board.delete()

    ret = {"del_result": "Y"}
    return JsonResponse(ret)

# 게시판 - 글수정
def func_board_modboard(request):
    bno = request.POST.get("bno")
    mod_board = NtBoard.objects.get(nt_board_idx=bno)
    mod_board.nt_board_subject = request.POST.get("title")
    mod_board.nt_board_contents = request.POST.get("text")
    mod_board.nt_board_cocktail = request.POST.get("tag")

    # 섬네일
    try:
        if request.FILES['thumbnail']:
            if mod_board.nt_board_thumbnail:
                os.remove(mod_board.nt_board_thumbnail.path)
            mod_board.nt_board_thumbnail = request.FILES['thumbnail']
    except:
        pass

    mod_board.save()

    ret = {"mod_board_result": "Y"}
    return JsonResponse(ret)

# 게시판 - 댓글등록
def func_board_addcomment(request):
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

# 게시판 - 댓글삭제
def func_board_delcomment(request):
    cmno = int(request.GET.get("cmno"))
    NtBoardComment.objects.filter(nt_board_comment_idx=cmno).delete()

    return JsonResponse({"del_result": "Y"})

# 게시판 - 댓글수정
def func_board_modcomment(request):
    cmno = int(request.GET.get("cmno"))
    comment_text = request.GET.get("text")

    mod_comment = NtBoardComment.objects.get(nt_board_comment_idx=cmno)
    mod_comment.nt_board_comment_text = comment_text
    mod_comment.save()

    ret = {"mod_comment_result": "Y"}
    return JsonResponse(ret)

# = = = = = = = = = = = = = = = = = = = = = = = = = = =
# 로그인
# = = = = = = = = = = = = = = = = = = = = = = = = = = =

# 회원가입 - ID 중복확인
def func_signup_dupid(request):
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

# 회원가입 - 닉네임 중복확인
def func_signup_dupname(request):
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

# 회원가입 - 회원가입 요청
def func_signup(request):
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

# 로그인 - 로그인 요청
def func_signin(request):
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

# 아이디 찾기 - 아이디 검색
def func_findid(request):
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

# 비밀번호 찾기 - 비밀번호 찾기
def func_findpw(request):
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

# 로그아웃 요청
def func_signout(request):
    request.session.flush()

    ret = {"sign_out_result": "Y"}
    return JsonResponse(ret)

# = = = = = = = = = = = = = = = = = = = = = = = = = = =
# 마이페이지
# = = = = = = = = = = = = = = = = = = = = = = = = = = =

# 내정보 관리 - 닉네임 변경요청
def func_namechange(request):
    name = request.GET.get("name")
    user = request.session['login_id']
    user_obj = NtUser.objects.get(nt_user_idx=user)

    user_obj.nt_user_nickname = name
    user_obj.save()

    ret = {"change_result": "Y"}
    return JsonResponse(ret)

# 비밀번호 변경 - 비밀번호 변경요청
def func_pwchange(request):
    curpw = request.GET.get("curpw")
    newpw = request.GET.get("newpw")
    user = request.session['login_id']
    is_valid_curpw = "N"
    is_pw_changed = "N"

    try:
        find_user = NtUser.objects.get(nt_user_idx=user)
        if find_user is not None:
            curpw_encrypted = hashlib.sha256(str(curpw).encode())
            curpw_encrypted_hash = curpw_encrypted.hexdigest()
            if find_user.nt_user_pw == curpw_encrypted_hash:
                is_valid_curpw = "Y"

                newpw_encrypted = hashlib.sha256(str(newpw).encode())
                newpw_encrypted_hash = newpw_encrypted.hexdigest()

                find_user.nt_user_pw = newpw_encrypted_hash
                find_user.save()
                is_pw_changed = "Y"
    except:
        pass

    ret = {"is_valid_curpw": is_valid_curpw, "is_pw_changed": is_pw_changed}
    return JsonResponse(ret)

# 내 냉장고 - 냉장고 저장
@csrf_exempt
def func_saverefrig(request):
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

# = = = = = = = = = = = = = = = = = = = = = = = = = = =
# 관리자
# = = = = = = = = = = = = = = = = = = = = = = = = = = =

# 메인화면 설정 - 메인화면 게시글 저장
def func_savesetmain(request):
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

# 칵테일 재료 관리 - 재료 추가 저장
def func_saveaddingrdnt(request):
    add_ingrdnt_tmp = request.GET.get("list")
    add_ingrdnt = json.loads(add_ingrdnt_tmp)

    for ing in add_ingrdnt:
        new_ing = NtIngrdnt()
        new_ing.nt_ingrdnt_type = ing["type"]
        new_ing.nt_ingrdnt_nm = ing["name"]
        new_ing.save()
    
    ret = {"save_result": "Y"}
    return JsonResponse(ret)

# 칵테일 재료 관리 - 재료 삭제
def func_delingrdnt(request):
    del_ingrdntno = request.GET.get("ingno")

    del_ingrdnt = NtIngrdnt.objects.get(nt_ingrdnt_idx=del_ingrdntno)
    del_ingrdnt.delete()

    ret = {"save_result": "Y"}
    return JsonResponse(ret)

# 칵테일 재료 관리 - 재료 수정
def func_savemodingrdnt(request):
    mod_ingrdnt_tmp = request.GET.get("ing")
    mod_ingrdnt_data = json.loads(mod_ingrdnt_tmp)

    mod_ingrdnt = NtIngrdnt.objects.get(nt_ingrdnt_idx=mod_ingrdnt_data["no"])
    mod_ingrdnt.nt_ingrdnt_type = mod_ingrdnt_data["type"]
    mod_ingrdnt.nt_ingrdnt_nm = mod_ingrdnt_data["name"]
    mod_ingrdnt.save()
    
    ret = {"save_result": "Y"}
    return JsonResponse(ret)